# My Sessions Spend Their Time Tidying Up

*Housekeeping is not work. Work is the thing the session was opened for. Here is the count, and the door we put in front of it.*

I started noticing that during /retro, and generally while sessions are running, they do a lot of parasitic activity. They edit claude.md, Memory.md and so on. They optimise them.

I want to run an analysis across sessions: what other parasitic activity of exactly this kind are they doing, and what can be moved to happening no more than once a day.

Because claude.md or memory.md can perfectly well be optimised once a day.

It is not a problem that they grow. That is normal. But once a day is better than every session, and we have about fifty of them, optimising the same files.

## The count, over seven days

We ran that analysis. It is not a close call.

**296 vault backups. 237 RAG reindexes.** Same week, same fleet. The record holder: **52 runs of one maintenance routine inside a single session.**

None of those runs were wrong. Each one was individually defensible: the session was about to touch the vault, so it took a backup first. The next session did the same. So did the next fifty.

That is the shape of the problem. Parasitic work is never one bad decision. It is one reasonable decision, repeated by every session that has no way of knowing the previous one already did it.

## Why it hides

Ordinary waste announces itself: something is slow, something fails, someone complains. This kind does not, for three reasons.

**Each instance is cheap and correct.** A backup takes seconds and protects real data. Argue against any single run and you lose the argument.

**It looks like diligence.** A session that reindexes, backs up, tidies the config and squeezes the memory file appears to be working hard. The transcript is full of green checkmarks. Nothing in it says the work was already done four hours ago.

**Nobody owns the total.** Every session sees its own one backup. No one sees 296.

The fix is therefore not "be more careful". It is a place where the count exists.

## The door

We built `maintenance_gate.py`. Any maintenance activity run by hand asks it first, and the rule is one run per node per day.

Three details that matter more than the gate itself:

**First knock is a hint, second is a block.** A session that meant well gets told the work was already done today, with the timestamp. Only the session that ignores that gets stopped.

**`--force` exists and requires a stated reason.** A gate with no override gets routed around, and then you have neither the gate nor the visibility. The reason goes in the log, which is the actual product.

**Diagnostics are never throttled.** Checking sync health or an MCP connector is not maintenance, it is looking. Throttle looking and you get a system that cannot be debugged on its worst day.

Orphaned routines, the ones that no robot ever called, got collected into a single nightly task at 03:20 rather than left to be triggered ad hoc.

## One writer per file

The second half is subtler than the throttle. `CLAUDE.md` and `MEMORY.md` are edited by exactly one writer each, on a schedule. Every other session leaves them alone.

Not because concurrent edits corrupt the file, though they can. Because **an optimiser deletes.** Fifty sessions each shortening the same document, each convinced it is removing noise, will between them remove something that mattered, and no single edit will look wrong in review. We have already paid for this: the instruction came down to stop squeezing those files entirely, because useful information was being erased in the name of tidiness.

So the file is allowed to grow. Growth is visible and reversible. Silent deletion is neither.

## What this costs, in the only unit that matters

Every one of those files is loaded into every session at startup. That makes them rent, not a purchase: you pay it on each of the fifty sessions, forever, and you only notice it on the day you build the thing.

Measured on our own fleet: session startup context sits between **98,000 and 123,000 tokens** depending on the node and the day, and the trend across two weeks is upward, not flat. That is the number that decides whether a "small addition to the always-loaded layer" is small.

One measurement trap, since we fell into it: the token counter in a transcript is charged to the whole message, thinking and tool calls included, and it repeats across records that share one message id. Calibrate on that naively and you get an answer that is off by nearly a factor of two. Before trusting a measuring instrument, show what its scale was checked against.

## The uncomfortable part

The rule is now two days old on some nodes and a few weeks on others, and it is honest to say what is not yet proven: we have the count of runs before the door, and we do not yet have a clean count of runs after it. Whether 296 becomes 7 or becomes 250 with `--force` on every one of them is an empirical question, and the log is where the answer will show up.

The reason to publish now anyway is that the failure mode generalises past AI agents entirely. Any system with many short-lived workers and shared state grows this exact tumour: work that is individually justified, collectively enormous, and invisible to everyone because nobody holds the total.

Do you know what your agents do when they are not doing the task? Not what they are allowed to do. What they actually do, counted.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
