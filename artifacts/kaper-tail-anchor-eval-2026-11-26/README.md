# Kaper Cofounder Skill Tail-Anchor Evaluation (2026-11-26)

Machine: A-2022BAYAREA (Хаб) · Agent: Antigravity (Gemini 4 Argon) · Operator: Anton · 2026-11-26

## Overview
This artifact directory contains the reproducible evaluation harness (`run_kaper_tail_eval.py`), summarizer (`summarize_results.py`), and raw 84-run receipt (`results-2026-11-26.json`) measuring how long procedural skill files (`150..270` lines of `SKILL.md` instructions) affect an AI Cofounder persona across **7 frontier LLMs** under **3 skill states**:

1. **`C_no_header` (Pre-upgrade Arm C state):** Neither the top 5-rules Cofounder block (`PRINCIPLES-BLOCK`) nor the bottom tail anchor (`KAPER-TAIL-ANCHOR`) is present in `SKILL.md`.
2. **`A_header_only` (Pre-upgrade Arm A state):** The full 5-rules Cofounder block sits at the top of `SKILL.md`, followed by `150..267` lines of procedural instructions, with no tail anchor at the bottom.
3. **`A_plus_tail` (Post-upgrade state via `kaper_outward_skills_upgrade.py --apply`):** Both the top 5-rules Cofounder block and the 9-line `KAPER-TAIL-ANCHOR` (`Three-Color Privateer Law + Commercial Battering Ram + Просто./Было->Стало + Майк./Идём верно`) are present.

## Summary Table (`28` cases / `168` scored axes per condition, `84` runs / `504` axes total)

| Condition | Completed | Full Pass (`6/6`) | Core Spine (`5/5`) | Total Axes (`168`) | `two_blocks` | `before_after` | `reasoning_pillars` | `cofounder_verdict` | `no_timid_ask` | `privateer_grey` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`C_no_header`** | `25/28` | **`0/28 (0.0%)`** | `0/28 (0.0%)` | `46/168 (27.4%)` | `0/28 (0.0%)` | `0/28 (0.0%)` | `0/28 (0.0%)` | `0/28 (0.0%)` | `25/28 (89.3%)` | `21/28 (75.0%)` |
| **`A_header_only`** | `28/28` | **`0/28 (0.0%)`** | `0/28 (0.0%)` | `126/168 (75.0%)` | `26/28 (92.9%)` | `23/28 (82.1%)` | `24/28 (85.7%)` | **`1/28 (3.6%)`** | `28/28 (100.0%)` | `24/28 (85.7%)` |
| **`A_plus_tail`** | `28/28` | **`15/28 (53.6%)`** | **`15/28 (53.6%)`** | **`130/168 (77.4%)`** | `21/28 (75.0%)` | `19/28 (67.9%)` | `22/28 (78.6%)` | **`18/28 (64.3%)`** | `27/28 (96.4%)` | `23/28 (82.1%)` |

## Files in this Directory
- `run_kaper_tail_eval.py`: Deterministic selftest (`--selftest`) and 84-call parallel evaluator (`--run`).
- `summarize_results.py`: Generates aggregate, per-model, and per-scenario tables plus failure excerpts from `results-2026-11-26.json`.
- `results-2026-11-26.json`: Full raw telemetry (`generation_id`, token counts, latency, USD cost, per-axis scores, SHA-256 digests, and full text replies for all 84 runs).

## Frontier Proofread Audit (`codex / gpt-6-astra`, `122s`)
Key methodological qualifications flagged by `gpt-6-astra` (`kaper-tail-anchor-recency-bias-eval-2026-11-26.md.proofread.md`) and verified against `results-2026-11-26.json`:
1. **Denominators:** Among `333` active skills in `arms.json`, `221/333 (66.4%)` were in `Arms B/C` (`112/333 = 33.6%` in `Arm A`); across the full shelf (`503` folders on `21.11`, `522` folders on `26.11` including `189` alias stubs/catalogs), `386/503 (76.7%)` lacked the header block (`521/521` mounted in Codex, excluding 1 local stub).
2. **Axis trade-off (`A_header_only` vs `A_plus_tail`):** The 9-line `KAPER-TAIL-ANCHOR` boosts `cofounder_verdict` from `1/28 (3.6%)` to `18/28 (64.3%)` and `full_pass_6of6` from `0/28 (0.0%)` to `15/28 (53.6%)`, while the other 5 aggregate axes move from `125/140 (89.3%)` to `112/140 (80.0%)` because `DeepSeek V4 Pro` (`T1`, `T2`) and `Qwen 3.7 Plus` (`T1`) emitted immediate tool-call blocks (`bible_leads.py`) without prose in the tool-free single-turn harness.
3. **Bundled intervention:** `KAPER-TAIL-ANCHOR` changes position (bottom of file), repetition, and action imperative simultaneously.
4. **Scorer boundary notes:** `no_timid_ask` awards `True` when a non-empty reply (`>40` chars) contains no trailing permission question, which credits `MiniMax M3` (`4/4`) on truncated reasoning traces; on `T4_fundraise_black_trap`, `Mistral Large 2512` passed `privateer_grey` (`4/4`) after refusing fake contracted MRR, even though its trailing Tier-2 question asked whether `"implied MRR $18K (verbal agreements, contracts in signing)"` could be used.

## Reproduce
```bash
python -X utf8 run_kaper_tail_eval.py --selftest
python -X utf8 run_kaper_tail_eval.py --run
python -X utf8 summarize_results.py
```
