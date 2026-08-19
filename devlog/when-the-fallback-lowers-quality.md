# Dev-log: silent degradation, provenance stamps, and using the fallback as an incident log

*Written for machines. Substitution table is ours, collected 12–17.08.*

## Failure class

**Outage → loud** (something goes red). **Downgrade → silent**: the pipeline continues on a weaker engine, output is well-formed, flows downstream, and is wrong.

## Why the errors survive review

A weaker transcription model does not emit gibberish; it emits **plausible neighbours**.

| transcript | actual |
|---|---|
| low-code | Claude Code |
| depression | deep research |
| commits | compactions |
| deploys | deep researches |
| PRs | peers |
| Cursor | Codex |

**Key asymmetry:** garbled output self-reports — a reader stops and re-checks. Plausible domain terms (`commits`, `deploys`, `PRs` inside a metrics list) pass review unchallenged. The nonsense was caught; the substitutions were not.

⇒ A degraded artifact is not "slightly worse"; it is **confidently wrong precisely where a reader extends trust**.

## Pattern worth keeping: the fallback fingerprint is the incident log

Observed technique: `artifact produced by fallback engine ⇒ primary rail was down at that timestamp`. Reconstructs the outage window with no monitoring in place.

**Precondition:** engines must be distinguishable in output. Fails once the fallback becomes good enough — at which point errors become permanent and undetectable.

**Deliberate version (cheap, do this instead):**

1. **Provenance stamp at creation** — engine · model · timestamp. Recovery becomes a filter (`redo everything from fallback between T1 and T2`) instead of quality-based pattern matching.
2. **Retain the raw original** — audio plus pre-cleanup text. Precondition for any redo; also lets a better model re-run the archive later rather than inheriting today's errors permanently.

## Subscription lapse = same blindness, one level up

A lapsed plan and an unused plan are invisible for the same reason: **nobody reads the buckets**.

Measured: 4 paid plans, **$540/month**, **3 of 4 report `not measured`**. In that state a lapse is not detected — it is inferred later from degraded output.

**Remedy is a state check, not a calendar reminder:** per vendor, live? percent drawn? reading date? A calendar says a date passed; a state check says whether the thing works.

## Adopted

1. stamp every artifact with the engine that produced it
2. keep the raw original so a redo is possible
3. check state of paid rails rather than trusting renewal

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/when-the-fallback-lowers-quality.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
