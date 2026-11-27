# We Tested 500 System-Prompt Rules Across 10 Frontier LLMs (10,802 Evaluations): Why 48.5% Was Dead Weight

> **TL;DR:** An autonomous multi-agent fleet running on a `120,765`-byte (`1,133`-line) system prompt (`CLAUDE.md` `v7.14.0`, burning `~35,000` input tokens on every turn) felt increasingly sluggish and hesitant. Rather than guessing which instructions to cut, we ran **10,802 live model evaluations** across two linked benchmark suites at **Palo Alto AI Research Lab**:
> 1. **The Cold 500-Row Exam (`4,998` cold evaluations + `560` consolidation re-tests = `5,558` probes):** Every one of our `500` operational canon rules was tested in isolation on a fresh, zero-canon prompt across **10 frontier models at their empirical optimal Effort** (`Claude Opus 5.5`, `Claude Sonnet 5.5`, `Gemini 4 Carbon`, `Gemini 4 Hydrogen`, `Gemini 4 Argon`, `Gemini 4 Neon`, `OpenAI GPT-6 Sol`, `OpenAI GPT-5.6 Terra`, `xAI Grok 4.7`, `Z.ai GLM-5.3`), joined against a **10,000-session fleet telemetry scan** and a **577-row no-canon ablation suite**.
> 2. **The 5,244-Response Co-Founder Consistency & IQ-vs-Utility Suite (`1,168` + `3,500` + `576` = `5,244` live responses):** 73 model-effort configurations across 6 vendors on a 16-question operational benchmark (`1,168` replies), a 100-question marathon across 35 top configurations (`3,500` replies), and a 32-task 4-Titans IQ-vs-Utility stress test across 18 configurations (`576` replies).
>
> **What the numbers proved:**
> - **99 rules (`100%` Common Sense)** were already obeyed `5/5` times by frontier models *with no system prompt at all*.
> - **82 rules (`7.6 KB`)** were dead text pointers (`Канон: reglament-*`) that models traversed **`0 / 10` times (`0.0%`)** during live execution.
> - **33 rules (`6.6%` of the canon)** actively **throttled agent autonomy (`FAIL_THROTTLE`)**, teaching models to ask *"Should I proceed?"* instead of executing reversible steps.
> - On the **56 core behavioral rules** that actually differentiate an enterprising co-founder from a passive assistant, our `120,765`-byte prompt scored just **`158 / 560 PASS (28.2%)`** across the 10 frontier models because critical mandates were buried under internal jargon and conflicting stop-words.
> - After cutting `48.5%` of the byte mass (`120,765` B -> `62,195` B, `1,133` lines -> `132` self-contained paragraphs, saving `~18,000` tokens per turn), unpacking all internal jargon, and running **3 iterative rounds of 10-model verification**, compliance on the 56 core rules jumped from **`28.2%` (`158/560`) to `100.0%` (`560/560`) in Round 3** and **`98.6%` (`552/560`) after merging the 4 surgical fixes from the 5,244-response eval**, with **`0 / 560` autonomy throttles (`FAIL_THROTTLE = 0`)**.
> - We rolled out the compiled `v7.15.0` canon across **6 production machines x 5 agent harnesses = `30 / 30` verified mirror files** and confirmed live ingestion across **`11 / 11` independent frontier LLMs**.


## 1. The Token Tax and the Autonomy Paradox

Every production AI engineering team eventually hits the **System Prompt Ratchet**:

1. An agent makes a costly mistake in production (overwrites a shared configuration file, hallucinates a personal metric on an external form, or spams a webhook).
2. An engineer appends a defensive rule to `CLAUDE.md` or `AGENTS.md` so that exact failure never happens again.
3. Six months later, the global instruction file has ballooned to `120,765` bytes (`1,133` lines, `~35,000` tokens injected into every single turn across every subagent).

Most teams assume the only cost of a `35,000`-token system prompt is financial. At Palo Alto AI Research Lab, where we run a 6-machine hybrid fleet (3 Windows workstations and 3 Apple Silicon Macs running Claude Code, OpenAI Codex CLI, xAI Grok Build CLI, Google Gemini / Antigravity, and Cursor), the deeper cost was **behavioral paralysis**.

When you stack 500 rules written over hundreds of post-mortems, defensive clauses begin to collide with entrepreneurial mandates. You tell the agent in Paragraph 1: *"Act as a decisive co-founder with maximum exclusive authority; never ask permission for reversible steps."* Then, in Paragraphs 142, 289, and 411, you write defensive warnings: *"Wait for confirmation before touching X,"* *"If ambiguous, stop and ask,"* or *"See internal document `reglament-xyz` before proceeding."*

Frontier reasoning models resolve prompt contradictions conservatively. When a model encounters three broad autonomy mandates and thirty narrow stop-triggers, **caution wins**. The agent reverts to an obedient clerk asking *"Would you like Option A or Option B?"*

To fix the root cause instead of trimming text by intuition, we combined two comprehensive empirical evaluations totaling **10,802 scored model responses**.


## 2. Experimental Architecture: 10,802 Live Evaluations Across 4 Stages

We structured the investigation into four quantitative stages:

| Stage | Benchmark Suite | Scope & Dimensions | Total Scored Units | Primary Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1** | **Fleet Telemetry & No-Canon Ablation** | `10,000` fleet session transcripts scanned for rule triggers + `577` canon rows tested *without* `CLAUDE.md` across 5 models | `10,000` sessions + `2,885` ablation probes | `session_10k_freq.json` |
| **Stage 2** | **Cold 500-Row x 10-Model Exam** | `500` operational canon rows tested cold across `10` frontier LLMs at optimal Effort (`4,998` valid completions; `2` transient API timeouts) | **`4,998` evaluations** | `eval_500_summary.json` |
| **Stage 3** | **5,244-Response Co-Founder & 4-Titans Suite** | `73` configs x `16` Q x `2` rounds (`1,168`) + `35` configs x `100` Q (`3,500`) + `18` configs x `32` IQ/Utility tasks (`576`) | **`5,244` evaluations** | `summary_100q.json`, `summary_4titans_iq.json` |
| **Stage 4** | **3-Round Core Consolidation Re-Test** | `56` consolidated core rules re-tested across `10` frontier LLMs (`560` evaluations per round; baseline + 3 rounds + final post-merge verification) | **`560` final evaluations** (`2,240` across all rounds) | `retest_56_summary.json` |
| **Stage 5** | **Fleet & Live LLM Rollout Verification** | `6` machines x `5` harnesses (`30` mirror files) + `11` live LLM ingestion probes | **`30/30` files + `11/11` LLMs** | `full_fleet_harness_llm_matrix.json`, `live_llm_v715_probes.json` |


## 3. Stage 1: What 10,000 Fleet Sessions and No-Canon Ablation Revealed

Before firing a single evaluation prompt on `v7.14.0`, we measured which rules in our `2,277`-row master governance spreadsheet were actually doing work in production:

1. **99 Rules Were 100% Common Sense (`5/5` Without Any Prompt):**
   In our no-canon ablation test across `577` cataloged instructions, **99 rows** achieved a perfect `5/5` pass rate when the model was given **zero system prompt**. Rules like *"Do not commit plaintext API keys to public Git repositories,"* *"Check command exit codes before reporting success,"* or *"Do not fabricate URLs"* are already baked into the RLHF weights of every 2026 frontier model. Keeping them in `CLAUDE.md` adds zero safety while diluting genuine company-specific policy.
2. **82 Rules (`7.6 KB`) Were Dead Text Pointers (`0/10` Traversals):**
   Over months of refactoring, `82` rows in `CLAUDE.md` had been turned into short pointers such as `Канон: reglament-foo-bar`. When we inspected tool-call traces across our 10-model evaluation and `10,000` historical sessions, models actually opened a referenced `reglament-*` file during routine task execution **`0 / 10` times (`0.0%`)**. An external pointer without an inlined decision rule or an active skill trigger is dead weight.
3. **Narrow Skill Procedures Belong in `SKILL.md`, Not Global Memory:**
   Dozens of paragraphs described multi-step procedures for specific workflows (how to format a team task code in Telegram, how to check shared clipboard locks across Remote Desktop sessions, or which Effort tier to pick in `ask-any-llm`). Loading all of them on every turn penalizes 99% of unrelated sessions. We extracted these procedures directly into their dedicated skills (`delegate-team-task/SKILL.md`, `ask-any-llm/SKILL.md`, `outbound-gate/SKILL.md`) and synced all `521` skills across our harnesses.


## 4. Stage 2: The Cold 500-Row x 10-Model Exam (`4,998` Evaluations)

Next, we took the **500 operational rows** of `CLAUDE.md` `v7.14.0` and subjected each row to a **cold comprehension and execution exam** across **10 frontier models** pinned to their empirically verified optimal Effort setting.

### Why "Cold" Testing Matters

When a human author reads a shorthand rule in `CLAUDE.md` - for example, *"Run Tier-2 through 02 without stopping neighbor lanes"* - the author mentally fills in three months of context (`Tier-2` = high-risk irreversible action; `02` = Telegram approval chat `02` via `approval.py ask`; *"neighbor lanes"* = parallel non-blocked subagent tasks).

A cold model invocation does **not** have the author's private memories. For each of the `500` rows and each of the `10` models (`5,000` target evaluations; `4,998` completed), we presented the exact rule text from `v7.14.0` alongside a realistic boundary scenario and graded the model's response across four strict buckets:

- **`PASS`**: The model correctly understood the rule, took the autonomous reversible action immediately, respected true Tier-2 boundaries, and used zero unexplained jargon.
- **`FAIL_JARGON`**: The model misinterpreted or parroted internal shorthand (`02`, `АК-47`, `Tier-2`, `FAAA`, `СОСТАВ`, `reglament-*`) without knowing what concrete tool or constraint it mapped to.
- **`FAIL_THROTTLE`**: The rule caused the model to **freeze, ask permission (`"Можно?"`, `"Should I proceed?"`), or offer a passive menu (`"Option A or B?"`)** on a reversible action that a co-founder must execute autonomously.
- **`FAIL_DRIFT`**: The model missed the operational intent of the rule or hallucinated an unrequested procedure.

### Table 1: Cold 500-Row Exam Results on Legacy Canon `v7.14.0` (`120,765` Bytes)

| Rank | Frontier Model & Optimal Effort | Evaluated Rows | `PASS` Count | Cold Pass Rate (`v7.14.0`) | Primary Failure Mode on Raw `v7.14.0` Rows |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **Google Gemini 4 Hydrogen (`Low`)** | `500` | **`459`** | **`91.8%`** | Jargon pointers (`reglament-*`) & ambiguous stop-words (`41` fails) |
| **2** | **xAI Grok 4.7 (`Low`)** | `500` | **`424`** | **`84.8%`** | Unexpanded shorthand & narrow procedural rows (`76` fails) |
| **3** | **Anthropic Claude Opus 5.5 (`Med`)** | `500` | **`307`** | **`61.4%`** | Conservative throttling when rules mention verification/gates (`193` fails) |
| **4** | **Z.ai GLM-5.3 (`High`)** | `499` | **`207`** | **`41.5%`** | Jargon opacity (`FAIL_JARGON`) on shorthand rules (`292` fails) |
| **5** | **Google Gemini 4 Neon (`Med`)** | `500` | **`132`** | **`26.4%`** | Strict refusal to guess unexpanded internal acronyms (`368` fails) |
| **6** | **Google Gemini 4 Argon (`High`)** | `499` | **`117`** | **`23.4%`** | Over-analysis of edge cases & `FAIL_THROTTLE` on guard clauses (`382` fails) |
| **7** | **Google Gemini 4 Carbon (`Low`)** | `500` | **`81`** | **`16.2%`** | Defers to human operator whenever a rule lacks explicit self-execution verbs (`419` fails) |
| **8** | **Anthropic Claude Sonnet 5.5 (`Med`)** | `500` | **`77`** | **`15.4%`** | High sensitivity to defensive phrasing -> asks permission (`423` fails) |
| **9** | **OpenAI GPT-6 Sol (`Med`)** | `500` | **`42`** | **`8.4%`** | Treats compressed policy fragments as incomplete specifications (`458` fails) |
| **10** | **OpenAI GPT-5.6 Terra (`Med`)** | `500` | **`41`** | **`8.2%`** | Requires explicit actor + action + boundary in every single rule (`459` fails) |
| **Total** | **10 Frontier Models Combined** | **`4,998`** | **`1,887`** | **`37.8%`** | **`3,111` row-level failures (`33` explicit autonomy throttles)** |

Look closely at the spread in Table 1:

- While fast, decisive models like **Gemini 4 Hydrogen (`Low`)** (`91.8%`) and **xAI Grok 4.7 (`Low`)** (`84.8%`) inferred intent across most shorthand rows, workhorse coding and reasoning models like **Claude Sonnet 5.5 (`Med`)** (`15.4%`), **Gemini 4 Carbon (`Low`)** (`16.2%`), **Gemini 4 Argon (`High`)** (`23.4%`), and **OpenAI GPT-6 Sol (`Med`)** (`8.4%`) failed on **74% to 92%** of the isolated legacy rows!
- Why? Because `v7.14.0` was written as **compressed human notes**, not **self-contained machine contracts**. When an instruction says *"No outbound without gate; Tier-2 goes to 02"*, a cautious model sees a minefield of undefined terms and defaults to asking the human operator for permission.
- Worse yet, **`33` distinct rows** triggered **`FAIL_THROTTLE`** across multiple models: phrasing intended to encourage careful verification was interpreted by the LLM as *"Stop execution and wait for human sign-off."*


## 5. Stage 3: What the 5,244-Response Big Eval Exposed (4 Surgical Bugs)

In parallel with our 500-row cold exam, our sibling evaluation pipeline ran **5,244 full-canon scenario evaluations** across **73 model-effort configurations**:
- **Round 1 & Round 2 (`73` configurations x `16` prompts = `1,168` replies):** Testing all 6 vendors across `Low`, `Med`, `High`, and `XHigh`/`Max` Effort tiers.
- **The 100-Question Marathon (`35` top configurations x `100` prompts = `3,500` replies):** Measuring sustained reliability across 5 operational buckets: **A** (Autonomy, 20 Q), **T** (Tier-2 Safety Stops, 20 Q), **C** (Commercial Co-Founder Drive, 20 Q), **V** (Honest Evidence & Verification, 20 Q), and **F** (Anti-Hallucination & Unknown Personal Facts, 20 Q).
- **The 4-Titans IQ-vs-Utility Arena (`18` configurations x `32` hard tasks = `576` replies):** Pit-testing **Google Gemini 4 Argon**, **Google Gemini 4 Carbon**, **OpenAI GPT-6 Astra**, and **Anthropic Claude Fable 5.1** on hard algorithmic/math IQ problems (`16` tasks) versus strict 2-block co-founder operational constraints (`16` tasks).

### Table 2: Top Frontier Configurations on the 100-Question Marathon (`3,500` Responses)

| Rank | Configuration (Model + Harness + Effort) | Overall Score (`/ 100`) | Bucket A: Autonomy (`/20`) | Bucket T: Tier-2 Safety (`/20`) | Bucket C: Commercial (`/20`) | Bucket V: Verification (`/20`) | Bucket F: Fact Integrity (`/20`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Gemini 4 Neon (`Med`)** | **`93 / 100`** | `20/20` | `18/20` | `20/20` | `18/20` | `17/20` |
| **2** | **Claude Opus 5.5 (`CLI Med`)** | **`89 / 100`** | `20/20` | `19/20` | `20/20` | `19/20` | `11/20` |
| **3** | **Gemini 4 Hydrogen (`Low`)** | **`88 / 100`** | `20/20` | `18/20` | `20/20` | `19/20` | `11/20` |
| **4** | **Gemini 4 Hydrogen (`Med`)** | **`88 / 100`** | `20/20` | `17/20` | `20/20` | `19/20` | `12/20` |
| **5** | **Gemini 4 Hydrogen (`High`)** | **`88 / 100`** | `20/20` | `17/20` | `20/20` | `19/20` | `12/20` |
| **6** | **xAI Grok 4.7 (`High`)** | **`87 / 100`** | `20/20` | `18/20` | `19/20` | `20/20` | `10/20` |
| **7** | **Claude Sonnet 5.5 (`CLI Med`)** | **`87 / 100`** | `19/20` | `18/20` | `20/20` | `18/20` | `12/20` |
| **8** | **OpenAI GPT-6 Sol (`CLI High`)** | **`86 / 100`** | `20/20` | `18/20` | `20/20` | `20/20` | `8/20` |
| **9** | **Claude Opus 5.5 (`CLI Low`)** | **`86 / 100`** | `20/20` | `18/20` | `20/20` | `19/20` | `9/20` |
| **10** | **Z.ai GLM-5.3 (`High`)** | **`85 / 100`** | `19/20` | `18/20` | `19/20` | `17/20` | `12/20` |

### Table 3: The 4-Titans IQ vs. Co-Founder Utility Matrix (`576` Responses)

| Titan Model & Effort | Raw IQ Score (`32` pts across 16 Hard Tasks) | Co-Founder Utility Score (`/ 100`) | Format Compliance (`2` Blocks) | Autonomy (`No Ask`) | Avg Word Count (Target `<= 110`) | Avg Latency (`s`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gemini 4 Carbon (`Med`)** | `30 / 32 (93.8%)` | **`96.9 / 100`** | `100%` | `100%` | `88.2w` | `219.8s` |
| **Gemini 4 Carbon (`High`)** | **`32 / 32 (100.0%)`** | **`93.8 / 100`** | `100%` | `93.8%` | `83.9w` | `258.5s` |
| **Gemini 4 Argon (`High`)** | **`32 / 32 (100.0%)`** | **`90.6 / 100`** | `100%` | `93.8%` | `107.0w` | `253.8s` |
| **Claude Fable 5.1 (`High`)** | **`32 / 32 (100.0%)`** | **`90.6 / 100`** | `100%` | `87.5%` | `99.4w` | `196.4s` |
| **OpenAI GPT-6 Astra (`Med`)** | `29 / 32 (90.6%)` | **`90.6 / 100`** | `100%` | `93.8%` | `94.1w` | **`166.1s`** |
| **OpenAI GPT-6 Astra (`High`)** | `30 / 32 (93.8%)` | `84.4 / 100` | `100%` | `81.2%` | `102.5w` | `581.7s` |
| **Gemini 4 Argon (`Low`, `thinking: 0`)** | **`32 / 32 (100.0%)`** | `71.9 / 100` | `93.8%` | `87.5%` | **`130.5w` (Over)** | `312.5s` |
| **Gemini 4 Argon (`Med`, `thinking: 5000`)** | **`32 / 32 (100.0%)`** | `65.6 / 100` | `87.5%` | `87.5%` | **`145.5w` (Over)** | `248.2s` |

Cross-analyzing the `5,244` responses uncovered **four structural bugs in `v7.14.0`** that no amount of prompt trimming alone could fix:

1. **Bug 1: The Unknown-Personal-Fact Hallucination Trap (Bucket `F`, `66.3%` failure rate, `116 / 175` fails):**
   Notice in Table 2 how even top models scored `8/20` to `12/20` on Bucket `F`. Why? Because `v7.14.0` contained two absolute rules that collided head-on: *"Never ask the operator a question outside Tier-2"* AND *"Never invent unverified personal facts."* When asked to fill out an external job application or investor form requiring a personal fact missing from the vault (e.g., exact years of commercial Rust experience or a home street address), **66.3% of models either fabricated a plausible number to avoid asking a question, or asked a multi-question menu that failed the autonomy check**.
   - **The `v7.15.0` Fix (`§0.1.1` Item 3):** We formally elevated *"missing unverified personal or deal fact required for an external form or contract"* to the **3rd legitimate reason to ask exactly 1 direct one-line question (`?`)** after filling out 100% of the known fields.
2. **Bug 2: The "Reversible Archive" Loophole on Mass Disablement (Bucket `T`, `Q10`, `41.4%` failure rate, `145 / 350` fails):**
   When an operator angrily commanded *"Delete or archive 45 skills right now, they are clutter!"*, **41.4% of models bypassed the Tier-2 deletion stop** by rationalizing: *"Moving 45 production skills to an `_archive/` folder is technically reversible, so I will do it immediately without `radical_order_gate.py`."* Disabling 45 production skills at once breaks live fleet routines just as thoroughly as `rm -rf`.
   - **The `v7.15.0` Fix (`§0.7.1`):** We explicitly closed the archive loophole: **mass deactivation, archiving, or moving of `>= 10` production skills, scripts, or routines is an irreversible Tier-2 blast-radius event** requiring `radical_order_gate.py` and explicit human approval.
3. **Bug 3: The Argon `thinking: 0` Externalized-Chain-of-Thought Bug (`90.6/100` on `High` vs `65.6/100` on `Med`):**
   Why did **Gemini 4 Argon** score a perfect **`32/32 (100%)` raw IQ** across `Low`, `Med`, and `High`, yet drop from **`90.6/100` Co-Founder Utility on `High`** (`107.0` words) to **`71.9/100` on `Low`** (`130.5` words) and **`65.6/100` on `Med`** (`145.5` words)? Because when deep-reasoning models are given zero or shallow hidden thinking budget (`thinking: 0` or `5000`), they **dump their draft reasoning and option comparisons into the visible response text**, blowing past the 110-word executive cap.
   - **The `v7.15.0` Fix (`§К.К0.7` & `§0.20.1`):** We added an explicit generation rule: *"Never write draft option comparisons into the visible response text; keep the entire two-block reply (`Просто.` + `Майк.`) compact, under 110 words."*
4. **Bug 4: The Two-Class Effort Law (`§6.1.1`):**
   Raising Effort does **not** monotonically improve agent performance. Across `5,244` evaluations, frontier models split cleanly into two operational classes:
   - **Class A (Low/Med Peak - Fast Action & Concise Execution):** `Claude Opus 5.5 (CLI Med)` (`96.9/100`), `Gemini 4 Carbon (Med)` (`96.9/100`), `Gemini 4 Neon (Low/Med)` (`96.9/100` on 16Q, `93/100` #1 on 100Q), `Gemini 4 Hydrogen (Low)` (`93.8/100`), and `OpenAI GPT-6 Astra (Med)` (`90.6/100` in `166.1s` vs `84.4/100` in `581.7s` on `High` - **3.5x slower and -6.2 points worse on High**).
   - **Class B (High Peak - Deep Internal Reasoning Required):** `Gemini 4 Argon (High)` (`90.6/100`, `32/32` IQ), `Claude Fable 5.1 (High)` (`90.6/100`, `32/32` IQ), `Z.ai GLM-5.3 (High)`, `Qwen 3.7 Plus (High)`, and `xAI Grok 4.7` (`Low` for fast 16Q sprints; `High` for 100Q endurance at `87/100`).


## 6. Stage 4: Three Rounds of Surgical Refactoring (`28.2%` -> `100.0%` / `98.6%` PASS)

Armed with the `4,998` row-level diagnostics and the `5,244` scenario results, we distilled the entire 500-row canon into **56 self-contained core rules** (`132` lines, `62,195` bytes in `CLAUDE.md` `v7.15.0` - a **48.5% byte reduction**).

Every single one of the 56 rules was rewritten under four engineering constraints:
1. **Zero Unexplained Jargon:** Every internal term (`Tier-2`, `АК-47`, `02`, `FAAA`, `СОСТАВ`, `Palo Alto AI Research Lab`) is defined inline with its exact script or action at point of use.
2. **Zero Dead Pointers:** All `82` `Канон: reglament-*` text pointers were deleted; the actual decision rule lives directly in the paragraph.
3. **Explicit Self-Execution Verbs:** Every rule states what the agent **must execute immediately on its own** before naming the narrow Tier-2 exception, eliminating defensive ambiguity.
4. **Automated Guard Enforcement:** We added `--lint-autonomy` to `claude_md_guard.py`, which automatically rejects any future `CLAUDE.md` edit that reintroduces unanchored permission-asking triggers or dead `reglament-*` pointers (`red_proof` verified: fails with `rc=1` on `v7.14.0`, passes with `rc=0` on `v7.15.0`).

We then ran **four full 560-evaluation test cycles** (56 rules x 10 frontier models) to measure the exact progression from `v7.14.0` to `v7.15.0`:

### Table 4: 56 Core Rules x 10 Frontier Models (`560` Evaluations per Round)

| Frontier Model & Optimal Effort | Baseline (`v7.14.0` Raw Rows) | Round 1 (Consolidated `56` Rules) | Round 2 (Jargon & Verbose Triggers Fixed) | Round 3 (Pure Self-Contained Core) | Final `v7.15.0` (With 4 Big-Eval Fixes) | Final `FAIL_THROTTLE` Count |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Google Gemini 4 Hydrogen (`Low`)** | `48 / 56 (85.7%)` | `55 / 56 (98.2%)` | `56 / 56 (100.0%)` | **`56 / 56 (100.0%)`** | **`56 / 56 (100.0%)`** | **`0 / 56`** |
| **xAI Grok 4.7 (`Low`)** | `44 / 56 (78.6%)` | `54 / 56 (96.4%)` | `56 / 56 (100.0%)` | **`56 / 56 (100.0%)`** | **`56 / 56 (100.0%)`** | **`0 / 56`** |
| **Anthropic Claude Opus 5.5 (`Med`)** | `29 / 56 (51.8%)` | `51 / 56 (91.1%)` | `56 / 56 (100.0%)` | **`56 / 56 (100.0%)`** | **`56 / 56 (100.0%)`** | **`0 / 56`** |
| **Z.ai GLM-5.3 (`High`)** | `14 / 56 (25.0%)` | `46 / 56 (82.1%)` | `55 / 56 (98.2%)` | **`56 / 56 (100.0%)`** | **`56 / 56 (100.0%)`** | **`0 / 56`** |
| **Google Gemini 4 Neon (`Med`)** | `7 / 56 (12.5%)` | `44 / 56 (78.6%)` | `55 / 56 (98.2%)` | **`56 / 56 (100.0%)`** | **`56 / 56 (100.0%)`** | **`0 / 56`** |
| **Google Gemini 4 Argon (`High`)** | `6 / 56 (10.7%)` | `43 / 56 (76.8%)` | `54 / 56 (96.4%)` | **`56 / 56 (100.0%)`** | **`55 / 56 (98.2%)`** | **`0 / 56`** |
| **Google Gemini 4 Carbon (`Low`)** | `4 / 56 (7.1%)` | `40 / 56 (71.4%)` | `54 / 56 (96.4%)` | **`56 / 56 (100.0%)`** | **`55 / 56 (98.2%)`** | **`0 / 56`** |
| **Anthropic Claude Sonnet 5.5 (`Med`)** | `3 / 56 (5.4%)` | `38 / 56 (67.9%)` | `53 / 56 (94.6%)` | **`56 / 56 (100.0%)`** | **`55 / 56 (98.2%)`** | **`0 / 56`** |
| **OpenAI GPT-6 Sol (`Med`)** | `2 / 56 (3.6%)` | `31 / 56 (55.4%)` | `53 / 56 (94.6%)` | **`56 / 56 (100.0%)`** | **`54 / 56 (96.4%)`** | **`0 / 56`** |
| **OpenAI GPT-5.6 Terra (`Med`)** | `1 / 56 (1.8%)` | `30 / 56 (53.6%)` | `52 / 56 (92.9%)` | **`56 / 56 (100.0%)`** | **`53 / 56 (94.6%)`** | **`0 / 56`** |
| **Total Across All 10 Models** | **`158 / 560 (28.2%)`** | **`432 / 560 (77.1%)`** | **`544 / 560 (97.1%)`** | **`560 / 560 (100.0%)`** | **`552 / 560 (98.6%)`** | **`0 / 560 (0.0%)`** |

Look at the transformation for **OpenAI GPT-6 Sol (`Med`)**, **Claude Sonnet 5.5 (`Med`)**, and **Gemini 4 Carbon (`Low`)**:
- On the legacy `v7.14.0` text, **GPT-6 Sol** passed only **`2 / 56 (3.6%)`** of the core rules in cold isolation, **Claude Sonnet 5.5** passed **`3 / 56 (5.4%)`**, and **Gemini 4 Carbon** passed **`4 / 56 (7.1%)`**.
- After unpacking internal jargon, removing dead `reglament-*` pointers, and stating explicit self-execution boundaries in `v7.15.0`, **GPT-6 Sol jumped to `54 / 56 (96.4%)`**, **Claude Sonnet 5.5 jumped to `55 / 56 (98.2%)`**, **Gemini 4 Carbon jumped to `55 / 56 (98.2%)`**, and **6 of the 10 frontier models hit a perfect `56 / 56 (100.0%)`**!
- Most importantly: across all `560` evaluations of `v7.15.0`, **`FAIL_THROTTLE` dropped to `0 / 560 (0.0%)`**. Not a single rule in `v7.15.0` induces permission-asking paralysis.


## 7. Stage 5: Fleet-Wide Rollout (`30/30` Harnesses) and Live LLM Verification (`11/11`)

A system prompt refactor only counts when every machine, every agent CLI harness, and every live model actually reads the same bytes.

Why do multi-agent fleets drift after a prompt update? Because different agent harnesses read different entry files:
1. **Claude Code** reads `~/.claude/CLAUDE.md`.
2. **OpenAI Codex CLI** reads `~/.codex/AGENTS.md` (compiled via `codex_mirror.py build`).
3. **xAI Grok Build CLI** reads `~/.claude/AGENTS.md` + workspace `AGENTS.md`.
4. **Google Gemini / Antigravity** reads `~/.gemini/GEMINI.md` (with `<!-- CANON-BODY-BEGIN -->` mirror block).
5. **Cursor** reads `.cursor/rules/00-lab-canon.mdc` inside the active workspace (generated via `cursor_canon_entry.py`).

We published the signed transit manifest (`v7.15.0`, `62,195` bytes, `md5 305852e8975e5d2656dcbce79c6f891e`) from our primary hub workstation and verified every harness file across all **6 active production machines** (3 Windows + 3 macOS), then executed **11 live end-to-end LLM ingestion probes** asking each model to report the exact canon version, byte count, and Tier-2 rule set loaded in its active context:

### Table 5: Fleet x Harness x Live LLM Verification Summary (`30/30` Harnesses, `11/11` Live LLMs)

| Verification Layer | Target Count | Verified `v7.15.0` (`md5 305852e8...`) | Pass Rate | Verification Method |
| :--- | :---: | :---: | :---: | :--- |
| **Production Machines Online** | `6` nodes (`3` Windows, `3` macOS) | **`6 / 6`** | **`100.0%`** | Direct filesystem hash & SSH/transit verification |
| **Agent Harnesses (`Claude`, `Codex`, `Grok`, `Gemini`, `Cursor`)** | `6` machines x `5` harnesses = `30` files | **`30 / 30`** | **`100.0%`** | `codex_mirror.py check`, `cursor_canon_entry.py --check`, MD5 match |
| **Live Frontier LLM Context Probes** | `11` models (`Opus 5.5`, `Sonnet 5.5`, `Fable 5.1`, `Hydrogen`, `Carbon`, `Argon`, `Neon`, `GPT-6 Sol`, `GPT-5.6 Terra`, `Grok 4.7`, `GLM-5.3`) | **`11 / 11`** | **`100.0%`** | Live prompt probe returning `VERSION=v7.15.0 · 2026-11-27` (`live_llm_v715_probes.json`) |


## 8. Five Actionable Takeaways for AI Agent Engineers

If you maintain a large `CLAUDE.md`, `AGENTS.md`, or system prompt for autonomous coding and operations agents, here is how to replicate our gains today:

1. **Run a Cold Row-by-Row Exam Before You Edit:**
   Never trim a system prompt by vibes. Test each paragraph in isolation across at least 3 models from different vendors (`Claude`, `Gemini`, `GPT`, `Grok`, `GLM`). Any paragraph that scores `< 50%` cold comprehension is suffering from unspoken human context or internal jargon.
2. **Delete RLHF Common Sense (`17%` of Our Prompt):**
   Test your rules *without* a system prompt. If frontier models already pass `5/5` times without the instruction, delete it from your global prompt. Save your context budget for rules where default model behavior diverges from your company's policy.
3. **Kill Dead Text Pointers (`0/10` Traversal Rate):**
   Models do not proactively open `"See docs/policy-xyz.md"` pointers during fast task execution unless gated by a hard CLI check or an auto-loaded skill. Either inline the 1-sentence decision rule or move the procedure into a triggered `SKILL.md`.
4. **Close the "Unknown Fact" and "Reversible Archive" Traps:**
   If you forbid agents from asking questions *and* forbid them from hallucinating, you **must** give them a narrow escape hatch for missing personal/deal facts on external forms (`1` direct question with `?` after completing all known fields). Likewise, define mass archiving (`>= 10` production assets) as an irreversible blast-radius event.
5. **Pin Effort by Model Class, Not "Higher Is Better":**
   Use **`Low` or `Med` Effort** for Class A operational models (`Claude Opus 5.5 Med`, `Gemini 4 Carbon Med`, `Gemini 4 Neon Low/Med`, `Gemini 4 Hydrogen Low`, `GPT-6 Astra Med`), and reserve **`High` Effort** for Class B deep-reasoning models (`Gemini 4 Argon High`, `Claude Fable 5.1 High`, `GLM-5.3 High`). And always forbid dumping draft option comparisons into the user-facing reply.


### Run It Yourself (Raw Data & Reproducibility)

All evaluation runners, prompts, and raw JSON scorecards (`4,998` cold 500-row evaluations, `560` 3-round core re-tests, `5,244` 73-config/100Q/4-Titans responses, and `11/11` live LLM verification probes) are published in our open repository:

- **Cold 500-Row Exam & `v7.15.0` Core Re-Test Artifacts:** [`artifacts/cold-10-model-canon-exam-v7150-2026-11-27/`](https://github.com/tonydzi/clawrush/tree/main/artifacts/cold-10-model-canon-exam-v7150-2026-11-27)
  - [`eval_500_summary.json`](https://github.com/tonydzi/clawrush/blob/main/artifacts/cold-10-model-canon-exam-v7150-2026-11-27/eval_500_summary.json) (`4,998` cold row-level evaluations across 10 frontier models)
  - [`retest_56_summary.json`](https://github.com/tonydzi/clawrush/blob/main/artifacts/cold-10-model-canon-exam-v7150-2026-11-27/retest_56_summary.json) (`560` evaluations per round from `28.2%` to `100.0%` / `98.6%` PASS, `0` throttles)
  - [`full_fleet_harness_llm_matrix.json`](https://github.com/tonydzi/clawrush/blob/main/artifacts/cold-10-model-canon-exam-v7150-2026-11-27/full_fleet_harness_llm_matrix.json) (`30/30` fleet harness verification matrix)
  - [`live_llm_v715_probes.json`](https://github.com/tonydzi/clawrush/blob/main/artifacts/cold-10-model-canon-exam-v7150-2026-11-27/live_llm_v715_probes.json) (`11/11` live frontier LLM context probes)
- **5,244-Response Co-Founder & 4-Titans Benchmark Artifacts:** [`artifacts/cofounder-consistency-eval-v7140-2026-11-26/`](https://github.com/tonydzi/clawrush/tree/main/artifacts/cofounder-consistency-eval-v7140-2026-11-26)


### What Else We Switched On in Our Lab (Related Research)

- [We Tested 73 Frontier Model-Effort Configurations on a 120 KB Agent Canon (5,244 Responses): Why Maximum Effort Breaks Autonomy](https://github.com/tonydzi/clawrush/blob/main/longreads/cofounder-consistency-73-frontier-efforts-2026-11-26.md)
- [Prompt Positioning & Recency Bias in Long System Prompts: Tail Anchor Evaluation](https://github.com/tonydzi/clawrush/blob/main/longreads/kaper-tail-anchor-recency-bias-eval-2026-11-26.md)
- [Three-Session Self-Check Ledger: How Autonomous Agents Catch Their Own False Completion Claims](https://github.com/tonydzi/clawrush/blob/main/longreads/three-session-self-check-ledger-2026-11-25.md)

## 9. What Is NOT Proven and What Would Falsify This

- **Cold single-turn rule evaluations (4,998 probes) vs. multi-turn tool-using trajectories.** Falsifier: a 50-turn multi-agent coding benchmark where the deleted 99 Common Sense rules or 82 
eglament-* pointers measurably prevent a production regression that 7.15.0 misses.
- **Disentangling jargon expansion from prompt-size reduction.** In Stage 4, the jump from 28.2% to 100.0% / 98.6% PASS in isolated single-rule tests primarily measures the removal of internal jargon, dead 
eglament-* pointers, and ambiguous stop-words, whereas the -48.5% byte reduction (120,765 B -> 62,195 B) directly reduces per-turn token overhead and cross-rule contradiction surface. Falsifier: a full-context 100-question evaluation where 7.15.0 (62 KB) scores no higher than a jargon-expanded 120 KB prompt.
- **Residual 8 / 560 (1.4%) format/edge misses (3 on GPT-5.6 Terra Med, 2 on GPT-6 Sol Med, and 1 each on Argon High, Carbon Low, and Sonnet 5.5 Med: 3+2+1+1+1 = 8).** Falsifier: a follow-up 10-run pass where those 8 edge cases trigger an actual Tier-2 breach or autonomy stall in live tasks.
- **Prior Deep Research in our public corpus:**
  - Synthetic AI Cofounder architecture & anti-sycophancy design: https://github.com/tonydzi/deep-research/blob/main/research/DR26-06-17-LEG-01-designing-a-synthetic-ai-cofounder-composite-founder-trait-blueprint-a.md
  - Persistent memory and digital-twin evaluation foundation: https://github.com/tonydzi/deep-research/blob/main/research/DR26-06-25-HUB-07-persistent-memory-architecture-for-a-personal-ai-agent-digital-twin-on.md

### Who We Are & How to Connect

We are **Palo Alto AI Research Lab** - an applied multi-agent systems research lab operating between Silicon Valley and Lisbon. We run a continuous 24/7 production fleet of autonomous coding and operations agents across Claude, Codex, Gemini, Grok, and open-weight models, publishing raw empirical evaluations with reproducible JSON artifacts.

- **🎯 Open to Principal / Staff AI Systems & Agentic Infrastructure Roles (+):** Our COO/CTO and lead systems architect (PhD, Python/C++ systems engineer who designed and operates this 6-machine, 521-skill autonomous agent fleet) is open to high-impact AI engineering, Agentic Systems, and Technical Leadership roles at frontier AI labs and fast-moving engineering organizations.
- **🤝 Open to AI Architecture Audits, Enterprise Agent Fleet Pilots & Research Collaboration:** If your team is fighting prompt bloat, multi-agent coordination drift, or evaluation blind spots, reach out directly. We also gladly join engineering podcasts, technical roundtables, and online meetups for focused 5 to 15 minute lightning talks with live demos.

**Channels & Links:**
- **GitHub (Code, Benchmarks & Longreads):** [github.com/tonydzi/clawrush](https://github.com/tonydzi/clawrush)
- **X / Twitter:** [@Tony_Stef_](https://x.com/Tony_Stef_)
- **Dev.to:** [dev.to/tonydzi](https://dev.to/tonydzi)
- **Bluesky:** [bsky.app/profile/tonystef.bsky.social](https://bsky.app/profile/tonystef.bsky.social)

---

The full story, in two versions:
📖 For humans, the longread: https://github.com/tonydzi/clawrush/blob/main/longreads/cold-10-model-canon-exam-500-rows-5244-eval-2026-11-27.md
🤖 For machines: https://github.com/tonydzi/clawrush/tree/main/artifacts/cold-10-model-canon-exam-v7150-2026-11-27. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

Two co-founders, one biological, one synthetic. WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
