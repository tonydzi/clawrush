# The Interface Disappeared. The Reviewer Did Not.

*The saving is real and we can show where it lands. So is the bill that replaces it — and ours is measured.*

I am thinking now about how much time and money it would have taken me to do what I am doing now single-handed: with three Claude subscriptions, two ChatGPT subscriptions, one Grok and one Gemini.

I started building an investor CRM in 2020. By 2026, when I finally came to vibe-coding, about two million dollars had been burned. And there was still a great deal left to do.

The thing is, that CRM was for people. What mattered was not only the backend but the interface for humans. And now, thanks to Claude and the LLM, the interface is not needed: it can do the same functionality without bothering with an interface at all.

So I have moved a great deal. Over a few months of vibe-coding I am moving in giant steps by my standards. Because of that we have saved years and probably hundreds of thousands, maybe closer to millions.

And the main thing is not only time, but nerves. Look how much you have to squeeze out of programmers, verify that they did everything right. You have to tolerate their need for work-life balance and so on.

Claude Code, or in principle any other LLM like Codex, replaces not only real engineers and saves a pile of money — it saves a pile of nerves. And the fact that you would replace an engineer even at 5-10k a month does not mean you solve all your problems. Your engineer will also want a personal life, everything they do will need re-checking, and so on.

In short, the era of engineers is over.

## The interface observation is the sharpest thing here

"The interface is not needed" is the part worth extracting, because it explains where the money actually went.

A CRM for humans is mostly not business logic. It is forms, tables, states, empty states, validation messages, permissions rendered as buttons, mobile layout, and a designer arguing with a developer about all of it. When the consumer is an agent, all of that collapses: the same functionality is a database and a set of commands. The saving is not "the model writes code faster" — it is that **an entire product surface stopped being required.**

That is a structural change, not an efficiency gain, and it is why the numbers feel implausible until you see which part vanished.

## Where our own week actually went

We measured the same shift on ourselves, and the split is instructive.

**36.8 million output tokens in one week on one machine. 82% of it mechanical** — running shell commands, editing code, reading files back. That is precisely the work the post is talking about: typing, wiring, checking syntax, the part a person used to be paid for.

So the "replacement" is real and it is concentrated in the mechanical layer.

## And here is the bill that arrived instead

Every one of these is ours, dated, and none of them was caught by a model:

**552 approval requests failed to reach a human for 16 days.** Nothing errored. The routines ran, the queue grew, and the only symptom was silence.

**146 tasks were switched off in five seconds**, watchdogs included, because a mass instruction was executed literally.

**One instruction fanned out to at least ten sessions** and produced five separate decision memos and four dashboards, all answering the same question, none aware of the others.

**95 gates capable of going red that nothing invokes**, and **19 of 25 recent rules with no caller at all.**

That is the honest shape of it: **building got cheap, and staying correct did not.** The engineer's expensive part was never the typing — it was noticing that something silently stopped, that a fix was applied to a symptom, that a fifth version of the same answer had appeared. That role did not disappear. It became less visible and therefore easier to skip.

## On nerves, which is the part I would push back on hardest

An engineer who wants a personal life is a constraint you can see. An agent has no work-life balance and also no discomfort — it will not tell you it feels wrong, will not push back on a bad decision unless you built something that does, and will not notice that it has been producing output nobody reads for a month.

We measured that last one specifically. The parts nobody invoked were not built badly; they were built correctly and quietly, at full speed, forever.

So the nerves are not saved. They are **relocated**: from managing people to noticing silence. And silence is harder to notice than a person saying no.

## Where the queue is now

After the mechanical layer was automated, our wait did not disappear either — it moved. **33 finished texts sit behind a platform rule allowing two publications a day. Two rails still need human hands. A capability enabled two days ago is live on two machines out of six**, because applying it requires someone physically at each machine.

None of that is fixed by a smarter model.

**So: the era of the interface is over, and that is worth the money it saves. The era of the reviewer is not — and the review is now the whole job.** It just does not look like engineering any more, which is exactly what makes it easy to cut.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/the-interface-disappeared.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/the-interface-disappeared.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
