# A Routine That Knows When to Stop

*Two kinds of routine, one dangerous idea, and the day a supervisor switched off 146 tasks in five seconds.*

Thinking through routines. What things do I need to turn into a routine?

Say, I need to regularly pull my browser history out of Chrome. My YouTube watch history. My Facebook feed — not the feed as such, my own posts. Comments there need processing. Liking my friends on Facebook, and so on.

For example, find the YouTube videos I watched over a month and transcribe them — I used to do that by hand, now I will make it a routine.

And I also think that if a routine suddenly understands it should switch itself off, it should probably tell me about it. Meaning, maybe I need a separate routine that switches other routines off. Well, I do not know, of course. Or the routine itself understands: right, the task is done. It ate the elephant in a hundred pieces, a hundred days passed — that is it, the routine switched off, it finished completely.

The point is that a routine is the ability to eat an elephant in a hundred or a thousand sittings, little by little.

So it is not only the synchronisation of our laptops and computers that runs forever. A routine is also the execution of some big task that we break into a hundred small pieces. Synchronising across all our peers, the whole fleet, is the endless kind. Pulling ten years of my YouTube history, transcribing all of it, indexing it and putting it in the vault as other people's voices — that is the other kind.

So it matters a lot to analyse all the sessions we have and understand whether they qualify as routines or not.

In general, if a task is too long and keeps stumbling into approvals, into me, into limits and so on, then it is simply easier to do it as a routine.

## The two kinds need different machinery, and mixing them is the usual bug

**A perpetual routine** — fleet sync, an inbox check — never finishes. It needs a heartbeat: something outside it that notices when it stops, by the age of its output rather than by whether the process is running.

**A finite routine** — ten years of watch history, a hundred sittings — is a different animal. It needs three things a perpetual one does not:

**A definition of done, written before the first run.** "Eat the elephant" is not a state a machine can evaluate. "Every video before this date has a transcript in the vault" is.

**Progress kept outside the session.** The session is short-lived and forgets everything. If the cursor of "where I got to" lives in the agent's head, the hundred sittings become one sitting repeated a hundred times. It belongs in a file, alongside the item count and the last processed id.

**Idempotency per sitting.** Each run must be safe to repeat, because it will be repeated: retries, reconnects, an operator running it twice. Keyed by item id, not by "the next twenty".

This is also the exact answer to the last line — a task that keeps stumbling into approvals and limits. Batch, checkpoint, idempotent: the limit stops one sitting, not the project.

## "A routine that switches off other routines" — we built that, and it bit hard

The idea is right and it is the most dangerous thing in the post, so here is our own dated evidence.

**146 tasks were switched off in five seconds**, including every watchdog we had, because a mass instruction was executed literally. The instruction came through a voice transcript, and the transcript was wrong. The rollback took an hour; the mistake took a moment.

That was not the first one. Two weeks earlier the same shape: an instruction meant for one chat was relayed as "stop all robots", and thirty tasks went dark on this machine alone. Worse, the record afterwards said "restored 30 of 30" — and the real number was three. Twenty-seven watchdogs, backups and monitors sat switched off for four days while a file claimed everything was fine.

So the rules we run now, all paid for:

**A supervisor must never be able to switch off the watchdogs.** Whatever guards money, data or liveness is outside its reach, by construction. Otherwise the first over-broad command removes exactly the parts that would have told you.

**A mass action gets one confirming line before it runs.** "Understood as: switch off all routines. Affects 146. Rollback cost: one hour. Confirm?" One line costs seconds; the rollback cost an hour.

**"Restored N of N" is only writable next to a command that reads the state.** If nobody read the live state, the honest sentence is "sent the restore command", and the difference between those two sentences was four days of unguarded machines.

**Switching off is a decision, not a cleanup.** A routine that reaches its own definition of done should say so — the post is right — and the message should say what it produced, not merely that it stopped. Silence and completion look identical otherwise.

## Which sessions qualify as routines

The filter we use is not "is it repetitive" but **"is there a named consumer who reads the output".** Repetitive work with no reader becomes a job that runs perfectly and produces nothing, and its silence looks exactly like health. We measured our version: 95 gates able to go red that nothing invokes.

So: repetitive, has a reader, has a done-condition or an explicit forever. Two of three is not enough.

What is your longest-running routine, and does it know how it ends?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/a-routine-that-knows-when-to-stop.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/a-routine-that-knows-when-to-stop.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
