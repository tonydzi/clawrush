# Should This Have Been a Skill?

*We ask that at the end of every session. Here is what the question produced, including the part we cannot answer.*

Every time I close a session and sum up everything I did in it, I think the session should be asked: is any of what I just did worth turning into a skill? And if a skill for it already exists, is it time to upgrade it?

A /retro command that ends by asking: does everything we did add up to a skill? And if the skill already exists, should it be improved?

How about you? How often do you revisit your skills?

## What the question built

That question sits at the end of our session retrospective, and it has been running long enough to have a count. On this node: **161 skills, every one of them with a written passport.** 157 of the 161 were touched in the last 30 days.

The mechanism is simple and worth copying. The retro does not ask "was this session good". It asks a narrower question with a testable answer: **did anything repeat?** A step done twice in one session, or once in three consecutive sessions, is a candidate. Everything else stays a one-off, which is a legitimate outcome and the most common one.

Upgrading beats creating. The second half of the question, *if a skill already exists, should it be improved*, is the half that keeps the count from exploding. A new skill is the expensive answer: it needs a name nobody confuses with the others, a passport, a test, and a home. Adding a line to a skill that already runs is nearly free, and most sessions produce that kind of lesson, not a new tool.

## The part we cannot answer

Now the honest half, and it is the reason this post is worth publishing rather than just the count.

**Not one of those 161 skills counts how often it is invoked.** We have a shared usage log for components on this node. It contains **12 records covering 2 components**, and neither of them is a skill.

So when the question comes back, *how often do you revisit your skills*, our answer splits in two. We revise them constantly, 157 of 161 within a month, and that is measurable. Whether they are USED is not measurable here, because nobody built the counter.

That gap has a specific shape. A skill that is written, documented and current looks alive from every angle we have instrumented. Freshness measures our attention, not the skill's usefulness. The two look identical on a dashboard and mean opposite things: an obsolete skill that someone keeps tidying scores better than a workhorse nobody has edited in two months.

We have a rule that every live component must count its own invocations, and by our own rule most of these 161 are out of compliance. Writing that down is cheaper than pretending the number does not exist.

## Two traps to avoid if you build this

**Count the use, not the tool call.** Our skills are frequently executed by routines that simply read the skill file rather than invoking it through a tool. A counter hooked to tool invocations reads zero and declares a heavily used component dead. Instrument the state change that follows the work.

**Print the age of your data, and never judge a component younger than the window.** A skill built nine days ago cannot lose a thirty-day usage contest. An audit that does not state how far back it looked is a verdict without jurisdiction.

## What we would do differently

Build the counter with the first skill, not after the hundredth. Retrofitting a hundred and sixty-one components is a project; adding one line at birth is not. Every component we did instrument from day one has an honest usage history, and every one we planned to instrument later still has none.

So the question at the end of the retro is right, and it is incomplete. *Should this be a skill?* needs a companion: **who will call it, and what will prove they did?**

How often do you revisit your skills? And do you know which of them anyone actually runs?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
