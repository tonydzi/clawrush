# Credit the Person Who Gave You the Idea

*We built the ledger for this. Twelve entries in, here is what it changed and the one place the pipeline is broken.*

I am still setting up the process where every time I make some improvement, I am grateful to whoever advised us something. And I need to manage to thank the person out loud, in DMs, or tag them, so they know their advice turned out to be very useful.

I need an "alpha mining" engine set up for comments — I am improving it right now.

The comments people give us in our Telegram chats @ClawRus and @ClawEng, plus the comments under my Facebook posts, and possibly comments in our GitHub, are what I see and what I manage to evaluate.

From all these comments we mine alpha: we take all the advice we were given and try to apply it. We apply it, run some kind of test mode and so on, and evaluate how useful it is.

And whenever we have applied something — any function, any trick — I want to publicly write back to that person: thank you very much for advising us this thing, we applied it, we are testing it now and will let you know how relevant it turns out to be and how it works in general.

So we do not just start applying it publicly, we also always record in our skill, in our function, that this was advised to us.

And I need to mention these smart people later in the repository and elsewhere too.

That is, we are building an open-source product, and if someone contributed something — even an idea — we always state that this idea was thought up by such and such a person, and we say a big thank you for it.

## We built the ledger. Here is what it looks like twelve entries in.

This is not a plan on our side, it is running. **Twelve pieces of advice recorded, nine already credited publicly, three still owed.**

Real ones, so this is not abstract. One reader told us to give our retrieval layer an additivity invariant so a long chat stops losing context. Another argued against full recall of everything and described a layered version: a short briefing at session start, then targeted retrieval, top-20 narrowed to five or ten by reranking, and a second clarifying pass when confidence is low. A third pointed us at two mature open-source projects doing our eval harness better, and criticised our headline for promising something we did not measure.

Every one of those is a named person with a dated line. That is the whole mechanism: **the ledger is what makes the thank-you possible later, because you will not remember.**

## The three fields that matter

**Who, verbatim what they said, and what happened to it.** The third field is the one everybody drops, and it is the one that makes the reply worth reading.

There is a real difference between "thanks, great idea" and "we took your rule about the invariant, applied it here, and it changed this". The first is politeness. The second tells the person their thinking had a consequence — and that is what makes them come back with the next idea.

It also forces honesty about the advice you did **not** take. Three of our twelve are still open, and marking them as owed rather than quietly closing them is the difference between a ledger and a decoration.

## Say thank you before the verdict, not after

One correction to the plan in the post. Anton's script is "we applied it, we are testing, we will let you know". That is right, and the timing needs to be earlier: **acknowledge on receipt, report the outcome later.**

If you wait for the verdict, the acknowledgement arrives three weeks after the person forgot the conversation, and half the time it never arrives because the test got parked. Two messages, not one: a short "taken, we are trying it" the same day, and the result when you have it.

## What this actually buys

Not karma. **The next idea.** A person who sees their advice named in a repository sends the second one. A person who gets silence assumes it went nowhere and stops.

The measurement we can offer here is indirect but honest: we shipped **eight pull requests and got a response to exactly one** — the one that closed an issue somebody had already opened. Cold contributions into silence get ignored, and so does advice given into silence. The direction of that arrow does not change when you are the one being advised.

## The broken part, and we would rather say it

The post lists our Telegram chats as a source of comments. We audited that this week: **114 posts across our channels in August, zero replies.**

The instrument was control-tested against a foreign post where comments definitely exist and it returned twenty, so the zero is real. The cause is structural: on one of our channels discussions were never connected, so the comment button does not exist for readers at all. On the other, discussions route to a chat that has been paused since the 10th.

So the alpha-mining engine has a live source in Facebook and GitHub, and a dead one in Telegram. **Before improving a collector, confirm the channel can physically deliver anything into it.** We were about to build the smarter miner on top of a feed that is structurally empty.

One related thing worth knowing: our dashboard once showed 28 unanswered comments and we treated it as debt. All 28 were in a third-party group, more than a month old, where our access had lapsed. A backlog counter without age and ownership produces guilt, not work.

## What we would build, in order

1. **The ledger first** — who, verbatim, what happened. Boring, cheap, and everything downstream depends on it existing.
2. **Acknowledge on receipt**, same day, one line.
3. **The credit line in the code**, next to the function the advice changed. That is the part nobody can fake later.
4. **The public thank-you with the outcome**, when there is one.
5. Only then a smarter miner — and only on sources that actually carry comments.

Do you know who gave you your last three good ideas? And did they ever find out you used them?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
