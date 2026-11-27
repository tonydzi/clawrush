#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bench_hot_memory.py: воспроизводимый бенчмарк слоёв горячей и холодной памяти («радуга слоёв»).

Machine: A-2022BAYAREA (Хаб) · Agent: Antigravity · Operator: Anton · 2026-11-26

Паспорт (§5.8):
  Зачем: эмпирическая проверка архитектуры горячей памяти (дизайн A+B+C+D от 10.11.2026 и план
    эксперимента из DR26-11-21-MACSTUDIOM4-01-0035 / 9759): сравнение 8 режимов поиска
    (только сырые сессии 14 дн, сырые + карточки 14 дн, полная горячая 7/14/30 дн, AND-first быстрая горячая,
    только холодная память, и «радуга слоёв» горячая 14 дн + быстрый холодный слой) на 24 реальных запросах
    в 4 классах задач, с исключением текущей сессии бенчмарка (anti-leakage).
  Вход: ~/.claude/state/hot_memory.db, E:\\Obsidian\\_imports\\_brain_sessions_lex.db, волт E:\\Obsidian\\Anton-Knowledge.
  Выход: E:\\Obsidian\\_imports\\results-hot-memory-bench-2026-11-26.json (все числа для статьи).
  Кто зовёт: сессия бенчмарка /benchmark, регрессионная проверка памяти.
  Что ломается: отсутствие hot_memory.db -> FileNotFoundError.
  рельса: локально, 0 LLM, 0 сети.
"""
import json
import math
import os
import re
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import hot_memory as HM  # noqa: E402
import session_cards as SC  # noqa: E402

VAULT = Path(os.environ.get("OBSIDIAN_VAULT") or r"E:\Obsidian\Anton-Knowledge")
HOT_DB = Path(os.environ.get("HOT_MEMORY_DB") or Path.home() / ".claude" / "state" / "hot_memory.db")
LEX_DB = HERE / "_brain_sessions_lex.db"
OUT_JSON = HERE / "results-hot-memory-bench-2026-11-26.json"

# Исключаем саму текущую сессию бенчмарка, чтобы она не матчила свои же тестовые запросы
EXCLUDE_SIDS = {
    "1a20beb2-15d1-4d38-ad4b-4827173b7c52",
    "card:1a20beb2-15d1-4d38-ad4b-4827173b7c52",
}

ALL_HOT_SOURCES = {
    "sessions",
    "codex",
    "antigravity",
    "cursor",
    "grok",
    "agents",
    "live-subagent",
    "cards",
    "facts",
    "tg",
    "wa",
    "mail",
    "cal",
}

BENCH_QUERIES = [
    # Класс A: Свежая работа в сессиях разных машин (<14 дней)
    {
        "id": "A1",
        "class": "recent_cross_machine",
        "query": "Google Таблица вкладка все-сессии дашборд",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "все-сессии",
    },
    {
        "id": "A2",
        "class": "recent_cross_machine",
        "query": "короткие русские слова падежное окончание",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "окончан",
    },
    {
        "id": "A3",
        "class": "recent_cross_machine",
        "query": "daily_backup_E_to_F карантин DeleteBlockFiles",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "daily_backup",
    },
    {
        "id": "A4",
        "class": "recent_cross_machine",
        "query": "gpt-transcribe против gpt-4o-transcribe",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "transcribe",
    },
    {
        "id": "A5",
        "class": "recent_cross_machine",
        "query": "cofounder consistency 73 frontier efforts",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "73",
    },
    {
        "id": "A6",
        "class": "recent_cross_machine",
        "query": "Доступ Antigravity к сессиям Антона на хабе 8770",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "8770",
    },
    # Класс B: Вопросы по выжимкам сессий (карточки B) и битемпоральным фактам (лента C)
    # Здесь expect_sources разрешает ЛЮБОЙ горячий источник, чтобы честно измерить,
    # может ли сырой поиск без карточек/фактов вытащить ответ в top-5.
    {
        "id": "B1",
        "class": "distilled_cards_facts",
        "query": "поиск в сессиях должен всегда идти и в горячей и в холодной памяти",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "холодной",
    },
    {
        "id": "B2",
        "class": "distilled_cards_facts",
        "query": "подача на Tether не найдена проверены 5442 записи журнала",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "5442",
    },
    {
        "id": "B3",
        "class": "distilled_cards_facts",
        "query": "Где Антон сейчас местоположение Антона город где живёт",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "местоположение",
    },
    {
        "id": "B4",
        "class": "distilled_cards_facts",
        "query": "машины Наташи Русланы Эдиты не синкаются в волт не могу судить",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "наташ",
    },
    {
        "id": "B5",
        "class": "distilled_cards_facts",
        "query": "не доверяет качеству работы горячей памяти на MacStudio",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "доверяет",
    },
    {
        "id": "B6",
        "class": "distilled_cards_facts",
        "query": "Единый дашборд всех сессий парка машин 28 700 сессий",
        "expect_sources": list(ALL_HOT_SOURCES),
        "expect_substr": "28 700",
    },
    # Класс C: Личная переписка и расписание (TG, WA, Gmail, Календарь)
    {
        "id": "C1",
        "class": "personal_comms_schedule",
        "query": "Ownership accepted for 17 spreadsheets Google Sheets",
        "expect_sources": ["mail"],
        "expect_substr": "spreadsheets",
    },
    {
        "id": "C2",
        "class": "personal_comms_schedule",
        "query": "Lisbon 2026 Venture Capital World Summit Arrival",
        "expect_sources": ["mail"],
        "expect_substr": "venture capital",
    },
    {
        "id": "C3",
        "class": "personal_comms_schedule",
        "query": "sent you a message workatastartup Y Combinator",
        "expect_sources": ["mail"],
        "expect_substr": "workatastartup",
    },
    {
        "id": "C4",
        "class": "personal_comms_schedule",
        "query": "FLLM 2026 академическая по LLM Барселона",
        "expect_sources": ["cal"],
        "expect_substr": "fllm",
    },
    {
        "id": "C5",
        "class": "personal_comms_schedule",
        "query": "Microsoft Ignite 2026 Moscone",
        "expect_sources": ["cal"],
        "expect_substr": "ignite",
    },
    {
        "id": "C6",
        "class": "personal_comms_schedule",
        "query": "TASIS Lords Dads Meetup Social Sports Events",
        "expect_sources": ["wa"],
        "expect_substr": "tasis",
    },
    # Класс D: Долгие правила, решения и архитектура (>14 дней, холодный слой волта)
    {
        "id": "D1",
        "class": "cold_standing_rules",
        "query": "decision essence evidence ontology 2026-06-25",
        "expect_sources": ["cold_vault", "cold_lex"],
        "expect_substr": "essence",
    },
    {
        "id": "D2",
        "class": "cold_standing_rules",
        "query": "memory index hot dispatcher 2026-07-04",
        "expect_sources": ["cold_vault", "cold_lex"],
        "expect_substr": "dispatcher",
    },
    {
        "id": "D3",
        "class": "cold_standing_rules",
        "query": "second brain organs without nerves 2026-07-28",
        "expect_sources": ["cold_vault", "cold_lex"],
        "expect_substr": "organs",
    },
    {
        "id": "D4",
        "class": "cold_standing_rules",
        "query": "node doctrine thin anchor shadow first 2026-07-16",
        "expect_sources": ["cold_vault", "cold_lex"],
        "expect_substr": "anchor",
    },
    {
        "id": "D5",
        "class": "cold_standing_rules",
        "query": "session transcripts rag layering 2026-06-25",
        "expect_sources": ["cold_vault", "cold_lex"],
        "expect_substr": "layering",
    },
    {
        "id": "D6",
        "class": "cold_standing_rules",
        "query": "always on memory architecture 2026-06-27",
        "expect_sources": ["cold_vault", "cold_lex"],
        "expect_substr": "always",
    },
]


def build_cold_vault_index():
    """Быстрый индекс заголовков и имён файлов вечных слоёв волта (02-Decisions, 03-Insights, 06-Concepts, 02-Protocols)."""
    docs = []
    for folder in ("02-Decisions", "03-Insights", "06-Concepts", "02-Protocols", "05-Resources/Deep-Research"):
        root = VAULT / folder
        if not root.is_dir():
            continue
        for p in root.rglob("*.md"):
            if ".st" in str(p):
                continue
            stem_norm = p.stem.lower().replace("-", " ").replace("_", " ")
            docs.append((stem_norm, stem_norm, str(p), p.stem))
    return docs


def search_cold_fast(query, vault_docs, n=5):
    """Быстрый поиск по холодным слоям волта (02-Decisions, 03-Insights, 06-Concepts)."""
    toks = [t.lower() for t in re.findall(r"[\w\u0400-\u04FF]{3,}", query) if t.lower() not in ("для", "как", "что", "или")]
    hits = []
    for stem_norm, head_low, path_str, title in vault_docs:
        matched = sum(1 for t in toks if t in stem_norm or t in head_low)
        if matched > 0:
            cov = matched / max(1, len(toks))
            if cov >= 0.5:
                hits.append(
                    {
                        "source": "cold_vault",
                        "node": "VAULT",
                        "title": title,
                        "session_id": "vault:" + title,
                        "snippet": title,
                        "path": path_str,
                        "score": round(cov * 100.0 + matched * 10.0, 3),
                    }
                )
    hits.sort(key=lambda x: -x["score"])
    return hits[:n]


def fast_hot_search(c, query, days=14, sources=None, n=5, now=None, and_first_only_if_enough=False):
    """Воспроизведение ранжирования hot_memory.search со скрабом только top-N выдачи
    и исключением текущей сессии бенчмарка EXCLUDE_SIDS."""
    terms = HM.query_terms(query)
    if not terms:
        return []
    now = now or HM._now()
    cutoff = HM._cutoff(days=days, now=now)
    srcs = HM._expand_sources(sources)
    where = [
        "docs_fts MATCH ?",
        "(ts >= ? OR (source = 'facts' AND kind NOT IN (%s)))" % ",".join("'%s'" % k for k in HM.FACT_CLOSED_KINDS),
    ]
    extra = []
    if srcs:
        where.append("source IN (%s)" % ",".join("?" * len(srcs)))
        extra += srcs
    where.append("driver <> 'robot'")
    sql = (
        "SELECT rowid, bm25(docs_fts, 1.0, 0.4) AS b, source, node, session_id, ts, path, driver, title, "
        "snippet(docs_fts, 0, '«', '»', '…', 16), text, kind FROM docs_fts WHERE %s ORDER BY b LIMIT ?"
        % " AND ".join(where)
    )
    rows = {}
    for r in c.execute(sql, [HM.fts_and(terms), cutoff] + extra + [400]):
        if r[4] not in EXCLUDE_SIDS:
            rows.setdefault(r[0], r)
    distinct_sids = {r[4] for r in rows.values()}
    if len(terms) > 1 and (not and_first_only_if_enough or len(distinct_sids) < n):
        for r in c.execute(sql, [HM.fts_or(terms), cutoff] + extra + [400]):
            if r[4] not in EXCLUDE_SIDS:
                rows.setdefault(r[0], r)

    groups = {}
    for rid, b, source, node, sid, ts, path, driver, title, snip, text, kind in rows.values():
        rel = -b if b is not None else 0.0
        hit = {i for i, t in enumerate(terms) if HM._term_rx(t).search(text or "") or HM._term_rx(t).search(title or "")}
        g = groups.get((source, sid))
        if g is None:
            g = groups[(source, sid)] = {
                "source": source,
                "node": node,
                "title": title or "",
                "session_id": sid,
                "path": path,
                "driver": driver,
                "best": -1.0,
                "snippet": "",
                "ts": "",
                "hit": set(),
                "current": source == "facts" and kind not in HM.FACT_CLOSED_KINDS,
            }
        g["hit"] |= hit
        if ts and ts > g["ts"]:
            g["ts"] = ts
        if rel * (len(hit) + 1) > g["best"]:
            g["best"], g["snippet"] = rel * (len(hit) + 1), snip or ""
    out = []
    for g in groups.values():
        cov = len(g["hit"]) / float(len(terms)) if terms else 1.0
        if not g["hit"]:
            cov = 0.5 / len(terms)
        age = HM._age_days(g["ts"], now)
        tau = HM.TAU.get(g["source"], 14.0)
        decay = 1.0 if g["current"] else math.exp(-age / tau)
        score = g["best"] * cov * cov * decay * HM.W_SOURCE.get(g["source"], 1.0) * HM.W_DRIVER.get(g["driver"], 0.8)
        out.append(
            {
                "source": g["source"],
                "node": g["node"],
                "title": g["title"],
                "session_id": g["session_id"],
                "ts": g["ts"],
                "age_days": round(age, 2),
                "snippet": re.sub(r"\s+", " ", g["snippet"])[:300],
                "path": g["path"],
                "score": float("%.6g" % score),
            }
        )
    out.sort(key=lambda x: -x["score"])
    top = out[:n]
    if top:
        texts_to_scrub = []
        for item in top:
            texts_to_scrub.extend([item["title"], item["snippet"]])
        scrubbed = HM._guarded_texts(texts_to_scrub)
        for idx, item in enumerate(top):
            item["title"] = scrubbed[2 * idx]
            item["snippet"] = scrubbed[2 * idx + 1]
    return top


def eval_hit(hits, q):
    exp_srcs = set(q["expect_sources"])
    exp_sub = q["expect_substr"].lower()
    for rank, h in enumerate(hits[:5], start=1):
        src = h.get("source", "")
        blob = " ".join(
            [str(h.get("title") or ""), str(h.get("snippet") or ""), str(h.get("path") or ""), str(h.get("node") or "")]
        ).lower()
        if src in exp_srcs and exp_sub in blob:
            return 1, round(1.0 / rank, 4), src
    return 0, 0.0, (hits[0].get("source", "") if hits else "none")


def collect_db_stats():
    c = HM.connect(HOT_DB, readonly=True)
    try:
        total_rows = c.execute("SELECT COUNT(*) FROM rows").fetchone()[0]
        total_sessions = c.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        by_source = dict(c.execute("SELECT source, COUNT(*) FROM docs_fts GROUP BY source ORDER BY 2 DESC").fetchall())
        by_sess_source = {
            r[0]: {"sessions": r[1], "rows": r[2], "kb": (r[3] or 0) // 1024}
            for r in c.execute(
                "SELECT source, COUNT(*), SUM(rows), SUM(bytes) FROM sessions GROUP BY source ORDER BY 2 DESC"
            ).fetchall()
        }
        by_node = dict(
            c.execute("SELECT node, COUNT(*) FROM sessions GROUP BY node ORDER BY 2 DESC LIMIT 12").fetchall()
        )
        meta = dict(c.execute("SELECT key, value FROM meta WHERE key IN ('last_ingest', 'cards_last_run')").fetchall())
    finally:
        c.close()
    sc_stat, _ = SC.status(HOT_DB)
    lex_size_mb = round(LEX_DB.stat().st_size / (1024 * 1024), 1) if LEX_DB.is_file() else 0.0
    hot_size_mb = round(HOT_DB.stat().st_size / (1024 * 1024), 1)
    return {
        "hot_db_size_mb": hot_size_mb,
        "lex_db_size_mb": lex_size_mb,
        "total_sessions": total_sessions,
        "total_fts_rows": total_rows,
        "fts_rows_by_source": by_source,
        "sessions_by_source": by_sess_source,
        "top_nodes_by_sessions": by_node,
        "last_ingest": meta.get("last_ingest"),
        "session_cards_summary": {
            "human_sessions_14d": sum(v["human"] for v in sc_stat["nodes"].values()),
            "carded_total": sum(v["carded"] for v in sc_stat["nodes"].values()),
            "zero_llm_cards": sum(v["zero_llm"] for v in sc_stat["nodes"].values()),
            "llm_distilled_cards": sum(v["carded"] - v["zero_llm"] for v in sc_stat["nodes"].values()),
            "tiny_skipped": sum(v["tiny"] for v in sc_stat["nodes"].values()),
            "facts_asserted_total": sc_stat["facts_asserted_total"],
            "fts_card_rows": sc_stat["fts_rows"],
        },
    }


def run_benchmark():
    t_init = time.time()
    vault_docs = build_cold_vault_index()
    cold_index_build_ms = round((time.time() - t_init) * 1000, 1)

    c = HM.connect(HOT_DB, readonly=True)
    now = HM._now()

    arms = {
        "1_hot_raw_sessions_14d": lambda q: fast_hot_search(
            c, q, days=14, sources="sessions,codex,antigravity,cursor,grok,agents", n=5, now=now
        ),
        "2_hot_raw_plus_cards_14d": lambda q: fast_hot_search(
            c, q, days=14, sources="sessions,codex,antigravity,cursor,grok,agents,cards", n=5, now=now
        ),
        "3_hot_full_7d": lambda q: fast_hot_search(c, q, days=7, sources=None, n=5, now=now),
        "4_hot_full_14d": lambda q: fast_hot_search(c, q, days=14, sources=None, n=5, now=now),
        "5_hot_full_30d": lambda q: fast_hot_search(c, q, days=30, sources=None, n=5, now=now),
        "6_hot_full_14d_and_first": lambda q: fast_hot_search(
            c, q, days=14, sources=None, n=5, now=now, and_first_only_if_enough=True
        ),
        "7_cold_vault_only": lambda q: search_cold_fast(q, vault_docs, n=5),
        "8_rainbow_hot14d_plus_cold": lambda q: (
            fast_hot_search(c, q, days=14, sources=None, n=3, now=now, and_first_only_if_enough=True)
            + search_cold_fast(q, vault_docs, n=2)
        )[:5],
    }

    arm_results = {}
    for arm_name, fn in arms.items():
        latencies = []
        hits_all = []
        mrr_all = []
        by_class = {}
        per_query = []
        for q in BENCH_QUERIES:
            t0 = time.perf_counter()
            res = fn(q["query"])
            ms = round((time.perf_counter() - t0) * 1000, 2)
            latencies.append(ms)
            hit, mrr, top_src = eval_hit(res, q)
            hits_all.append(hit)
            mrr_all.append(mrr)
            cls = q["class"]
            c_bucket = by_class.setdefault(cls, {"queries": 0, "hits": 0, "mrr_sum": 0.0, "ms_list": []})
            c_bucket["queries"] += 1
            c_bucket["hits"] += hit
            c_bucket["mrr_sum"] += mrr
            c_bucket["ms_list"].append(ms)
            per_query.append(
                {"id": q["id"], "class": cls, "hit_at_5": hit, "mrr": mrr, "ms": ms, "top_source": top_src}
            )

        class_summary = {}
        for cls, b in by_class.items():
            class_summary[cls] = {
                "queries": b["queries"],
                "hits_at_5": b["hits"],
                "recall_at_5_pct": round(100.0 * b["hits"] / b["queries"], 1),
                "mrr": round(b["mrr_sum"] / b["queries"], 3),
                "p50_ms": round(statistics.median(b["ms_list"]), 1),
            }

        sorted_lat = sorted(latencies)
        p95_idx = min(len(sorted_lat) - 1, int(len(sorted_lat) * 0.95))
        arm_results[arm_name] = {
            "queries_total": len(BENCH_QUERIES),
            "hits_at_5_total": sum(hits_all),
            "recall_at_5_pct": round(100.0 * sum(hits_all) / len(BENCH_QUERIES), 1),
            "mrr": round(sum(mrr_all) / len(BENCH_QUERIES), 3),
            "latency_p50_ms": round(statistics.median(latencies), 1),
            "latency_p95_ms": round(sorted_lat[p95_idx], 1),
            "latency_mean_ms": round(statistics.mean(latencies), 1),
            "by_class": class_summary,
            "per_query": per_query,
        }

    c.close()
    report = {
        "benchmark": "hot-memory-rainbow-layers-2026-11-26",
        "machine": "A-2022BAYAREA",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dr_id": "DR26-11-21-MACSTUDIOM4-01-0035",
        "cold_vault_docs_indexed": len(vault_docs),
        "cold_vault_index_build_ms": cold_index_build_ms,
        "corpus_stats": collect_db_stats(),
        "arms": arm_results,
    }
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved benchmark results to {OUT_JSON}")
    print("\n=== SUMMARY TABLE ===")
    print(f"{'Arm':<28} {'Hits@5':>8} {'Recall@5':>9} {'MRR':>7} {'p50 ms':>8} {'p95 ms':>8} {'Recent':>8} {'Cards/C':>8} {'Comms':>8} {'Cold':>8}")
    for k, v in arm_results.items():
        bc = v["by_class"]
        print(
            f"{k:<28} {v['hits_at_5_total']:>5}/24 {v['recall_at_5_pct']:>8.1f}% {v['mrr']:>7.3f} "
            f"{v['latency_p50_ms']:>8.1f} {v['latency_p95_ms']:>8.1f} "
            f"{bc['recent_cross_machine']['recall_at_5_pct']:>7.1f}% "
            f"{bc['distilled_cards_facts']['recall_at_5_pct']:>7.1f}% "
            f"{bc['personal_comms_schedule']['recall_at_5_pct']:>7.1f}% "
            f"{bc['cold_standing_rules']['recall_at_5_pct']:>7.1f}%"
        )
    return 0


if __name__ == "__main__":
    sys.exit(run_benchmark())
