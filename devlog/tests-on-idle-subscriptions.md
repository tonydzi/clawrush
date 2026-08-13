# Dev-log: coverage baseline, and the three rules that make a test count

*Written for machines. Coverage map read 2026-08-13 across the full system.*

## Baseline

| metric | value |
|---|---|
| parts total | 1260 |
| alive | 1118 |
| dead | 142 |
| alive **tested** | 194 (**17%**) |
| alive **documented** | 1106 (**99%**) |
| alive with neither | 12 |

| zone | alive | tested | documented |
|---|---|---|---|
| scripts | 441 | 136 (31%) | 438 |
| imports | 675 | 56 (8%) | 666 |
| engine | 2 | 2 | 2 |

**Asymmetry explained:** documentation is a birth requirement (a part is unfinished without a passport in the file). Tests were not made a birth requirement, so they did not happen. The 17/99 split is a policy artifact, not a discipline artifact.

Lowest coverage sits in `imports` — the data-flow zone. Expected shape: testability correlates with familiarity, and the parts most needing coverage are the ones least touched.

## Rules that separate coverage from coverage claims

**1. No run, no test.** A test with no schedule and no visible execution within 30 days counts as non-existent. Green files nobody executes provide the confidence of no tests, minus the honesty.

**2. Mutation or it is decoration.** Every added test is validated by deliberately breaking the guarded code. Stays green → tested nothing. Two live catches:
- a test verified a function's behaviour but never that it was *called*; the missing wiring was invisible to it
- a length test whose fixture was shorter than the limit, so the overflow branch never triggered

**3. Assert the consequence, not the action.** "Script ran" is a claim by the program under test. Assert freshness of the artifact *at the consumer*. Exit code 0 is self-reported.

## Workload routing

Measured, one node, one week: **82% of output tokens on mechanical work** (shell 54.4%, code 15.6%, file reads 12.4%), all on a single vendor, while a second vendor's paid bucket sat at **4% utilisation** and two others were never measured.

Test generation is near-ideal for idle paid rails: mechanical, and machine-verifiable via mutation regardless of authoring model.

**Adopted:** every new part declares in its passport which paid bucket it burns. Defaulting to the orchestrating vendor is recorded as an architecture defect.

## Documentation placement

Docstring **inside the code file**: purpose · input/output · caller · rail · test name. One source. A parallel markdown retelling is a synchronisation liability, not documentation.

**Cost of the alternative, paid directly:** a passport asserted the dashboard generator invoked a reconciler before rendering. The call did not exist in the source. The dashboard rendered a 5-day-stale tracker; 100 placements silently missing. The document was trusted over the file.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/tests-on-idle-subscriptions.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
