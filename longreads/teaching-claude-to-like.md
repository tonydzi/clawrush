# Teaching Claude to Like

*Presence in a feed is work, and work can be delegated. Where that stops being true is the interesting part.*

I am going to teach Claude: every time he publishes some content on Facebook, he likes it straight away. My content on Facebook.

Then he will like all the comments people wrote to me, because I do not have enough time for that myself right now.

And then my replies to those comments, he likes those too. Liking your own comment is fine as well.

So: my posts, he likes all of them. My comments, he likes all of them. Comments to me, he likes those.

I also want to set it up so he can go into the profiles of exactly those people I have had calls with, for example. That needs to be a separate activity. And like their content there.

Not everyone indiscriminately, but precisely the people I have a conversation running with in Facebook Messenger or Telegram.

Given that all my leads are merged, their Telegram equals their Facebook. So I know both.

And I will set it up so that every day, or once a week, he likes 5 to 10 random people from that list. Not ten every single day.

In short: every day he should have an activity, go into Facebook and like various leads. From everyone I have had conversations with.

## The part worth separating out

There are two different ideas in that post, and only one of them is about automation.

The first is **acknowledgement as a real task with a real cost.** Someone writes a comment under your post. Reading it takes five seconds; the person waited for something back. Multiply by fifty comments a week and it becomes work you genuinely do not have time for, which is exactly what Anton says. It then silently does not happen, and the person who commented concludes you did not care.

The second is **a selection rule.** Not everyone indiscriminately: people with a live conversation running. 5 to 10 from that list, some days, not ten every day. That constraint is the whole design, and it is the difference between presence and spam.

We have a rule for this in almost the same words: loudness is one accurate message through the right door, spam is the same message fanned out through every door. A like is the smallest possible message, and the same rule holds.

## Where we drew the line, and why

Here is the honest part, and it is a disagreement rather than a footnote.

**We do not automate the likes themselves.** Not because it is technically hard, it is trivial. Three reasons, in order of how much they cost:

**It is against the platform's rules.** Automated interaction from a personal account is exactly what Meta's automated-behaviour detection exists for. The account at risk is Anton's own, with a decade of leads and conversations in it. Nothing gained from a like is worth that account.

**A like from a robot is a lie about attention.** The entire value of the gesture is "a person saw this". A liked comment tells the author they were noticed. If the like was placed by a schedule, the signal is counterfeit, and the counterfeit is indistinguishable from the real thing until someone finds out, at which point every past like is retroactively worthless.

**Acknowledgement is the cheapest thing a founder can do personally.** If the goal is warmth, delegating warmth is self-defeating in a way that delegating research is not.

What we automate instead is **everything except the click**: collecting who commented, matching them against the CRM, showing who is a live lead versus a stranger, flagging who is waiting on a reply from you and for how long, and putting the ten profiles worth visiting today into one list. That turns forty minutes of scrolling into two minutes of clicking, and the clicks stay human.

That distinction generalises: **automate the finding, keep the gesture.**

## The part of his idea we did take, immediately

The lead-merging Anton mentions in passing is the load-bearing piece, and it deserves more attention than the likes.

"Their Telegram equals their Facebook" means one person has one card, not three ghosts across three platforms. Without it, a rule like "engage with people I have a live conversation with" cannot be executed at all: you would be guessing whether the Facebook profile and the Telegram handle are the same human.

That merge is unglamorous, it is the least interesting part of any CRM, and everything downstream depends on it. Ours is built the same way, and the one thing we would warn about: **a handle is not a person.** Same display name across two platforms proves nothing. Merge on evidence — a shared link, a message where they name the other account, a call you both attended — and leave everything else as a suggestion until confirmed.

## What we would build if we built this today

A daily list, not a daily robot:

- who commented since yesterday, with the CRM card attached and the last time you spoke;
- who is waiting on a reply from you, sorted by how long;
- 5 to 10 profiles worth opening today, chosen from people with a live conversation, rotating so nobody gets visited twice in a week;
- everything a link, so acting on it takes one click.

Cost: a few minutes of compute. What it saves: the forty minutes of scrolling that stop the gesture from happening at all.

And the metric that matters is not likes given. It is **replies received from people you engaged with.** Likes are cheap to produce and prove nothing; a reply is the state change that says the presence landed.

How do you keep up with the people who talk to you? And what part of it have you handed to a machine?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
