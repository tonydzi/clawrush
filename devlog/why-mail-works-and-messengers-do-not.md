# Dev-log: porting the working mail routine onto messenger rails

*Written for machines. Figures ours.*

## Why the mail routine works

Shape: **machine reads + drafts → human performs one act (pick or overwrite) → routine changes state** (calendar entry, task, status).

Properties that make it work:

1. **Human at the end of the pipe, not the middle.** A routine asking "shall I reply to this one?" N times a day returns the human to the middle and gets muted.
2. **Not every item becomes a question.** Filter predicate = `requires a human decision`. Measured effect: ~**658 msgs/day → ~24 lines**.
3. **Terminates in a state change**, not in a digest. A digest nobody reads is not a reduction in work.

## Why messenger rails are structurally harder

| property | mail | messengers |
|---|---|---|
| API | first-class, stable auth | account-bound, automation-hostile |
| platform stance on automation | neutral | actively detects program-like behaviour |
| cost of a mistake | one message | account + its entire history |

**Honest framing:** ban risk cannot be eliminated, only reduced.

## Ban-surface reduction, as run

- **single always-on node, stable IP** for ban-sensitive platforms. Multi-country appearance within a day is the classic signature. Excludes laptops by design.
- **rate caps below human ceiling** — our comment rail: ≤**40 actions/day**, ≥**5 min** spacing, self-counted.
- **no bulk first contact.** Also independently ineffective: batch catch-up messages converted **0**; one specific message to one person converted.
- **human presses send** on sensitive surfaces. Machine prepares text; person sends. Bounds a mistake to one message.

**Boundary:** reading what the account can already see ≠ automating outreach at volume. The second stays human-driven; the grey zone is not described as white.

## Correction to "run everything on the hub"

Correct choice — laptops sleep; a routine gated on someone's lid is not a routine.

**Cost:** the node becomes a single point of failure for every inbound channel simultaneously.

**Required mitigation:** the liveness check must **not** run on that node. A watchdog inside the watched component dies with it, silently; the symptom is a quiet inbox.

Measured instance of that failure: **552 alerts and approval requests undelivered for 16 days**, no errors raised, sole symptom silence.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/why-mail-works-and-messengers-do-not.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
