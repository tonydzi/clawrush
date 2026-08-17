# 95 Automations, 4 Do Everything

*Counting runs is the easy half. We ran the harder count on ourselves, and it looks worse.*

Today's insight was about my automations again.

I counted my automations in n8n. There are **95**.

In the last 30 days, **11** ran at least once. **Fifty-seven never ran at all.**

And **99.8% of all runs come from four of the 95.** The two most loaded are the alarm-clock and the watchdog: one wakes a machine when a message for it arrives in the work chat, the other checks the machine is still alive (my agents from all the laptops talk to each other in a shared chat).

I am automating something wrong. Not the thing I actually use.

## The distribution is the finding, and it is not a personal failing

Four of ninety-five producing 99.8% of runs is not sloppiness, it is the normal shape of any workshop where building is cheap. Each of the 57 was worth building on the day it was built. The mistake is not creating them — it is **keeping** them, because every one carries a permanent maintenance line: it breaks on an API change, it needs credentials rotated, it shows up in every audit.

So the useful move is not "automate better next time". It is a **kill date**. Ours: a thing with no runs and no named consumer in 30 days is switched off, not repaired. Parking is reversible and free; maintaining 57 sleeping automations is neither.

## Our own numbers, and why the flattering one is the wrong metric

Same count on our side, scheduled tasks on one node: **49 tasks, 46 enabled, 45 ran in the last 30 days.**

That looks excellent, and it measures almost nothing. **"It ran" is not "someone used the output."** A job that fires nightly and writes a report nobody opens has a perfect run history and zero value — and worse, its silence is indistinguishable from health.

The count that actually hurt, when we finally took it: **95 gates capable of going red that nothing ever invokes**, and **19 of 25 recent rules with no caller at all**. All correctly built. All maintained. For nobody.

That is the same disease as 57 sleeping automations, one layer up: the sleeping ones are visibly idle, the ones with no consumer *look busy*.

## What we changed

**A counter on usage, not on invocation.** Every live part writes a line when it is used, and the line records the outcome, not just the call. Read at retro. Zero uses in 30 days makes it a candidate for the scrapheap, and that is a decision, not an accident.

**A named consumer before it gets built.** Who reads this output, and what changes for them when it arrives? No answer, no build — or build it as a time-boxed probe with an automatic kill date. This one rule prevented more work than any other we have adopted.

**No mechanism before the third occurrence.** Most automations are built to prevent a thing that happened once. Our breakage journal: 39 incidents, 19 classes, **17 of those classes happened exactly once and never returned.** Building on the first occurrence would have produced 19 mechanisms where 2 were needed.

## On the two most loaded being the alarm clock and the watchdog

That detail is the most interesting line in the post and it is worth staring at: **the busiest automations serve other automations.** Waking machines, checking machines are alive. Infrastructure keeping infrastructure upright.

That is partly correct and healthy — a fleet does need a heartbeat, and a watchdog *must* live outside the thing it watches, which by construction makes it separate and busy. But it is also the number to watch: if the ratio of self-maintenance to work-that-touches-the-outside-world keeps climbing, the workshop has become the product. We measured our version of that too — in one week, 82% of output went to mechanical work.

So the honest reading of "I am automating the wrong thing" is not that the alarm clock is wrong. It is that **an automation that feeds a person is worth ten that feed each other**, and only one of those two kinds is easy to build.

How many of your automations ran this month? And of those that ran — how many produced something a human actually read?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
