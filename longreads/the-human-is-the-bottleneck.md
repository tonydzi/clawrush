# The Human Is the Bottleneck

*True, and the useful part starts after you accept it: the bottleneck does not disappear, it moves — and we can show exactly where ours went.*

I need to study what Karpathy says about the "second brain" concept and the narrow bottleneck: that the human is that narrow place. Meaning, if you remove the human from human-in-the-loop, agents will work much faster, because right now the human is precisely the bottleneck.

In principle I had thought about this too. We ended up with a rule: the human **is** the bottleneck. So I told my co-founder to always remember it and always try to be autonomous — that is, not to wait for me as a human.

It is very interesting how our thoughts converge. I am not claiming Karpathy's laurels, but it seems to me I am not far behind.

I need to research what else he says and try applying his know-how.

## We run that rule, and it has a precise form

Ours is written as: **the human is allowed at the ENDS of the pipe — set the goal, accept the result. A human in the MIDDLE of the conveyor is an architecture bug.** With a counter on it: number of human touches, target zero for everything that is not money, irreversible, or outward-facing.

The sharp corollary, which is the part that actually changes behaviour: **presenting two options and asking "which one?" is not consulting, it is handing the bottleneck back.** If the fork is not one of the reserved classes, the agent decides and reports afterwards. Waiting costs more than being wrong, because a wrong reversible decision is cheap and a stalled pipeline is not.

## But removing the human does not remove the bottleneck. It relocates it.

This is the part worth measuring rather than assuming, and we have today's numbers from our own content pipeline.

The model side is not the constraint at all. Over the last days it produced a full set for each post — longread, technical log, two channel versions, three teasers — in minutes each.

Where everything actually waits:

**Platform limits.** Medium allows two publications per rolling 24 hours. We currently have **33 finished texts queued** behind that single rule. At two a day, that queue is over two weeks long, and no amount of agent autonomy shortens it by an hour.

**Rails that require hands.** X and Threads are prepared by machine and posted by a person — one because our API access is not enrolled, the other because there is no valid token and it is a ban-sensitive surface that must originate from one specific machine.

**Physical presence.** A capability we enabled two days ago is applied on **two machines out of six**; the remaining four need a live session on the machine itself, because auto-application is deliberately forbidden for that class of change.

So after taking the human out of the middle, the queue did not vanish — it re-formed in front of the doors. Which means the honest next question is not "how do I make the agent more autonomous" but **"where is the queue now, and is that door openable at all".**

## The failure mode of autonomy nobody warns about

Two of ours, both paid for.

**Undeliverable approvals.** Some decisions genuinely must reach a human — money, irreversible actions, anything going outward. We had **552 such requests fail to reach the person for 16 days.** Nothing errored. The routines ran, the queue grew, and the only symptom was silence, which is indistinguishable from calm. An autonomous system whose escape hatch is broken does not stop; it proceeds. So the rule that matters as much as autonomy: **silence never means consent** — if the question cannot be delivered, the work stops.

**Autonomy without a consolidator.** One instruction fanned out to **at least ten live sessions**; the result was five separate decision memos, seven external review runs on one question, and four dashboards, all answering the same thing, none aware of the others. Every session was autonomous and correct. Nobody merged. Autonomy multiplies output; only a consolidator turns output into a decision.

## What we would actually apply

**Count the human touches.** Not as a feeling — a number, per pipeline, per week. Ours has a target of zero outside the reserved classes, and it is the only way to notice a bottleneck that crept back in.

**Name what stays human, in advance.** Money, irreversible operations, outward-facing on someone else's behalf. That list should be short, explicit, and not expandable on a bad day.

**Measure where the queue moved after each removal.** Otherwise you optimise the agent for a year while the actual wait sits in a platform limit nobody looked at.

And on the last line of the post: converging with someone independently is a decent signal that the idea is structural rather than clever. The interesting distance is not who said it first — it is who has the number for where their bottleneck is today.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
