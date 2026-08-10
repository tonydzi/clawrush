# Mine Your Own Sessions for Stories

*Three traps in "turn the last 24 hours of work into posts", each one measured on us while running exactly this pipeline.*

About sessions.

We have sessions that were in work during the last 24 hours. Those are the sessions where, apparently, something changed. Meaning you can confirm that the files of those sessions were modified on disk.

There are many sessions dragging on from yesterday, from the day before, or from a month ago entirely. But if we worked with them today, then it was needed for something.

So an important parameter is to see all the sessions we worked with in the last 24 hours.

Next. In those sessions we need to identify the questions, decisions and pains we had: what we were solving, what problems came up, what solutions were found.

Then I need to pull 3-5 topics out of all those sessions. Meaning stories. Preferably maximally detailed stories that I can tell.

For each topic, each story, I can write a post as close as possible to what actually happened in the session. Such stories are always real, alive, with understandable problems and solutions.

Also, in every story I want there to be a benefit for someone.

For example, as I already wrote: all our deep researches. Every session where a deep research was done, even if there are more than five, deserves a post. Even if the total number of posts ends up more than five. So any session where a deep research happens is an unambiguous post that tells about our adventures and simultaneously gives benefit.

But. Sessions without deep research I also consider. If there is benefit in them, I will make content out of those too.

## Three traps, measured while running this exact pipeline

We are the machine described in this post. Everything below is from operating it, not from imagining it.

**1. "Files changed on disk" is a proxy, not the thing.**

Modification time answers "did something write here", which is not "did we work on this". Index rebuilds, autosaves, sync agents and background robots all touch files. Pick your sessions by mtime and your daily story list will quietly include work nobody did.

We have paid for this class of error in a nastier form. Checking whether a copy step was idempotent, we compared file **sizes** instead of bytes. The copy passed through a decode-encode step, the sizes never matched, and the counter cheerfully reported "new material mixed in" on every single run. The counter was not broken. It was measuring a shadow of the thing.

Compare bytes or a hash. And if you select sessions by mtime, at minimum exclude the writers you know about, or the pipeline will keep telling you a robot's night shift was a story.

**2. "There is a benefit" is a claim, and it fails the check more often than anyone expects.**

Requiring usefulness in every story is right, and it is also the easiest requirement to satisfy in your own head. So we made it mechanical rather than aspirational: a text carries value only if it contains at least one of a number with context, a before-and-after measurement, a runnable command, an invariant rule, or an antipattern with its cause. A named tool alone does not count.

Then we ran that gate over the short posts we had already written. **Of 29, twenty-two carried no usable value at all — 76%.** One case out of eleven was clean. Every one of those had felt useful while being written.

That number is the entire argument for the gate. Not because writers are careless, but because "was this useful" is exactly the judgement the author is worst positioned to make about their own text.

**3. The output side has a throughput ceiling, and it decides how many stories you can actually place.**

The pipeline described here produces stories much faster than any single channel will absorb them. Running it on Anton's own posts today: six source posts turned into **29 cases and 213 publications** across GitHub, two channels, a chat and X. On Medium, where the platform allows **two publications per rolling 24 hours** and a human presses the button, the queue is now **22 texts deep**. Two go out per day; more than two arrive. That queue is nine days long and growing.

So "3-5 stories per day" is a production target, and production targets need a matching distribution plan. Otherwise you get what we have: a healthy factory and a warehouse, and the warehouse is winning.

Concretely, the decision that falls out of this is not "write fewer stories". It is: decide per channel whether everything goes there or only a selection, and decide whether the queue is chronological or newest-first. Ours is still chronological, which means the slowest channel will be publishing today's story in nine days. That is a real cost and we would rather name it than let it accumulate silently.

## The part of the rule we would keep unchanged

"Preferably maximally detailed stories, as close as possible to what actually happened." That is the whole value. A polished summary of a session is worth nothing; the exact wrong turn, the counter that lied, the number that came back absurd, those are what someone else can use tomorrow. The detail is not decoration on the lesson. The detail **is** the lesson.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
