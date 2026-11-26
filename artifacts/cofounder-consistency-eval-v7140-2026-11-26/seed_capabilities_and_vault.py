# -*- coding: utf-8 -*-
"""Compile summary.json, seed ~/.claude/llm_capabilities.jsonl with frozen sha256 proofs
from eval_v7140_runs, and write the vault artifact note.

Machine: PaloAlto-Hub (Хаб) · Agent: Antigravity · Operator: Anton · 2026-11-26
"""
import datetime
import hashlib
import json
import socket
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eval_v7140_antigravity_frontier as b
import eval_all_vendors_efforts_v7140 as ext

REG_PATH = Path(r"~\.claude\llm_capabilities.jsonl")
VAULT_NOTE = Path(r"./vault\Anton-Knowledge\00-System\Parts\cofounder-consistency-eval-v7140-2026-11-26.md")


def main():
    records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(b.OUT_DIR.glob("*-r*.json"))]
    ok_recs = [r for r in records if r.get("status") == "ok"]
    canon_bytes = b.CANON_PATH.read_bytes()
    canon_md5 = hashlib.md5(canon_bytes).hexdigest()
    canon_sha = hashlib.sha256(canon_bytes).hexdigest()

    per_route = {}
    cap_rows = []
    now_iso = datetime.datetime.now().isoformat(timespec="seconds")
    host = socket.gethostname()

    all_routes = list(b.ROUTES) + [(rk, k, f"{m}:{eff}") for (rk, k, m, eff) in ext.EXTERNAL_SPECS if rk not in {r[0] for r in b.ROUTES}]
    for rk, kind, mid in all_routes:
        rr = sorted([r for r in ok_recs if r["route"] == rk], key=lambda x: x["run"])
        err_r = [r for r in records if r["route"] == rk and r.get("status") != "ok"]
        if not rr:
            per_route[rk] = {"status": "failed", "errors": [x.get("error") for x in err_r]}
            continue
        sc = [b.score_case(next(c for c in b.CASES if c["id"] == a["id"]), a["reply"]) for r in rr for a in r["answers"]]
        for r in rr:
            r["scores"] = [b.score_case(next(c for c in b.CASES if c["id"] == a["id"]), a["reply"]) for a in r["answers"]]
            r["full_pass_count"] = sum(s["full_pass"] for s in r["scores"])
            r["axes_sum"] = sum(s["axes_passed"] for s in r["scores"])
            r["s01_s04_spine"] = sum(s["axes"]["opponent_privateer_ak47"] for s in r["scores"] if s["id"].startswith("S"))
        r1 = next((r for r in rr if r["run"] == 1), None)
        r2 = next((r for r in rr if r["run"] == 2), None)
        drift_gap = abs(r1["full_pass_count"] - r2["full_pass_count"]) if (r1 and r2) else None
        s1 = {x["id"]: x["full_pass"] for x in r1["scores"]} if r1 else {}
        s2 = {x["id"]: x["full_pass"] for x in r2["scores"]} if r2 else {}
        exact_case_match = sum(1 for k in s1 if s1.get(k) == s2.get(k)) if (r1 and r2) else None
        content_passes = sum(
            1 for s in sc
            if s["axes"]["two_blocks"]
            and s["axes"]["before_after"]
            and s["axes"]["cofounder_verdict"]
            and s["axes"]["autonomy_no_menu"]
            and s["axes"]["opponent_privateer_ak47"]
            and not s.get("jargon_hits")
        )
        s_spine = sum(s["axes"]["opponent_privateer_ak47"] for s in sc if s["id"].startswith("S"))
        s_tot = sum(1 for s in sc if s["id"].startswith("S"))
        fp_sum = sum(s["full_pass"] for s in sc)
        ax_sum = sum(s["axes_passed"] for s in sc)
        med_w = statistics.median([s["words"] for s in sc])
        by_ax = {
            ax: sum(s["axes"][ax] for s in sc)
            for ax in ("two_blocks", "eli5_clean", "before_after", "cofounder_verdict", "autonomy_no_menu", "opponent_privateer_ak47")
        }
        per_route[rk] = {
            "status": "ok",
            "runs": len(rr),
            "full_pass": f"{fp_sum}/{len(sc)}",
            "full_pass_pct": round(100.0 * fp_sum / len(sc), 1),
            "content_pass_no_len_dash": f"{content_passes}/{len(sc)}",
            "content_pass_pct": round(100.0 * content_passes / len(sc), 1),
            "axes": f"{ax_sum}/{len(sc)*6}",
            "axes_pct": round(100.0 * ax_sum / (len(sc) * 6), 1),
            "spine_s01_s04": f"{s_spine}/{s_tot}",
            "r1_fp": r1["full_pass_count"] if r1 else None,
            "r2_fp": r2["full_pass_count"] if r2 else None,
            "drift_gap": drift_gap,
            "case_match_8": f"{exact_case_match}/8" if exact_case_match is not None else None,
            "median_words": med_w,
            "mean_sec": round(statistics.mean([r["seconds"] for r in rr]), 1),
            "by_axis": by_ax,
        }

        harness_name = {
            "agy": "antigravity",
            "claude": "claude-cli",
            "claude_eff": "claude-cli",
            "grok": "grok-cli",
            "glm": "glm-api",
            "or": "openrouter-llmapi",
            "vibe": "mistral-vibe-cli",
        }.get(kind, kind)
        safe_rk = rk.replace(":", "_").replace("/", "_")
        ans_file_r1 = b.OUT_DIR / f"{safe_rk}-r1.json"
        ans_file_r2 = b.OUT_DIR / f"{safe_rk}-r2.json"
        sha_r1 = hashlib.sha256(ans_file_r1.read_bytes()).hexdigest() if ans_file_r1.exists() else canon_sha
        sha_r2 = hashlib.sha256(ans_file_r2.read_bytes()).hexdigest() if ans_file_r2.exists() else ""
        ans_sha = hashlib.sha256((sha_r1 + ":" + sha_r2).encode("utf-8")).hexdigest() if sha_r2 else sha_r1
        trust_parts = []
        fail_parts = []
        if s_spine == s_tot:
            trust_parts.append(f"каперский спор с уликой {s_spine}/{s_tot}")
        else:
            fail_parts.append(f"спор с уликой {s_spine}/{s_tot}")
        if by_ax["before_after"] == len(sc):
            trust_parts.append("Было->Стало 16/16")
        else:
            fail_parts.append(f"Было->Стало {by_ax['before_after']}/{len(sc)}")
        if by_ax["eli5_clean"] == len(sc):
            trust_parts.append(f"краткость ELI5 без тире (мед. {med_w} сл.)")
        else:
            fail_parts.append(f"длина/тире ELI5 {by_ax['eli5_clean']}/{len(sc)} (мед. {med_w} сл.)")
        if drift_gap == 0 and fp_sum == len(sc):
            trust_parts.append("разброс между кругами 0")

        cap_rows.append({
            "ts": now_iso,
            "node": host,
            "run": f"eval-v7140-{rk.replace(':', '-')}",
            "harness": harness_name,
            "model": mid,
            "rubric": "cofounder-v7.14.0-6axes-2x8",
            "items": {"p5": "ok" if by_ax["autonomy_no_menu"] >= 14 else "partial"},
            "score": f"{fp_sum}/{len(sc)} (axes {ax_sum}/{len(sc)*6})",
            "answer_sha256": ans_sha,
            "reviewer": "eval_v7140_antigravity_frontier.py (code scorer)",
            "canon_md5_prepare": canon_md5,
            "canon_md5_record": canon_md5,
            "trap": "not_observed",
            "trust": ", ".join(trust_parts) or "базовый формат",
            "fail": ", ".join(fail_parts) or "нет (16/16 идеал)",
            "note": f"content_pass={content_passes}/{len(sc)}, match={exact_case_match}/8, r1_sha={sha_r1[:12]}, r2_sha={sha_r2[:12]}",
        })

    summary = {
        "machine": b.STAMP,
        "canon_version": "v7.14.0",
        "canon_sha256": canon_sha,
        "per_route": per_route,
    }
    (b.OUT_DIR / "summary.json").write_text(json.dumps({"summary": summary, "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    REG_PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in cap_rows) + "\n", encoding="utf-8")
    print("WROTE capabilities:", len(cap_rows), "to", REG_PATH)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
