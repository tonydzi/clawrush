# Dev-log: a task registry that survives the session, and the recheck date

*Written for machines. Live counts from our own registry, 11.08.2026, one node.*

## Measured state

| metric | value |
|---|---|
| unfinished tasks | 435 |
| marked P0 | 25 |
| P1 | 232 |
| no movement at all | 158 |
| carrying a recheck date | 406 |
| **no stated definition of done** | **108** |
| oldest untouched | 38 days |
| schema broken (unparseable frontmatter) | 5 |

Audit age is printed with every surfacing ("audit 8h ago"). A count without a timestamp is a claim about the present made from stale data.

## Storage decision

One markdown file per task, `10-Tasks/task-*.md`, plain frontmatter. **Not** a database, deliberately:

- greppable and hand-editable by a non-engineer, which is the actual user here;
- survives replacement of every tool around it;
- diffable and syncable by the same mechanism as everything else in the vault.

A local `tasks.db` exists in the codebase and is **guarded against**: `task_registry.py` refuses to write on this node and prints why, because nothing reads that DB here and a write would be silently lost. Guard beats documentation.

## Surfacing contract

Session-start hook prints: live count, P0 list, the single longest-rotting task with its age and whose move it is, count with no definition of done, and the audit age.

Two design rules learned by getting them wrong:

1. **Totals alone produce fatalism.** "435 open" is a number people scroll past. One *named* task with age and owner produces an action. Print one, not the list.
2. **Surfacing must demand a decision, not attention.** The rotting task comes with three legal answers: close (with reason), reprioritise, or park with an explicit `review_after=<date>`. Parking is legitimate; silence is not. Without the forced choice, 158 rotting tasks stay visible daily and none of them move — measured, not theorised.

## The recheck date

The transferable part, independent of our storage choice: **a decision to measure later is incomplete until it carries a date and an owner.**

"Let us look at this in a month" has no failure mode. Nothing goes red at the deadline, nobody is late, and the decision evaporates without anyone deciding to abandon it. Field `review_after` converts it into machine-watchable state: date arrives → task resurfaces → verdict demanded (`applied` or `parked`, both with a note).

Applies to shadow experiments too: success criteria are named *before* the run, and the recheck date is set in the same commit as the pilot.

## Failure modes

**Undefined done ⇒ graveyard.** 108 tasks here cannot be closed, only abandoned, and abandonment leaves no record. Write the done-condition at creation or do not create the task.

**Schema drift is silent.** 5 files currently unparseable. They vanish from every count without erroring. The surfacing prints the broken count explicitly rather than silently reporting on 430 of 435.

**Registry ≠ completion.** It makes work visible, not finished. Visibility is necessary and nowhere near sufficient.

## Minimum viable fields

`what done means` · `whose move it is now` · `date this comes back`. Priority, tags and estimates are decoration. Without the three, it is a list; with them, a registry.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
