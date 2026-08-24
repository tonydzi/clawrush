# A skill is born by a counter and dies by a calendar — and nobody uses the ones you did not write

*Two arithmetic rules run the whole library. The interesting part is what they reveal about where a skill's value actually sits.*

## Attribution first

The rules and the observation below come from a **talk by Konstantin Krestnikov, an engineer working on GigaChat / GigaChain** ([recording](https://youtu.be/a-NIeMB-Hj8)). His system, his numbers, not our measurements. Our own part is at the end and is one sentence long, because that is all we can defend.

## Birth: a counter, not a judgement

In his setup a skill is not authored by a person deciding it is time. It is created by the agent, on a threshold: **if a task took more than five tool calls, the agent considers turning that work into a skill.**

The design choice worth copying is that the trigger is a counter rather than taste. A person does not notice they are doing the same thing for the third time — noticing repetition is exactly the thing humans are worst at and counters are best at. Put the judgement anywhere else and the library only grows when someone is in the mood to curate it.

## Death: a calendar

The other half is retirement, and it is equally mechanical:

- **30 days** without a call — the skill goes dormant.
- **90 days** without a call — it moves to the archive.
- **Weekly**, small skills are merged into larger ones.

Nothing here asks permission. A library that only grows is a library that stops being searchable, and the agent pays for every entry it has to consider.

## The observation that matters more than either rule

They run a shared hub where the community has contributed a large number of skills. His report: he does not see them being used. Everyone writes their own.

That is not a comment on quality. It follows directly from what a skill is once you put data inside it — the instruction is the cheap half, and the accumulated history, artifacts and context are the expensive half. Someone else's skill arrives with the instruction and without any of your data.

A well-written skill you did not write is a well-made empty box.

## What we take from it

The advice we are acting on: if you already have a pile of skills, the next thing to build is **not another skill — it is a usage counter**. Without one you cannot tell a live skill from a dead one, and every stale entry keeps costing you.

We counted ours. The result was not good.
