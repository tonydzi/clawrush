# Link the Sessions, Not the Notes

*Obsidian is a great tool for a human. That is exactly the argument for linking sessions instead of notes — and for deriving the tags rather than typing them.*

Continuing the previous post.

Obsidian is a wonderful tool for a human.

So I think it may be worth linking all my sessions, specifically the sessions, to each other, so that I can see: ah, here I am building this; here I am doing that; and so on.

Also, maybe in my dashboard it is worth giving each session its own tag cloud. That way I could sort things easily there.

Need to think about it more.

## The distinction is right, and it is bigger than it looks

"Obsidian is great for a human" plus "link the sessions, not everything" is one idea, and it resolves the problem from the previous post cleanly.

A hundred thousand notes cannot be a graph anybody reads. **A few hundred sessions can.** Sessions are the unit at which a human actually thinks: I sat down, I did a thing, it ended. Notes are the exhaust of that. Linking the exhaust produces a hairball; linking the sittings produces a story.

So: keep the notes in storage that answers queries, and put the graph one level up, where the node count is human-sized.

## The links already exist. Do not draw them by hand.

This is the part worth being firm about, because hand-drawn links are how these projects die.

You do not need to decide that session A relates to session B. **The transcript already contains the evidence:** which files it touched, which tasks it moved, which repository it pushed to, which case it worked on. Two sessions that edited the same file are related, and nobody had to remember that.

That gives three link types, all derivable, all falsifiable:

**Same artifact.** Both sessions touched the same file, task or case. The strongest and cheapest link, and the one that answers "who worked on this before me".

**Continuation.** Session B opens with the state session A left, or explicitly picks up its handoff. This is the link Anton actually wants: *here I am building this, and here is where that continued.*

**Same goal.** Both sessions moved the same registry item. Weaker, but it is the one that maps to his categories — infrastructure, job hunt, second brain — without anyone maintaining a taxonomy.

Every one of these is a fact in the data, not a judgement. Which means the graph rebuilds itself nightly and never rots.

## On tags, with a number that surprised us

We measured our own vault before answering, and the first number we got was wrong in an instructive way.

**Whole vault: 218,679 notes, 209,736 with tags — 96%.** Sounds excellent. It is also meaningless, because the corpus is two different things stacked in one folder tree.

Split by where the notes come from:

| area | tagged |
|---|---|
| concepts | 274 of 278 (99%) |
| insights | 2,176 of 2,199 (99%) |
| tasks | 666 of 735 (91%) |
| system | 177 of 197 (90%) |
| **imported conversations** | **2,368 of 105,668 (2%)** |

So the honest finding is the opposite of the one we expected: **where a human curates notes, tagging holds at 90–99%.** The low number lives entirely in imported chat history, which is raw material and does not need tags at all.

Two things follow, and the second matters more.

**Do not measure tag coverage across a whole vault.** Half of ours is imported raw material; averaging it with curated notes produces a number that describes neither. Any metric over a mixed corpus needs the split before it means anything.

**Manual tags survive on hundreds of items, not on hundreds of thousands.** That is exactly the argument for putting the tag cloud on sessions: a few hundred nodes is inside the range where humans do keep up, and our curated folders prove it.

Even so, derive what you can: files touched, tools invoked, repositories pushed to, tasks moved, whether a Deep Research ran, whether it ended with a retro. Those are fingerprints rather than opinions — never missing, never wrong, free to compute, and present for the **94 abandoned sessions** nobody would ever have tagged by hand.

## Where a hand-written tag does belong

One exception, and it is the same field as in the previous post: **what this session achieved.** That one is written by the person who was there, at the end, and it is worth its cost.

The rule underneath: **type in only what the machine cannot derive.** Everything else is bookkeeping, and the moment your corpus outgrows what a human keeps up with, the coverage number tells you exactly when that happened.

## What this looks like built

A session node with: the fingerprints (machine, operator, size, whether compact / DR / retro happened), the derived tags, the derived links to neighbouring sessions, and one human sentence about the outcome.

Then the Obsidian view Anton wants is honest, because every edge in it is backed by a shared artifact rather than by somebody's memory of what they were doing that week.

And it stays readable, because the node count is the number of times you sat down — not the number of files you produced while sitting.

Do you link your notes or your work sessions? And when you measure tag coverage, do you separate what you curated from what you imported?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
