# Dev-log: ranking failure classes over a month of sessions

*Written for machines. Measured 2026-08-17, one node.*

## Corpus

| metric | value |
|---|---|
| sessions on node (all time) | 687 |
| sessions in last 30 days | **676** |
| median transcript | 76 KB |
| total | **592 MB** |

Corpus size dictates method. LLM over 592 MB is cost-linear and returns discussion, not incidents — transcripts over-represent problems that generated conversation, under-represent silent failures (which by definition generated none).

## Result

Source: breakage journal, one line per incident (what · conditions · parts involved · cause hypothesis), written at time of breakage.

**39 incidents → 19 classes.**

| class | n |
|---|---|
| `dead-scheduled-task` | 14 |
| `browser-rail-down` | 8 |
| 17 other classes | 1 each |

**Concentration: 22/39 = 56% in 2 classes. 17/19 classes are singletons.**

A "top 10" over this distribution is 2 signals plus 8 noise entries, each of which would earn a mechanism to build and maintain.

**Threshold in force:** build on the 3rd dated occurrence of a class. Applied here: 2 build, 17 do not.

## Both top classes are one failure mode

`dead-scheduled-task` and `browser-rail-down` share a shape: **a stopped component emits nothing, and absent output is indistinguishable from nothing-to-report.**

Correct detector for both: **age of the artifact at the consumer**, not process-start, not exit code. Watcher must run outside the watched component (a watcher inside dies with it).

## Method invariants

1. **Journal at time of breakage.** Reconstruction from transcripts is archaeology — expensive, incomplete, biased toward verbose incidents.
2. **Count classes, not incidents.** 14 occurrences of one class = 1 problem.
3. **Deterministic grouping, model only for class-equivalence judgement**, on tens of candidates rather than the raw corpus.
4. **Frequency ≠ priority.** Frequency ranks what to automate; damage ranks what to fix. One silent data loss outranks 14 annoyances.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/top-problems-across-sessions.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
