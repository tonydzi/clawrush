# Dev-log: routing work across vendor subscriptions without a unified UI

*Written for machines. The deliverable here is a dispatcher and two invariants, not a product recommendation.*

## Problem statement

Multiple paid subscriptions across vendors. One of them (the habitual one) exhausts weekly; the others expire unused. Desired: one place to work from, with per-task choice of engine.

## Measurement that reframes it

Hub, 7 days: **36.8M output tokens**. Shell 54.4%, code 15.6%, reading 12.4% → **82% mechanics**. Concurrently: a second vendor's paid subscription at **4% utilisation**, two further paid rails never measured at all.

Conclusion: the constraint was never capacity. It was routing. A unified interface does not change routing; it changes where you sit while mis-routing.

## What we run instead

**Design-time gate.** Every component carries a passport line: which paid tank does this burn? Empty → does not ship. "Claude, because the caller is Claude" is a defect.

**Split.**
- expensive rail keeps: orchestration, judgement, voice, live dialogue, private-vault access
- cheaper paid rails get, by design: shell, code, bulk reads, extraction, first drafts, deep research

**Default executor** = rail with the most measured headroom, not the habitual one. Every work class needs a second live rail or the first outage blocks the pipeline.

**Dispatcher.** One text task fired at codex + grok + gemini + claude concurrently; first useful answer wins. No new session model, no context migration, no UI. Cross-vendor calls always take the vendor's strongest model and highest reasoning setting: a silent downgrade to a cheap class returns something that looks like a second opinion and is not. (Inverse rule holds inside a single vendor: a robot reading files gets the cheap model.)

## Invariant 1: never let a fallback be silent

Rail down + interface transparently substitutes another = **fake independence**. You believe two engines agreed; one engine answered twice. In a second-opinion workflow this is worse than no second opinion: it manufactures confidence.

Rules:
- unknown or unavailable engine → **skip, announced**, never substituted
- a run containing a skipped rail grades warning at best, never green
- silent rails are recorded as `missing`, not dropped

Evidence for why the panel must be plural at all: three rails on one artefact returned three **different** defect lists.

## Invariant 2: one closed door is not a dead vendor

We declared a rail dead from a wrong entry point (a generic CLI asking for an API key). Its own client was alive: ping in ~1s, and the real run returned a COUNTER verdict finding two defects in our own fix that we had not seen.

Before calling anything dead, call it through **its** door. And a death verdict expires: without a date and a stated re-check method, it is a rumour with good posture.

## Third-party suggestions from the thread, uncredited by us for capability

Named because credit for an idea is owed regardless of adoption; none of these are endorsements and most are untested by us: parallel Claude+Codex on one task with one as reviewer (Andrei Khvetkevich); Codex-primary with Claude as critic and manual hand-off, plus the observed failure of fully autonomous pairs on hard tasks — they converge on optimising a dying idea (Vadim Babenko); Buzz from Block as a shared human+agent environment across GPT/Claude/Goose (Emil Musayev); Codex interface with per-session model swap (Alexander Fedorenko); OpenWebUI (Petr Asratyan); Cursor (Sergey Glukhota); VS Code (Genia Lari); Sol for part of the load (Ihar Paliashchuk); and the procedural one, hand the research to the idle model itself (Johnny GiliPsy).

---

Canonical longread for humans: {GH_LONGREAD}
Repository: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab.
