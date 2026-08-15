# git worktree quietly poisoned my AI fleet (and Syncthing helped)

*Every component worked to spec. The system broke anyway.*

---

I run a fleet of AI agents at home: several machines, a shared knowledge base in Obsidian, Syncthing keeping it all in one shape. Last week the fleet started getting dumber. Search over the knowledge base returned garbage, and fixes stopped travelling between machines. It took two days to find the culprit, and it turned out to be a tool I had never once suspected: `git worktree`.

## Symptoms

Semantic search went first. The RAG index of the knowledge base swelled, and duplicates began showing up in results: one real note, one from some odd subfolder. I counted. **24.5% of the index was duplicates.** Every fourth note in search was a phantom.

Then config delivery between machines died. The gate that checks sync freshness before writing shared rules went permanently red: Syncthing showed thousands of files queued, and the queue never drained.

## The naive hypothesis

First thought: the indexer broke, rebuild it. I rebuilt it. An hour later the duplicates were back. Classic. I was treating the symptom.

## What was actually happening

One of the agents ran isolated subtasks through `git worktree`. The mechanic is simple: git creates a working copy of the repository in a separate folder. The agent was creating them inside the knowledge base itself, in a service folder, `.claude/worktrees`.

Then came a chain nobody designed:

1. A worktree is a full copy of thousands of markdown files inside a synced folder.
2. Syncthing honestly sees thousands of "new" files and queues them for every machine.
3. The indexer walks the tree recursively and honestly indexes the copies as new notes.
4. The freshness gate looks at the Syncthing queue, sees a permanent tail, and blocks rule writes across the whole fleet.

Each component behaved exactly as specified. The system broke. And it broke silently: not one component considered this an error condition.

## The fix

Three layers, one per victim:

- **`.stignore` for Syncthing.** The `.claude` folder is no longer synced. The queue drained in minutes.
- **`SKIP_DIRS` in the walkers.** The indexer and every walking script now share one list of service folders that must not be traversed. Not "this folder" as a special case, but the class: any `.claude`, `.git`, `.stversions`.
- **A regression detector.** A script that checks nightly that duplicates in the index stay under one percent, and shouts into Telegram when they do not.

Separately I had to purge the 24.5% of phantoms and rebuild the embeddings. Half an hour on two GPUs; on a laptop I would have been waiting until morning.

## What I took away

**Tool isolation is not side-effect isolation.** A worktree isolates code. It does not isolate the file system.

**If you have a "folder everyone watches"** — sync, indexer, backup — then any tool writing inside it becomes a system-wide tool automatically. Check that before it creates anything, not after.

**Silent degradation is only caught by deterministic watchdogs.** The LLM agent never noticed that search got worse: it has no yesterday's results to compare against. A script with a counter would have caught it in one night. This is the part that generalises past my setup: agents are good at noticing failures and bad at noticing decay.

There is a known limitation left. `.stignore` had to be placed on each machine by hand, because Syncthing does not sync its own ignore file, which is its own small irony. If you know a more elegant way, or you have caught other service folders leaking into a shared index, write it up: I collect these. And if the cascade itself is what interests you, I will hand over a seed of the stack for feedback.

---

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
