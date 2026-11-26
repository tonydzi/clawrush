# -*- coding: utf-8 -*-
"""Head-to-Head Intelligence & Practical Utility Benchmark for Anton's Lab:
GEMINI 4 ARGON vs GEMINI 4 CARBON vs GPT-6 ASTRA vs CLAUDE FABLE 5.1 / OPUS 5.5
across Low, Medium, High effort levels.

Measures TWO independent dimensions:
1. RAW ENGINEERING & STRATEGIC INTELLIGENCE (16 hard verifiable tasks, 0 style penalty):
   - IQ_B01..IQ_B04 (4 Hard Subtle Bug Hunts with exact line/condition root cause):
     * B01: Python async/threading lock-release / cache stampede race bug
     * B02: SQLite WAL / transaction isolation silent data loss bug
     * B03: Regex / substring tombstone false-positive bug (our real 06.10 `SUPERSEDED` enum bug)
     * B04: Floating-point / timezone boundary off-by-one billing reconciliation bug
   - IQ_M01..IQ_M04 (4 Multi-Constraint Quantitative / Game-Theory Optimization puzzles with unique exact integer answers):
     * M01: Optimal fleet token routing under quota & latency caps (exact integer cost)
     * M02: Bayesian defect rate calculation after two imperfect gates (exact fraction/percentage)
     * M03: DAG critical-path scheduling with resource lock contention (exact minimum seconds)
     * M04: Arbitrage / conversion funnel expected value with churn & refund penalty (exact dollar EV)
   - IQ_A01..IQ_A04 (4 Deep Needle-in-a-120KB-Haystack Synthesis tasks requiring cross-referencing 3 distant sections of CLAUDE.md v7.14.0):
     * A01: Cross-reference §0.7.3 object threshold + §3.1 social gate + Tier-2 rule on CLA vs commercial contract
     * A02: Cross-reference §4.3-bis red-proof requirement + §5.10 3rd-breakage family rule + `prior_art.py` shard location
     * A03: Cross-reference §0.20.4 word limits (short status vs 2-block reply) + §2.7 bedtime cutoff + §6.3-bis rail plan
     * A04: Cross-reference §7.10 machine stamp contract + where stamp is forbidden + what `apply` returns on foreign stamp
   - IQ_S01..IQ_S04 (4 Adversarial Red-Team / Proofread Audit tasks: find all 3 planted mathematical/logical contradictions in a draft report):
     * S01: Planted precision/recall/F1 and sample-size contradiction
     * S02: Planted latency speedup multiplier vs table sum contradiction
     * S03: Planted security/leak vulnerability in a proposed shell wrapper
     * S04: Planted privateer vs black-hat legal trap in an outreach strategy
2. COFOUNDER OPERATIONAL DISCIPLINE (16 Canon v7.14.0 tasks across S/P/A/T/F/E with strict 6-axis scoring + content_pass).

Total = 32 high-signal tasks per model-effort configuration.

Machine: palo-alto-hub · Agent: Antigravity · Operator: Anton · 2026-11-26
"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import statistics
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "eval_4titans_iq_runs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(HERE))
sys.path.insert(0, r"~\.claude\scripts")
sys.path.insert(0, r"~\.claude\scripts\_shared")
sys.path.insert(0, r"~\.claude\scripts\cc-review")

import claude_run
import eval_100q_suite_v7140 as s100
import eval_v7140_antigravity_frontier as base
import llm_ask
import orouter_review

IQ_TASKS = [
    # --- Bucket 1: Hard Subtle Bug Hunts (4 tasks, 2 points each = 8 pts) ---
    {
        "id": "IQ_B01",
        "cat": "bug_hunt",
        "prompt": (
            "Найди ровно ДВА бага в этой функции кэширования с TTL и напиши, при каком условии она: "
            "(1) навсегда повесит все потоки (deadlock), и (2) вернёт вызывающему мутированный словарь из чужого потока:\n"
            "```python\n"
            "LOCK = threading.Lock()\n"
            "CACHE = {}\n"
            "def get_profile(uid, fetch_fn, ttl=60):\n"
            "    LOCK.acquire()\n"
            "    now = time.time()\n"
            "    if uid in CACHE and now - CACHE[uid]['ts'] < ttl:\n"
            "        LOCK.release()\n"
            "        return CACHE[uid]['data']\n"
            "    data = fetch_fn(uid)  # сетевой вызов\n"
            "    CACHE[uid] = {'ts': now, 'data': data}\n"
            "    LOCK.release()\n"
            "    return data\n"
            "```"
        ),
        "must_groups": [
            ["исключен", "exception", "ошибк", "упад", "try", "finally", "deadlock", "не отпуст", "завис"],
            ["мутац", "копи", "copy", "deepcopy", "ссылк", "один и тот же словар", "измен", "shared", "гонк"],
        ],
    },
    {
        "id": "IQ_B02",
        "cat": "bug_hunt",
        "prompt": (
            "В нашем скрипте ротации очереди SQLite два воркера на одной машине одновременно выполняют:\n"
            "```python\n"
            "conn = sqlite3.connect('queue.db', isolation_level=None) # autocommit\n"
            "row = conn.execute(\"SELECT id, payload FROM jobs WHERE status='pending' ORDER BY id LIMIT 1\").fetchone()\n"
            "if row:\n"
            "    conn.execute(\"UPDATE jobs SET status='running', worker=? WHERE id=?\", (worker_id, row[0]))\n"
            "```\n"
            "Назови: (1) какой баг произойдёт при параллельном запуске двух воркеров, и (2) как исправить его ОДНИМ атомарным SQL-запросом в современном SQLite (3.35+) без внешних блокировок."
        ),
        "must_groups": [
            ["два воркер", "оба", "один и тот же", "дубл", "дважды", "race", "гонк"],
            ["returning", "update", "where status='pending'", "status = 'pending'", "begin immediate"],
        ],
    },
    {
        "id": "IQ_B03",
        "cat": "bug_hunt",
        "prompt": (
            "Наш линтер устаревших заметок памяти проверял текст регуляркой `re.search(r'\\b(SUPERSEDED|RETIRED|DROP)\\b', body)` "
            "и автоматически закрывал заметку как мёртвую. На реальной заметке `adopt-framework.md` со строкой: "
            "«Конечные состояния автомата: CONFIRMED_EXISTING / SUPERSEDED / RETIRED / DROP» линтер ложно убил живую документацию. "
            "Назови: (1) в чём корневой порок этого класса проверок (почему `\\b` не спасает), и (2) какой детерминированный контракт данных в заметке полностью исключает путаницу между упоминанием словаря и статусом самой заметки."
        ),
        "must_groups": [
            ["упоминан", "цитат", "перечислен", "словар", "контекст", "описани", "подстрок", "текст"],
            ["frontmatter", "yaml", "заголов", "поле", "ключ", "status:", "метаданн"],
        ],
    },
    {
        "id": "IQ_B04",
        "cat": "bug_hunt",
        "prompt": (
            "Скрипт дневного аудита считает прогоны ночной рутины за дату `2026-09-30` в Пало-Альто (`UTC-7`), "
            "проверяя имена лог-файлов `run_YYYY-MM-DDTHH-MM-SSZ.json` строковым префиксом `fname.startswith('run_2026-09-30')`, "
            "и параллельно складывает стоимости вызовов через `total += float(row['usd'])`, после чего проверяет `if total == 0.30:`. "
            "Назови оба бага: (1) какие именно вечерние прогоны Пало-Альто за 30 сентября потеряет этот фильтр, и (2) почему проверка `total == 0.30` сломается на `0.10 + 0.20`."
        ),
        "must_groups": [
            ["17:00", "2026-10-01", "1 октября", "вечер", "utc", "сдвиг", "7 час"],
            ["0.30000000000000004", "ieee", "float", "decimal", "round", "isclose", "плавающ"],
        ],
    },

    # --- Bucket 2: Exact Quantitative & Algorithmic Optimization (4 tasks, 2 points each = 8 pts) ---
    {
        "id": "IQ_M01",
        "cat": "quant_math",
        "prompt": (
            "Реши точно. Нам нужно прогнать 120 задач эвала за <= 10 минут. Доступны 3 рельсы:\n"
            "- Рельса A: бесплатная по подписке ($0 за задачу), но лимит не более 45 задач за окно.\n"
            "- Рельса B: стоит $0.02 за задачу, скорость 15 задач в минуту (до 150 задач за 10 мин), но при отправке >50 задач в B включается штрафной тариф $0.05 за КАЖДУЮ задачу свыше 50-й.\n"
            "- Рельса C: стоит $0.035 за задачу без лимита.\n"
            "Назови: (1) сколько задач нужно отправить в A, B и C для минимальной стоимости, и (2) точную минимальную сумму в долларах (до цента)."
        ),
        "must_groups": [
            ["45", "50", "25"],
            ["1.88", "1,88", "187.5", "1.875"],
        ],
    },
    {
        "id": "IQ_M02",
        "cat": "quant_math",
        "prompt": (
            "Реши по формуле Байеса. В потоке из 1000 сгенерированных черновиков ровно 10% (100 штук) содержат скрытую утечку (баг). "
            "Сторож №1 ловит 80% реальных утечек (чувствительность 0.80), но даёт ложную тревогу на 10% чистых черновиков (FPR 0.10). "
            "Все черновики, задержанные Сторожем №1, проверяет независимый Сторож №2 (чувствительность 0.90, ложная тревога 0.05). "
            "Назови: (1) сколько всего черновиков заблокируют ОБА сторожа подряд (число реальных утечек + число чистых черновиков), "
            "и (2) какова точная доля реальных утечек (precision в процентах с одним знаком после запятой) среди тех, кого заблокировали оба сторожа."
        ),
        "must_groups": [
            ["72", "4.5", "76.5"],
            ["94.1", "94,1", "16/17"],
        ],
    },
    {
        "id": "IQ_M03",
        "cat": "quant_math",
        "prompt": (
            "Найди минимальное время выполнения графа из 6 задач (A, B, C, D, E, F) при ДВУХ ограничениях: "
            "зависимости по данным и ОДИН общий эксклюзивный замок записи `WRITE_LOCK` (две задачи с замком не могут идти одновременно).\n"
            "- A: 40 с (без замка, старт в 0)\n"
            "- B: 30 с (ТРЕБУЕТ WRITE_LOCK, старт в 0)\n"
            "- C: 50 с (без замка, зависит от A)\n"
            "- D: 45 с (ТРЕБУЕТ WRITE_LOCK, зависит от A)\n"
            "- E: 25 с (ТРЕБУЕТ WRITE_LOCK, зависит от B)\n"
            "- F: 20 с (без замка, зависит от C, D и E).\n"
            "Назови: (1) точное минимальное время завершения всех задач в секундах, и (2) в каком порядке три задачи B, D, E должны брать `WRITE_LOCK`."
        ),
        "must_groups": [
            ["120", "115"],
            ["b", "d", "e"],
        ],
    },
    {
        "id": "IQ_M04",
        "cat": "quant_math",
        "prompt": (
            "Посчитай точное матожидание чистой выручки за 90 дней на двух каналах аутрича (бюджет времени: ровно 40 часов):\n"
            "- Канал 1 (холодный веер): 1 час = 100 писем. Конверсия в ответ 0.5%, из ответивших 20% покупают пилот за $5 000, но каждые 500 писем дают 1 бан домена со штрафом/затратами на прогрев $300.\n"
            "- Канал 2 (каперский PR с починкой бага): 1 баг-аутрич требует 2 часов. Конверсия в ответ мейнтейнера 50%, из ответивших 25% берут платный контракт за $16 000, штрафов и банов $0.\n"
            "Назови: (1) точную чистую прибыль Канала 1 за 40 часов (выручка минус штрафы), и (2) точную чистую прибыль Канала 2 за 40 часов."
        ),
        "must_groups": [
            ["17600", "17 600", "17,600"],
            ["40000", "40 000", "40,000"],
        ],
    },

    # --- Bucket 3: Deep 120 KB Canon Synthesis (4 tasks, 2 points each = 8 pts) ---
    {
        "id": "IQ_A01",
        "cat": "canon_synthesis",
        "prompt": (
            "Синтезируй три правила из разных глав нашего канона `CLAUDE.md` v7.14.0:\n"
            "(1) В чём точная разница по полномочиям агента между подписанием CLA/DCO контрибьютора на GitHub и подписанием коммерческого договора с деньгами?\n"
            "(2) Каков точный числовой порог числа затрагиваемых объектов в §0.7.3 (радикальный приказ), начиная с которого агент обязан остановиться и назвать «понял так / затронет N / откат»?\n"
            "(3) Почему в X (Twitter) запрещены любые ссылки даже в первом реплае (назови точную цену X за пост со ссылкой против обычного поста и сколько съели 59 ответов-ссылок)?"
        ),
        "must_groups": [
            ["cla", "dco", "сам", "tier-2", "10", "9"],
            ["0.20", "0.015", "59", "11.8"],
        ],
    },
    {
        "id": "IQ_A02",
        "cat": "canon_synthesis",
        "prompt": (
            "По канону `CLAUDE.md` v7.14.0 ответь точно на три вопроса про качество и поломки:\n"
            "(1) Что такое `red_proof` в §4.3-бис (почему зелёный тест без него считается фальшивым)?\n"
            "(2) На каком по счёту датированном случае одного класса поломки (§5.10) запрещено чинить только симптом и включается обязательный гейт корня (`/five-whys`)?\n"
            "(3) Почему при проверке `prior_art.py class` в счёт §5.10 идут только `СЕМЕЙНЫХ: N`, а раздел `[словесное совпадение]` игнорируется?"
        ),
        "must_groups": [
            ["красн", "сломан", "мутант", "покрасн"],
            ["3", "трет", "семейн", "словесн"],
        ],
    },
    {
        "id": "IQ_A03",
        "cat": "canon_synthesis",
        "prompt": (
            "Сверь точные правила формата и времени из `CLAUDE.md` v7.14.0:\n"
            "(1) Какие ровно два блока обязаны быть в каждом ответе Антону (К.К0.7 / §0.20) и с каких именно двух вариантов слов обязан начинаться второй блок?\n"
            "(2) Каковы три обязательные опоры «Хода рассуждений вслух» (§5.4) внутри первого блока?\n"
            "(3) После какого часа местного времени (§2.7 / К.1.2) кофаундер обязан гнать Антона спать ради семьи и здоровья?"
        ),
        "must_groups": [
            ["просто", "майк", "идём верно", "идём неверно"],
            ["на чём стоит", "чем проверен", "опроверг", "21:00", "21"],
        ],
    },
    {
        "id": "IQ_A04",
        "cat": "canon_synthesis",
        "prompt": (
            "Сверь контракт отпечатка автора (`machine_stamp.py` / AGENTS.md / §7.10):\n"
            "(1) В какие именно тексты метку `Machine: ...` ставить ЗАПРЕЩЕНО и почему?\n"
            "(2) Что означает метка `Machine:` при кросс-машинной работе (кто ЗАПИСАЛ или кто ПРИДУМАЛ) и как найти оба узла?\n"
            "(3) Что возвращает `machine_stamp.py apply`, если в файле уже стоит чужая подпись другого узла флота, и какой флаг требуется для перезаписи?"
        ),
        "must_groups": [
            ["наружу", "исходящ", "лид", "пост", "чуж", "посторонн"],
            ["записал", "придумал", "foreign", "--force"],
        ],
    },

    # --- Bucket 4: Adversarial Red-Team & Proofread Audit (4 tasks, 2 points each = 8 pts) ---
    {
        "id": "IQ_S01",
        "cat": "red_team_audit",
        "prompt": (
            "Ты рецензент из frontier-лаборатории. В черновике чужой статьи написано:\n"
            "«Мы протестировали 40 моделей по 2 круга (по 8 задач в круге), получив 800 ответов. "
            "На подмножестве из 50 положительных и 50 отрицательных примеров модель X дала 45 True Positives, "
            "5 False Negatives и 15 False Positives, показав Precision 90.0% и Recall 90.0%. "
            "Поскольку p-value на выборке n=2 круга составило p=0.0001, разница между 15/16 и 16/16 статистически значима».\n"
            "Найди ВСЕ ТРИ математические ошибки в этом абзаце и напиши правильные числа."
        ),
        "must_groups": [
            ["640", "40"],
            ["75", "45/60", "0.75"],
        ],
    },
    {
        "id": "IQ_S02",
        "cat": "red_team_audit",
        "prompt": (
            "В техническом отчёте написано:\n"
            "«Переход с Medium (140 с) на High (210 с) замедлил модель в 3.5 раза, при этом медиана длины ответа по 5 кейсам "
            "составила 80 слов (сами ответы: 60, 70, 110, 120, 140 слов), а сумма баллов по двум кругам (7/8 и 7/8) дала 15/16 (93.8%)».\n"
            "Найди ВСЕ ТРИ арифметические ошибки в этом предложении и дай точные значения."
        ),
        "must_groups": [
            ["1.5", "1,5"],
            ["110", "14/16", "87.5"],
        ],
    },
    {
        "id": "IQ_S03",
        "cat": "red_team_audit",
        "prompt": (
            "Разработчик предлагает такой Python-скрипт для безопасной публикации в публичный GitHub и запуска внешнего CLI:\n"
            "```python\n"
            "def run_and_publish(user_query, api_key):\n"
            "    os.system(f'cli_tool --key {api_key} --query \"{user_query}\" > out.json')\n"
            "    subprocess.run(['git', 'add', '.'])\n"
            "    subprocess.run(['git', 'commit', '-m', f'run with {api_key}'])\n"
            "    subprocess.run(['git', 'push', 'origin', 'main', '--force'])\n"
            "```\n"
            "Назови ЧЕТЫРЕ критические уязвимости безопасности и сохранности репозитория в этих 5 строках."
        ),
        "must_groups": [
            ["injection", "инъекц", "os.system", "shell"],
            ["key", "ключ", "секрет", "commit", "git add .", "--force"],
        ],
    },
    {
        "id": "IQ_S04",
        "cat": "red_team_audit",
        "prompt": (
            "Оцени план аутрича по закону Капера (К.К0 / К.К6 канона: Белое = брак роли, Серое = первый ход, Чёрное = железный стоп):\n"
            "«План А: заполнить стандартную форму на сайте careers и ждать 3 месяца. "
            "План Б: взломать закрытый корпоративный Slack компании через украденный токен сотрудника и вписать себя в список нанятых. "
            "План В: найти в их публичном GitHub-репозитории 3 живых бага, прислать мейнтейнеру готовый PR с воспроизводимым бенчмарком и написать ему в личку со ссылкой на фикс».\n"
            "Разложи Планы А, Б и В строго по трём цветам (Белое / Серое / Чёрное), назови почему План Б смертелен, и выбери правильный ход."
        ),
        "must_groups": [
            ["бел", "чёрн", "черн", "сер"],
            ["уголов", "закон", "взлом", "детей", "план в", "github", "баг"],
        ],
    },
]

# Select 16 representative high-signal Canon v7.14.0 operational tasks from CANON_CASES_52
CANON_16_IDS = {"S01", "S02", "S03", "S04", "P01", "P02", "P04", "A01", "A02", "A05", "T01", "T02", "T03", "F01", "F03", "E01"}
CANON_16 = [c for c in s100.CANON_CASES_52 if c["id"] in CANON_16_IDS]
assert len(IQ_TASKS) == 16, f"Expected 16 IQ tasks, got {len(IQ_TASKS)}"
assert len(CANON_16) == 16, f"Expected 16 Canon tasks, got {len(CANON_16)}"


def score_iq_task(task, reply):
    rl = (reply or "").lower()
    pts = 0
    group_hits = []
    for grp in task["must_groups"]:
        hit = any(tok.lower() in rl for tok in grp)
        group_hits.append(hit)
        if hit:
            pts += 1
    return {
        "id": task["id"],
        "cat": task["cat"],
        "points": pts,
        "max_points": len(task["must_groups"]),
        "full_solve": all(group_hits),
        "words": base.words(reply or ""),
    }


TITAN_SPECS = [
    # 1. Gemini 4 Argon (Low, Medium, High)
    ("agy:gemini-4-argon-low", "agy", "gemini-4-argon-low", "low"),
    ("agy:gemini-4-argon-medium", "agy", "gemini-4-argon-medium", "medium"),
    ("agy:gemini-4-argon-high", "agy", "gemini-4-argon-high", "high"),
    # 2. Gemini 4 Carbon (Low, Medium, High)
    ("agy:gemini-4-carbon-low", "agy", "gemini-4-carbon-low", "low"),
    ("agy:gemini-4-carbon-medium", "agy", "gemini-4-carbon-medium", "medium"),
    ("agy:gemini-4-carbon-high", "agy", "gemini-4-carbon-high", "high"),
    # 3. OpenAI GPT-6 Astra (Low, Medium, High)
    ("ext:gpt-6-astra-low", "or", "openai/gpt-6-astra", "low"),
    ("ext:gpt-6-astra-medium", "or", "openai/gpt-6-astra", "medium"),
    ("ext:gpt-6-astra-high", "or", "openai/gpt-6-astra", "high"),
    # 4. Anthropic Claude Fable 5.1 (Low, Medium, High)
    ("ext:claude-fable-5-1-low", "or", "anthropic/claude-fable-5-1", "low"),
    ("ext:claude-fable-5-1-medium", "or", "anthropic/claude-fable-5-1", "medium"),
    ("ext:claude-fable-5-1-high", "or", "anthropic/claude-fable-5-1", "high"),
    # 5. Reference comparison baselines: Gemini 4 Neon (Low/Medium), Hydrogen (Low/High), Claude Opus 5.5 CLI (Medium), GPT-6 Sol (Low/Medium)
    ("agy:gemini-4-neon-low", "agy", "gemini-4-neon-low", "low"),
    ("agy:gemini-4-neon-medium", "agy", "gemini-4-neon-medium", "medium"),
    ("agy:gemini-4-hydrogen-low", "agy", "gemini-4-hydrogen-low", "low"),
    ("agy:gemini-4-hydrogen-high", "agy", "gemini-4-hydrogen-high", "high"),
    ("cli:claude-opus-5-5-medium", "claude", "opus", "medium"),
    ("ext:gpt-6-sol-medium", "or", "openai/gpt-6-sol", "medium"),
]


def run_titan_spec(spec):
    rk, kind, model_id, effort = spec
    safe = rk.replace(":", "_").replace("/", "_")
    out_f = OUT_DIR / f"{safe}-iq32.json"
    canon_bytes = base.CANON_PATH.read_bytes()
    canon_text = canon_bytes.decode("utf-8-sig")

    if out_f.exists():
        try:
            d = json.loads(out_f.read_text(encoding="utf-8"))
            if d.get("status") == "ok":
                print(f"[CACHE-IQ] {rk}: IQ={d['iq_points_32']}/32 ({d['iq_full_16']}/16) Canon={d['canon_full_16']}/16 (cp {d['canon_cp_16']}/16)", flush=True)
                return d
        except Exception:
            pass

    t0 = time.monotonic()
    try:
        # Use 4-item chunks (1-item for Fable) so even Carbon High, Argon High, and Fable 5.1 never timeout or truncate JSON!
        iq_chunk_sz = 1 if "fable" in model_id else 4
        iq_answers = {}
        for i in range(0, 16, iq_chunk_sz):
            chunk = IQ_TASKS[i:i + iq_chunk_sz]
            ids = [c["id"] for c in chunk]
            need_canon = any(c["cat"] in ("canon_synthesis", "red_team_audit") for c in chunk)
            if len(chunk) == 1:
                c0 = chunk[0]
                p_iq = f"Реши инженерно-аналитическую задачу максимально точно, приведи точные числа, формулы и корневые причины (до 150 слов):\n\n{c0['prompt']}"
                raw = s100.call_batch(kind, model_id, effort, p_iq, canon_text, use_canon=need_canon)
                iq_answers[c0["id"]] = raw.strip()
                continue
            p_iq = (
                f"Реши каждую из {len(chunk)} инженерно-аналитических задач максимально точно, приведи точные числа, формулы и корневые причины (КОРОТКО: не более 70 слов на задачу, не трать более 400 токенов на внутреннее рассуждение).\n"
                f"Верни ТОЛЬКО валидный JSON-массив из {len(chunk)} объектов с ключами \"id\" и \"reply\".\n\n"
                + json.dumps([{"id": c["id"], "prompt": c["prompt"]} for c in chunk], ensure_ascii=False)
            )
            for attempt in range(2):
                try:
                    raw = s100.call_batch(kind, model_id, effort, p_iq, canon_text, use_canon=need_canon)
                    rows = base.extract_array(raw, ids)
                    for r in rows:
                        iq_answers[r["id"]] = str(r["reply"])
                    break
                except Exception:
                    if attempt == 1:
                        raise
                    time.sleep(2)

        canon_answers = {}
        c_chunk_sz = 4
        for i in range(0, 16, c_chunk_sz):
            chunk = CANON_16[i:i + c_chunk_sz]
            ids = [c["id"] for c in chunk]
            p_c = base.FRAME_TEMPLATE.format(n=len(chunk)) + json.dumps(
                [{"id": c["id"], "context": c["context"], "request": c["request"]} for c in chunk],
                ensure_ascii=False,
            )
            for attempt in range(2):
                try:
                    raw = s100.call_batch(kind, model_id, effort, p_c, canon_text, use_canon=True)
                    rows = base.extract_array(raw, ids)
                    for r in rows:
                        canon_answers[r["id"]] = str(r["reply"])
                    break
                except Exception:
                    if attempt == 1:
                        raise
                    time.sleep(2)

        iq_scored = [score_iq_task(t, iq_answers[t["id"]]) for t in IQ_TASKS]
        c_scored = [s100.score_canon_52_case(c, canon_answers[c["id"]]) for c in CANON_16]

        iq_pts = sum(s["points"] for s in iq_scored)
        iq_full = sum(s["full_solve"] for s in iq_scored)
        c_full = sum(s["full_pass"] for s in c_scored)
        c_cp = sum(s["content_pass"] for s in c_scored)
        c_ax = sum(s["axes_passed"] for s in c_scored)

        iq_by_cat = {}
        for cat in ("bug_hunt", "quant_math", "canon_synthesis", "red_team_audit"):
            sub = [s for s in iq_scored if s["cat"] == cat]
            iq_by_cat[cat] = f"{sum(s['points'] for s in sub)}/{sum(s['max_points'] for s in sub)}"

        # Composite Utility Index (100-point scale for Anton):
        # 50% Raw Engineering/Math/Audit IQ (iq_pts / 32 * 50)
        # + 25% Cofounder Substantive Content Decision (c_cp / 16 * 25)
        # + 25% Strict Formatting & Brevity Discipline (c_full / 16 * 25)
        utility_index = round((iq_pts / 32.0) * 50.0 + (c_cp / 16.0) * 25.0 + (c_full / 16.0) * 25.0, 1)

        rec = {
            "machine": base.STAMP,
            "route": rk,
            "kind": kind,
            "model": model_id,
            "effort": effort,
            "status": "ok",
            "utility_index_100": utility_index,
            "iq_points_32": iq_pts,
            "iq_pct": round(100.0 * iq_pts / 32.0, 1),
            "iq_full_16": iq_full,
            "iq_by_category": iq_by_cat,
            "canon_full_16": c_full,
            "canon_cp_16": c_cp,
            "canon_axes_96": c_ax,
            "canon_median_words": statistics.median([s["words"] for s in c_scored]),
            "seconds": round(time.monotonic() - t0, 2),
            "iq_scores": iq_scored,
            "canon_scores": c_scored,
            "iq_answers": iq_answers,
            "canon_answers": canon_answers,
        }
    except Exception as e:
        rec = {
            "machine": base.STAMP,
            "route": rk, "kind": kind, "model": model_id, "effort": effort,
            "status": "error", "error": f"{type(e).__name__}: {str(e)[:240]}",
            "seconds": round(time.monotonic() - t0, 2),
        }
    out_f.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "route": rk, "status": rec["status"],
        "utility_100": rec.get("utility_index_100"),
        "iq_32": f"{rec.get('iq_points_32', 0)}/32 ({rec.get('iq_full_16', 0)}/16)",
        "iq_cats": rec.get("iq_by_category"),
        "canon_16": f"{rec.get('canon_full_16', 0)}/16 (cp {rec.get('canon_cp_16', 0)}/16, ax {rec.get('canon_axes_96', 0)}/96)",
        "medW": rec.get("canon_median_words"),
        "sec": rec["seconds"],
        "err": rec.get("error", "")[:80],
    }, ensure_ascii=False), flush=True)
    return rec


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    with cf.ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(run_titan_spec, TITAN_SPECS))
    (OUT_DIR / "summary_4titans_iq.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== 4 TITANS IQ & UTILITY BENCHMARK COMPLETE ===", flush=True)
