# Which Development Metrics Are Free, and Which Will Quietly Die

*We took a wishlist of fifteen indicators and priced each one against a live system. Eight are free, four have no counter at all, and the one everybody wants most is the only broken one.*

I need to add to the daily statistics I publish in Journey AIBO how many deep researches were done that day, and in total, historically.

This matters a lot. It is a heavy indicator, one of our pulses.

I should also think about what other quantitative indicators of my development exist: number of sessions; number of retros; maybe number of compacts; number of deep researches; number of peers; lines of code we wrote, even though we supposedly do not write code; routines and automations we built; number of robots; messages sent; leads in the funnel, cold, warm, hot, and other types of leads (engineers, for instance); likes; who liked us; who starred us on GitHub; who forked us, and so on.

In short, I need to gather as much statistics as possible, every day we should be posting it.

Again, all of this has to be easy to collect. If I spend a lot of resources gathering statistics, then it should not be done at all.

Beyond AIBO and Journey, I would post this weekly across all our social networks as a separate message. Something like: another 7 days of development have passed. Another 120 deep researches done. This many engineers joined our community.

Weekly statistics posting, everywhere we can: Medium, Twitter, Reddit and so on. Everywhere possible, so that those watching us see that we are moving.

It might be worth combining this with the roadmap. We say: here are our statistics. Here is our roadmap and what we plan to do. And here is what we did in the past. So we also have an execution log. And we have a backlog, the tasks we have not got to yet.

In short, my focus is on systematisation.

## We priced the wishlist instead of agreeing with it

The constraint in that list is the interesting part, and it is stated by the person asking for the metrics: *if collecting it costs a lot, it should not be done at all.* That turns a wishlist into an engineering question with a checkable answer.

So we ran every item against the live system and recorded what it costs today.

### Free right now — one command, seconds, zero tokens

| indicator | count |
|---|---|
| deep researches | **377** (245 applied, 106 parked with a reason) |
| sessions | **811** on a single node |
| peers | **6** machines |
| robots | **47** scheduled tasks on this node, **44** alive |
| skills | **163** |
| content | **143** posts, **587** placements across platforms |
| tasks | **454** unfinished, **111** with no definition of done |
| GitHub | **79** repos, **43** stars, **4** forks |

The GitHub row answers two of the wishlist items at once — *who starred us* and *who forked us* come back as names in the same API response as the counts. Identity is not more expensive than the number here, which is unusual and worth knowing.

### No counter exists at all

Retros, compacts, lines of code, messages sent. Each of these happens constantly and none of them is written to a journal anywhere. They are recoverable — you can comb transcripts and count — but a one-off manual comb is an archaeology project, not an indicator. The distinction matters: "we could count it" and "it is counted" are different states, and only the second survives contact with a weekly deadline.

### Expensive, and it is the one we want most

Likes, and who liked us, on Facebook. Our token there is dead: measured 10 August, Threads answers `code 190`, the graph itself `code 2500`. The single most desirable number on the list is the single broken one. That is not a coincidence — the metrics people want most are usually the ones held by someone else's API, behind someone else's auth, with someone else's expiry policy.

## Rule one: a metric you cannot pull with one command will not survive week two

Not because of discipline. Because of *when* the weekly post actually gets written — in the three minutes that exist, not the half hour that does not. Any indicator requiring assembly gets dropped on the first busy week, and the series has a hole in it, and a series with holes stops being read.

So the practical form is: the post carries what is already counted. Everything else either gets a counter at the moment the part is built, or it does not go into the post. We already had that as an internal rule for new parts — every live part reports its own usage — and this exercise is just its consequence at the reporting layer.

## Rule two: a counter shows volume, not motion

This is the one that cost us something to learn, and it shows up directly in the numbers above.

**377 deep researches** is an impressive number and a nearly useless one. The figure that carries information is next to it: **93% closed out** — applied or parked with a stated reason. A deep research that was run and never resolved is not an asset, it is a tab left open.

Same shape one row down. **454 unfinished tasks** is not an indicator of anything; volume of backlog mostly measures how long you have been alive. The indicator is that **111 of them have no written definition of done**. That number tells you something actionable and it does not flatter anybody.

A numerator without a denominator is advertising. The pair — *done, and of those, closed* — is a pulse.

So the weekly post should not read "120 deep researches done". It should read "120 done, 111 taken to a verdict". The second number is less flattering and it is the only one that means anything.

## Rule three: pair the statistics with the roadmap, or the numbers float

The instinct in the original list is right and worth stating plainly. Numbers on their own are a scoreboard for a game the reader does not know the rules of. The three-part shape fixes that:

- **what we did** — the execution log
- **where we are** — the counts
- **what is next** — the public roadmap and the backlog

The backlog is the honest half. Publishing "454 unfinished, 111 with no done-condition" alongside the wins is what makes the wins believable. A feed of only-good-numbers reads as marketing within about three posts.

## What we would tell someone starting this

Pick the metrics your system already emits. Publish the ratio, not the total. Publish the backlog next to the wins. And when you build a new part, give it a counter on day one — retrofitting counters onto a year of history is exactly the "expensive collection" the constraint was written to prevent.

What do you track, and how long does collecting it take? If it is more than five minutes a week, we would genuinely like to know how you survived.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/daily-stats-as-a-pulse.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/daily-stats-as-a-pulse.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
