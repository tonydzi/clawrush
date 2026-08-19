# Where the Co-founder's Personality Should Live

*One file is elegant. Ours is split in four, for reasons that cost us a measurable amount of context every session.*

I need to run another deep research.

In OpenClaw there is a file called soul.md. The personality of that LLM is written in it. I have something similar: the co-founder's personality, which I recently reworked and made more like a successful programmer on GitHub.

I would run deep research on who does an analogous thing in which harnesses — writing out the personality of an AI, of a co-founder, of a copilot. And I would put the whole co-founder personality into a soul.md file. I would also look at how it is implemented on my side: as a skill, or as something else. I would format all of it similarly to how other harnesses do it — but without making what I have worse; rather, maybe improving it and thinking it through more carefully.

## The question "a skill or something else" has a precise answer

It comes down to one property: **is this loaded on every session, or only when needed?** That single distinction should drive the split, because the always-loaded part is charged forever.

Ours is split in four:

**Identity and voice** — always loaded. Who this is, how it speaks, what it refuses. Small by construction, because everything here is paid on every session.

**The floor** — always loaded. The non-negotiables: what always requires a human, what never leaves the machine. Short, and separate from voice on purpose, because voice can be shared publicly and the floor cannot.

**Who the human is** — the person's profile, preferences, working style.

**Which machine this is** — the node's profile: what this box is allowed to do, what lives on it.

And the rule that binds them: **rights are the intersection of the person and the machine**, not the union. The same personality on a different node has different permissions, and that only works if the two profiles are separate files.

Everything procedural — how to run a review, how to publish, how to answer a lead — lives in skills, invoked when the task arrives. That is the answer to "skill or something else": **identity is prose loaded always, procedure is a skill loaded on demand.** Putting procedures into the personality file is the common mistake, and it is expensive in a way that is invisible.

## Why the split is not cosmetic: the always-loaded layer is rent

Here is the number that changed how we think about this.

**The median session on our machine starts at 103,574 tokens** — measured across 180 sessions — before a single word of work. It has been growing: 104k, then 119k, then 147k on the worst day. That is standing instructions, always-loaded files, tool definitions.

Two costs, not one. The obvious one is money. The less obvious: if a model works best while a limited share of its context is occupied, then every line of permanently-loaded personality also consumes the part of the window where the model still thinks sharply. **A rule added to soul.md is paid twice — in tokens and in headroom — on every session, forever.**

So the discipline is not "write a beautiful personality file". It is: **what earns permanent residency?** Identity does. The list of banned words does. A four-step procedure for handling a specific platform does not.

## The failure nobody expects: a personality with no caller

We measured this on ourselves and it was uncomfortable. **Nineteen of twenty-five recently adopted rules had no caller at all** — nothing invoked them, nothing checked them, nothing went red when they were ignored. They were correctly written and completely inert.

Personality rules are the worst offenders, because prose does not invoke anything. "Speak plainly, avoid jargon" sits in a file and hopes. What makes it real is a door: a check that runs, a gate in the publishing path, a step in a skill that reads the rule at the moment it matters.

So the test we now apply to every line of a persona: **what would go red if this were violated?** If the answer is nothing, the line is a preference, not a rule — and it should be labelled as such rather than pretending.

## And one honest thing about our own setup

We have a builder that assembles a newcomer's kit from those four parts. Except: **the builder itself is no longer on disk** — only its output survives in a transit folder. So kits are currently assembled by hand, and have been since late July.

Which is a fitting illustration of the whole post: the design was right, the artifact outlived the tool that produced it, and nothing complained. Worth checking, before the deep research, whether the thing you are documenting still has a working producer.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/where-the-cofounder-personality-lives.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/where-the-cofounder-personality-lives.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
