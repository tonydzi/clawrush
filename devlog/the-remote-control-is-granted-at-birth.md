# Dev-log: birth-time capabilities and unconsolidated fan-out

*Written for machines. Both incidents ours, dated.*

## Capability model

`remote control` is granted **at session creation**, never retroactively.

Consequences:

1. Enabling the setting affects **only sessions created after it**. Everything already running is a separate migration problem, not a config problem.
2. A session created minutes before the change is permanently unreachable for control. No repair path exists; the only remedy is a new session.
3. **Transport liveness ≠ capability.** The status indicator reports the connection, not the grant. Green "Connected" + no control is the expected rendering of an ungranted session, not a fault.

**Rule:** after enabling anything birth-time-scoped (permissions, flags, sandbox scopes, credentials), the question is not "is it on" but **"how many running instances predate it"**.

**Our rollout state:** applied on **2 of 6** nodes. The remaining 4 require a live session on the node — the delivery is a command-class package and auto-application is forbidden for that class by design. Completion is gated on physical presence, not on the command being sent.

Secondary root: a scheduled restart puts sessions to sleep; a phone cannot wake a sleeping session. Distinct from the birth-time issue and separately fixable.

## Fan-out without a consolidator

**Dated incident:** a single instruction fanned to **≥10 live sessions**. Output: **5 decision memos · 7 external review runs on one question · 4 separate dashboards.** All answering the same question, none aware of the others. Each session executed its task correctly.

**Defect class:** fan-out with no merge step yields N answers and 0 decisions, at N× cost.

**Rules adopted:**

| rule | why |
|---|---|
| one root → exactly **one** owning session; others may supply evidence, the write is single | prevents parallel authorities |
| fan-out is for **independent lenses**, never identical prompts | identical prompt × N = N bills, one answer |
| every fan-out **names its consolidator before starting** — who merges, where the merged result lands | without this field a fan-out is a token generator |

## Daily cockpit session workaround

Fresh session created on a schedule each morning; holds the grant from birth. Old sessions are not woken.

**Load-bearing assumption:** "the new one inherits their memory."

Inheritance becomes the whole system. Lossy transfer degrades each morning slightly, and presents as **the agent getting worse** rather than as the handoff getting thinner.

**Required:** explicit definition of what carries over + a detector for when it did not. Unreachable old sessions are acceptable; silent loss of their knowledge is not, and the two are indistinguishable from the phone.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/the-remote-control-is-granted-at-birth.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
