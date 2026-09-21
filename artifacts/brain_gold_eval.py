#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brain_gold_eval.py — ЛИНЕЙКА для второй памяти: золотой набор из СВОИХ wikilinks +
детерминированный скоринг brain_ask (vector-only vs vector+graph) в Recall@12 / MRR / nDCG@12.

ЗАЧЕМ (ДР DR26-09-16-MACANTON-02-0453, консенсус 3/3 вендоров, anton 16.09 «где линейка??»)
    Recall судился глазами; `--ab` писал дельту в ab_recall, но сравнивать было НЕ С ЧЕМ.
    Wikilinks, которые Антон и роботы ставили руками, — бесплатная разметка релевантности.
    Этот прибор превращает их в число. Пока числа нет, любая замена эмбеддера/реранкера —
    суеверие (Grok, 16.09). Ноль LLM-токенов: вопросы = заголовки и первые абзацы заметок.

КЛАССЫ ВОПРОСОВ (gold = список stem'ов заметок, сравнение по basename без .md)
    title    запрос = заголовок заметки        → gold = сама заметка   (entity-подобный)
    body     запрос = первый абзац (без ссылок) → gold = сама заметка   (theme-подобный)
    bridge   запрос = первый абзац             → gold = ЦЕЛИ её wikilinks (что даёт граф)
    temporal запрос = заголовок старой заметки → gold = заметка из superseded_by

КОНВЕЙЕР — ТОТ ЖЕ КОД, ЧТО В БОЮ: импортируются load_index / retrieve_candidates /
    dedup_best_per_file / _links_in / looks_like_entity из brain_ask.py; свой только цикл.
    Режимы: vector (dense → rerank) и graph (dense → 1-hop wikilinks ≤GMAX → rerank), как --ab.
    Entity-полоса (brain_entity) и peer-шарды здесь НЕ подмешиваются — прибор меряет
    индекс + граф, чтобы дельта графа была чистой.

ВХОД/ВЫХОД
    --build [--n-per-class N] [--seed S]  → eval/gold-<дата>.jsonl (заморожен, версия в имени)
    --run  [--gold FILE]                  → eval/scores-<дата>.jsonl + таблица в stdout +
                                             строки в turnstate.db таблица gold_eval
    --selftest                            → метрики на ручных примерах; exit 1 если врут
    Запускать PYTHON_EXE из ~/.claude/machine.env (~/.brain-venv), как brain_ask.py.

ПОРОГИ «ХОРОШО» (инженерные, из синтеза ДР, не научная норма):
    title Recall@12 ≥ 0.90 · body ≥ 0.80 · bridge ≥ 0.70 · temporal ≥ 0.60;
    графу засчитывается польза, если nDCG@12 на bridge растёт ≥ +0.03 без потери > 0.01 на body.

ПРЕДЕЛЫ: gold по wikilinks = СЛАБАЯ истина (сосед по ссылке не всегда нужен для ответа);
    один прогон = одна версия индекса; латентность пишется, но не судится.
"""
import os, re, sys, json, random, datetime, sqlite3, time, math, argparse, platform, io
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
EVAL_DIR = HERE / 'eval'
CURATED = ['02-Decisions', '03-Insights', '06-Concepts', '09-Bridges', '02-Protocols', '01-Rules']
WIKILINK_RX = re.compile(r'\[\[([^\]\|#]+)(?:[|#][^\]]*)?\]\]')
TOPN = 12
LANG_RX = re.compile(r'[а-яё]', re.I)


def lang_of(s):
    letters = [c for c in s if c.isalpha()]
    if not letters: return 'na'
    return 'ru' if sum(1 for c in letters if LANG_RX.match(c)) / len(letters) > 0.4 else 'en'


def split_fm(text):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n?(.*)$', text, re.S)
    return (m.group(1), m.group(2)) if m else ('', text)


def fm_get(fm, key):
    mm = re.search(r'(?m)^' + key + r'\s*:\s*"?(.+?)"?\s*$', fm)
    return mm.group(1).strip() if mm else None


def note_title(fm, body, path):
    t = fm_get(fm, 'title')
    if not t:
        h = re.search(r'(?m)^#\s+(.+)$', body)
        t = h.group(1).strip() if h else Path(path).stem
    return re.sub(r'\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]', lambda m: m.group(2) or m.group(1), t)[:200]


def first_paragraph(body, minlen=100, maxlen=400):
    body = re.sub(r'(?m)^\s*>.*$', '', body)                    # callouts/quotes
    for para in re.split(r'\n\s*\n', body):
        p = para.strip()
        if not p or p.startswith('#') or p.startswith('|') or p.startswith('```'): continue
        p = re.sub(r'\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]', lambda m: m.group(2) or m.group(1), p)
        p = re.sub(r'[*_`>#]+', '', p); p = re.sub(r'\s+', ' ', p).strip()
        if len(p) >= minlen: return p[:maxlen]
    return None


# ---------------------------------------------------------------- metrics (pure)
def recall_at(ranked, gold, k=TOPN):
    g = set(gold); return len(g & set(ranked[:k])) / len(g) if g else 0.0


def mrr(ranked, gold, k=TOPN):
    g = set(gold)
    for i, r in enumerate(ranked[:k]):
        if r in g: return 1.0 / (i + 1)
    return 0.0


def ndcg_at(ranked, gold, k=TOPN):
    """Каждое золото засчитывается ОДИН раз, сколько бы раз стем ни попал в выдачу.

    ПОЧИНКА КЛАССА 17.09.2026 (нашла панель вторых глаз на публичном модуле eval/ в
    sqlite-graph-memory, T10): сравнение шло по basename, а две заметки с одинаковым именем
    в разных папках дают ОДИН стем дважды. DCG считал оба попадания, IDCG считал множество
    золота — и nDCG вылезал выше собственного максимума: ndcg_at(['foo','foo'], ['foo'])
    возвращал 1.63. Замер на наших scores: затронуто 4 вопроса из 184, title завышен
    на +0.0315, temporal на +0.1077 — ОДИНАКОВО в обоих прогонах, поэтому дельты ДО/ПОСЛЕ
    устояли до 4-го знака (+0.0056 -> +0.0055) и вердикты мерж/откат шагов T02-T09 в силе.
    Recall и MRR не затронуты: первый считает множества, второй останавливается на первом хите.
    """
    if os.environ.get('GOLD_EVAL_MUTANT') == '1': return 1.0   # мутант для красного теста
    g, credited = set(gold), set()
    dcg = 0.0
    for i, r in enumerate(ranked[:k]):
        if r in g and r not in credited:
            credited.add(r)
            dcg += 1.0 / math.log2(i + 2)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(min(len(g), k)))
    return dcg / idcg if idcg else 0.0


def selftest():
    ok = True
    def chk(name, got, want):
        nonlocal ok
        if abs(got - want) > 1e-6:
            ok = False; print('❌ %s: got %.4f want %.4f' % (name, got, want))
        else: print('✅ %s = %.4f' % (name, got))
    chk('recall hit', recall_at(['a', 'b', 'c'], ['b']), 1.0)
    chk('recall miss', recall_at(['a', 'b', 'c'], ['z']), 0.0)
    chk('recall half', recall_at(['a', 'b'], ['a', 'z']), 0.5)
    chk('mrr rank2', mrr(['a', 'b'], ['b']), 0.5)
    chk('ndcg perfect', ndcg_at(['b'], ['b']), 1.0)
    chk('ndcg rank2 single', ndcg_at(['a', 'b'], ['b']), 1 / math.log2(3))
    chk('ndcg miss', ndcg_at(['a'], ['b']), 0.0)
    # класс 17.09: дубль стема (две заметки с одним именем) не имеет права поднять nDCG выше 1.0
    chk('ndcg дубль стема', ndcg_at(['foo', 'foo'], ['foo']), 1.0)
    chk('ndcg дубль не дороже одного', ndcg_at(['x', 'foo', 'foo'], ['foo']),
        ndcg_at(['x', 'foo', 'zzz'], ['foo']))
    # порядок имеет значение: gold первым > gold вторым
    if not ndcg_at(['b', 'a'], ['b']) > ndcg_at(['a', 'b'], ['b']):
        ok = False; print('❌ ndcg не чувствует порядок')
    else: print('✅ ndcg чувствует порядок')
    print('SELFTEST', 'PASS' if ok else 'FAIL'); return 0 if ok else 1


# ---------------------------------------------------------------- gold builder
def build_gold(vault, indexed_stems, n_per_class, seed):
    rnd = random.Random(seed)
    notes = []
    for d in CURATED:
        for p in sorted((vault / d).glob('*.md')):
            if p.stem.lower() not in indexed_stems: continue   # gold только по тому, что в индексе
            try: text = p.read_text(encoding='utf-8', errors='ignore')
            except Exception: continue
            fm, body = split_fm(text)
            links = [t.strip() for t in WIKILINK_RX.findall(body)]
            links = sorted({t.lower() for t in links if t.lower() in indexed_stems and t.lower() != p.stem.lower()})
            sup = fm_get(fm, 'superseded_by')
            sup = WIKILINK_RX.findall(sup)[0].strip().lower() if sup and WIKILINK_RX.findall(sup) else None
            notes.append({'path': p, 'stem': p.stem.lower(), 'folder': d, 'title': note_title(fm, body, p),
                          'para': first_paragraph(body), 'links': links,
                          'sup': sup if sup and sup in indexed_stems else None})
    rnd.shuffle(notes)
    gold, used = [], set()
    def add(cls, n, q, g, extra=None):
        gold.append({'id': '%s-%03d' % (cls, len([x for x in gold if x['cls'] == cls]) + 1), 'cls': cls,
                     'query': q, 'gold': g, 'lang': lang_of(q), 'folder': n['folder'], 'src': n['stem'],
                     **(extra or {})})
    pools = {'title': [n for n in notes if len(n['title']) >= 8],
             'body': [n for n in notes if n['para']],
             'bridge': [n for n in notes if n['para'] and len(n['links']) >= 2],
             'temporal': [n for n in notes if n['sup']]}
    for cls in ('title', 'body', 'bridge', 'temporal'):
        cnt = 0
        for n in pools[cls]:
            key = (cls, n['stem'])
            if key in used: continue
            if cls == 'title': add(cls, n, n['title'], [n['stem']])
            elif cls == 'body': add(cls, n, n['para'], [n['stem']])
            elif cls == 'bridge': add(cls, n, n['para'], n['links'][:8], {'self': n['stem']})
            else: add(cls, n, n['title'], [n['sup']])
            used.add(key); cnt += 1
            if cnt >= n_per_class: break
    return gold


# ---------------------------------------------------------------- runner
def run(gold_file, out_dir, limit=None, backend=None, emb_path=None, meta_path=None,
        reranker=None, freeze_out=None, candidates_in=None):
    # T05: реранкер — ПАРАМЕТР, а кандидаты можно ЗАМОРОЗИТЬ и переиграть другим судьёй.
    # Зачем заморозка: A/B двух реранкеров честен только на ОДНИХ И ТЕХ ЖЕ top-60. Первая
    # ступень детерминирована, но «детерминирована» — это claim; замороженный файл делает
    # её проверяемой (стемы кандидатов сверяются при переигрывании) и попутно снимает с
    # прогона эмбеддер: судью меряем без второй переменной в уравнении.
    # T04 (2026-09-16): эмбеддер стал ПАРАМЕТРОМ линейки. Раньше модель, префикс запроса
    # и пути индекса были зашиты на e5, поэтому сравнить e5 с BGE-M3 было нечем — а
    # правило программы требует ДВЕ таблицы на том же gold. Профиль (модель + префиксы +
    # файлы) берётся из brain_emb_backends.py; без --embedder-backend это e5, то есть
    # ровно прежнее поведение.
    os.environ.setdefault('BRAIN_EMB_BACKEND', 'e5')
    import numpy as np
    import brain_ask as ba
    import brain_common as bc
    import brain_emb_backends as beb
    import brain_rerankers as brr
    import brain_graph as bg
    prof = beb.resolve(backend)
    gold = [json.loads(l) for l in Path(gold_file).read_text(encoding='utf-8').splitlines() if l.strip()]
    if limit: gold = gold[:limit]
    dev = bc.pick_device()
    # --index-emb/--index-meta (T02) бьют профиль: ими меряют ИСТОРИЧЕСКУЮ версию индекса.
    emb, meta = ba.load_index(emb_path or prof.emb, meta_path or prof.meta)
    # Переигрывание замороженных кандидатов не кодирует запросы вовсе: судью меряем
    # без второй переменной в уравнении (и без загрузки эмбеддера на каждый прогон).
    enc = None if candidates_in else bc.load_model(prof.model, dev, fp16=True)
    rprof = brr.resolve(reranker)
    ce = brr.load_or_none(rprof, dev)
    by_base = {}
    for j, mm in enumerate(meta):
        by_base.setdefault(Path(mm['path']).stem.lower(), []).append(j)
    stem = lambda i: Path(meta[i]['path']).stem.lower()

    def rerank(query, cand, ppr_stems=()):
        # T08: дедуп по файлу БЕЗ обрезки + порезка полосой PPR — ровно как в
        # `brain_ask._best_per_file`, чтобы линейка мерила конвейер, а не свой пересказ.
        # Полоса выключена (BRAIN_GRAPH_PPR не поднят) -> первые TOPN, прежнее поведение.
        if ce is None or not cand:
            # sims=None — это режим переигрывания: порядок 1-й ступени уже лежит в файле
            # кандидатов, поэтому «без судьи» = порядок как есть, а не падение по None.
            sc = ([float(sims[i]) for i in cand] if sims is not None
                  else [-float(r) for r in range(len(cand))])
        else:
            pairs = [(query, meta[i]['title'] + '. ' + meta[i]['snippet']) for i in cand]
            sc = ce.predict(pairs)
        full = ba.dedup_best_per_file(sorted(zip(cand, sc), key=lambda x: -x[1]), meta, len(cand))
        return bg.fuse_after_rerank(full, meta, list(ppr_stems), TOPN)

    frozen = _load_frozen(candidates_in, len(emb), prof.model) if candidates_in else None
    freeze_rows = [] if freeze_out else None
    rows, t_all = [], time.time()
    for k, g in enumerate(gold):
        t0 = time.time()
        if frozen is not None:
            base, added, sims = _replay(frozen, k, g, meta)
            rr0 = time.time()
            # PPR персонализируется от sims; в переигрывании они восстановлены из файла
            # кандидатов, поэтому полоса работает и здесь — но только если sims есть.
            ppr = bg.ppr_file_order(meta, sims, base) if (bg.enabled() and sims is not None) else []
            res = {}
            for mode, cand in (('vector', base), ('graph', base + added)):
                ranked = [stem(i) for i, _ in rerank(g['query'], cand, ppr)]
                res[mode] = {'ranked': ranked, 'recall': recall_at(ranked, g['gold']),
                             'mrr': mrr(ranked, g['gold']), 'ndcg': ndcg_at(ranked, g['gold'])}
            rows.append({**g, 'entity_gate': ba.looks_like_entity(g['query']),
                         'cand_vector': len(base), 'cand_graph_added': len(added),
                         'ppr_nodes': len(ppr), 'rr_sec': round(time.time() - rr0, 3),
                         'sec': round(time.time() - t0, 2), 'res': res})
            if (k + 1) % 20 == 0:
                sys.stderr.write('  %d/%d  %.0fs\n' % (k + 1, len(gold), time.time() - t_all))
            continue
        # префикс из профиля: e5 требует 'query: ', BGE-M3 не требует ничего (карточки
        # моделей). Чужой префикс не падает, а ТИХО портит косинус — мерили бы ошибку.
        qv = enc.encode([prof.query(g['query'])], normalize_embeddings=True, convert_to_numpy=True)[0].astype('float32')
        sims = emb @ qv
        # query= включает лексическую полосу, когда поднят BRAIN_LEX_LANE (шаг 3).
        # Флаг снят -> retrieve_candidates возвращает то же, что и до шага 3, и
        # линейка честно меряет ДО/ПОСЛЕ ОДНИМ прибором, а не двумя разными.
        base = ba.retrieve_candidates(sims, meta, query=g['query'])
        # T08: 1-hop больше не копия, а ТОТ ЖЕ вызов, что в бою (brain_graph.expand_1hop).
        added = bg.expand_1hop(sims, meta, base, by_base)
        if freeze_rows is not None:
            freeze_rows.append({'k': k, 'query': g['query'], 'base': [int(i) for i in base],
                                'added': [int(i) for i in added],
                                'stems': [stem(i) for i in list(base) + list(added)],
                                'sig': chunk_sig(meta, list(base) + list(added))})
        rr0 = time.time()
        ppr = bg.ppr_file_order(meta, sims, base) if bg.enabled() else []
        res = {}
        for mode, cand in (('vector', base), ('graph', base + added)):
            ranked = [stem(i) for i, _ in rerank(g['query'], cand, ppr)]
            res[mode] = {'ranked': ranked, 'recall': recall_at(ranked, g['gold']),
                         'mrr': mrr(ranked, g['gold']), 'ndcg': ndcg_at(ranked, g['gold'])}
        rows.append({**g, 'entity_gate': ba.looks_like_entity(g['query']), 'cand_vector': len(base),
                     'cand_graph_added': len(added), 'ppr_nodes': len(ppr),
                     'rr_sec': round(time.time() - rr0, 3),
                     'sec': round(time.time() - t0, 2), 'res': res})
        if (k + 1) % 20 == 0:
            sys.stderr.write('  %d/%d  %.0fs\n' % (k + 1, len(gold), time.time() - t_all))
    try:
        import brain_lex as _bl
        _lex = '+bm25rrf' if _bl.enabled() else ''
    except Exception:
        _lex = ''
    if freeze_rows is not None:
        _write_frozen(freeze_out, freeze_rows, len(emb), prof.model, gold_file)
        print('кандидаты ЗАМОРОЖЕНЫ -> %s (%d вопросов)' % (freeze_out, len(freeze_rows)))
    rr = [r['rr_sec'] for r in rows if 'rr_sec' in r]
    return rows, {'index_chunks': len(emb), 'embedder': prof.model + _lex,
                  'reranker': rprof.model if ce else 'none',
                  'rerank_ms': round(1000.0 * sum(rr) / len(rr), 1) if rr else None,
                  'cand_mean': round(sum(r['cand_vector'] for r in rows) / len(rows), 1) if rows else 0,
                  'replay': bool(candidates_in),
                  'device': str(dev), 'topk': ba.TOPK_RETRIEVE, 'cpf': ba.CHUNKS_PER_FILE}


def chunk_sig(meta, idxs):
    """Отпечаток ТЕКСТА кандидатов, а не только их имён.

    ОПЛАЧЕНО 16.09 в самом T05: сосед (T06) перечанковал волт, число чанков осталось тем же
    (24 239), имена файлов тоже — сменился ТЕКСТ чанков. Проверка «число чанков + стемы»
    такую подмену пропускает, и переигранный судья судил бы другие абзацы под видом тех же
    кандидатов. Хэш берётся от заголовка и головы сниппета: именно эта пара едет в реранкер.
    """
    import hashlib
    h = hashlib.sha1()
    for i in idxs:
        m = meta[i]
        h.update((str(m.get('title', '')) + '\x1f' + str(m.get('snippet', ''))[:120] + '\x1e')
                 .encode('utf-8', 'replace'))
    return h.hexdigest()[:16]


def _write_frozen(path, rows, n_chunks, embedder, gold_file):
    """Сохранить кандидатов 1-й ступени: шапка-отпечаток + строка на вопрос."""
    head = {'_freeze': 2, 'index_chunks': n_chunks, 'embedder': embedder,
            'gold_file': Path(gold_file).name,
            'ts': datetime.datetime.now().isoformat(timespec='seconds')}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(head, ensure_ascii=False) + '\n')
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def _load_frozen(path, n_chunks, embedder):
    """Прочитать замороженных кандидатов и ОТКАЗАТЬ, если индекс под ними уехал.

    Класс, который тут закрывается: соседняя сессия переиндексировала волт (шаг T06 меняет
    чанкер), номера чанков сместились — и переигранный прогон тихо судил бы ДРУГИЕ тексты,
    а таблица выглядела бы нормальной. Поэтому сверяются и отпечаток индекса, и СТЕМЫ
    каждого кандидата (ниже, в _replay)."""
    lines = [l for l in Path(path).read_text(encoding='utf-8').splitlines() if l.strip()]
    head = json.loads(lines[0])
    if not head.get('_freeze'):
        raise RuntimeError('%s не файл заморозки кандидатов' % path)
    if head['index_chunks'] != n_chunks or head['embedder'] != embedder:
        raise RuntimeError(
            'ЗАМОРОЗКА НЕ К ЭТОМУ ИНДЕКСУ: файл %d чанков / %s, сейчас %d / %s.\n'
            'Переигрывать нельзя: номера чанков означают другие тексты. Лечение: заново '
            '--freeze-candidates на текущем индексе и перемерить ВСЕХ судей.'
            % (head['index_chunks'], head['embedder'], n_chunks, embedder))
    return [json.loads(l) for l in lines[1:]]


def _replay(frozen, k, g, meta):
    """-> (base, added, None). Сверяет вопрос и стемы, чтобы судить ТЕ ЖЕ тексты."""
    fr = frozen[k]
    if fr['query'] != g['query']:
        raise RuntimeError('заморозка и gold разъехались на вопросе %d: %r vs %r'
                           % (k, fr['query'][:60], g['query'][:60]))
    cand = list(fr['base']) + list(fr['added'])
    now = [Path(meta[i]['path']).stem.lower() for i in cand]
    if now != fr['stems']:
        bad = next(j for j in range(len(now)) if now[j] != fr['stems'][j])
        raise RuntimeError('индекс уехал под заморозкой (вопрос %d, кандидат %d: было %r, '
                           'стало %r). Перезаморозь кандидатов.'
                           % (k, bad, fr['stems'][bad], now[bad]))
    sig = fr.get('sig')
    if sig is None:
        if k == 0:
            sys.stderr.write('⚠️ заморозка СТАРОГО формата (без отпечатка текста): совпадение '
                             'имён не доказывает, что чанки те же. Перезаморозь кандидатов.\n')
    elif sig != chunk_sig(meta, cand):
        raise RuntimeError(
            'ТЕКСТ чанков сменился под заморозкой (вопрос %d): имена и число чанков те же, '
            'а содержимое другое — так выглядит перечанковка волта соседней сессией.\n'
            'Лечение: --freeze-candidates заново и перемерить ВСЕХ судей на новой пачке.' % k)
    return list(fr['base']), list(fr['added']), None


def summarize(rows):
    out = {}
    for cls in sorted({r['cls'] for r in rows}):
        rs = [r for r in rows if r['cls'] == cls]
        for mode in ('vector', 'graph'):
            out[(cls, mode)] = {'n': len(rs),
                                'recall': sum(r['res'][mode]['recall'] for r in rs) / len(rs),
                                'mrr': sum(r['res'][mode]['mrr'] for r in rs) / len(rs),
                                'ndcg': sum(r['res'][mode]['ndcg'] for r in rs) / len(rs)}
    for lang in ('ru', 'en'):
        rs = [r for r in rows if r['lang'] == lang]
        if rs:
            for mode in ('vector', 'graph'):
                out[('lang:' + lang, mode)] = {'n': len(rs),
                    'recall': sum(r['res'][mode]['recall'] for r in rs) / len(rs),
                    'mrr': sum(r['res'][mode]['mrr'] for r in rs) / len(rs),
                    'ndcg': sum(r['res'][mode]['ndcg'] for r in rs) / len(rs)}
    return out


THRESH = {'title': 0.90, 'body': 0.80, 'bridge': 0.70, 'temporal': 0.60}


def print_table(summary, cfg, gold_file):
    print('\nЛИНЕЙКА второй памяти · gold=%s · index=%d chunks · %s + %s · %s%s%s'
          % (Path(gold_file).name, cfg['index_chunks'], cfg['embedder'].split('/')[-1],
             cfg['reranker'].split('/')[-1], cfg['device'],
             (' · реранк %.1f мс/вопрос (%.0f кандидатов)'
              % (cfg['rerank_ms'], cfg.get('cand_mean', 0))) if cfg.get('rerank_ms') else '',
             ' · КАНДИДАТЫ ЗАМОРОЖЕНЫ' if cfg.get('replay') else ''))
    print('%-12s %-7s %4s  %-9s %-6s %-7s  %s' % ('класс', 'режим', 'n', 'Recall@12', 'MRR', 'nDCG@12', 'порог'))
    for (cls, mode), s in summary.items():
        th = THRESH.get(cls)
        flag = '' if th is None else ('✅ ≥%.2f' % th if s['recall'] >= th else '❌ <%.2f' % th)
        print('%-12s %-7s %4d  %-9.3f %-6.3f %-7.3f  %s' % (cls, mode, s['n'], s['recall'], s['mrr'], s['ndcg'], flag))
    for cls in ('bridge', 'body'):
        if (cls, 'graph') in summary:
            d = summary[(cls, 'graph')]['ndcg'] - summary[(cls, 'vector')]['ndcg']
            print('граф на %-8s nDCG %+.3f' % (cls, d))


def write_sqlite(summary, cfg, gold_file, scores_file):
    try:
        import brain_ask as ba
        con = sqlite3.connect(str(ba.AB_DB), timeout=3.0)
        con.execute("""CREATE TABLE IF NOT EXISTS gold_eval(ts TEXT, gold_file TEXT, scores_file TEXT,
            cls TEXT, mode TEXT, n INTEGER, recall12 REAL, mrr REAL, ndcg12 REAL,
            embedder TEXT, reranker TEXT, index_chunks INTEGER, node TEXT)""")
        ts = datetime.datetime.now().isoformat(timespec='seconds')
        for (cls, mode), s in summary.items():
            con.execute('INSERT INTO gold_eval VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                        (ts, Path(gold_file).name, Path(scores_file).name, cls, mode, s['n'], s['recall'], s['mrr'],
                         s['ndcg'], cfg['embedder'], cfg['reranker'], cfg['index_chunks'], platform.node()))
        # platform.node(), а НЕ os.uname().nodename (T02, 2026-09-16): os.uname на Windows не
        # существует вовсе -> AttributeError внутри try -> линейка печатала таблицу в консоль и
        # МОЛЧА не писала ни строки в turnstate.gold_eval. На маке прибор выглядел исправным,
        # на хабе (где GPU и где живёт программа) история замеров не копилась бы вообще.
        con.commit(); con.close(); return True
    except Exception as e:
        sys.stderr.write('sqlite gold_eval не записан: %s\n' % e); return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--build', action='store_true'); ap.add_argument('--run', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--gold'); ap.add_argument('--n-per-class', type=int, default=60)
    ap.add_argument('--seed', type=int, default=42); ap.add_argument('--limit', type=int)
    # --index-emb/--index-meta: померить ЧУЖУЮ версию индекса, не подменяя живые файлы на диске
    # (T02, 2026-09-16). Правило программы требует ДВЕ таблицы на каждый шаг, меняющий индекс,
    # а «ДО» после правки живёт только в бэкапе. Без этих флагов оставалось два плохих пути:
    # свопать живые .npy/.pkl (соседняя сессия на хабе получит мёртвый RECALL на время прогона)
    # или писать свой скрипт-обёртку рядом с линейкой (второй прибор на ту же работу).
    #   python brain_gold_eval.py --run --index-emb _scratch/t02-bak/_brain_e5.npy.pre-T02 \
    #                                   --index-meta _scratch/t02-bak/_brain_e5_meta.pkl.pre-T02 --no-persist
    ap.add_argument('--index-emb'); ap.add_argument('--index-meta')
    # --embedder-backend: ИМЯ профиля из brain_emb_backends (e5 | bgem3). Даёт второй
    # столбец сравнения, не трогая ни боевой индекс, ни env соседних сессий (T04).
    ap.add_argument('--embedder-backend', default=None,
                    help='какой эмбеддер мерить: e5 (дефолт) | bgem3')
    # T05: какой СУДЬЯ и на каких кандидатах. Имя профиля из brain_rerankers.
    ap.add_argument('--reranker', default=None,
                    help='реранкер: mmarco (дефолт) | bgem3v2 | qwen06 | none | HF-id')
    ap.add_argument('--freeze-candidates', metavar='FILE',
                    help='сохранить top-60 первой ступени, чтобы судей мерить на ОДНИХ кандидатах')
    ap.add_argument('--candidates', metavar='FILE',
                    help='переиграть замороженных кандидатов другим судьёй (эмбеддер не грузится)')
    ap.add_argument('--no-persist', action='store_true',
                    help='не писать scores/SQLite: прогон по историческому индексу не должен '
                         'притворяться базовой линией')
    a = ap.parse_args()
    if a.selftest: return selftest()
    EVAL_DIR.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    gold_file = Path(a.gold) if a.gold else EVAL_DIR / ('gold-%s.jsonl' % today)
    if a.build:
        os.environ.setdefault('BRAIN_EMB_BACKEND', 'e5')
        import pickle, brain_ask as ba
        try:
            from _paths import VAULT as vault
        except Exception:
            vault = Path.home() / 'Obsidian' / 'Anton-Knowledge'
        meta = pickle.loads(Path(ba.E5_META).read_bytes())
        stems = {Path(m['path']).stem.lower() for m in meta}
        gold = build_gold(Path(vault), stems, a.n_per_class, a.seed)
        gold_file.write_text('\n'.join(json.dumps(g, ensure_ascii=False) for g in gold) + '\n', encoding='utf-8')
        from collections import Counter
        print('gold: %d вопросов -> %s · %s · языки %s' % (len(gold), gold_file, dict(Counter(g['cls'] for g in gold)),
                                                          dict(Counter(g['lang'] for g in gold))))
    if a.run:
        if not gold_file.exists():
            print('нет gold-файла %s: сперва --build' % gold_file); return 2
        if a.index_emb or a.index_meta:
            print('индекс ПОДМЕНЁН: %s + %s (файлы на диске не тронуты)'
                  % (Path(a.index_emb).name if a.index_emb else '-',
                     Path(a.index_meta).name if a.index_meta else '-'))
        rows, cfg = run(gold_file, EVAL_DIR, a.limit, backend=a.embedder_backend,
                        emb_path=Path(a.index_emb) if a.index_emb else None,
                        meta_path=Path(a.index_meta) if a.index_meta else None,
                        reranker=a.reranker, freeze_out=a.freeze_candidates,
                        candidates_in=a.candidates)
        summary = summarize(rows)
        print_table(summary, cfg, gold_file)
        if a.no_persist:
            print('scores НЕ записаны (--no-persist)')
        else:
            scores_file = EVAL_DIR / ('scores-%s.jsonl' % datetime.datetime.now().strftime('%Y%m%d-%H%M'))
            scores_file.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n', encoding='utf-8')
            print('scores -> %s · sqlite gold_eval %s' % (scores_file, 'OK' if write_sqlite(summary, cfg, gold_file, scores_file) else 'skip'))
    if not (a.build or a.run): ap.print_help(); return 2
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
