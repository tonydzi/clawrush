#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""codex_ttl.py -- сколько живёт кэш Codex: доля холодных вызовов против паузы перед вызовом.

ВХОД: каталог с файлами codex_<узел>.jsonl от зонда codex_probe.py (строка на сессию:
calls = [ts, вход, из_кэша, ход_начат]). ВЫХОД: таблицы в stdout + data/codex_ttl.json.
Холодный вызов: из кэша прочитано меньше половины ПРЕДЫДУЩЕГО контекста (то, что могло быть
в кэше); считаем только вызовы, где предыдущий контекст от 30K. рельса: локально, 0 LLM.
Machine: MacStudioM4 · Agent: Claude Code (claude-fable-5-2) · Operator: Anton · 2026-11-20
"""
import glob
import json
import os
import sys
from collections import defaultdict

BINS = [(0, 300, "0-5 мин"), (300, 600, "5-10 мин"), (600, 1800, "10-30 мин"), (1800, 3600, "30-60 мин"),
        (3600, 7200, "1-2 ч"), (7200, 6 * 3600, "2-6 ч"), (6 * 3600, 12 * 3600, "6-12 ч"),
        (12 * 3600, 86400, "12-24 ч"), (86400, 3 * 86400, "1-3 сут"), (3 * 86400, 10 ** 9, ">3 сут")]


def gbin(g):
    for a, b, n in BINS:
        if a <= g < b:
            return n


def main():
    src = sys.argv[1]
    tab = defaultdict(lambda: [0, 0, 0, 0])   # n, cold, uncached tokens, ctx tokens
    by_model = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    by_node = defaultdict(lambda: [0, 0, 0])
    meta, seen, wins, peaks = [], set(), defaultdict(set), defaultdict(list)
    for f in sorted(glob.glob(os.path.join(src, "codex_*.jsonl"))):
        node = os.path.basename(f)[6:-6]
        for line in open(f, encoding="utf-8"):
            d = json.loads(line)
            if d.get("meta"):
                meta.append((node, d["files"], d["zst"]))
                continue
            if d["sid"] in seen:
                continue
            seen.add(d["sid"])
            by_node[node][0] += 1
            wins[d["model"]].add(d["win"])
            peaks[d["model"]].append(max(c[1] for c in d["calls"]))
            prev = None
            for c in d["calls"]:
                if prev and prev[1] >= 30000 and c[0] >= prev[0]:
                    g = gbin(c[0] - prev[0])
                    cold = c[2] < 0.5 * prev[1]
                    x = tab[g]
                    x[0] += 1
                    x[1] += cold
                    x[2] += c[1] - c[2]
                    x[3] += c[1]
                    m = by_model[d["model"]][g]
                    m[0] += 1
                    m[1] += cold
                    if c[0] - prev[0] >= 3600:
                        by_node[node][1] += 1
                        by_node[node][2] += cold
                prev = c
    print("узел: несжатых журналов / сжатых .zst (не прочитаны):", meta)
    print("сессий с вызовами:", len(seen), {k: v[0] for k, v in by_node.items()})
    print("\nпауза      | вызовов | холодных | доля  | некэш. вход M")
    out = {}
    for _, _, n in BINS:
        x = tab[n]
        if x[0]:
            print(f"{n:>10} | {x[0]:>7} | {x[1]:>8} | {100 * x[1] / x[0]:>4.1f}% | {x[2] / 1e6:.1f}")
            out[n] = x
    print("\nпо моделям (пауза: вызовов/холодных):")
    for m, t in sorted(by_model.items(), key=lambda kv: -sum(v[0] for v in kv[1].values())):
        tot = sum(v[0] for v in t.values())
        if tot < 200:
            continue
        pk = sorted(peaks[m])
        print(f"  {m} окно {sorted(wins[m])} пик p50/p90/max {pk[len(pk) // 2] // 1000}K/"
              f"{pk[int(len(pk) * .9)] // 1000}K/{pk[-1] // 1000}K:",
              ", ".join(f"{n} {t[n][0]}/{t[n][1]}" for _, _, n in BINS[3:] if t[n][0]))
    print("\nвозвраты после часа по узлам (сессий, возвратов, холодных):", dict(by_node))
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "codex_ttl.json"), "w") as fh:
        json.dump({"meta": meta, "sessions": len(seen), "table": out, "by_node": by_node}, fh, ensure_ascii=False)


if __name__ == "__main__":
    main()
