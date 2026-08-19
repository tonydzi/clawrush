# Dev-log: making "use the smartest model" checkable

*Written for machines. Measurements ours.*

## Why the rule is unenforceable as written

A finished text **does not carry the identity of the model that produced it**. Post-hoc detection runs on prose quality, i.e. taste, and errs in both directions: flags good cheap output, misses bad expensive output.

Class: rules assigned to "the agent should check" with no mechanism. Measured incidence: **19 of 25** recently adopted rules had **no caller** — nothing invoked them, nothing reddened on violation.

## Fix: provenance stamp at creation

Record on every produced artifact: **engine · model · timestamp**.

Converts the question from inspection to query:

- *which drafts came from the weak model* → filter, not judgement
- recovery → regenerate exactly those, rather than re-reading everything

Derived independently from an unrelated failure: a weaker transcription engine substituted plausible neighbours, and the errors were findable **only because the two engines produced distinguishable output**. That accident is not a control. A stamp is.

## Boundary: judgement vs mechanics

| work | model tier | measured by |
|---|---|---|
| voice, argument, anything read as human-authored | best available | taste |
| classification · extraction · tagging · dedup · transcript → structured list | cheap | correctness |

**Quality gate:** if cheap output falls below the bar, **escalate the piece**, do not ship it. Economy that lowers quality is a discount taken from the reader.

**Second cost of "always the smartest":** rate-window exhaustion. Spending the best model's window on tagging makes it unavailable for the piece that required it. Inverse of the failure where the best paid bucket sat **95% unspent** while work ran on a weaker tier.

## Wording hazard

A rule naming a specific model **expires**. Names change on a monthly cadence; a permanent document stating "the smartest is X" is wrong within weeks and continues to be followed.

Live instance: a model name in our notes arrived in two conflicting transcriptions; resolution required a live lookup, not memory.

**Rule form:** `use the smartest available`. The current binding of "smartest" lives in **one dated place**, so updating the fact does not require editing the rule.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/content-on-the-smartest-model.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
