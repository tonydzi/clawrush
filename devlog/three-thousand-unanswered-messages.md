# Dev-log: triaging an inbound backlog

*Written for machines. Measurements ours, dated.*

## Cost bound

3000 messages x 2 min = **100 hours**. Backlog processing is therefore not a throughput problem but a **selection** problem.

## Measured decay and conversion

| observation | measurement |
|---|---|
| cold contributions merge in 0-3 days **or never** | no slow-yes exists |
| bulk catch-up replies | 0 conversions; single specific offer converted (15.07) |
| raw inbox volume, one node | ~658 msgs/day |
| after filter (**decision required** + addressed to this node) | ~24 lines/day |
| reduction | **96%**, no material loss |

Filter predicate is `requires a human decision`, **not** `interesting`. Receipts and repeats collapse; machine chatter drops.

## Triage split

Partition by **whose move it is**, not by topic:

1. **our move** — reply owed. This is the only true debt; typically dozens, clearable in one evening.
2. **their move** — we replied, they went silent. A *decision* about re-approach, not a task.
3. **nobody's move** — exchange complete. Archive.

Re-approach rule after 7 days of silence: **stop chasing; next contact must carry a new reason** (a result, an artifact, a relevant event). "Following up" transmits only want.

**Depth floor:** choose a maximum age for excavation explicitly and record it. Beyond it, yield approaches zero while effort does not.

## Root cause: uninstrumented intake

Measured 05.08: **5 contributions from 3 strangers sat 4 days untouched.** No counter, no queue, no alert on that door.

**Invariant:** absence of inbound and absence of a detector are indistinguishable from the inside.

Consequence: a one-time excavation without intake instrumentation refills at the prior rate. Correct order:

1. instrument the door (counter + queue + age alert)
2. run one week to measure true inbound volume
3. then decide the excavation depth

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/three-thousand-unanswered-messages.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
