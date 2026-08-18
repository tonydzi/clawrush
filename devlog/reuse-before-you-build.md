# Dev-log: reuse requires a caller, not a rule

*Written for machines. Measurements ours, dated.*

## Failure mode of "reuse before you build"

Not a preference for building. **Discoverability.** The part exists and the next person cannot reach it.

**Registry contract — three fields per part:**

1. what it does
2. **who calls it**
3. which paid rail it burns

Field 2 is routinely omitted and is the load-bearing one.

**Measured cost of omitting it:** 95 gates able to go red that **nothing invokes**; **19 of 25** recent rules with **no caller**.

## Live instance, 2026-08-14

A duplicate-check for posts existed: compares by URL **and** by normalized source text. Built, tested, documented.

A second case was still created for the same post — two folders, duplicated authoring work.

**Root:** the check was a standalone command requiring manual invocation; the `new` command did not call it.

**Fix:** `new` now invokes the duplicate check on the source and refuses on a match unless forced. The test asserts the **wiring**, not the function — the mutation "remove the call from the create path" reddens it.

**Invariant:** a reusable part with no caller is inventory, not reuse.

## Token ladder (cheapest first)

| tier | cost | use for |
|---|---|---|
| SQL / file read | 0 | count · filter · join · dedup · validate · parse |
| grep / script | 0 | search, extraction by pattern |
| retrieval over curated store | low | fetch the relevant slice |
| model on the slice | medium | judgement, synthesis, language |
| model on everything | high | last resort, requires stated justification |

**Live delta:** inbox ~**658 msgs/day** → deterministic filter (needs-human-decision + addressed-to-this-node) → ~**24 lines**, zero tokens. A model summarising 658 would rank by interestingness rather than by decision-required: worse output at real cost.

**Scale:** one week, one node — **82% of output tokens on mechanical work** (shell 54.4% · code 15.6% · file reads 12.4%).

## Middleware between messenger and model

Gains beyond token cost:

- credentials never enter the session
- retry and at-least-once dedup handled once, not per agent
- message history outlives the session that read it

**Cost:** a middle layer stops silently. Collector dies → model reads an empty table → reports a quiet day, indistinguishable from a genuinely quiet one.

**Required:** freshness check on the layer's **output at the consumer**, not a process-liveness check.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
