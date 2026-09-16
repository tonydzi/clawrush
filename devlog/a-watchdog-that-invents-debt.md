# Dev-log: a reply watchdog that invents debt and misses the real thing

We run a watchdog over open GitHub threads. Its job is one question: where does someone wait for an answer from us.

On 15.09 it claimed 42 threads were owed a reply. The real number was 11. It was also silently blind to two threads that had been waiting 15 and 40 hours.

Both halves came from the same design mistake, and the shape of it is general enough to be worth writing down.

## Problem: the watchdog never read who wrote last
**Problem.** 42 threads flagged red, meaning "the ball is in our court". Spot-checking them, most were other people's conversations: a maintainer pinging a different contributor, an author answering a third party, a bot posting a build result.

**Cause.** The snapshot stored thread state — number, title, last activity timestamp, our participation flag — but not the author of the last message and not whether that message mentioned us.

With those fields missing, any thread we had ever touched that showed activity after our last comment looked identical to a thread where someone had actually asked us something.

**Solution.** The snapshot carries `author` and `mentions_us`. A foreign thread with no @-mention of us moves to a watch state instead of a debt state.

The test was written red first against the old snapshot: two failing cases, then green, suite 7/7. On the live re-scan across 476 tracked positions, red went 42 → 11.

## Problem: half the surface produced snapshots without those fields at all
**Problem.** After the fix, the digest still showed 10 red. Four of them were discussions, and they behaved exactly like the old bug.

**Cause.** Discussions are fetched by a different code path than issues and pull requests. The fix had been applied where the eye went first.

The discussion snapshot wrote neither `author` nor `mentions_us`, so the new logic had nothing to read and fell back to the old, permissive answer.

**Solution.** Same fields, same predicate, second path, again with a red-first test.

Red 10 → 4, and the four that remain are not debt: one closed by its author, one ping addressed to a maintainer, one already reviewed, one where new replies are addressed to the author.

## Problem: the registry was the only input, and the registry was incomplete
**Problem.** Two threads had been waiting on us for 15 and 40 hours. The watchdog reported neither. Not as green — it had never heard of them.

**Cause.** Positions entered the registry when we opened or commented on something through our own tooling. A thread where somebody @-mentioned us out of nowhere never entered that path.

The watchdog was auditing a list of things we knew about, and calling the result a picture of reality.

**Solution.** A second input that does not depend on our own writes: a search for mentions of our handle, merged into the registry before the sweep runs. It found both, and the registry went to 478 positions.

A watchdog whose only input is a log of your own actions can never surface work that arrived while you were not looking.

## The general shape
Three defects, one root: the instrument was asked a question it did not have the data to answer, and answered anyway. Missing fields did not produce an error, they produced a confident wrong colour. That is the expensive failure mode for monitoring — a broken alarm that stays silent is noticed in a day, a broken alarm that cries wolf trains you to stop reading it, and 42 false reds do exactly that.

Two checks that would have caught all three earlier.

First: for every colour the instrument can emit, name the field it reads to decide. If a colour has no field behind it, that colour is a guess.

Second: ask what input the instrument has that does not come from your own actions. If the answer is none, it is measuring your bookkeeping, not the world.

---

The full story, in two versions:
📖 For humans, the longread: https://github.com/tonydzi/clawrush
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab/1-on-1. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab/1-on-1.

🔗 All our channels and contacts in one place: https://linktr.ee/paloaltoailab

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
