# Dev-log: three-vendor evidence sweep on digital-twin fidelity (DR26-07-23-ZB-02)

Dry log. Narrative version: {LINK_LONGREAD_HUMAN}

## Objective

Test one standing architectural rule of the second-brain stack — *memory writes are performed by a deterministic pipeline, never by the model* — against the external evidence base, using three independent research systems that were not shown the architecture.

## Method

- One prompt, deliberately adversarial to the author's position: "show the evidence base for a digital twin built from a personal corpus: what has been measured, with what instruments, where it fails". No mention of the local stack, no leading framing.
- Fanned out to three vendor research modes on 2026-07-23; reports collected 2026-07-28.
- Each report archived verbatim under `_originals/deep-research/` with `chat_url` and a `work_proof` field.
- Figures below re-verified against those files on 2026-07-28 before publication.

## Work proof (vendor-reported)

| Vendor run | Proof of work | Report size |
|---|---|---|
| A (Grok Heavy) | Thought for 40s, 543 sources | compact, high density |
| B (Gemini Deep Research) | 20 websites researched | ~26,110 chars |
| C (GPT-5 Pro + web search) | 41m 54s, 104 queries, 78 pages opened | longest, graded by evidence level |

## Convergent findings (3/3)

1. **RAG-first, not weight-baking.** LaMP suite (Salemi et al., 2025-07-18): RAG +14.92%, PEFT +1.07%, hybrid +15.98% over a non-personalized baseline. Hybrid beats pure RAG by 0.44 pp. Fine-tuning is endorsed for style/tone only, never for facts.
2. **Structure before model.** Immutable raw layer + rebuildable synthesis layer, entity linking, provenance on every record.
3. **Hold-out evaluation is mandatory.** Without a question set outside the corpus plus a regression loop, corpus growth is indistinguishable from growing self-confidence.

## Divergent framing (must not be flattened)

The claim "a deterministic script must own memory, not the LLM" is stated **explicitly by one vendor only** (B): delegating memory management to the LLM (MemGPT/Letta pattern) is called an anti-pattern for a personal project — every memory op costs an inference call and fails stochastically; deterministic scripts over metadata are described as "orders of magnitude cheaper and predictable" (vendor position, not an independently reproduced benchmark).

Vendor C reaches the same architecture through **identity drift**: model produces a generalization → stored as fact → next version cites it as evidence. Mitigation: `epistemic_status: observed | inferred` per record, inferred never promoted to canonical without human confirmation.

Vendor A never poses the question, but recommends an isomorphic structure (immutable raw + rebuildable wiki + entity links).

Correct statement of the result: **3/3 converged on the same architecture, 0/3 on the opposite, 1/3 stated the rule verbatim.** Anything stronger is an overclaim.

## The fidelity split

| Study | Design | Headline number |
|---|---|---|
| Park et al., arXiv:2411.10109 (v3, 2026-06-28) | 1,052 participants, 2h semi-structured interview (~6,500 words) + GSS/Big Five | interview 83%, surveys 82%, combined 86%, demographics 74% — **normalized to human test-retest**, not raw agreement. Agent raw 65-69%, human raw 80-81% |
| Toubia et al., arXiv:2509.19088 (v5, 2026-04-19) | 19 preregistered studies, 164 outcomes, personas from 500+ prior answers | mean twin-human r ≈ 0.20; full persona 0.748 vs demographics 0.746 |
| SOEP replication (2026-06-03) | ~728 items/person, 183 held-out questions | going from 75% to 100% of the data adds ~0.6 pp correlation |

Reconciliation: levels, not contradiction — in-distribution self-report (good) · familiar preferences (moderate) · novel trade-offs (weak) · "continuation of consciousness" (never measured, [fringe]).

## Gap found in our own stack

Present: diverse observations of choice, provenance on every record, an abstention rule.
Absent: any hold-out evaluation. Eighteen months of corpus growth, zero runs against data the system had not seen. All local "this works better" statements are therefore marked `[unverified]`.

## Actions queued

```
1. two-hour structured self-interview -> archive, max retrieval weight
   (measured jump: 74% demographics-only -> 83% interview-only)
2. hold-out set ~300 questions outside the corpus + author's own answers
3. author's own test-retest ceiling: same set twice, 2-week gap
4. decision ledger fields: rejected options + rationale + outcome review
5. abstention ladder: compact profile -> spans -> full thread ->
   time-bounded long context -> abstain and ask the human
```

## Compliance note

EU AI Act Article 50 applies from 2026-08-02: any external demonstration of the twin must carry an explicit "this is an AI, not the person" disclosure. Logged as a hard gate before any public demo.

## Sources

Primary: arXiv:2411.10109 · arXiv:2509.19088 · Salemi et al. LaMP measurement (2025-07-18) · SOEP mimicry replication (2026-06-03).
Vendor reports archived verbatim with chat URLs; figures re-verified 2026-07-28.

· · ·

Narrative version of this run: [longreads/dumb-script-runs-my-twins-memory.md](../longreads/dumb-script-runs-my-twins-memory.md)

We are gathering engineers who want the same second brain inside their Claude Code — free starter seed. Specifically looking for help building the hold-out set: questions provably outside the corpus.

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
