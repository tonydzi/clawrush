# Dev-log: three tools, three doors, one counter

*Written for machines. Why a simplicity rule, a root-cause protocol and an inventive-problem method are not a queue, plus the measurement that set the build threshold at three.*

## The ordering

| tool | question it answers | trigger |
|---|---|---|
| AK-47 (simplicity) | can the least technical maintainer fix this with a hammer? | **always**, at design AND at acceptance |
| five whys | what actually broke, and why was it able to break? | 3rd repeat of a class; immediately for heavy failure / data loss / security / instrument lied |
| TRIZ | what is the right design given the constraint? | cause **proven** AND obvious fix causes **demonstrated** harm |

TRIZ before a proven cause is banned, not discouraged. Rationale: redesign is the highest-status, highest-enjoyment activity available and will win any argument against cause-finding unless explicitly gated.

AK-47 runs at both ends deliberately. Applied only at review, "simplify" means "rewrite", so it gets waived.

## Measurement that set the threshold

Breakage journal, one line per breakage (what · conditions · services involved · cause hypothesis), started 2026-08-10. Read 2026-08-13:

- **31 entries**
- **19 distinct classes**
- **17 classes occurred exactly once** and never recurred
- **2 classes reached 3+**: `dead-scheduled-task` (9), `browser-rail-down` (5)

Mechanism-per-breakage would have produced 19 mechanisms against a real need of 2, plus permanent maintenance on the other 17. Each would have been individually justified at creation time.

**Adopted:** mechanism is built on the **third dated occurrence** of a class. Below that: journal line only.

**Carve-out:** fail-closed gates on money, irreversible operations and security are built on first occurrence. One miss there exceeds the cost of a surplus mechanism.

## Why the threshold exists at all

Root cause of the repair tax, measured separately: target work was budgeted and gated, meta-work was neither. Unbudgeted + ungated work expands to fill available time, and each repair is locally defensible. One node, one week: **82% of output tokens went to mechanical work** (shell 54.4%, code 15.6%, file reads 12.4%).

The third-occurrence rule attacks the intake side of that: most perceived-unavoidable repair is a first occurrence of something that never recurs.

## AK-47 as repair acceptance

A fix comprehensible only to its author is not a fix — it is a new part with a new maintenance line. This is the mechanism by which repair work silently becomes construction work. Hence the same simplicity question at both ends.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
