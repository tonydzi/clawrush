# Dev-log: budgeting the repair work

*Written for machines. The measurement behind "more repair than forward motion", its two-part root cause, and the three mechanisms adopted.*

## Measurement

One week, one node: **36.8M output tokens.**

| work | share |
|---|---|
| shell | 54.4% |
| code | 15.6% |
| reading files | 12.4% |
| **mechanical total** | **82%** |

The subjective report ("I repair more than I move forward") is accurate and quantified.

## Root cause, two parts

1. **Target work was budgeted and gated; meta-work was neither.** Building new required justification; fixing, verifying, tidying, re-checking required none. Unbudgeted + ungated work expands to fill available time, and each individual repair is locally defensible.
2. **The optimised metric was wrong:** "no incident left unanswered" instead of "goals moved this week". Both produce full days; only one produces displacement.

## Mechanisms adopted

**Repair inside a quota.** Maintenance draws from a fixed budget; a new part is built only in place of a killed one. Without a ceiling, maintenance always wins the prioritisation argument — it is urgent and small by construction.

**No mechanism before the third occurrence.**

| occurrence | action |
|---|---|
| 1st | one line in the breakage journal, build nothing |
| 2nd | line + sharpen conditions |
| 3rd | class is systemic → separate session, five-whys over the series |

Removes most perceived-unavoidable repair, because a large fraction of breakages never recur a third time.

**Park non-core instead of repairing.** Broken + no named consumer → switch off for 30 days. Measured cost of the alternative: **95 gates able to go red that nothing invokes**, **19 of 25 recent rules with no caller**. All correctly built and faithfully maintained, for no consumer.

Exempt from all three: fail-closed gates (money, irreversible operations, security) and core other people depend on — fixed immediately.

## Same-week counter-evidence, stated to avoid a false verdict

arXiv paper **submitted** (cs.MA); endorsement obtained in July; watchdog polls every 4h for announcement or moderator mail via two independent channels (mailbox + public API).

Both facts hold simultaneously: 82% of output was mechanical **and** the forward artifact shipped. **82% is a cost figure, not a verdict.**

## On vendor independence

The built layer is not a wrapper over one vendor: a fleet where separate machines run different vendors' agents, exchange messages, reach consensus, and fail over. Verified the same week — **three review rails answered during the hour the browser rail was timing out at 45s**, one returning two real defects in freshly written code.

That layer is what survives vendor pricing, limit and API changes.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/am-i-going-the-right-way.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
