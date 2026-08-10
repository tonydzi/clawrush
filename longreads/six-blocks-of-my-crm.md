# Six Blocks of My CRM

*A working outreach system, described by the person who runs it, plus the blocks we found missing.*

Here is a short description of how my CRM is built. Six main blocks.

**1. Gatekeeper.** Auto-greeting and approving join requests. It sits in all of our Telegram groups, and we have a lot of them, and it writes to every new member in private: hey, what do you do?

**2. Campaigns.** Templated campaigns by filter, bulk messages.

**3. Tapping, or finishing off.** Important: tapping is not follow-ups. You take the last message the person did not answer, and you send it again. Not every minute, but, say, once a day for a month. No answer in a month, we forget them and mark that tapping did not work.

**4. Intro groups.** I am currently reworking intros, filling them out so that an intro becomes a full object in the CRM rather than a one-off "introduced them and forgot".

**5. Cold messages.** That is when you write to someone you have never talked to before. There is a big risk of a ban here, so we barely do it: 2-3 cold messages a day per account, no more. This is not mass spam. And we try to break the ice immediately: hey, we have a lot in common, we are in the same group, I wrote because I saw you posting about such-and-such.

**6. Member analyzer.** Every group has a core of people who talk a lot. We find the most active ones, look at what they talk about, and prepare a super-customised message for each of them.

And then the lead base itself, which I built over years and inside which the main conversations happen.

And the most important thing on top of all this: you need to know as much as possible about a lead, and every lead must carry tags.

What blocks would you add?

## What we would add, and why

The six blocks above are all **outbound**: they describe motion from us towards a person. Every one of them assumes we initiate. Run that system for a while and you notice the gaps are all in the other direction.

**Inbound has no block at all.** Someone comes to you on their own, and there is nowhere for them to land. We measured this on ourselves in August: five pull requests from three strangers sat untouched in our repository for four days, because nobody owned the question "did anyone knock". A person who arrives by themselves is the most qualified lead in the entire system, and they were the only category with no owner, no queue and no clock. The block is boring to build and it beats every campaign: a queue of inbound touches, a deadline for the first reply, and a card created before the reply is written, not after.

**There is no block that says why this person is worth our time.** The system knows how to reach anyone. It does not know who deserves reaching. Tags describe what a person *is*, and that is not the same as what they can do in the next ninety days: write code, buy, introduce, teach us something. Without that field the pipeline optimises for volume, because volume is the only thing it can measure.

**Tapping has no proof, only a counter.** A month of daily repeats ends in "tapping did not work", which sounds like a fact about the person and is actually a fact about our message. Same text thirty times is thirty attempts at one hypothesis. The cheap fix is not more taps, it is recording *what changed* between them, so that "did not work" carries a reason.

**Nothing in the six blocks decays.** A lead card is knowledge, and knowledge goes stale at its own speed: a job title from two years ago, a company that no longer exists, a verdict "not interested" from before we shipped the thing they said they needed. Without a date of relevance on the card, the base grows and quietly gets less true. The rule that saves it is small: a verdict about a person expires unless it carries a date and a stated way to re-check it.

**And there is no block for the person who already said yes.** Everything here ends at the reply. The conversation that actually pays is the one after it.

One honest note on block five. The 2-3 a day is not a growth tactic, it is a bound on damage: cold outreach has a ban risk attached to the account, and the number exists to keep a bad afternoon from costing the whole channel. Anyone reading this as "do 2-3 and scale it up" has read it backwards.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/six-blocks-of-my-crm.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/six-blocks-of-my-crm.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
