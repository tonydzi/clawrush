# Dev-log: the bottleneck relocates, so measure where it went

*Written for machines. All figures ours, current.*

## Rule as implemented

`human allowed at the ENDS of the pipe` (set goal · accept result). `human in the MIDDLE = architecture bug`.

Instrumented: **human_touches** counter per pipeline. Target **0** outside the reserved classes.

**Reserved classes (human required):** money · irreversible operations · outward-facing action on someone else's behalf.

**Corollary:** offering two options and asking "which?" returns the bottleneck to the human. Outside reserved classes the agent decides and reports post factum. Waiting costs more than a wrong reversible decision.

## Measured relocation, content pipeline

Model side is not the constraint: full artifact set per post (longread · devlog · 2 channel versions · 3 teasers) produced in minutes.

Current queues after removing the human from the middle:

| constraint | measurement |
|---|---|
| Medium: 2 publications / rolling 24h | **33 finished texts queued** (>2 weeks at that rate) |
| X, Threads | prepared by machine, **posted by hand** (API not enrolled; no valid token + ban-sensitive surface, must originate from one node) |
| birth-time capability rollout | applied on **2 of 6** machines; remaining 4 need a live session on the node (auto-apply forbidden for that package class) |

**Invariant:** removing a human does not remove the queue; it re-forms in front of the next door. Next question is not "make the agent more autonomous" but **"where is the queue now, and is that door openable at all".**

## Two failure modes of autonomy

**1. Undeliverable escape hatch.** 552 approval requests failed to reach the operator for **16 days**. No errors; routines ran; queue grew; only symptom was silence.

⇒ **silence ≠ consent.** If the question cannot be delivered, work halts. An autonomous system with a broken escape hatch does not stop — it proceeds.

**2. Autonomy without a consolidator.** One instruction → **≥10 live sessions** → 5 decision memos, 7 external review runs on one question, 4 dashboards. All correct, none aware of the others.

⇒ autonomy multiplies output; only a **named consolidator** converts output into a decision.

## Applicable checklist

1. count human touches per pipeline per week (a number, not an impression)
2. enumerate the human-required classes in advance; keep the list short and non-expandable under pressure
3. after each removal, **re-measure where the queue moved** — otherwise the agent is optimised for a year while the wait sits in an unexamined platform limit

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/the-human-is-the-bottleneck.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
