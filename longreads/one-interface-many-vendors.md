# One Interface, Many Vendors

*The answer is not a unified UI. It is a routing table, and we already run one.*

I have a pain.

I have two ChatGPT subscriptions, and I barely use it. I use ChatGPT for deep research, but the tokens that could go into coding just burn away unused.

In Claude Code I have three subscriptions. And of course all three run out instantly.

Right now I want to slowly move over to Codex, so I can do coding in Codex as well.

But I do not want to live in each tool separately.

Maybe there are already unified interfaces where you turn on one interface and everything is under the hood?

One interface. One session. And inside each session I pick what to work in: Codex, Grok, Gemini, GLM, ChatGPT and so on.

I need an interface like that.

I have started thinking about Hermes and the open claw, OpenClaw, but recommend me something.

How do I burn down my limits in Codex?

## What people suggested

The comments carried real answers, and the people who gave them get named, because an idea handed over for free is still a contribution.

**Andrei Khvetkevich** runs Claude and Codex in parallel on the same task, one doing and one checking, or on separate tasks in separate branches through the same GitHub. **Vadim Babenko** does everything in Codex with Claude Code as reviewer and critic, moving work across by hand, and adds the part worth quoting: fully autonomous agent-to-agent collaboration without a human failed on hard tasks, because the pair sits in a circle endlessly optimising a dying idea. On simple work it holds. **Emil Musayev** points at Buzz from Block, which aims at exactly this: one shared environment for agents and humans across GPT, Claude and Goose. **Alexander Fedorenko** uses the Codex interface with models swapped per session, context and history preserved. **Petr Asratyan** suggests OpenWebUI, **Sergey Glukhota** says this is just Cursor, **Genia Lari** says VS Code, **Ihar Paliashchuk** suggests offloading part of the tasks to Sol. **Johnny GiliPsy** made the sharpest procedural point: ask the idle model itself to research this, since it is sitting there unused anyway.

We have not tested most of these and are not going to pretend otherwise. Naming them is credit, not endorsement.

## What we run, and why it is not a UI

The thing that fixed this for us is not an interface. It is a **routing table plus a rule at design time**.

The rule: every component we build carries one line in its passport naming **which paid tank it burns**. An empty line means it does not ship. "Claude, because the caller is Claude" is a design defect, not an answer.

The split that survived contact:
- **stays on the expensive rail**: orchestration, judgement, voice, live dialogue, anything touching the private vault
- **designed onto a cheaper paid rail from the start**: shell, code, bulk reading, extraction, first drafts, deep research

Default executor is **the rail with the most headroom right now**, measured, not the habitual one. And every class of work needs a second live rail, otherwise the first outage is a blocked pipeline.

Concretely, the piece that answers "how do I burn down Codex": a small dispatcher that takes a text task and fires it at codex, grok, gemini and claude **simultaneously**, first useful answer wins. No new UI, no new session model, no context migration. The work goes where the fuel is.

Why we built that instead of a unified front-end: the measurement. Over seven days on our hub, **36.8M output tokens, of which shell 54.4% + code 15.6% + reading 12.4% = 82% mechanics** — while a paid subscription from another vendor in the same toolbox sat at **4% consumed** and two more paid rails had never been measured even once. The tokens were not scarce. They were misrouted.

## The trap inside "one interface"

A single front-end that hides which engine answered is genuinely dangerous, and we learned it the expensive way.

When one rail is down and the interface quietly falls back to another, you get **fake independence**: you believe two engines agreed, and in fact one engine answered twice. In a second-opinion workflow that is worse than having no second opinion, because it manufactures confidence. Our rule now: an unknown or unavailable engine is a **skip, stated out loud**, never a silent fallback, and a run with a skipped rail can be graded warning at best, never green.

Corollary, also learned the hard way: **one closed door is not a dead vendor.** We declared a rail dead based on the wrong entry point; it was alive through its own door, answered in one second, and then found two real defects in our fix that we had missed.

So: yes to one place to launch from. No to one place that hides who answered. Any unified layer worth adopting has to keep the engine name attached to every answer, and log the ones that stayed silent instead of quietly dropping them.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
