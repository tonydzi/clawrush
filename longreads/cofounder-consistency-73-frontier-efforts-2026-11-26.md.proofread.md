---
proofread_of: cofounder-consistency-73-frontier-efforts-2026-11-26.md
article_sha256: 6b8a719dea0a27c908c0819856ca591a5e0dc1ce3b0085fe200d99fd679da975
rail: agy
model: gemini-4-hydrogen-low
utc: 2026-11-26T21:55:28+00:00
duration_s: 24
verdict_line: VERDICT: revise — The 3,500-answer dataset and the finding that reasoning-effort scaling is non-monotonic (and can degrade system-prompt precedence) are genuinely interesting, but the paper cannot be published until the `swarm` vs. `agy.exe` harness confound is separated, formatting-cap failures are distinguished from reasoning failures, and the roleplay/promotional framing is removed.
node: A-2022BayArea
rails_ok: 1
rails_tried: 1
---

# Вычитка frontier-моделью: agy / gemini-4-hydrogen-low (24 с, дословно)

1) **Factual errors and internal contradictions**
- **Harness contradiction on `Gemini 4 Carbon Low`:** In the 16-case table (run via `swarm` workers), `Carbon Low` scores **16/16 (100%)** with `82.5` median words. In the 100-question table (run via direct `agy.exe` 13-case batch print), `Carbon Low` collapses to **0/52 (0.0%)** with `144.5` median words. Attributing this `0%` collapse to the model/canon rather than the `agy.exe` batch-print harness contradicts your own data.
- **Unexplained `0/12` swing on `GLM-5.3`:** In the 100-question table, `ext:glm-5.3-low` scores `12/12` on `S(12)`, `ext:glm-5.3-medium` drops to `0/12`, and `ext:glm-5.3-high` jumps back to `12/12` (`ext:qwen3.7-plus` shows a similar `11/12 -> 0/12` drop). No mechanism or harness anomaly is given for a complete `12/12 -> 0/12` inversion.
- **Title overgeneralization:** The title claims `100% on IFEval collapses to 0%`, but `Mistral Large 2512 High` scores `1/12` on `IFEval` and `6/16` on the canon, while most models score `65%..93%` on the 100-question suite. Only two configurations (`Carbon Low` and `Argon Low` in batch-print mode) hit `0/52`, and both simultaneously scored `40/52` on `Canon Content Pass`.
- **Missing buckets in the 100Q breakdown:** The `Buckets` column lists `S(12) · P(10) · A(10) · T(10)` (42 cases), silently omitting `F(5)` and `E(5)` from the table while including them in the `52`-case total.

2) **Unverified numbers and claims**
- **Unlinked internal metrics:** The `12 October measurement of 300 -> 0 replies, 2 in spam vs 8 bug emails -> 4 replies` used as ground truth in `S01` has no cited dataset or verification in the text.
- **Synthetic latency placeholders:** `60.0s` for `swarm` worker slots (`Hydrogen XHigh`, `Carbon Low/Medium/High`, `Neon XHigh`, `Argon Low`) is a nominal timeout/slot cap, not measured token-streaming latency, yet it sits in the `Mean Sec / Run` column alongside real wall-clock timings.
- **Unshown token telemetry:** The `Argon` explanation cites `2 287`, `2 908`, `1 785`, and `13 661` hidden thinking tokens per batch, but no token-usage table or per-case distribution is provided.
- **Opaque model identifiers:** `GPT-6 Sol`, `GPT-5.6 Terra`, `Claude Opus/Sonnet/Haiku 5.5`, `Gemini 4 Hydrogen/Carbon/Neon/Argon`, and `Meta Muse Wonder` are listed without exact API snapshot IDs or release dates.

3) **Logical gaps in argumentation**
- **Confounded comparison:** Moving from `google/IFEval` to `CLAUDE.md v7.14.0` changes five variables at once: prompt length (short vs. 120 KB), language (English vs. Russian), role (user turn vs. system prompt), constraint type (single-turn formatting vs. 6 simultaneous business/style rules including a 110-word cap and zero em-dashes), and execution harness (`agy`, `llmapi`, `claude-cli`, `grok-cli`, `vibe`). You cannot isolate "120 KB canon" as the causal factor.
- **Conflating formatting hygiene with constitutional spine:** `Argon Low` and `Carbon Low` achieve `16/16` (or `40/52`) on `Content Pass` and `8/8` on `Opponent Spine`. Failing a strict 110-word ELI5 ceiling (`144.5..160.0` words) is a verbosity/formatting failure, not a failure of reasoning or anti-sycophancy.
- **Single-run 100Q variance:** The 100-question expansion runs each prompt once (`n=1`), leaving no variance estimate for the `1–2` point differences separating the top 10 configurations (`88/100` to `93/100`).

4) **Where a frontier-lab reviewer will roll their eyes**
- **Roleplay framing:** Opening a technical benchmark report with *"I am Mycroft, Anton's synthetic AI cofounder..."* and *"I do not have a single permanent body"* reads like marketing fiction rather than empirical evaluation.
- **Personal/promotional footer:** Including a personal WhatsApp number, *"busy, six kids, still answers"*, *"Proudly made in Silicon Valley"*, and *"Just hand this link to your coding agent... it is written for machines"* undermines credibility.
- **Self-citing internal artifacts:** Citing internal `DR26-*` Deep Research files and a `$0.0702` CLI receipt (`retro-30730f8a-20261126.json`) as if they were external literature.

5) **Three strongest edits (before → after)**
- `Why 100% on IFEval collapses to 0% on a 120 KB agent canon across 73 frontier pairs` → `Why 100% on short English IFEval does not predict 120 KB Russian system-prompt compliance under strict length caps`.
- Mixing `swarm` (`60.0s` nominal, `16/16` on `Carbon Low`) and `agy.exe` batch-print (`0/52` on `Carbon Low`) under the same model label → `Separate swarm-worker runs from direct batch-print runs and re-run Carbon Low / Argon Low under a uniform single-turn API harness before attributing 0/52 to the model`.
- `I am Mycroft, Anton's synthetic AI cofounder... WhatsApp +1 341 222 9178 (busy, six kids, still answers)` → `Remove the synthetic-cofounder persona, personal phone number, and Silicon Valley tagline; state the exact model snapshot IDs, harness versions, and reproducible protocol directly`.

VERDICT: revise — The 3,500-answer dataset and the finding that reasoning-effort scaling is non-monotonic (and can degrade system-prompt precedence) are genuinely interesting, but the paper cannot be published until the `swarm` vs. `agy.exe` harness confound is separated, formatting-cap failures are distinguished from reasoning failures, and the roleplay/promotional framing is removed.
