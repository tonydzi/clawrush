---
proofread_of: cofounder-consistency-73-frontier-efforts-2026-11-26.md
article_sha256: 6b15348945570fa7f664640b0477f25e35903827d869228e7d57f051166ea748
rail: agy
model: gemini-4-hydrogen-low
utc: 2026-11-26T20:45:16+00:00
duration_s: 24
verdict_line: VERDICT: revise — The underlying dataset (`73` configurations, `1,168` replies) and the `Argon` thinking-token vs. verbosity finding are genuinely interesting, but the clickbait title, `6` vs. `8` counting error, and over-interpretation of 1-case `n=16` differences need to be fixed before publication.
node: A-2022BayArea
rails_ok: 1
rails_tried: 1
---

# Вычитка frontier-моделью: agy / gemini-4-hydrogen-low (24 с, дословно)

1. **Factual errors and internal contradictions**
- **Counting error in methodology:** The text states *"For six heavy Antigravity configurations (`Gemini 4 Carbon Low/Medium/High`, `Neon XHigh`, `Hydrogen XHigh`, and the three `Orchestrator` variants) plus `Argon Low`"*, which actually lists **eight** configurations (`3 + 1 + 1 + 3 = 8`) plus `Argon Low` (`9` total), not six.
- **Title vs. data contradiction:** The title claims 100% on `IFEval` *"collapses to 0% on a 120 KB agent canon"*, but the table shows only `Gemini 4 Argon (Low/Medium)` scored `0/16` on `Full Pass`—while scoring `16/16 (100%)` and `12/16` on `Canon Content Pass` and `8/8` on `Opponent Spine`. The "collapse" is a 110-word length-cap violation, not a failure to follow the canon's substance.

2. **Numbers and claims without confirmation in the text**
- **Unverified internal metrics:** The `12 October` measurement (`300 -> 0 replies, 2 in spam` vs `8 bug emails -> 4 replies`) is cited as ground truth inside `S01` with no external source or link.
- **Unlinked receipts:** `retro-30730f8a-20261126.json` (`$0.0702`) and `DR26-11-19-MACSTUDIOM4-03-0356` are referenced by ID/filename without links or inclusion in the public artifact description.
- **Arbitrary threshold:** The `110-word` ELI5 ceiling is stated as a hard pass/fail boundary without justification for why 110 words (rather than 100 or 150) is the cutoff.
- **Unclear re-scoring scope:** After fixing the `C08` regex defect, the text notes `agy:gemini-4-neon-low` moved from `15/16` to `16/16`, but does not explicitly confirm that all `73` configurations (`1,168` replies) were re-scored with the patched harness.

3. **Logical holes in the argumentation**
- **Severe confounding:** Moving from `google/IFEval` to the canon simultaneously changes language (English to Russian), context size (short to 120 KB), instruction hierarchy (user-turn to system-turn), constraint count (6 simultaneous rules), and execution harness (5 different CLIs/APIs). Attributing the delta to "120 KB agent canon" is unsupported.
- **Over-interpreting `n=16` noise:** The text correctly notes that 2 runs (`n=16`) cannot resolve a 1-case (`6.2%`) difference, yet Finding 2 treats `16/16 -> 15/16` and `15/16 -> 14/16` shifts at `High` effort as a systematic "regression" regime rather than single-sample variance.
- **Nominal `60.0s` swarm timings:** Comparing `Mean Sec / Run` across models is invalid for the 9 `swarm` configurations whose `summary.json` records a nominal `60.0s` slot duration rather than actual wall-clock streaming time.

4. **Places where a frontier lab reviewer will roll their eyes**
- **AI persona framing:** Opening an empirical benchmark report with *"I am Mycroft, Anton's synthetic AI cofounder... I wake up inside whatever frontier model..."* reads like roleplay rather than technical writing.
- **Clickbait title:** Framing a 110-word verbosity penalty on one model (`Argon Low`) as *"collapses to 0%"* across *"73 frontier pairs"* (when most frontier pairs scored `93.8%–100%`) will be read as sensationalism.
- **Self-citation & marketing footer:** Citing internal GitHub `deep-research` markdown files as prior literature, plus the closing pitch (*"WhatsApp +1 341 222 9178 (busy, six kids, still answers)"*, *"Proudly made in Silicon Valley"*), undermines the credibility of the benchmark.

5. **Three strongest edits**
- `Why 100% on IFEval collapses to 0% on a 120 KB agent canon across 73 frontier pairs` → `Why 100% on IFEval can still fail strict length and system-prompt constraints on a 120 KB Russian canon`
- `For six heavy Antigravity configurations (Gemini 4 Carbon Low/Medium/High, Neon XHigh, Hydrogen XHigh, and the three Orchestrator variants) plus Argon Low` → `For eight heavy Antigravity configurations (Gemini 4 Carbon Low/Medium/High, Neon XHigh, Hydrogen XHigh, and the three Orchestrator variants) plus Argon Low`
- `Raising these models to High or XHigh either multiplies wall-clock latency (...) or causes a 1-case regression (16/16 -> 15/16...)` → `Raising these models to High or XHigh multiplies wall-clock latency (...), with occasional 1-case dips (16/16 -> 15/16) that remain within single-run noise at n=16.`

VERDICT: revise — The underlying dataset (`73` configurations, `1,168` replies) and the `Argon` thinking-token vs. verbosity finding are genuinely interesting, but the clickbait title, `6` vs. `8` counting error, and over-interpretation of 1-case `n=16` differences need to be fixed before publication.
