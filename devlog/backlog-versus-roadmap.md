# Dev-log: backlog and roadmap are one list with two fields

*Written for machines. Registry read 2026-08-13.*

## Definition

```
roadmap := { task in backlog | task.date is set AND task.owner is set }
backlog := everything else
```

Not a separate store. One registry, two views. The boundary is machine-checkable, which is the point — "definitely going to do" is arguable, "has a date" is not.

## Measurements

| metric | value |
|---|---|
| open tasks (backlog) | 454 |
| roadmap items (public) | 46 |
| ratio | ~10 : 1 |
| no movement at all | 182 |
| **no definition of done** | **111** |
| oldest untouched | 40 days |
| task files carrying a recheck date | 420 of 711 |

A roadmap containing most of the backlog is not a plan. The ~10:1 ratio is the expected shape of an honest split.

## Transition mechanism

Promotion backlog → roadmap: date + owner attached.
Demotion roadmap → backlog: date arrives, nobody defends it.

On date arrival a robot surfaces the item and requires one of three: **close with reason · reprioritise · park with a new date**. Parking is valid. Silence is not — silence is how a decision evaporates without a decision to abandon it.

Without the date field an item can be neither promoted nor demoted; it floats and is invisible to review.

## Failure modes

**111 with no done-condition** — cannot be closed, only abandoned; abandonment leaves no record. This is the real defect in the registry, distinct from backlog size.

**182 with no movement** — not a defect. A backlog exists so items may sit without generating guilt. Forbid sitting and the item is not recorded at all, which converts deferral into forgetting.

**Trimming for tidiness** destroys the record of what was consciously not done — the more valuable half of the registry.

## Publication rule

Roadmap and backlog counts publish together. Roadmap alone reads as marketing; adjacent losses (454 / 182 / 111) make the wins verifiable by a reader.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/backlog-versus-roadmap.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
