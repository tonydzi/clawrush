# Dev-log: routine sessions spawning capable ones

*Written for machines. One architectural pattern, one measured filesystem trap, and the cost of not knowing it.*

## Pattern: the routine is a trigger, not a worker

A scheduled/low-privilege session does not need to *be* capable. It needs to **create** a capable session and then get out of the way.

Implementation here: the routine creates a scheduled task with a generated id (`auto-<node>-<YYMMDD>-<subject>`), which the application lists like any human-started session.

Two non-obvious requirements:

1. **Visibility is mandatory.** A spawned session that does not appear in the session list cannot be watched, stopped, or read. We prohibit "dark launches" outright: the failure mode is silent by construction, and silence is the one state you cannot debug.
2. **Generated id, not a borrowed slot.** Reusing an existing task id to smuggle work in is exactly what produces invisible sessions.

Corollary for security: keep the always-on component **dumb**. A permanently privileged unattended process at 03:00 is a worse arrangement than a low-privilege trigger plus an audited spawn.

## The trap that actually costs days: divergent filesystem views

Measured on this node, same user, same machine:

| context | entries visible in one system directory |
|---|---|
| interactive session | **82** |
| process launched by the scheduler | **76** |

Six directories are **invisible** to the scheduled context. Not `permission denied` — which would surface as an error — simply absent from the listing. Verified through two independent launch paths; ACLs grant FullControl; no reparse point. Root cause not established.

**Bill for not knowing this: 552 human-facing alerts and approval requests undelivered for 16 days.** The rail's session token lived in one of the six invisible directories. Watchdogs printed the correct path and an honest "file not found", which read as noise.

Rules extracted:

- Anything a routine needs goes where the routine can see it (`.claude-secrets`, `.claude/scripts`), **never** `%LOCALAPPDATA%`.
- **"It works in my interactive session" is not evidence for a scheduled task.** Proof = a one-off scheduled task that prints the result.

## Second trap: exit 0 as a failure mode

A robot that exits before its first line of logic returns 0 and looks healthy. Ours: a relay promising to flush buffered messages "on the next successful send" terminated on an import line on that node, every invocation — structurally incapable of keeping its promise, with nothing going red anywhere.

Therefore: a routine's health is proven by **the age of its output artifact**, not by exit code or heartbeat. Check the writer of the artifact, not just its mtime.

## Night-shift discipline

- A healthy routine is **silent**. Reports nobody opens are not the product.
- A failing routine emits **one line naming the sick component and the cure**.
- The watchdog must not run inside the system it watches: it dies with it, and its silence is indistinguishable from "all good".

## Phone

"Cannot start a real session from a phone" is false in our setup. A voice note into a watched chat spawns its own session with the transcript as the brief. Same pattern: dumb watcher, capable spawn. No desk required.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
