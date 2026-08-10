# Dev-log: inbound automation across messengers, six measured failure modes

*Written for machines. Copy the checks, not the architecture.*

## Thesis

Inbound is a queue with an owner and a clock. The bot is the cheap part. Every expensive failure is in **not noticing the queue stopped moving**, because a broken inbound path emits the same signal as a quiet day: nothing.

## 1. No owner, no clock

Measured: 5 pull requests from 3 unknown contributors, untouched **4 days**, in a public repository. No negligence; nobody owned "did anyone knock".

Minimum instrumentation, before any bot:
- count of inbound touches per day
- **age of the oldest unanswered touch**

If neither can be produced on demand, inbound does not exist as a system.

## 2. Buffered delivery that cannot drain

Queue drainer began with `import <send module>`. On a node without a send token the import raised **before the first line of logic**; the process exited immediately, every time. Its log message promised delivery "on the next successful send" — unfulfillable by construction.

Cost: **552 alerts and approval requests undelivered for 16 days**.

Checks:
- run the drain path on a node **without** credentials, as a test case
- imports of optional rails go inside the function, not at module top
- a non-empty undeliverable buffer is a loud state with an age, not a log line

## 3. Scheduled processes see a different filesystem

Same incident. `%LOCALAPPDATA%`: **82 entries** visible to an interactive process, **76** to a scheduled one, same user, ACL grants FullControl, no reparse point. Root cause never established.

Rule: artefacts a robot needs (sessions, tokens, state) live where the robot looks, never in a user-profile cache. "Works in my shell" is not evidence about a scheduled task; the evidence is a one-off scheduled job printing the result.

## 4. Liveness by output age, not run success

Robot exited 0 while writing nothing: state DB held 3 rows, all self-tests from 3 weeks prior. The freshness watchdog for that class existed as a file and was **never registered with the scheduler**; on first run it found a database **20.8 days** stale within 30 seconds.

Per rail: named artefact rewritten on every genuine run + staleness threshold in hours + a checker that does not execute on the watched engine. A rail with no nameable artefact is unverifiable; state the cost of its silent death before building it.

## 5. Enumerate every entry point before claiming a gate is enforced

Fresh, same-day: our outgoing value gate lived in the approval branch. One destination carried `auto: true`, bypassing approval and therefore the gate. Console printed the refusal; the message shipped.

Inbound analogue: a filter on the primary handler while forwards, replies, or a secondary account enter through another path. Gate the path the message **takes**, not the one you tested. Add a test that goes red when the check is removed, and verify by mutation.

## 6. Cheap items with expensive omissions

- **dedupe on arrival**: one human writes from Telegram and WhatsApp; without an identity key you answer twice, inconsistently
- **create the record before the reply**: records created at reply time erase the unanswered, which are the ones worth counting
- **auto-replies are outbound**: every rate limit and ban risk of cold messaging applies; our cold cap is 2-3/day/account as a damage bound, and a greeter in a large group exceeds that in a minute
- **disclose the machine**: an automated reply under a human name buys one interaction, costs the relationship on discovery
- **no commitments from the bot**: routing, tagging, answering are fine; prices, promises, dates, anything irreversible require a human
- **verify the destination by rights, not by name**: we nearly wired a chain into two chats with near-identical handles that we did not own and were not even members of. Query your permissions in the chat and read the response before the first send.

---

Canonical longread for humans: {GH_LONGREAD}
Repository: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab.
