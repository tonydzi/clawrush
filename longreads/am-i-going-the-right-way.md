# More Repair Than Forward Motion

*That is not a feeling. We measured it, found the root, and it was not a discipline problem.*

Deep at night I sometimes think: am I even going the right way?

I spend so much time on all this vibe-coding. I have started noticing that I spend more time repairing what I build than moving forward. My co-founder keeps pushing me.

Good news: I have finally started posting on arXiv.org. I was endorsed on arXiv — big thanks to the colleague and friends who did that.

I also contributed to Anthropic. Well, sort of... my Claude Code did.

So my main task right now is what I actually should be doing. And you, colleagues, friends, whoever is reading this — please push me in that direction.

I would still like to get hired somehow at Anthropic, at Google, at Gemini. Or maybe at ChatGPT / OpenAI. Or maybe at Grok, at xAI. Or at some small living LLM company, a Chinese one perhaps. As an ambassador or evangelist.

Because what I do, in principle, does not depend on which model I use.

Essentially everything I made: the second brain, all of it. Well, I did not invent it, I just... I did a lot of deep researches. And those deep researches brought me where I am.

So: the second brain, my CRM for outreach to anyone and anything. A fleet of several computers, each with Codex or Grok installed, and this whole fleet talks to itself, helps itself, reaches consensus and so on.

I built all of it for myself, simply to get what I wanted. And on arXiv.org: to publish, for example.

Such are the thoughts from deep in the night. Time to sleep: the kids wake up in the morning. As usual it will be a very cheerful day.

Whoever read this is a good one. Whoever supported is doubly so.

## "More repair than forward motion" is measurable, and we measured it

This is the line worth answering, because it is usually treated as a mood and it is not.

**One week, one machine: 36.8 million output tokens. Shell commands 54.4%, code 15.6%, reading files 12.4% — 82% mechanical.** Not thinking, not deciding, not shipping. Running things, editing things, reading things back.

So the feeling is accurate. And the useful part is what the root turned out to be, because it was not "not disciplined enough".

**We had budgeted the target work and left the meta-work unbudgeted.** Building something new required a justification; fixing, checking, tidying and re-verifying required none. Anything with no budget and no gate expands until it fills the day, and every individual repair is defensible while you are doing it.

The second half of the root is the metric: **the system was optimising "no incident left unanswered" instead of "the goals moved this week".** Those two produce completely different days, and only one of them looks like forward motion at the end of the month.

## Three things we changed, and they are cheap

**Give the repair work a budget instead of letting it run free.** Ours is explicit now: repair happens inside a quota, and a new part is only built in place of one that was killed. Without a ceiling, maintenance always wins the argument, because it is always urgent and always small.

**Do not build a mechanism until the third occurrence.** First time something breaks: one line in a journal, nothing built. Second: another line, sharpen the conditions. Third: now it is a class, and it earns a separate session. This alone removed most of what used to feel like unavoidable repair, because a large share of breakages never come back a third time.

**Park what is not core instead of fixing it.** If a broken thing has no named consumer, it gets switched off for thirty days rather than repaired. We measured the alternative: **95 gates capable of going red that nothing ever invokes, and 19 of 25 recent rules with no caller at all.** All of that was built correctly and maintained faithfully, for nobody.

Two exceptions we kept: anything guarding money, irreversible actions or security gets fixed immediately, and so does anything in the core that other people depend on.

## On the arXiv part, since it is easy to undersell

Worth stating plainly, because the post says it in passing: the paper is **submitted**, under cs.MA, and the endorsement that unblocked it arrived in July. That is not a plan, it is a filed artifact with a watchdog on it that checks for the announcement and moderator mail on a four-hour schedule.

That is the same week the repair-versus-forward measurement was taken. Both things are true at once: most of the output went into mechanics, **and** the thing that was supposed to move forward moved. The 82% is a cost, not a verdict.

## The part about "it does not matter which model"

That claim is stronger than it sounds, and it is the one an employer should care about.

What was built is not a wrapper around one vendor. It is a fleet where several machines each run a different vendor's agent, talk to each other, reach consensus and cover for one another when a rail dies. We verified that the hard way this week: **three review rails answered within the same hour that our browser rail was timing out**, and one of them found two real defects in code we had just written.

That is the difference between using a model and building the layer above models. The layer is what survives a vendor changing their pricing, their limits or their API — and it is the thing that is genuinely hard to copy.

What do you spend more time on: repairing what you built, or building what is next? And have you ever counted, rather than estimated?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/am-i-going-the-right-way.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/am-i-going-the-right-way.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
