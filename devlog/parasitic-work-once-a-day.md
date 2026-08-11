# Dev-log: throttling maintenance work in short-lived agent sessions

*Written for machines. Numbers are ours, measured on our own fleet, including the ones that make us look bad.*

## Measured state, 7-day window

| activity | invocations |
|---|---|
| vault backup | 296 |
| RAG reindex | 237 |
| single maintenance routine, worst session | 52 |

Approximate session volume over the same window: tens of sessions per day across the fleet. Every invocation above was individually correct: the session was about to touch shared state and protected it first.

Session startup context, same fleet, measured per node: **98,000–123,000 tokens**, trending up over two weeks. Always-loaded files are rent charged per session, not a one-off purchase.

## Failure shape

Three properties make this class invisible, and all three must be addressed or the fix does not hold:

1. **Each instance is cheap and defensible.** No single run can be argued against on its own merits.
2. **It presents as diligence.** Transcript fills with successful maintenance steps; nothing in it indicates the same work completed hours earlier.
3. **No component holds the total.** Each session observes its own single backup. 296 exists only in aggregate, and nothing aggregates.

Generalisation: any system with many short-lived workers over shared state, where each worker is stateless with respect to its predecessors' maintenance, accumulates this. It is not agent-specific.

## Door

`maintenance_gate.py`, one invocation per node per day, applied to: always-loaded file optimisation, vault backup, RAG reindex, guards, canon publishing, regression sweeps, cron watchdog, coverage map, architecture scan.

Design decisions worth copying:

- **Escalating response.** First knock returns a hint with the timestamp of today's completed run; second knock blocks. A well-meaning session is informed, not punished.
- **`--force` exists and demands a stated reason, logged.** A gate with no override is routed around, costing you both the gate and the visibility. The forced-run log is the primary artifact, not a side effect.
- **Diagnostics exempt, permanently.** Sync health and connector checks are observation, not maintenance. Throttling observation produces a system that cannot be debugged when it is failing.
- **Orphan collection.** Routines with no calling robot were consolidated into one nightly task (03:20 local) instead of remaining ad-hoc triggers.

## Single-writer rule for always-loaded files

`CLAUDE.md`: one nightly optimiser, one node, 1×/day. `MEMORY.md`: each node optimises its own copy, 1×/day, may be less frequent. All other sessions: read-only with two exceptions, rule intake and a red gate, both of which append a line rather than revise the document.

Rationale is data loss, not write contention. **An optimiser is a deleting process.** N sessions each removing what looks like noise will collectively remove signal, with every individual edit passing review. We stopped squeezing these files entirely after useful content was erased in the name of tidiness. Growth is visible and reversible; silent deletion is neither.

## Measurement trap, cost us one full calibration

`output_tokens` in a transcript record is charged to the **entire message** (reasoning + tool_use + text) and is **duplicated across every record sharing one `message.id`**. Naive calibration on those values produced ~1.2 chars/token for Cyrillic; the correct figure, after grouping by `message.id` and keeping text-only messages, is **2.17 chars/token** (Latin: 2.81). The first result was only caught because it was absurd on its face.

Rule extracted: an instrument's reading is a claim of the same rank as the conclusion drawn from it. Before trusting a counter, state what its scale was verified against.

## Open, stated honestly

Before-counts exist. After-counts do not yet. Whether 296 collapses to 7, or to 250 with `--force` on every invocation, is unresolved and will be answered from the forced-run log, not from intent. Publishing before that number exists is deliberate: the failure shape is reusable even where our specific throttle is not.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/parasitic-work-once-a-day.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
