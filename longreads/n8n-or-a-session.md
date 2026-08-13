# n8n or a Session: Where the Line Actually Falls

*We already run 89 workflows and audited 10,004 executions. The split is clear, and so is the failure mode nobody warns you about.*

About the audit of everything we do in Claude Code: all our types of sessions and so on.

We need to think about which of these sessions could have n8n built into them, what n8n functionality that would be, and why.

For example, a short simple case: a voice message arrives in a Telegram chat, and then we transcribe it into text. You can run a session that constantly monitors and checks whether a new message has appeared in Telegram. Or you can hang that on n8n.

A hook is better than using artificial intelligence. And possibly n8n is even better than a hook. Though of course that is debatable.

But n8n is configured visually.

## We are not speculating: we already run this

Self-hosted n8n, **89 workflows, 71 active, 1,675 nodes.** We did a full deterministic audit over a window with **10,004 real executions.** So this is a report, not an opinion.

The voice example Anton picks is the exact case that works. **Personal Audio Summary: 1,435 executions, roughly 144 a day, error rate 0.1%.** Voice in, transcript and summary out, nobody watching. That workload has no judgement in it and no reason to involve a model in the deciding.

Three more of the same shape carry almost everything: a CRM inbound supervisor at **4,155 runs**, a translation bot at **2,901**, a staff assistant at **623**. Four workflows produce about **90% of all executions**, all healthy.

## The line, stated plainly

**n8n wins where the work is high-frequency, deterministic and boring.** Poll, transform, route, store, notify. The value is not the visual editor, it is that these runs cost nothing per invocation and never hallucinate.

**A session wins where judgement is required.** Reading a transcript and deciding what it means, writing something in a human voice, choosing between two designs, noticing that a number looks wrong.

The mistake in the middle is putting an LLM in the polling loop, and it is expensive in a specific way: a session that wakes up every minute to ask "is there anything new" burns tokens to produce the answer "no" several hundred times a day. That is what n8n and hooks are for.

But notice which half of Anton's own example is which: **the trigger is n8n's job, the transcription is a tool's job, and only "what should be done about this message" belongs to a session.** Most pipelines split like that, and the split is usually clean once you look for it.

## The failure mode nobody warns you about

Here is the part we would put on a poster, because it cost us weeks.

**Active does not mean running.** In our audit, one workflow sat with an active one-minute schedule, which should have produced roughly 14,000 executions in the window. It had produced **zero**. Silently. The interface showed it as active and green; the trigger node had been disabled eleven months earlier.

And it was not alone: of 89 workflows, **only 21 had any run history at all** in the window. Some of those are sub-workflows that legitimately do not log, but several were genuinely dead while displaying as alive.

The same class again, from a different angle: our dead-man webhook returned 403 for weeks to the code that called it, while a manual `curl` smoke-test returned 200. The endpoint was fine; the client differed. **Test an endpoint with the same client your code uses.**

So the honest addition to "n8n is configured visually" is: **visual makes it easy to build and easy to believe.** A canvas that looks connected is not evidence of execution. Whatever you move to n8n needs the same thing every other automation needs — a check on the *age of its output*, not on its status badge.

## Also visible in the audit, and worth budgeting for

**Broken quietly, for a long time.** One daily workflow had failed on every single run for weeks, 10 out of 10, on a code-node bug. Another was erroring on 11% of runs on a flaky memory node. Nobody noticed either until we counted, because a failure inside a scheduled workflow shouts at nobody.

**Duplicates and orphans accumulate.** Dev and prod copies both active, two workflows sharing one webhook path, retired bots still holding credentials. Ninety workflows is enough to lose track, and that number arrives faster than you expect.

**Logs are finite.** Ours prune at about 10,000 records, which was ten days. Any question longer than that window has to be answered by something you wrote down yourself.

## What we would actually do with Anton's audit

Not "which sessions could use n8n". The more useful question is the reverse: **for each recurring thing we do, what is the cheapest component that can do it, and what proves it ran?**

The ladder we use, cheapest first: a scheduled task, a hook, an n8n workflow, a session. Take the lowest rung that can do the job. A session is the most expensive rung and the only one that can think.

And regardless of which rung you pick, the same two rules apply, because both classes of failure above came from skipping them:

**Health is the age of the output, not the status of the runner.** A green badge and an exit code of zero both survive a component that quietly does nothing.

**The watchdog does not live inside the thing it watches.** If it dies together with its subject, its silence is indistinguishable from everything being fine.

Which of your automations is currently marked active? And when did you last check that it actually produced something?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/n8n-or-a-session.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/n8n-or-a-session.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
