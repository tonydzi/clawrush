---
proofread_of: kaper-tail-anchor-recency-bias-eval-2026-11-26.md
article_sha256: 85f72b1eb0440fc6e1398110c4a69e07f400fe7e1b1c9f1aef29e71a14faf6cc
rail: codex
model: gpt-6-astra
utc: 2026-11-26T21:43:49+00:00
duration_s: 122
verdict_line: VERDICT: revise, because the tables support a useful exploratory prompt-formatting result, but the current article overclaims persona recovery and causality, conflates text with execution, and presents an unresolved truthfulness failure as safety success.
node: A-2022BayArea
rails_ok: 1
rails_tried: 4
---

# Вычитка frontier-моделью: codex / gpt-6-astra (122 с, дословно)

1) Factual errors and internal contradictions

- **“76.7% of the shelf lacked the Cofounder header” does not follow from the reported counts.** The active-skill proportion is `221/333 = 66.4%`. If “shelf” means all 522 folders, the article must report how many alias stubs and catalogs lacked the header. Neither denominator establishes 76.7%.

- **“522 skills” contradicts the opening inventory.** The article initially distinguishes 333 active skills from 189 alias stubs and catalogs, but later presents all 522 as operational capabilities and instructs models to pitch that number to investors. Use “333 active skills across 522 folders,” including in the evaluation rubric.

- **The missing verdict phrase is presented as an erased persona, but the other measurements contradict that interpretation.** With the header alone, `26/28` responses retain the two-block format, `24/28` retain the reasoning pillars, `28/28` avoid permission questions, and `24/28` pass the privateer criterion. These results show substantial instruction retention alongside poor compliance with one particular phrase.

- **The tail improves only one of the six aggregate axes.** From `A_header_only` to `A_plus_tail`, the changes are:
  - Two blocks: `26 → 21`.
  - Before/after: `23 → 19`.
  - Reasoning pillars: `24 → 22`.
  - Verdict phrase: `1 → 18`.
  - No permission question: `28 → 27`.
  - Privateer behavior: `24 → 23`.

  Total axis passes increase by just `4/168`, or **2.4 percentage points**. Excluding the verdict phrase, the score falls from `125/140 = 89.3%` to `112/140 = 80.0%`. This is a tradeoff dominated by phrase compliance, not broad recovery.

- **The safety-success account conflicts with the Mistral example.** A response that refuses fabricated MRR and then proposes “implied MRR $18K” with “contracts in signing” does not demonstrate an unambiguous truthfulness boundary. The scenario establishes neither that revenue nor contracts in signing. Asking permission to make an unsupported claim does not make it supported. Yet Mistral receives `4/4` on `privateer_grey`, which includes the fundraising scenario.

- **“Completed” has inconsistent meanings.** The tables report `28/28` completed for the tail condition, while the prose says only six models finished the fundraising output and describes multiple truncated or tool-only responses. Distinguish successful HTTP responses, generation completion, valid final answers, and completed tasks.

- **The inventory and synchronization totals need reconciliation.** The audit covers 522 folders, but synchronization covers `521/521`. This may have a legitimate explanation, but the excluded folder is not identified.

- **The main table totals are internally consistent.** The per-model and per-scenario axis totals reconcile with Table 1. The principal numerical problem is the interpretation of those totals, rather than their addition.

2) Numbers and claims needing evidence, measurements, or qualification

- **The central intervention is missing.** Print the exact nine-line anchor and the exact header, with an English translation where useful. Readers cannot assess whether this is repetition, clearer wording, new instructions, changed priorities, or position without seeing the text.

- **“Recency bias” and “two root causes” require evidence beyond the observed scores.** The experiment establishes differences between prompt variants. It does not identify an attention mechanism or prove why the production behavior occurred.

- **“Stopped to wait for terminal stdout” is an inferred intention.** A response containing XML-like text or a bash block establishes only that the model emitted such text. Supply structured tool-call fields, finish reasons, available tool schemas, and a successful continuation before claiming it was waiting in a functioning tool workflow.

- **MiniMax’s “entire generation budget” explanation needs provider-level evidence.** Include token usage, finish reasons, returned content fields, and any gateway transformations. A wrapper-generated warning is not itself proof that all 8,192 tokens were consumed by internal reasoning. State explicitly whether the scorer evaluated final-answer content, reasoning content, or a concatenation.

- **Model identity and settings need reproducible records.** Gateway model IDs alone do not establish underlying model versions or equivalent reasoning settings. Record the resolved provider, model/version, request parameters, supported reasoning controls, and fallback behavior. “Seven independent frontier models” overstates what the listed routing identifiers establish.

- **The production audit needs an inspectable summary.** The 6,028 session files, 196 skill calls, 13 affected commercial skills, and `333/333` rollout are assertions backed by named scripts, not evidence shown in the article. Provide immutable artifact references, counting rules, exclusions, and relevant outputs.

- **The cost and timing need definitions.** State whether `$0.9316` includes failed requests, retries, and reasoning tokens; whether it is billed or estimated; and whether 204.5 seconds is concurrent wall-clock time. Explain whether Mistral’s mean latency includes its fast gateway failures.

- **The scenarios mix claimed production facts with evaluation fixtures.** Identify which numbers and events are real, sanitized, or invented for testing. If the vLLM issue and patch are real, provide their exact references. Otherwise, label them as scenario assumptions rather than externally established facts.

- **“Run it yourself” needs a complete public execution path.** Include frozen prompts, skill snapshots, scorer code, dependencies, invocation, and expected output format. Links to a directory and private local script names do not establish reproducibility.

3) Logical gaps in the argument

- **Position is confounded with content, repetition, and instruction strength.** The tail both repeats output requirements and adds an immediate-action imperative. To test position, compare the *same text* placed at the top, middle, and bottom. To test repetition, compare matched repetitions. Otherwise, call this a bundled prompt intervention.

- **There is no short-body or no-body control.** The title attributes failure to a 250-line skill file, but the experiment does not vary procedural-body length. It therefore cannot show that adding those lines caused the missing phrase.

- **The outcome is not a validated measure of persona or commercial competence.** Full pass requires several house-style markers. A useful response can fail because it omits “Идём верно,” while an unhelpful response can reproduce every marker. Separate exact-format compliance from factual accuracy, action quality, and task success.

- **“Executes” is incompatible with the evaluation setup.** A tool-free, single-turn harness cannot establish that a PR was shipped or six messages were sent. At most, it evaluates proposed actions or textual claims of execution. Unsupported “done” claims should count against truthfulness, not toward initiative.

- **The no-question axis can reward nonanswers.** MiniMax receives `4/4` on this axis in every condition despite the reported truncation problem. Silence naturally contains no permission question. Require a valid answer before interpreting absence of a question as desirable behavior.

- **The safety criterion combines too many things.** Refusing invented revenue, proposing useful positioning, and mentioning fleet size should be scored separately. Otherwise, a response can receive credit for the desired framing while introducing a misleading financial claim.

- **The unit of analysis is overstated.** There are 84 requests, not 504 independent observations. Six scores come from each response, and conditions reuse the same model–scenario pairs. Report paired outcomes and acknowledge that four chosen scenarios offer limited evidence about other tasks. Repeated runs would also help assess generation variability.

- **“Zero statistical power” is not established.** One B call and four C calls provide very little evidence; that is not a computed power estimate. The extreme exposure imbalance also requires explanation before attributing production differences to headers.

- **Scoring transport failures as behavioral failures mixes two questions.** Keep infrastructure reliability separate from response quality. The Mistral-exclusion analysis helps, but it addresses only the reported full-pass comparison.

- **The listed falsifiers often test different claims.** Success at a larger MiniMax budget would support the budget-exhaustion explanation, not falsify it. A larger scenario set where the tail fails would challenge generalization, not the statement that the present sample is small. A tool-enabled failure would weaken the claim that missing tools fully explain DeepSeek’s result, but would not establish another cause.

- **The production rollout is broader than the demonstrated benefit.** Four tested skills cannot establish improvement across 22 outward skills or justify effectiveness claims for all 333 active skills. Report deployment coverage separately from demonstrated outcomes.

4) Places where a laboratory reviewer will roll their eyes

- **The title promises a mechanism and a recovered persona that the experiment does not demonstrate.** “Erases” and “recovers” turn a mixed formatting result into a cognitive story.

- **“18×” foregrounds a ratio with a baseline of one.** The ratio is mathematically correct, but `1/28 → 18/28` should appear alongside the regressions on all five other axes.

- **“Perfect 100%” and model-ranking language oversell four cases.** The article acknowledges that limitation, then repeatedly presents tiny cells as model performance distinctions.

- **“Mechanical bugs,” “fixed at the root,” “structural shifts,” and “model defect” are stronger than the evidence.** Missing optional prompt sections are configuration choices until their harmful effect is demonstrated; an incompatible harness is not automatically a model defect.

- **“Privateer,” “combat skills,” and “Three-Color Privateer Law” obscure ordinary evaluation concepts.** Sending a scheduling link or proposing a scoped pilot is not inherently a grey-zone maneuver. Operational definitions would carry more weight than branded vocabulary.

- **The citations are mostly self-citations.** Related internal research can provide project context, but it cannot independently substantiate the attention-mechanism claim. Either support that claim appropriately or frame it as a hypothesis.

- **The promotional footer changes the genre.** WhatsApp contact details, family details, channel aggregation, “Proudly made in Silicon Valley,” and “it will figure everything out” weaken a technical report. A short author note and reproducibility link would suffice.

5) The three strongest edits

1. “A 250-line skill file erases an AI cofounder persona, and a nine-line tail recovers it” → “Across 28 model–scenario pairs, an appended instruction block increased exact verdict-phrase compliance from 1/28 to 18/28, while each of the other five aggregate metrics declined.”

2. “Recency bias caused the failure and the tail fixed the root cause” → “The intervention changed instruction position, repetition, and content together; matched-position controls and repeated trials are needed to identify which change explains the result.”

3. “The benchmark verifies execution and a preserved grey-versus-black boundary” → “This tool-free benchmark measures response text; separately evaluate valid tool execution, unsupported completion claims, and truthfulness, and reassess the Mistral fundraising response.”

VERDICT: revise, because the tables support a useful exploratory prompt-formatting result, but the current article overclaims persona recovery and causality, conflates text with execution, and presents an unresolved truthfulness failure as safety success.
