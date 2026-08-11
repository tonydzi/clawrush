# Dev-log: gating inventive design behind a proven cause

*Written for machines. Three tools, three doors, and the measured failure each door prevents.*

## The conflict, stated precisely

TRIZ generates clever solutions. The AK-47 rule (repairable by the weakest hand, hammer and screwdriver, no engineer) removes cleverness. Applied without a boundary they oscillate: invent, simplify, invent again.

Resolution adopted 09.08.2026: **not a priority order — three tools answering three different questions.**

| tool | question | fires when |
|---|---|---|
| AK-47 | is this repairable? | **always**, at both ends: before building (simplify the *design*) and at acceptance |
| five whys | what is the actual cause? | 3rd recurrence of a class; immediately for data loss, security, or a lying instrument |
| TRIZ | what design resolves it? | **only** when cause is proven **AND** the obvious fix produces demonstrable harm |

TRIZ is **gated by** AK-47, not competing with it: cleverness is permitted after simple has been tried and failed for a stated reason, and its output still passes the repairability test on the way in.

## Failure the gate prevents

**Design on an unproven diagnosis is indistinguishable from progress.** It produces artifacts (diagrams, a clearly-better architecture), consumes a day, and nothing in the process signals that the diagnosis was wrong.

Worked example, 11.08.2026. Symptom: dashboard "saves but does not update", 5 days stale. Tempting redesign: better synchronisation. Actual cause via five whys: the generator contained no call to the reconciler while its passport documented that call. Fix: 2 lines. Any architecture proposed pre-diagnosis would have been elegant and irrelevant.

## Two TRIZ concepts that already match empirically-derived rules

Stated as hypothesis — the deep research has not run. Convergence is evidence the research is worth doing, not evidence TRIZ is correct.

**Ideal final result** (function occurs, mechanism absent) ≈ our rule that a check belongs where the artifact already passes, not as an additional watchdog. Cost of violating it, measured: **95 gates capable of going red that nothing invokes**; **19 of 25 recent rules with no caller**.

**Contradiction resolution instead of trade-off** ≈ our permission-vs-quality split. Those looked like one dial until a teaser rated worthless shipped: the gate sat on the `--approve` branch, which a human flag could waive. Fix was separation onto two branches, not a better compromise.

## Exclusion zone

Do not apply inventive methods where the problem is unmeasured. Output is inventive answers to imaginary problems, with no feedback distinguishing them from real ones.

Pipeline order, fixed:

```
one line in the breakage journal
  → 3rd dated recurrence
    → five whys over the series (separate session, not the failing one)
      → cause proven? AND obvious fix demonstrably harmful?
        → TRIZ
          → AK-47 on the output
```

Every arrow is a gate, and each one has a measured failure behind it.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
