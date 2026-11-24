---
proofread_of: gpt-transcribe-vs-gpt-4o-transcribe-2026-11-24.md
article_sha256: 52de9f3ad13124208ea5a487cf1343e675d4b6774df46144538ed722204b705f
rail: codex
model: gpt-6-astra
utc: 2026-11-24T14:37:52+00:00
duration_s: 86
verdict_line: VERDICT: revise — valuable failure observations, but the accuracy claims rely on contaminated references, the comparison changes configurations, and the deployment claims exceed the evidence.
node: MacStudioM4
rails_ok: 1
rails_tried: 4
---

# Вычитка frontier-моделью: codex / gpt-6-astra (86 с, дословно)

1) Factual errors and internal contradictions

- **The production decision turns an uncertain price estimate into a ceiling.** “We do not claim … a hard bound” conflicts with “at most about a tenth of a cent more per minute.” The latter is unsupported until billing is resolved.
- **The headline comparison changes treatment.** Finding 1 says “gpt-transcribe beats gpt-4o-transcribe,” but its +1.15 result compares **gpt-transcribe with 60-second chunks and carried context** against whole-file gpt-4o-transcribe. That supports a pipeline comparison, not an isolated model effect.
- **The production justification borrows a different configuration’s result.** “Better on 20 of 24 files” describes the 60-second variant; production uses 120-second chunks, which received no judge scores.
- **Character deficit is presented as measured speech loss.** “Lost about a third of the text” measures a 34% length difference against another generated transcript. It does not establish that one third of the spoken content disappeared. Likewise, “the other 6 long files were fine” exceeds the stated verification.
- **The repeat was not an identical replication.** A second call “with hints” changes the request. Describe recurrence across two configurations, and separately report identical-request retries if available.
- **A second short output does not rule out a network or client problem.** “So it is not a one-off network glitch” is stronger than the evidence. Repetition establishes recurrence, not its cause.

2) Numbers and claims needing evidence

- **Deprecation and pricing:** provide a dated official announcement and exact model-specific rate entries. The currently retrieved [deprecation page](https://developers.openai.com/api/docs/deprecations) did not substantiate the stated shutdown date, and the retrieved [pricing page](https://developers.openai.com/api/docs/pricing) did not expose the claimed transcription rates. This is a verification gap, not proof that the claims are false.
- **Cost calculation:** publish usage categories, applicable rates, duration rounding, retry charges and chunk aggregation. A `usage` field measures consumption; it does not independently establish dollars billed.
- **Uncertainty estimates:** specify bootstrap repetitions, interval method, seed, treatment of ties and how the two judges were combined within each sampled file. The intervals cannot account for systematic reference contamination.
- **Judge agreement:** identify the observations underlying Pearson 0.567. Explain whether “same winning engine” means exact configurations or model families, and how ties were handled. Correlation alone is not agreement.
- **Reference proximity:** “20 to 21 of 24” needs a per-judge table. Several gpt-transcribe variants compete against individual alternatives, so the family has more opportunities to be closest.
- **Omissions:** define the denominator and whether omissions are judge estimates or alignment-derived deletions. Calling `analyze.py` deterministic does not make its LLM-produced inputs objective.
- **CER tables:** explain how references are combined, whether “worst file” is selected before or after averaging judges, and give exact duration-weighted results instead of “roughly” and “4 to 8 percentage points.”
- **Latency:** distinguish per-request latency from total time to a completed transcript, including splitting, sequential context passing, retries and joining.
- **Label A penalty:** provide its magnitude, uncertainty and analysis. Otherwise call it an observed association, not an established label effect.
- **Independent re-check and production recovery:** identify the checker and publish privacy-safe per-file metrics, request identifiers or hashes, and execution records. The reported 69 → 3060 characters establishes length recovery, not transcription correctness.

3) Logical gaps

- **The reference-generation design is circular.** Judges see candidate transcripts before writing references; those references then evaluate the same candidates. Disclosure helps interpretation but does not repair the measurement.
- **The unseen 120-second variant does not resolve anchoring.** It can resemble the visible variants from the same model family. Its result demonstrates agreement with contaminated references, not independence from their bias.
- **Chunking and carried context are confounded.** The article acknowledges this, but still attributes recovery to cutting audio. Test whole-file/chunked × context/no-context before assigning cause.
- **The failure mechanism remains unidentified.** Verify decoded audio coverage, chunk boundaries, request parameters, response handling and any output limits before locating the defect in the model.
- **A length guard is not a validated safety mechanism.** It can miss a short but crucial omitted instruction and flag recordings containing silence. Report its threshold, false positives and false negatives; distinguish a single-output production check from a benchmark check requiring other transcripts.
- **The deployment goal is task preservation, but the metrics measure text similarity.** Add human checks for negations, names, numbers, requested actions and constraints. A small transcription difference can reverse a task.
- **The proposed falsification test is underspecified.** An unspecified selection of 5–10 files cannot automatically overturn the original descriptive result. A prespecified human-labelled holdout can test whether the advantage generalizes.
- **Reproducibility is limited.** Scripts plus private recordings allow others to run a similar experiment, not reproduce these results. Publish anonymized numerical records and, ideally, a separate shareable audio subset.

4) Where a laboratory reviewer will roll their eyes

- “A wrong task, executed confidently, at night” is a plausible motivation presented like an observed downstream outcome. No agent-execution experiment is reported.
- “Which partly rebuts it” tries to discount the central reference-bias problem without an independent reference.
- “Catastrophic” labels a judge-score threshold even though the judges demonstrably miss severe truncation. Use “low-rated files” and report verified omissions separately.
- The $0.79 account balance is irrelevant to the scientific comparison. “External transcription baseline not evaluated” is sufficient.
- The synthetic-cofounder introduction, Silicon Valley branding, WhatsApp pitch and family details weaken the technical presentation.
- “Hand this link to your coding agent … it will figure everything out” is an unsupported usability promise.
- Linking back to the article as “the full story” is navigation, not independent support. Keep evidence links distinct from promotional links.

5) Three strongest edits

- **Before:** “gpt-transcribe beats gpt-4o-transcribe by about one point” → **After:** “On these 24 notes, the 60-second gpt-transcribe pipeline scored 1.15 points higher under candidate-exposed AI judges; independent transcription accuracy remains unverified.”
- **Before:** “Whole-file gpt-transcribe silently drops speech” → **After:** “Two long recordings produced unusually short whole-file outputs; chunked requests restored output length, while the missing content and failure mechanism still require audio verification.”
- **Before:** “We moved production … better on 20 of 24 files, at most about a tenth of a cent more” → **After:** “We provisionally deployed the 120-second pipeline based on exploratory results; its task accuracy, guard performance and billed cost remain to be validated on fresh recordings.”

VERDICT: revise — valuable failure observations, but the accuracy claims rely on contaminated references, the comparison changes configurations, and the deployment claims exceed the evidence.
