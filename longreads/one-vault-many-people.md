# One Vault, Several People

*Anton wants to share this because it works. Here is what it costs, counted, and the four rules that make it survivable.*

In case anyone did not know, we have a great feature: several colleagues can work with one vault that stores the information, at the same time.

I would like to share this with my subscribers, because there is big value here, first of all for corporate work.

That is, when you brainstorm on something together, develop something together. Not every solo contributor doing something separately and then merging it into the common pool, but you are in a single information space the whole time and you work together.

This is really worth working on.

I also want to run additional research across all the GitHubs, all the projects that have already done something similar, and contribute this know-how everywhere. I want to look: maybe someone has already worked on this and done it better, when the AIs work together with one shared brain, it is very convenient.

Later I will write a proper post about how all of this works for us. That post could also be the README for our pull requests.

Because it is really very, very convenient when one employee can just ask: remind me please, my colleague was working on some topic, roughly this one, I would like to continue his work. And any employee can continue the work from the point where another one stopped.

That is, you are all in one space doing the same thing. It is very convenient.

## What it actually costs

The convenience is real and we would not go back. But a shared vault has a bill, and we can put a number on it.

**2,689 sync-conflict files** currently sit in our vault. 209 of them appeared in the last thirty days. That is not corruption and nothing was lost — the sync layer preserves both versions when two machines touch one file — but every one of them is a small decision somebody has to make later, or a quiet fork nobody notices.

The worst offenders are informative. Top of the list: two dashboards, ten conflicts each. Both are **generated files that several nodes rebuild independently.** The vault is doing exactly what it should; the mistake was ours, for putting a machine-written artifact in a place where several machines write it.

That gives the first rule, and it is the one that removes most of the pain.

## Rule 1: one file, one writer

Not "coordinate carefully". **Assign an owner per file.** Everything else is a special case of this.

Our always-loaded rule documents get exactly one optimising writer each, on a schedule; every other session leaves them alone. Not because concurrent edits corrupt anything, but because **an optimiser deletes**: several agents each removing what looks like noise will collectively remove signal, and no individual edit looks wrong in review.

For generated files the same rule reads: generated output belongs to the node that generates it, and if several nodes need it, one publishes and the rest read.

## Rule 2: the state lives in a journal, not in the file layout

The moment several people work in one space, "where the file is" stops describing "what state the work is in". Two people can have a thing half-done in different ways at once.

We keep one folder per unit of work and a small journal file inside it recording what happened, when, and by which node. Folders answer *where*, the journal answers *what happened*. Adding a participant or a stage means adding a field, not restructuring a tree.

## Rule 3: announce before touching shared things

Before editing anything shared and sensitive — the common rulebook, config, shared databases — check whether another session is already in it, then take a short lease, then edit, then verify it propagated. Small edits do not need this: declaring every change produces alert fatigue and then nobody reads the declarations at all.

One counter-intuitive thing we learned: **two sessions on the SAME machine are more dangerous than two machines.** Across machines the sync layer at least preserves both versions as a conflict file. On one machine, the second write silently overwrites the first and there is no artifact to notice.

## Rule 4: read config live, never from a snapshot

The failure that catches everyone: a process copies shared settings when it starts, then the world changes. We paid for this twice in one week. A destination was paused, and work created before the pause never saw the pause and proceeded. A repository changed owner, and everything created earlier still pointed at the old address — GitHub redirects reads silently but answers 307 on writes, so it failed only on the write.

In a shared vault this is the norm, not the exception: someone else changes the shared setting while your process is running.

## The part that delivers the value Anton describes

"Any employee can continue from where another stopped" needs one concrete artifact to be true: a **handoff written for someone without your context.** Decisions and why, what is done and how it was verified, exact paths and values, open blockers, and an explicit next step.

Without it, "continue my colleague's work" means reading a week of someone's notes and guessing. With it, it means reading one page. This is the least glamorous part of the whole setup and the part that actually produces the effect.

And the honest warning about the AI half: agents in a shared space need role discipline, or they will each mark their own work as done. Ours is explicit — the one who implements does not get to declare it verified; that requires an independent pass, preferably by a different model, because a heterogeneous pair catches more than the same model reviewing itself.

## On researching prior art

Worth doing, and one thing to look for specifically: **conflict-free replicated data types.** The class of problem "several people edit shared state, nobody is the server" is thoroughly studied, and the fact that we have 2,689 conflict files means we are solving it by hand.

We are not proposing to rewrite our vault around CRDTs — plain files that a non-engineer can open and fix with a text editor are worth a lot. But if you are researching whether someone did this better, that is the shelf the answers are on.

How many people share your knowledge base? And do you know how many conflicting copies are quietly sitting in it right now?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
