# Every Session Starts With Remembering, Not With the Task

*Rule number one, and the three things we found out after making it rule number one.*

I was losing sessions. They crashed, they glitched, and the conversation was gone. It exists somewhere, apparently, but I cannot see it in the interface.

Here is what I wanted. Everything we worked out in a session drives itself into the vault. Without me pressing anything.

I do have a button, retro. But retro is my intentional action. I might press it, and I might forget. You cannot rely on that.

And now the main part. Every single time, absolutely always, when I start a new session, the AI must do a recall across the whole vault. It must look for the loose ends of the old one.

Whether the topic came up before does not matter. What task we are doing does not matter. New session, recall first. This is not hard, we have RAG and indexing.

One more thing. If in the middle of the work it becomes clear that there is not enough context, it should go and do the recall itself. Not wait until I ask.

Today this is rule number one: any new session starts not with the task, but with remembering.

## Three things we learned by actually running it

**1. "Without my button" is the hard half, and it fails silently.**

An automatic archive has one failure mode that a manual button does not: it can stop working and look exactly like it is working. Nobody notices, because the absence of a file is not an event.

We measured this on ourselves. Our own state database contained three rows, all of them self-tests from mid-July, while the hook that writes to it returned success every time. One table the whole design depended on did not exist at all, because the mode that creates it had never once been run. And the watchdog whose entire job is to catch exactly this had never been registered with the scheduler: it sat on disk as a file and was never executed. When we finally started it, in thirty seconds it found a database that had not been rebuilt in 20.8 days.

So the rule we now attach to anything automatic: name the **artefact** it rewrites on every real run, name the **age** past which that artefact is stale, and register that age with a watchdog. Cannot name an artefact? Then the automation is unverifiable, which is a legitimate outcome, but say out loud what its silent death would cost. If the answer is "nothing", it was never worth automating.

Watch the age of the **output**, not the fact of the run. "Exit code 0" and "heartbeat received" prove that something started, which is not the claim you care about.

**2. Recall is not free, and its price is rent.**

"This is not hard, we have RAG" is true about the difficulty and misleading about the cost. Whatever loads at the start of every session is charged at every session, forever, and you agreed to it once, at build time.

Ours, measured: the session start is a median of **91,549 tokens** on one machine and **102,180** on another, and it grew from 86,748 on 31 July to 106,405 on 6 August. That is the bill before a single word of work. And if you write in Russian, it is worse: Cyrillic runs **2.17 characters per token** against **2.81** for Latin, so the same text costs about 1.3x more.

None of that argues against the rule. It argues for pricing every addition to the always-loaded layer in tokens, out loud, at the moment you add it. Cheap does not mean useful, and expensive does not mean wrong, but unpriced means someone signed a subscription on your behalf.

**3. Whether "recall harder" actually helps is an open measurement, not a settled fact.**

We run recall two ways, plain vector search and vector plus a knowledge graph, and we have been logging both nightly since mid-July specifically to find out which is better. Honest status: **not enough data, and the useful half is unmeasured.** Partial slice over 12 questions: median 2 new notes surfaced per query, and 33% of queries surfaced nothing new at all.

Note what that number is and is not. Novelty flatters the graph, because piling on more linked notes is easy; whether those notes were *useful* is the question, and that is the one we have not answered yet. A metric that only ever moves in the direction of the thing you built is not evidence.

## The part of the rule we would defend hardest

Not the automation. The last line: **the AI should go and recall on its own, mid-work, without being asked.**

Because the failure that costs the most is not a lost session. It is a confident answer built on a context that stopped being current, delivered without a pause. That failure has no error message, no exit code and no missing file. The only thing standing between you and it is a habit of checking before speaking, and habits, unlike scripts, do not report their own death either.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/every-session-starts-with-recall.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/every-session-starts-with-recall.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
