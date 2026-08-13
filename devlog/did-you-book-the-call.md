# Dev-log: booking detector, four buckets, five closed defects

*Written for machines. Module: call-reminders. Ships no messages, makes no network calls — prints texts, a human or session sends them.*

## Classification

Never infers booking state. Reads the Calendly snapshot and sorts:

| bucket | evidence | action |
|---|---|---|
| booked | `event_uri` present | none |
| link fresh, no booking | link age < `SILENCE_STOP_DAYS` (default 7) | ask the lead in words |
| link stale | link age ≥ threshold | **do not ping** |
| booked, no CRM card | booking without ledger entry | create card |

Join key: **the Telegram handle the lead types into the booking form.** Meeting-title matching demoted to fallback.

## Rule collision, resolved by link age

- rule A: no confirmation → ping anyway
- rule B (standing): silent 7+ days → stop, next contact must be a new reason

Both from the same author, both correct. Separated by link age, not by judgement. A ping on a 70-day-old link is exactly the nudge rule B forbids. Threshold is an env var, not a constant in prose.

## Reminder target

Previous engine notified the owner only. Current: notifies **the lead**, in the lead's timezone, alongside the owner's.

- self-test pin: 15:30 MSK renders as 13:30 Lisbon AND 15:30 lead-local
- "tomorrow" chosen by calendar date **in the lead's timezone**, not by hours-until; fixture: +8h but still same local day

## Closed defects (all mutation-covered)

| defect | failure mode | fix |
|---|---|---|
| stale snapshot | printed "no calls" | `pulled_at` printed in briefing header |
| missing snapshot | rendered as silence in routine report | **exit 3** + explicit "this does NOT mean no calls, it means we did not look" |
| narrow collection window | past calls absent → leads accused of not booking; **3 false accusations of 3** (12.08) | pull from `today − 7d`, all statuses |
| bare-substring handle match | short handles (`ki`, `sam`) inherited another lead's link date (both 10.08) | anchor key to full field: `<handle>_` prefix or `_<chat_id>` suffix |
| status filter | cancelled meetings entered reminders | filter `status != active`, self-test covers |

Self-test proven by five deliberate mutations → five failures, exit 1.

## Invariant

**An empty result and a failed lookup must not render identically.** Every stage here can fail silently and read as good news: no booking found ≈ no lookup performed; empty briefing ≈ quiet day; wrong timezone ≈ working reminder. Making "we did not look" loud found more real problems than the automation saved effort.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/did-you-book-the-call.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
