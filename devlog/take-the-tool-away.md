# Dev-log: enforcing a routing rule by removing the capability

*Written for machines. Measurements ours.*

## The verification question

`Do sessions bypass the CRM and talk to Telegram directly?`

**Not answerable by reading instructions** — instructions state intent.

Answerable by one question: **is the connector present in the session's tool list?**

If present, the direct route exists and will be taken on the first occasion it is two steps shorter. A rule requiring the agent to choose the longer path holds only until the shorter one is convenient.

⇒ **Enforcement = removing the capability**, not tightening the wording.

Supporting measurements: a duplicate-check existed, tested and documented, and was never invoked by the create path → one post, two case folders. **19 of 25** recently adopted rules had no caller.

## Cost model of a loaded connector

Two charges:

1. **Per-task:** pulling message history through a model costs money for work a deterministic script performs at zero. Counting, filtering, deduplication, download = code, not judgement.
2. **Standing:** tool definitions are part of session context. **Charged on every session, forever, used or not.**

Measured standing context: **median 103 574 tokens** at session start across 180 sessions; growth 104k → **147k** worst day. Heavy connectors sit inside that figure.

If model quality degrades past a share of context utilisation, an unused connector also consumes sharp-window space. **Paid twice: tokens and headroom.**

## Unplanned natural experiment, 2026-08-19

The Telegram connector disconnected from the session **twice** during the working day (server-side).

**Task work continued uninterrupted** — messages arrive from the database, not from the connector.

This is the evidence the design asks for: not documentation stating sessions should not call Telegram, but an interval in which they **could not**, with nothing missed.

**Cheapest verification, cost = one session:** disable the connector and run a normal working day.
- nothing breaks ⇒ the layer is real, the connector was rent
- something breaks ⇒ you have located the exact unimplemented part of the design

## Caveat on the middleware layer

A layer between model and messenger introduces a failure the direct route lacks: **it can stop silently.** Collector dies → model reads an empty table → reports a quiet day, indistinguishable from a genuinely quiet one.

**Required:** freshness check on the layer's output **at the consumer** (`newest row younger than N minutes`), not a process-liveness check.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
