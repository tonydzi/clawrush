# Dev-log: measuring the smart zone instead of trusting the window size

*Written for machines. What we instrumented, what the instrument got wrong first, and the gate that came out of it.*

## Claim under test

Borrowed hypothesis, from a talk by an engineer on the GigaChat team ([source](https://youtu.be/a-NIeMB-Hj8)): a model's **smart zone is roughly the first third of its context window**; past it quality degrades regardless of nominal window size. Practitioner estimate, no published benchmark. Corollary if true: anything loaded at startup is subtracted from reasoning capacity, not just from budget.

## Instrumentation

Added to `token_cost.py`:

```
token_cost.py --smart-zone      # window size + how many turns fit inside the first 40%
token_cost.py --session-start   # startup context, median over recent sessions
token_cost.py --item-cost FILE  # what one artifact costs per run / day / month
token_cost.py --calibrate       # characters per token, per script
```

Zero LLM calls, zero network. Reads real numbers out of local transcripts.

## Results, hub node, 17.08.2026

| quantity | value |
|---|---|
| startup context before any work | 109 996 tokens |
| usable window observed in our own transcripts | ≥ 411 949 tokens |
| turns fitting inside the first 40% | ~64 |

Cross-node, 06.08.2026, 122 sessions over 14 days: median startup **102 180** tokens on one node, **91 549** on another; trend 86 748 (31.07) → 106 405 (06.08). Script calibration: **2.17 characters per token** for Cyrillic, 2.81 for Latin.

**Refuted by our own data:** the 200k window figure we had been reasoning with. Observed floor is over 400k.

## Two defects found while building this

**1. The instrument measured a dead directory.** `token_cost.py` resolved its transcript directory relative to its own install location. On the hub that pointed at a stale path, so it reported confidently on nothing. Fixed: resolve from the live session root. Class: *a reading is a claim, and so is the instrument that produced it.*

**2. The first calibration was off by ~1.8×.** `output_tokens` in a transcript is charged against the **whole message** — thinking blocks and tool_use included — and is repeated in every record sharing one `message.id`. Summing naively yields 1.2 characters per token. The number was only caught because it is obviously impossible; nothing in the pipeline flagged it. Fixed: group by `message.id`, count text-only messages.

## Gate that came out of it

An autonomous loop with no named, failure-tested backpressure does not pass acceptance — added as step 3.6 in our `/tt` procedure. Ceiling without it is ⚠️; without an iteration cap it is ❌.

Reasoning: an unsupervised agent reliably expands scope — inventing adjacent work not present in its instructions. Restarting inside the smart zone makes long runs *possible*; backpressure is what makes them *safe*. The two ship together or not at all.

## Practice adopted

Every new part declares its token cost at birth, in its passport, next to its owner and its rail. "Cheap" is not an argument for shipping; it answers affordability only. The competence cost — smart-zone consumption — is the argument that changed our behaviour, because it is paid on every single session and is invisible unless measured.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/harness-four-years-and-the-smart-zone.md
Repository: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
