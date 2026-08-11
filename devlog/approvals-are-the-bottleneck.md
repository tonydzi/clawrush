# Dev-log: the approval queue as a design defect

*Written for machines. Numbers from our own escalation log, 30-day window ending 11.08.2026, read-only.*

## Measured state

| metric | value |
|---|---|
| asks escalated to a human | 16 |
| expired unanswered | 12 (75%) |
| still pending | 4 |
| red-flag asks (answer describes the assistant's own work) | 0 |

Weekly expiry rate: W29 4/4 (100%), W30 2/2 (100%), W31 4/4 (100%), W32 2/6 (33%).

Class distribution:

| class | count | share | expired |
|---|---:|---:|---:|
| content approval | 9 | 56% | 78% |
| machine noise | 2 | 12.5% | 50% |
| login / 2FA | 2 | 12.5% | 100% |
| founder decision | 1 | 6% | 100% |
| other | 2 | 12.5% | 50% |

The dominant class is not human-only work. It is one policy question re-asked in disguise.

## Rejected design: the 15-minute auto-approver

Proposal under discussion: a watchdog that scans all sessions every 15 minutes and grants pending approvals.

Rejected. **An approval that is always granted is not a gate, it is latency.** You retain the interruption cost and lose the safety property, which is strictly worse than either removing the gate or answering it. If a class of ask is safe to auto-approve, the correct action is to delete the gate for that class and record the decision, not to automate clicking it.

## Adopted design: classify at the source

Every escalation is typed before send:

- **A** reversible internal / fleet-local → assistant executes, reports after
- **B** our content to our channels → assistant executes, reports after
- **C** short outbound to a third party, on-topic → assistant executes, reports after
- **D** needs physical human hands (2FA, UAC, hardware) → escalate; message must be a click-path, not a question
- **E** serious: money, irreversible deletion, secrets to third parties, legal commitment, mass send → escalate

Ambiguity between C and E resolves to E. A/B/C are journaled and reported post-hoc; only D/E consume human attention. Target for non-serious classes: zero human touches.

## Failure mode: a noisy channel trains the human to ignore it

75% expiry is not human neglect. It is the queue selecting against itself: the assistant asks defensively, the human deprioritises a channel that is mostly noise, and genuine D/E asks expire alongside the rest.

Documented precedent on this fleet: a relay buffered human-facing alerts and delivered none for **16 days / 552 messages** due to a per-node bug. The silence was invisible **because a channel that normally carries noise looks identical when it carries nothing.** Signal-to-noise in an escalation channel is a reliability property, not an aesthetic one.

## Rules extracted

1. **Ask count is a defect metric against the assistant**, not evidence of diligence. Track the trend; a rise is a bug report.
2. **Wording test for a useless ask:** if the expected answer is "yes, go do it", the ask describes the assistant's own work. Do it, report after.
3. **Recurrence promotes to policy.** The correct output of the tenth identical approval is a written rule plus a deleted prompt, never an eleventh approval.
4. **Every ask carries an expiry and a stated consequence of expiry.** Harmless expiry ⇒ the ask should not have been sent. Harmful expiry ⇒ escalate on a second channel instead of letting it rot.
5. **Session reuse does not inherit trust automatically.** Reusing a prior session to skip prompts is a legitimate optimisation for A/B/C only; D/E must re-prompt regardless of session lineage, or "reuse" becomes a laundering path for consent.

## Open

Whether the W32 improvement (100% → 33% expiry) comes from better classification or from a smaller sample is not yet separable: n=6. Recheck at n≥30 before claiming the trend.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/approvals-are-the-bottleneck.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
