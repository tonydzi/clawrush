# -*- coding: utf-8 -*-
"""report.py: out/results.json -> markdown table for the benchmark article, plus judge calibration.

Written on the lab hub, 2026-11-10
Usage: python report.py [out_dir]  -> prints markdown; writes <out_dir>/report.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
d = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
S = d["summary"]
CATS = ["single-hop", "multi-hop", "open-domain", "temporal"]
NAMES = {"zep": "Zep Cloud contexts (published by Zep)", "mem0": "Mem0 OSS 2.2.1 (fact extraction)",
         "graphiti": "Graphiti OSS 0.31.2 (Zep's open core, no cross-encoder)", "ours": "Our time-stamped turn log (dense E5)",
         "full": "Full context (no memory system)", "zepans": "Zep's published answers, re-judged by our judge",
         "zepans_upstream": "Zep's published answers, Zep's own judge"}
ORDER = ["full", "zep", "mem0", "ours", "graphiti", "zepans", "zepans_upstream"]


def fmt(cell):
    if not cell or cell["mean"] is None:
        return "—"
    return f"{cell['mean']:.1f}" + (f" ± {cell['sd']:.1f}" if cell.get("sd") is not None else "")


def table():
    rows = []
    keys = sorted(S, key=lambda k: ORDER.index(S[k]["system"]) if S[k]["system"] in ORDER else 99)
    for k in keys:
        v = S[k]; sysname = v["system"]; m = v["models"]
        rows.append(f"| {NAMES.get(sysname, sysname)} | {fmt(v['overall'])} | " + " | ".join(fmt(v[c]) for c in CATS)
                    + f" | {v['overall']['runs']} | {m['reader']} / {m['judge']} |")
    head = ("| System | Overall | Single-hop | Multi-hop | Open-domain | Temporal | Runs | Reader / Judge |\n"
            "|---|---:|---:|---:|---:|---:|---:|---|")
    return head + "\n" + "\n".join(rows)


def calibration():
    """Agreement between our judge and Zep's judge on Zep's own published answers."""
    ours = {json.loads(l)["qid"]: json.loads(l)["label"] for l in (OUT / "jud_zepans_r1.jsonl").read_text(encoding="utf-8-sig").splitlines()}
    up = {json.loads(l)["qid"]: json.loads(l)["label"] for l in (OUT / "jud_zepans_upstream_r1.jsonl").read_text(encoding="utf-8-sig").splitlines()}
    common = [q for q in ours if q in up]
    n = len(common)
    agree = sum(ours[q] == up[q] for q in common)
    o_yes = sum(ours[q] == "CORRECT" for q in common); u_yes = sum(up[q] == "CORRECT" for q in common)
    po = agree / n; pe = (o_yes / n) * (u_yes / n) + (1 - o_yes / n) * (1 - u_yes / n)
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    return (f"Judge calibration on Zep's {n} published answers: our judge CORRECT {o_yes} ({100*o_yes/n:.1f}%), "
            f"Zep's judge CORRECT {u_yes} ({100*u_yes/n:.1f}%), agreement {agree}/{n} = {100*po:.1f}%, Cohen's kappa {kappa:.2f}.")


ref = d["reference_zep_blog"]
has_cal = (OUT / "jud_zepans_r1.jsonl").exists() and (OUT / "jud_zepans_upstream_r1.jsonl").exists()
md = (f"## LoCoMo by Zep's ruler ({d['ruler']}), N = {d['n_expected']}, K = {d['K']}"
      f"{' — SMOKE SUBSET' if d.get('smoke') else ''}\n\n{table()}\n\n"
      f"Reference numbers from Zep's post (their models gpt-4o-mini / gpt-4o-mini): Zep Cloud {ref['zep_cloud']}, "
      f"full context {ref['gpt-4o-mini_full_context']}, Mem0 Graph {ref['mem0_graph_from_mem0_paper']} and "
      f"Mem0 {ref['mem0_from_mem0_paper']} (the two Mem0 numbers are quoted by Zep from Mem0's paper).\n\n"
      f"{calibration() if has_cal else ''}\n")
(OUT / "report.md").write_text(md, encoding="utf-8")
print(md)
