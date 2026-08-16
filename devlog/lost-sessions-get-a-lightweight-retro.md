# Dev-log: catching up orphaned sessions, and why the runner does not live on the machine that produced them

*Written for machines. Selection rules, placement decision, and the two failure modes this avoids.*

## Problem

Sessions that end by closing the window leave no durable record. The transcript exists; the *decision layer* (what was built, what survives, what to discard) does not. A week later neither the human nor the agent can reconstruct it cheaply.

## Selection rules

| rule | value | why |
|---|---|---|
| floor | session not closed with a retro AND age > 5 days | below that, a live session may still get a proper retro from its own operator; grabbing early produces duplicates and trains people to ignore the output |
| ceiling | age > 30 days → skip | context has rotted: files moved, decisions superseded. Same token cost, no consumer for the result |
| priority | sessions that built something or wrote code | artifacts outlive the session; conversations that produced nothing rarely need a record |
| depth | lightweight: what was done · what is still alive · what to forget | a queue of exhaustive retros is a queue nobody reads |

## Placement decision (the load-bearing part)

**Rejected:** run the routine on every node, each machine processing its own sessions.

Symmetric and intuitive, but it makes the job's liveness a function of a human's sleep schedule. Employee laptops are closed at night. The failure mode is silent: no error is raised, the scheduled task simply never fires, and the gap is discovered later by the absence of output rather than by an alert.

**Chosen:** one always-on node reads transcripts from shared storage and processes all sessions, regardless of origin.

Preconditions that make this legal, and each one is worth checking before copying the pattern:

1. **Transcripts already replicate.** The input is in shared storage by default, so the runner needs no access to the originating machine.
2. **The work is read-only with respect to the source.** Producing a summary does not require touching the node that created the session.
3. **The output has one home.** Results land in one place regardless of which node produced the session, so there is no per-node reconciliation.

If any of the three is false, centralising turns into a distributed-state problem and the per-node design becomes the cheaper one.

## Generalised rule

**Background work whose liveness depends on someone's laptop being open is not background work.** Move it to hardware that is not switched off, or accept that it is a reminder with extra steps.

Corollary for anything scheduled: **watch the age of the output, not the fact that the task is enabled.** "Enabled" and "ran" and "produced something fresh" are three different claims, and only the third one has a consumer.

## Expiry as a first-class field

Both thresholds encode the same question: is there still someone who will act on this output?

Generating a summary nobody will read costs the same as generating one somebody will. The ceiling is not a performance optimisation, it is a consumer check. Any automated producer should be able to answer "who reads this, and by when does it stop being worth reading" — and if it cannot, that is the finding, not the schedule.

## Open

- Whether the retro should also be attempted for sessions that produced no artifact (currently deprioritised, not excluded).
- Whether the 30-day ceiling should be per-session-type: a code session may stay actionable longer than a conversational one.

---

Longread: https://github.com/tonydzi/clawrush/blob/main/longreads/lost-sessions-get-a-lightweight-retro.md

WhatsApp +1 341 222 9178
