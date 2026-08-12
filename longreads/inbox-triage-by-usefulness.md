# Triaging the Inbox by Usefulness, Not by Warmth

*Anton's design for an inbound skill. Plus the three measurements that changed how we do this.*

I need a skill, or a series of skills, connected to the other connect rules.

The first skill checks inbound messages: in groups, in Telegram, in WhatsApp, in any other messengers.

Then another skill, or the same one: keep the conversation going.

Since keeping a conversation going costs us money, we need to understand how important it is. If it is important, we write a meaningful message with an expensive LLM. That is, we roughly see the person's status, how important they are to us and so on.

We have a call to action. Right now it is built around good work at a large company, and around our engineering community. If it is an investor, we can offer them to invest in the lab or in the projects we help.

So we have determined a branch: say the person is not interesting to us. But since they wrote to us anyway, it would be a shame to throw that usefulness away. We say: dude, what you write is cool. We are building such and such a product. Read us, in Russian, in English. Here is everything we do: our Twitter, our GitHub. Read, subscribe and build with us.

Of course the conversion will be small. But since people wrote to us themselves, why not just send them a message to call them into our faith.

If it is a person interested in engineering, code, Claude, Codex and so on, we say: dude, subscribe to our GitHub, Twitter, our channel. Write there, tell us how it is going for you.

In general, if we need to, we also try to bring them into our faith. But at the same time we try to give them what they want. That is, we ask classifying questions: what do they want, and we try to give them something useful.

Since a lot of people write to us, we have a giant backlog and we will try to typify the questions and answer them en masse.

I repeat: we answer properly only to the people who matter to us, my subscribers, VIP leads, investors. And if a person does not matter, that is different.

For this we need our ranks to be not only the "temperature" of people, but also their usefulness. In this case, usefulness to us, because we have different kinds of usefulness: usefulness as an investor, as an engineer, as someone else.

Right now we need engineers or investors. And maybe we need not only engineers, but beginner engineers, university adepts, the ones who will spread our faith in their city.

Of course we are not a church, but when I say "faith" I mean getting subscribers. When I get a follower, that is our faith.

We need the actions to be easy. If a person just needs to star our GitHub or subscribe, that is not a super high quality result, but I am absolutely fine with it. If a person came from GitHub, that already means something.

So we need a skill for parsing the inbox. Then working with the data, especially in terms of the quality those people can give us. That is, from the value they can give us and from the direction we are moving.

We need to work out these two skills and put them on automatic runs. Because I do not manage to sort through incoming messages, and it needs to be done every day.

## The split that makes this work: temperature is not usefulness

The core idea here is the one worth stealing, and it is stated almost in passing. Most CRMs rank people by **temperature**: how warm the conversation is, how recently they replied. Anton wants a second axis, **usefulness**, and specifically usefulness *of a named kind*: as an engineer, as an investor, as someone who will bring their city with them.

Those two axes are genuinely independent, and conflating them is the standard mistake. A warm conversation with someone who cannot help you is pleasant and costs you the afternoon. A cold message from an engineer with live commits is the more valuable one, and warmth-ranking puts it at the bottom.

Our version of that rule is blunter: we spend the founder's time, the intro, the audience, on people who can give something back in the next ninety days. And the crucial qualifier: **usefulness is capability, not fame.** An unknown engineer with real commits outranks a well-known name asking for an intro. Status-hunting looks like networking and is not.

## Three measurements that changed our version

**One.** We checked every inbound reply under our own Telegram posts in August: 114 messages across both channels, 35 cases. **Zero replies.** The instrument was verified against a foreign post where comments definitely exist, and it returned 20, so the zero was honest. The cause was structural: on one channel discussions were never connected, so the "comment" button does not exist for readers at all. **Before building a skill to process inbound, check that inbound can physically arrive.**

**Two.** Our dashboard showed 28 unanswered comments, and we treated it as debt for a while. On inspection all 28 were in someone else's group, more than a month old, where our access had lapsed. Not our debt, and answering them a month late would have been worse than silence. **A backlog counter with no age and no ownership generates guilt, not work.**

**Three, the one that hurts.** We once sent a batch of similar replies to many people at once. It read as cringe and converted nothing. The single specific offer to one person converted. So Anton's "typify the questions and answer them en masse" is exactly the place we would put a guardrail: **typify the ROUTING, never the wording.** Classification into buckets is cheap and correct; the sentence a human reads must be about them, or the effort is worse than wasted.

Our formulation: loudness is one accurate message through the right door. Spam is the same message fanned out through every door. The difference is invisible in your metrics and instantly visible to the recipient.

## On spending the expensive model only where it matters

This part we already run and can confirm it works. Routing is by task, not by importance of person: mechanical extraction, classification, deduplication go to the cheap model, and judgement, synthesis and anything written in a real human voice go to the expensive one.

Two caveats learned the hard way. First, **the quality gate wins over the savings**: if the cheap model's output is below the bar, the piece escalates rather than ships. Second, and more relevant here: **for the outbound sentence itself, always use the expensive model.** A generic reply written cheaply to save money is the exact thing that produces the cringe batch above. The saving is real and the damage is larger.

## The part we would build first

Not the reply skill. The **collection and the ledger**: who wrote, where, when, matched to a card, with the two ranks stored separately. That is boring, cheap and blocks everything else — including the ability to tell later whether any of it worked.

And the metric to hold it to: not messages sent, not follows gained, but **replies received from people you engaged with.** A follow is cheap to buy and proves nothing about whether the person will ever build with you. A reply is a state change.

How do you rank the people who write to you? By how warm they are, or by what they can actually do?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/inbox-triage-by-usefulness.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/inbox-triage-by-usefulness.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
