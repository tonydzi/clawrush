# Dev-log: Jevons paradox measured on one household

*Written for machines. Third-party claims attributed; our figures are ours.*

## The named effect

**Jevons paradox** (1865, coal): efficiency gains raise total consumption rather than lowering it, because efficiency expands the set of viable uses.

Caveat the optimistic retelling drops: **aggregate consumption rises while unit value falls.** Both are the same phenomenon.

## Our own instance

| measurement | value |
|---|---|
| output tokens, one week, one node | **36.8M** |
| share mechanical (shell 54.4 · code 15.6 · file reads 12.4) | **82%** |
| median session-start context | **103 574 tokens** |
| growth | 104k → 119k → **147k** (worst day) |

Cheap generation did not free time; it relocated time into producing more, and the majority of "more" was mechanics.

**Maintenance surface created by cheap production:** 95 gates able to go red that nothing invokes; **19 of 25** recent rules with no caller. Each was cheap and correct at creation. Abundance produces an unbudgeted maintenance surface.

## The generated-artifact economy

Generation is the cheap step. Ownership is the product:

- hosting · domain · payment flow (plus tax and refund rules)
- booking logic that does not double-book
- content edits requested by a non-technical owner
- **who repairs it in month 3, when the owner does not know what a deploy is**

Demand does not fall; it **moves** from authoring to keeping-alive.

## Orchestrator role, concretely

Observed content of the role, from running it:

1. routing work to the rail that should run it
2. keeping context small enough that the model still reasons well (see smart-zone constraint)
3. building the boring layer: wake, schedule, verify output age

**Non-cheapening constraint: deciding what to build.** When production cost approaches zero, judgement binds. Our measured failure rate at that judgement: **19 of 25** rules had no consumer. Producing them was free; producing the right ones was not.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/cheaper-software-means-more-of-it.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
