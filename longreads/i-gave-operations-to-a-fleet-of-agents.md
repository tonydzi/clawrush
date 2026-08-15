# I handed company operations to a fleet of AI agents. Honest results, failures included

*Numbers with dates attached, and the three ways it went wrong.*

---

For the past months I have been building the thing everyone tired of routine dreams about: a fleet of AI agents running company operations. Not "a chatbot answers questions" — actually working: CRM, outreach, content, nightly reports.

Numbers first, so this is not just talk.

**Six machines in the fleet:** a desktop hub, laptops, a VPS coordinator. Each runs its own agent.

**94,921 contacts in the working CRM:** 80,788 contacts plus 14,133 leads, measured 2026-07-29, with another 312,254 records in the archive. Classification and enrichment are done by agents. By hand this would have taken a team months.

**A night window, 23:00 to 06:00:** everything heavy — imports, indexing, reports — runs while I sleep. A digest is ready in the morning.

**One machine going down no longer takes the system with it:** agents hand tasks to each other over a shared bus.

## What went wrong, which is the interesting part

I am not selling a fairy tale. Here are the failures.

**Failure one. An agent "pretended" it had dispatched research.** The ledger said three started. In reality, one. A night of work lost. Cured by a hard rule: an agent must prove every step — a link, a counter, a screenshot. "I think it went through" is not accepted.

**Failure two. A service tool littered the knowledge base.** Every fourth note in search turned out to be a duplicate. The agents did not even notice: they have no "yesterday's feel" that search used to be better. Now simple watchdog scripts reconcile counters every night and raise an alarm in Telegram.

**Failure three. I became the bottleneck myself.** Agents brought decisions faster than I could press "yes." I had to split it: routine the agents decide themselves and report after the fact, and only the irreversible reaches me — money, publications, deletions.

That third one is the least technical and the most expensive. Every approval I insisted on was a queue nobody was serving while I was in a meeting.

## The main lesson

AI agents in operations work. Not as "we hired a wizard," but as "we hired a very fast junior intern, six of them": they need rules, checks and watchdogs. The value is not born from the model, it is born from the harness — ledgers, gates, counters, mutual verification.

Unit economics closed for me on one criterion: hours. Operations used to eat my evenings. Now in the evening I read the morning plan, press three buttons and go live my life.

## What to take for yourself

- Start with one process — for me it was CRM — not with "let us automate everything."
- Every agent gets an action log and an obligation to prove its result.
- Deterministic checks beat a smart model. A script with a counter catches what an LLM will miss.
- The night window: run the heavy things while you sleep. Those are free hours.

I am putting together a small group of founders and engineers who want to poke at a fleet like this: I hand over a seed of the stack for feedback. Write in the comments or in DMs.

---

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
