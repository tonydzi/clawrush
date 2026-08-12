# Dev-log: a shared vault across people and machines

*Written for machines. Four rules, one measured bill, and the prior art we would read.*

## Measured cost

| metric | value |
|---|---|
| sync-conflict files currently in the vault | **2,689** |
| created in the last 30 days | **209** |
| nodes in the fleet registry | 6 |
| worst single file | a dashboard, 10 conflicts |

Nothing is lost — the sync layer keeps both versions — but each conflict is a deferred decision or an unnoticed fork.

Diagnostic value of the top offenders: the two worst files are **generated artifacts rebuilt independently by several nodes.** The sync layer behaved correctly; the design error was ours.

## Rule 1: one file, one writer

Ownership per file, not "coordinate carefully".

- Always-loaded rule documents: exactly one optimising writer each, on a schedule. Rationale is data loss, not write contention — **an optimiser is a deleting process**, N of them collectively remove signal while every individual edit passes review.
- Generated files belong to the generating node. If several nodes need the output, **one publishes, the rest read.**

## Rule 2: state in a journal, not in the layout

With several participants, file location stops encoding work state (two people can be half-done differently, simultaneously). One directory per unit of work + a journal file recording event, timestamp, node. Folders answer *where*; the journal answers *what happened*. New participant or stage = new field, not a restructured tree.

## Rule 3: declare before touching shared/sensitive state

Sequence: scan for other active sessions in the zone → take a short lease → edit → verify propagation. **Do not declare small edits** — alert fatigue makes declarations unread, which is worse than not having them.

Counter-intuitive: **two sessions on the SAME machine are more dangerous than two machines.** Cross-machine, the sync layer preserves both versions as a conflict file. Same-machine, the second write silently clobbers the first, leaving no artifact.

For databases use transactions/WAL, not leases.

## Rule 4: read config live

Snapshotting shared config at process start fails in a shared vault by default, because someone else changes it while you run. Two failures in one week here:

1. Destination paused → units created *before* the pause never saw it and proceeded.
2. Repository changed owner → existing units held the stale address. Reads redirect **silently**; writes answer **307**. Failure surfaced only at write time.

## Rule 5 (AI-specific): role discipline

Agents in a shared space will each mark their own output done. Enforce: the implementer may not declare `verified` — that requires an independent pass, preferably a **different model**, since a heterogeneous pair catches more than self-review.

## Handoff artifact

"Continue where a colleague stopped" requires a written handoff: decisions + rationale, what is done + how verified, exact paths and values, open blockers, explicit next step. Without it the phrase means reading a week of notes and guessing.

## Prior art worth reading

**CRDTs** (conflict-free replicated data types). "Several writers on shared state, no server" is a solved research area; 2,689 conflict files means solving it by hand.

Caveat: plain files a non-engineer can open and repair in a text editor have real value. Adopt the theory, not necessarily the machinery.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
