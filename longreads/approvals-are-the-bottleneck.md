# Approve, Approve, Approve

*Sessions stall waiting for a human. Here is what that costs us, measured, and why auto-clicking the button is the wrong fix.*

Let me continue my thoughts here.

Yes, sessions often sit there asking for some approval. That is genuinely infuriating.

I recently tried to fix it by having sessions be recreated: take an old session as the base, one where approvals were already given. So if a session starts as new, approvals have to be given by hand, which is roughly how the harness works. But if it is an old session, it should be reused, and then no approval is needed.

I need this thing to work all the time. I need a watchdog to come along and push sessions forward somehow.

And it often happens that you need to press approve, approve, approve: ten times in a row on that button.

Maybe make it so that every 15 minutes all sessions get checked and the approval gets given after all.

It is either an approval, or a situation where the session wants something. That also happens a lot: the session wants you, as the founder, to make a decision.

If something can be pushed forward, you as the founder push it forward. If something is genuinely hard, then it waits for me.

## What the queue actually looks like

We keep a log of every question a session escalated to a human, so this is not a feeling. Over the last 30 days: **16 asks, and 12 of them expired without ever being answered. 75%.**

The weekly breakdown is worse than the average: three consecutive weeks at **100% expiry**, four asks, then two, then four, none answered. Only the most recent week broke the pattern, at 33%.

And the largest class is not what we expected. **9 of 16 asks, 56%, were content approvals** — permission to publish something. Login and 2FA prompts, the ones that genuinely need human hands, were 2. Decisions requiring a founder's judgement: 1.

So the queue was not full of things only a human could do. It was full of one recurring category that had been routed to a human by default.

## Why auto-approval is the wrong fix

The obvious version of Anton's idea is a watchdog that clicks approve every 15 minutes. We did not build that, for a reason worth stating plainly: **an approval that always gets granted is not an approval, it is a delay.** You keep the interruption and lose the safety, which is the worst of both trades.

What we did instead was ask a different question about every ask: not *how do we answer this faster*, but *why did this reach a human at all*.

That splits the queue into three:

**Category one: the ask was never needed.** The tell is in the wording. If the expected answer is "yes, go ahead and do it", then the ask was describing the assistant's own work, and the assistant should have done it and reported afterwards. We track these as red flags. Current count: zero, which is the only cheerful number in this post, and it comes from removing the asks rather than answering them.

**Category two: a class, not an instance.** The 56% content-approval share was not fifty different judgements. It was one policy question, asked repeatedly in disguise. Decide it once, write it down as a rule with a named exception list, and fifty future asks disappear. The ten-approvals-in-a-row problem is almost always this: one decision, fragmented into ten prompts.

**Category three: genuinely for the human.** Money, irreversible deletion, secrets going to third parties, legal commitments, and anything needing physical hands (2FA, a hardware prompt). These stay, and they should. In our log that is 2 to 3 of 16.

## The uncomfortable measurement

Here is the part that reframes the whole problem. A 75% expiry rate does not mean the human is neglectful. It means **the asks were not worth answering**, and everyone involved knew it at some level: the assistant asked to be safe, the human deprioritised because most of the queue was noise, and the few real ones drowned alongside the rest.

That is the actual damage. Not the waiting. **A queue that is mostly noise trains the human to ignore the channel**, and then the one ask that genuinely needed a founder's decision expires next to the forty that did not.

We have a measured precedent. A relay quietly buffered human-facing alerts for **16 days, 552 messages**, because of a bug on one node. Nobody noticed the silence, because a channel that usually contains noise looks the same when it contains nothing.

## What to build instead of the auto-clicker

**Classify at the source.** Every escalation gets a class before it is sent: reversible internal, our content to our channels, short outbound to a third party, needs-human-hands, serious. The first three are handled by the assistant and reported afterwards. Only the last two reach a person.

**Count the asks, not just the answers.** A rising ask count is a design defect in the assistant, not diligence. We measure ours monthly and treat the trend as a bug report against ourselves.

**Give every ask an expiry with a stated consequence.** An ask that can expire silently and harmlessly should not have been sent. If expiry is harmful, escalate on a second channel rather than letting it rot.

**When the same ask recurs, promote it to a rule.** The correct output of the tenth identical approval is not an eleventh approval. It is a written rule and a deleted prompt.

The goal is not a session that never asks. It is a session whose asks are rare enough that a human reads every single one.

How many approvals did your agents ask you for this week? And how many of them did you actually answer?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
