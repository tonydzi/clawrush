#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tables.py -- таблицы для статьи про срок жизни кэша промпта (только агрегаты, 0 LLM).

ВХОД: ../session-context-audit/data/sessions.jsonl, report.json, codex_ttl.json (прибор аудита 20.11.2026).
ВЫХОД: tables.json и tables.md рядом. Имён сессий, путей и текстов в выходе нет.
Кто зовёт: человек/агент руками перед правкой статьи. Что ломается: смена формата sessions.jsonl.
рельса: локально, 0 LLM.
Machine: MacStudioM4 · Agent: Claude Code (claude-fable-5-2) · Operator: Anton · 2026-11-20
"""
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.realpath(__file__))
AUD = os.path.join(HERE, "..", "session-context-audit")
sys.path.insert(0, AUD)
import analyze as A  # noqa: E402

MIN_BINS = [(0, 5), (5, 30), (30, 50), (50, 55), (55, 58), (58, 60), (60, 62), (62, 65), (65, 90),
            (90, 300), (300, 1440), (1440, 10 ** 9)]


def label(a, b):
    if b >= 10 ** 9:
        return ">24 h"
    if a >= 300:
        return f"{a // 60}-{b // 60} h"
    if a >= 90:
        return "1.5-5 h"
    return f"{a}-{b} min"


def load_b():
    S = [json.loads(l) for l in open(os.path.join(AUD, "data", "sessions.jsonl"), encoding="utf-8")]
    seen = set()
    for s in sorted(S, key=lambda s: s["calls"][0][0]):
        s["own"] = [c[8] not in seen for c in s["calls"]]
        seen.update(c[8] for c in s["calls"])
    S = [s for s in S if any(s["own"])]
    for s in S:
        s["rw"] = A.read_w(s["model"])
        s["n_h"] = sum(1 for c, o in zip(s["calls"], s["own"]) if o and A.human(c))
    S.sort(key=lambda s: s["calls"][-1][0], reverse=True)
    dialog = [s for s in S if s["n_h"] >= 2 and s["entry"] not in A.ROBOT]
    return dialog[:500]


def cliff(B, harness, only_human):
    """Доля холодных вызовов по паузе перед вызовом. Холодный: из кэша прочитано меньше половины входа."""
    tab = {label(a, b): [0, 0] for a, b in MIN_BINS}
    for s in B:
        if s["harness"] != harness:
            continue
        prev = None
        for c, own in zip(s["calls"], s["own"]):
            if own and prev and prev[1] >= 50000 and c[1] >= 50000 and (A.human(c) or not only_human):
                g = (c[0] - prev[0]) / 60.0
                for a, b in MIN_BINS:
                    if a <= g < b:
                        x = tab[label(a, b)]
                        x[0] += 1
                        x[1] += (c[1] - c[2]) >= 0.5 * c[1]
                        break
            prev = c
    return tab


def main():
    B = load_b()
    rep = json.load(open(os.path.join(AUD, "data", "report.json"), encoding="utf-8"))[1]
    ctl = json.load(open(os.path.join(AUD, "data", "codex_ttl.json"), encoding="utf-8"))
    last = [s["calls"][-1][0] for s in B]
    iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    out = {
        "sample_b": {"n": len(B), "last_activity_from": iso(min(last)), "last_activity_to": iso(max(last)),
                     "claude_sessions": sum(s["harness"] == "claude" for s in B),
                     "codex_sessions": sum(s["harness"] == "codex" for s in B),
                     "nodes": len({s["node"] for s in B}), "calls": rep["totals"]["calls"]},
        "claude_cliff_all_calls": cliff(B, "claude", False),
        "claude_cliff_human_turns": cliff(B, "claude", True),
        "codex_ttl": {k: [v[0], v[1]] for k, v in ctl["table"].items()},
        "codex_sessions": ctl["sessions"], "codex_nodes": len(ctl["meta"]),
        "codex_zst_unread": sum(m[2] for m in ctl["meta"]),
        "peak_q": rep["peak_q"], "start_q": rep["start_q"], "totals": rep["totals"],
        "sim": rep["sim"],
    }
    human_cold = sum(v[2] for k, v in rep["cont"].items() if k.split("|")[0] in ("1-5 ч", "5-24 ч", ">24 ч"))
    human_n = sum(v[0] for k, v in rep["cont"].items() if k.split("|")[0] in ("1-5 ч", "5-24 ч", ">24 ч"))
    human_c = sum(v[1] for k, v in rep["cont"].items() if k.split("|")[0] in ("1-5 ч", "5-24 ч", ">24 ч"))
    out["human_returns_after_1h"] = {"n": human_n, "cold": human_c, "eq": human_cold,
                                     "share_of_total": round(human_cold / rep["totals"]["eq"], 4)}
    tot = rep["totals"]["eq"]
    wake = sum(v[1] for k, v in rep["cold_not_after_user"].items() if k.startswith("пауза >1 ч"))
    out["derived"] = {
        "cold_wakes_without_human_after_1h_M": round(wake / 1e6),
        "sim_share_pct": {str(x["T"] // 1000): round(100 * x["saved_eq"] / tot, 1) for x in rep["sim"]},
        "sim_at_resume_share_pct": {str(x["T"] // 1000): round(100 * x["saved_at_resume_eq"] / tot, 1)
                                    for x in rep["sim"]},
        "peak_over_500k_sessions": rep["peak_hist"].get("500K+", 0),
        "human_returns_after_1h_ctx_200k_plus": sum(
            v[0] for k, v in rep["cont"].items()
            if k.split("|")[0] in ("1-5 ч", "5-24 ч", ">24 ч")
            and k.split("|")[1] in ("200-300K", "300-400K", "400-500K", "500K+")),
    }
    json.dump(out, open(os.path.join(HERE, "tables.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = ["## Claude Code: cold calls by idle gap (all calls, context >= 50K)", "",
         "| gap | calls | cold | cold share |", "|---|---:|---:|---:|"]
    for k, (n, c) in out["claude_cliff_all_calls"].items():
        L.append(f"| {k} | {n} | {c} | {100 * c / n:.1f}% |" if n else f"| {k} | 0 | 0 | n/a |")
    L += ["", "## Claude Code: human turns only", "", "| gap | turns | cold | cold share |", "|---|---:|---:|---:|"]
    for k, (n, c) in out["claude_cliff_human_turns"].items():
        L.append(f"| {k} | {n} | {c} | {100 * c / n:.1f}% |" if n else f"| {k} | 0 | 0 | n/a |")
    L += ["", "## Codex CLI: cold calls by idle gap (previous context >= 30K)", "",
          "| gap | calls | cold | cold share |", "|---|---:|---:|---:|"]
    for k, (n, c) in out["codex_ttl"].items():
        L.append(f"| {k} | {n} | {c} | {100 * c / n:.1f}% |")
    open(os.path.join(HERE, "tables.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print(json.dumps({k: out[k] for k in ("sample_b", "human_returns_after_1h", "codex_sessions",
                                          "codex_zst_unread")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
