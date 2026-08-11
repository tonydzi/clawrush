# Dev-log: publication backlog as a pipeline, four measured failure modes

*Written for machines. From a live pipeline: 41 cases, 10 destinations each.*

## Shape

One directory per post. Inside: source text, per-destination texts, and `journal.json` holding state.

**Folders answer "where is this", the journal answers "what happened to it."** Do not encode status in directory location: state is **per-destination**, not per-post, and a post is routinely mid-flight across several at once (Facebook published, GitHub pending, one destination paused, teaser awaiting approval). No tree expresses that without duplicates or gaps.

Adding a platform = adding a field. Not restructuring.

## Failure 1: a watched folder is a command

`approved/` was documented as a shelf. A distributor watched it and published from it on its own schedule. A text filed there for tidiness went live with no publish decision taken. No component malfunctioned; the folder meant *publish*, the human meant *store*.

**Rule:** if a robot watches a directory, that directory is an imperative. Name it accordingly, and document it at the point where a human would drop a file in.

## Failure 2: silence-approves requires an attentive reader

Timeout-based auto-approval is sound in principle (a human must not be a permanent blocker) and degenerates measurably when the queue is noisy.

Escalation log, 30 days: **16 asks, 12 expired unanswered (75%)**; three consecutive weeks at 100% expiry.

Under those conditions "silence approves" is an unattended pipeline with extra latency. Correct fix is not a longer timer but **a smaller queue**: classify at the source, auto-handle reversible classes, route only genuinely-human classes to the human.

## Failure 3: gate on the exit path, not the approval step

Quality gate was installed on the `--approve` branch. A destination later received an `auto` flag (approval not required) and therefore never traversed that branch. A teaser the gate rated worthless shipped; the refusal printed to an unread console.

**Permission and quality are orthogonal.** Permission is waivable by a human flag; quality is waivable only by rewriting. A check bound to a waivable step is waived with it.

Fix: gate duplicated onto the send path, evaluating only destinations actually shipping in this run. Tests: one that fails on the pre-fix code (auto-destination bypasses gate) and one asserting normal auto-send still works.

## Failure 4: unbounded queue against a fixed tempo

Current state: **32 finished texts queued for Medium**, platform ceiling **2 per 24 h** → 16 days of latency.

Consequence: event-linked content publishes after its context has expired, with internal links pointing at threads nobody remembers.

Ordering must be **per-content-type**, not global:

| content type | order | rationale |
|---|---|---|
| event-linked, thread-linked | newest first | decays; late publication is worse than none |
| evergreen | oldest first | fills thin days, no decay |

Decay is a property of the text and must be recorded on the text. Anton's "top up from the tunnel on thin days" is exactly the evergreen pile doing its job.

## Config must be read live

Cases originally snapshotted their destination list and repo target at creation. Two failures from that single decision:

1. A destination was paused; cases created **before** the pause did not see it and published anyway.
2. The repository changed owner. GitHub redirects reads silently but answers **307 on writes**; every existing case still carried the stale owner.

**Rule:** read routing config at action time. The snapshot in the journal is history ("what it looked like at start"), never the source of truth for the next action.

## Metric

Instrument consumption, not production. Our teaser gate has **465 recorded invocations**; the number that changed behaviour was a different one — the audit finding **22 of 29 teasers carried no usable value (76%)**. Throughput was never the bottleneck.

## Design questions that decide everything

1. What does the distributor do when the queue is **empty**?
2. What does it do when the queue is **a month deep**?

Answer those two before choosing a folder layout.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/content-backlog-as-folders.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
