#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""codex_after_claim.py -- контроль: холодные вызовы Codex по паузе ТОЛЬКО после 21.10.2026.

Зачем: 21.10.2026 сотрудник OpenAI публично написал, что у вошедших пользователей Codex кэш
хранится «forever». Проверяем на своих журналах, видна ли деградация после этой даты.
ВХОД: ../session-context-audit/data/sessions.jsonl (сессии Codex, какие есть в выгрузке).
ВЫХОД: stdout + codex_after_claim.json (только агрегаты). Определение холодного вызова как в codex_ttl.py:
из кэша прочитано меньше половины ПРЕДЫДУЩЕГО контекста, предыдущий контекст от 30K.
рельса: локально, 0 LLM.
Machine: MacStudioM4 · Agent: Claude Code (claude-fable-5-2) · Operator: Anton · 2026-11-20
"""
import json
import os
import time
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.realpath(__file__))
SRC = os.path.join(HERE, "..", "session-context-audit", "data", "sessions.jsonl")
CUT = datetime(2026, 10, 22, tzinfo=timezone.utc).timestamp()  # сутки запаса после поста
BINS = [(0, 300, "0-5 min"), (300, 1800, "5-30 min"), (1800, 3600, "30-60 min"), (3600, 7200, "1-2 h"),
        (7200, 6 * 3600, "2-6 h"), (6 * 3600, 12 * 3600, "6-12 h"), (12 * 3600, 86400, "12-24 h"),
        (86400, 10 ** 9, ">24 h")]


def main():
    tab = defaultdict(lambda: [0, 0])
    nodes, models, n_s, seen, tmin, tmax = defaultdict(int), defaultdict(int), 0, set(), 1e18, 0
    for line in open(SRC, encoding="utf-8"):
        s = json.loads(line)
        if s["harness"] != "codex" or s["sid"] in seen:
            continue
        seen.add(s["sid"])
        used, prev = False, None
        for c in s["calls"]:
            if prev and prev[1] >= 30000 and c[0] >= prev[0] and prev[0] >= CUT:
                g = c[0] - prev[0]
                for a, b, n in BINS:
                    if a <= g < b:
                        tab[n][0] += 1
                        tab[n][1] += c[2] < 0.5 * prev[1]
                        break
                used = True
                tmin, tmax = min(tmin, prev[0]), max(tmax, c[0])
            prev = c
        if used:
            n_s += 1
            nodes[s["node"]] += 1
            models[s["model"]] += 1
    iso = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")
    out = {"sessions": n_s, "nodes": len(nodes), "models": dict(models), "from": iso(tmin), "to": iso(tmax),
           "table": {n: tab[n] for _, _, n in BINS}}
    print(json.dumps({k: v for k, v in out.items() if k != "table"}, ensure_ascii=False))
    print("| gap | calls | cold | cold share |\n|---|---:|---:|---:|")
    for _, _, n in BINS:
        x = tab[n]
        print(f"| {n} | {x[0]} | {x[1]} | {100 * x[1] / x[0]:.0f}% |" if x[0] else f"| {n} | 0 | 0 | n/a |")
    json.dump(out, open(os.path.join(HERE, "codex_after_claim.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
