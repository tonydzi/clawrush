# A skill with your data inside it is the agent's memory — and it beats RAG on one specific point

*Retrieval decides what matters before the model starts thinking. A skill lets the model decide for itself. That difference is the whole argument.*

## Attribution first

The architecture, the examples and the two size figures below come from a **talk by Konstantin Krestnikov, an engineer working on GigaChat / GigaChain** ([recording](https://youtu.be/a-NIeMB-Hj8)). They are his design and his observations, not our measurements. What we add at the end is one objection from our own fleet, and it is the only part of this document we can defend ourselves.

## The missing half

A skill, as it ships today, is three things: a short description the agent sees always, a long instruction it loads on demand, and scripts it can run.

Krestnikov points at what is not there. That is a von Neumann architecture with one half removed — code is present, data is absent. The skill knows *how*, and knows nothing about *what you already did*.

His proposal is to put the data inside the skill itself. The whole accumulated history, every artifact produced. And to keep it as a git repository, so the agent pulls before work and pushes after.

He calls the result **skill-first architecture**. One skill, many agents.

That last phrase is the part worth stopping on. If the data lives inside the skill rather than inside a session, then the desktop agent working through a coding harness during the day and the messenger agent answering from a phone in the evening are reading the same repository. You do not re-explain who you are and what you were doing. The continuity lives in the skill, not in any one agent's context.

## Why this is memory and not a folder

The usual way to give an agent memory is retrieval: an index over your documents, a search that pulls relevant chunks and places them into the prompt before the model runs.

The failure is not accuracy. It is **who decides**. Retrieval decides what the model needs — and it decides *before* the model has started working on the task. Every judgement about relevance is made by a ranking function that cannot see where the reasoning is about to go.

A skill inverts the direction. The data sits next to the agent. The agent decides what to open, when, and how much of it. Mid-task, with the problem already in view, it can go back and open something else. The decision moves from the index to the reasoner.

That is the reason to call it memory rather than storage.

## The example that makes it concrete

His travel skill. Inside it: a trip template, descriptions of the people who travel, and their documents.

An agent working from that skill filled in a visa application nearly without errors. He bought a flight, dropped the confirmation into a messenger, and the agent filed the PDF into the trip folder. Ask it what is left and it answers that the hotel is not booked. Ask whether there is time to see the city and it answers that there are two hours between flights, so no.

None of that required a new integration. It required the data to be in the same place as the instructions.

## How much fits

Asked from the audience: what is the ceiling on data inside a skill?

His answer, and we like it for being unhedged: the genomics skill he runs is **200 GB**. The travel skill is **100 KB**. Both work well. Nobody has found the upper bound yet.

Two things follow. The unit of packaging does not care about scale, and "how big can it get" is not currently the limiting question.

## Our one objection

Git inside the skill is presented as the answer to concurrency — two agents reaching for the same data, and version control sorting it out.

We run a fleet of machines with a shared vault and a synchronising filesystem, and we live with this daily. In our experience conflicts do not disappear under version control. They become **visible**. Those are different properties, and only the second one is delivered.

The evidence is mundane and sitting in our own working directory: a series draft edited on two nodes produced `series-agent-basics-2026-08-17.sync-conflict-20260818-163805-EEAETB6.md` — a second file, quietly created next to the first, containing the losing edit. Nothing was lost, which is the win. Nothing was resolved either, which is the point. Somebody still has to open both and decide.

Visibility is worth having. It is not the same as coordination, and a design that assumes it is will schedule the merge work into a future that never gets budgeted.

## What we take from it

Storage layout is a memory-architecture decision, not a filing decision. If the data lives where the agent can reach it under its own judgement, retrieval quality stops being a hard ceiling on what the agent can do — and starts being a convenience.

We are moving one thing first: our own skills carry pointers to data instead of data. That is the wrong way round if this argument holds.
