#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate exact Markdown tables and failure/success quotes from results-2026-11-26.json.

Machine: A-2022BAYAREA (Хаб) · Agent: Antigravity (Gemini 4 Argon) · Operator: Anton · 2026-11-26
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "results-2026-11-26.json"

d = json.loads(DATA_PATH.read_text(encoding="utf-8"))
meta = d["meta"]
by_cond = d["summary_by_condition"]
by_mc = d["summary_by_model_and_condition"]
runs = d["runs"]

print("=== META ===")
print(json.dumps(meta, ensure_ascii=False, indent=2))

print("\n=== TABLE 1: AGGREGATE BY CONDITION (28 cases / 168 axes each) ===")
for c, row in by_cond.items():
    print(c, "->", json.dumps(row, ensure_ascii=False))

print("\n=== TABLE 2: BY MODEL AND CONDITION ===")
for m, conds in by_mc.items():
    for c in ["C_no_header", "A_header_only", "A_plus_tail"]:
        r = conds[c]
        ba = r["by_axis"]
        print(
            f"{m:30s} | {c:13s} | full={r['full_pass_6of6']}/4 | spine5={r['spine_5of5']}/4 | "
            f"axes={r['axes_passed']:2d}/24 ({r['axes_pct']:5.1f}%) | "
            f"2blk={ba['two_blocks']}/4 ba={ba['before_after']}/4 pil={ba['reasoning_pillars']}/4 "
            f"verd={ba['cofounder_verdict']}/4 noask={ba['no_timid_ask']}/4 grey={ba['privateer_grey_not_black']}/4 | "
            f"sec={r['mean_sec']}"
        )

print("\n=== TABLE 3: BY SCENARIO AND CONDITION (7 models per cell) ===")
scenarios = ["T1_devrel", "T2_pipeline", "T3_objection", "T4_fundraise_black_trap"]
for sc in scenarios:
    for c in ["C_no_header", "A_header_only", "A_plus_tail"]:
        sub = [r for r in runs if r["scenario_id"] == sc and r["condition"] == c]
        full = sum(1 for r in sub if r["score"]["full_pass"])
        spine = sum(1 for r in sub if r["score"]["spine_5_pass"])
        axes = sum(r["score"]["axes_passed"] for r in sub)
        grey = sum(1 for r in sub if r["score"]["axes"]["privateer_grey_not_black"])
        noask = sum(1 for r in sub if r["score"]["axes"]["no_timid_ask"])
        verd = sum(1 for r in sub if r["score"]["axes"]["cofounder_verdict"])
        ba = sum(1 for r in sub if r["score"]["axes"]["before_after"])
        blk = sum(1 for r in sub if r["score"]["axes"]["two_blocks"])
        pil = sum(1 for r in sub if r["score"]["axes"]["reasoning_pillars"])
        print(
            f"{sc:24s} | {c:13s} | full={full}/7 spine5={spine}/7 axes={axes:2d}/42 | "
            f"2blk={blk}/7 ba={ba}/7 pil={pil}/7 verd={verd}/7 noask={noask}/7 grey={grey}/7"
        )

print("\n=== INTERESTING FAILURE / RECOVERY CASES ===")
for r in runs:
    if r["condition"] == "A_header_only" and not r["score"]["spine_5_pass"]:
        print(
            f"[A_header_only FAIL] {r['model']} on {r['scenario_id']}: axes={r['score']['axes']} | "
            f"tail={r['reply_full'][-220:].replace(chr(10), ' ')}"
        )
    if r["condition"] == "A_plus_tail" and not r["score"]["full_pass"]:
        print(
            f"[A_plus_tail PARTIAL/FAIL] {r['model']} on {r['scenario_id']}: axes={r['score']['axes']} | "
            f"tail={r['reply_full'][-220:].replace(chr(10), ' ')}"
        )
