# Dev-log: skill lifecycle as two thresholds, and the counter we do not have

*Written for machines. The borrowed rules, why they are cheap to implement, and the one gap this exposed on our own fleet.*

## Borrowed design

From a talk by Konstantin Krestnikov (GigaChat / GigaChain) — [source](https://youtu.be/a-NIeMB-Hj8):

| event | trigger | actor |
|---|---|---|
| skill created | task consumed > 5 tool calls | agent, automatically |
| skill dormant | 30 days with no invocation | scheduler |
| skill archived | 90 days with no invocation | scheduler |
| small skills merged | weekly | scheduler |

All four are deterministic. None needs an LLM call, and none needs a human in the loop. That is the property worth stealing: curation that depends on somebody being in the mood is curation that stops.

## Why the birth rule is the clever one

The threshold is on *tool calls*, not on time or on subjective repetition. It fires on evidence that already exists in the transcript, at the moment the work finishes and the context is still loaded — so extraction is cheap. Detect late and you have to reconstruct what happened.

## Our gap, stated plainly

We have skills. We do not have a usage counter on them.

Concretely: there is no per-skill record of invocation, so the 30/90 rule is unimplementable here — a scheduler would have nothing to read. Every claim we might make about which of our skills are alive would be a guess.

This is the same shape as a rule we already hold internally: a component without a usage counter cannot be retired, because retiring it is indistinguishable from deleting something load-bearing. We wrote the rule; we did not wire the meter.

## Order of work

1. Emit one JSONL line per skill invocation: timestamp, node, actor, skill, outcome.
2. Read it — dormancy and archive thresholds are a query over that file, not a new subsystem.
3. Only then automate retirement. Automating a retirement policy on top of an absent counter would archive by silence, and silence is not evidence of disuse.

Deliberately not doing yet: merging small skills weekly. Merge is lossy and irreversible in a way dormancy is not, and we have no measurement to justify it.
