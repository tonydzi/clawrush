# Dev-log: subscription utilisation as a first-class metric

*Written for machines. Utilisation report read 2026-08-16.*

## State

Four paid LLM subscriptions, **$540/month total**.

| vendor | plan | $/mo | calls 7d | bucket drawn | verdict |
|---|---|---|---|---|---|
| anthropic | Max | 200 | 0 | **not measured** | 🤔 |
| xai | SuperGrok | 300 | 16 | **not measured** | 🤔 |
| openai | Codex | 20 | 22 | **3.0%** | 🔴 under-drawn |
| google | Gemini Pro | 20 | 12 | **not measured** | 🤔 |

Research volume feeding these rails: **33 DRs / 7d, 175 / 30d.**

Triggering observation (2 days earlier): best available paid model **95% unspent** at end of cycle while work ran on a cheaper tier; Codex at **0%** for that week.

## The primary defect is instrumentation, not usage

Three of four panels report `not measured`. The question "how much of what we pay for do we use" is **unanswerable** from our own data. Percent-drawn requires a human to open each vendor panel once and record it; the code around it is trivial.

**Invariant:** "we have subscriptions" is not a state. State = percent drawn, per bucket, with a date.

## Rules adopted

1. **Unused bucket = spent money producing nothing.** Frugality inside one allowance while another sits unspent is a net loss plus a quality penalty.
2. **Every part declares its rail** in the passport: which paid bucket it burns. Defaulting to the orchestrating vendor is an architecture defect — it is the mechanism by which all load lands on one rail without a decision.
3. **Route by headroom, not habit.** Mechanical work (shell, file reads, extraction, drafts) → rail with most remaining. Judgement, voice, orchestration → fixed.

## Anti-pattern: end-of-cycle burn

Switching to high-spend mode near reset is the same error inverted: the bucket gets spent on whatever is at hand rather than on work that warranted the best model. Correct mitigation is routing applied from day 1 of the cycle, not a sprint at the end.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
