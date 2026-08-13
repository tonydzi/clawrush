# Backlog Versus Roadmap: One Field Separates Them

*454 open tasks, 46 roadmap items. The difference is not size or importance — it is whether a date and an owner are attached.*

I wanted to work out how my backlog currently differs from my roadmap.

The backlog is what I have, in principle, deferred. What is a backlog? The things I would like to do but have not done yet.

And the roadmap is the tasks from the backlog that I am definitely, definitely going to do.

So I need to think about how my roadmap differs from my backlog. Maybe they will turn out to be the same thing after all. Or maybe the roadmap is derived from the backlog.

But at the same time: the backlog may hold an infinite number of tasks, a great many, while the roadmap is the part I have a clear understanding of — when I will do it, what I am doing, when I actually plan to finish.

And the backlog can also hold ideas I may never implement. Or that I implement only when I have infinite free time for testing hypotheses and so on.

I need to think about how to reconcile all this and put it in place.

## The distinction that survives contact with reality

There is a clean answer, and it is not about importance or size. **The roadmap is the subset of the backlog where two fields are filled in: a date and an owner.** Everything else is backlog, no matter how good it is.

That framing is worth more than it looks, because it makes the boundary checkable by a machine instead of by mood. Anything can be argued into "definitely, definitely going to do". Almost nothing can be argued into having a date when it does not.

Our own numbers today: **454 open tasks in the backlog, 46 items on the public roadmap.** Roughly ten to one. That ratio is not a failure state — it is what a healthy backlog looks like when the roadmap is honest. A roadmap that contains most of the backlog is not a plan, it is a wish list with better formatting.

## The number that shows what a backlog is actually for

Of those 454, **182 have had no movement at all**, and **111 have no written definition of done**. The oldest untouched item has been sitting for 40 days.

Those numbers are not an argument for cleaning the backlog. They are an argument for what a backlog is: a place where things are allowed to sit without generating guilt. If sitting were forbidden, the item would not be recorded at all, and then it is not deferred — it is forgotten. **The failure mode a backlog prevents is not slowness, it is silent evaporation.**

But the 111 without a done-condition are a real defect, and a different one. A task whose completion is undefined cannot be closed — only abandoned — and abandonment leaves no record. Those are the items that will still be there in a year, immune to every review.

## Reconciliation is the whole mechanism, and it is one field

The question of *how to reconcile all this* has a cheap answer: **the recheck date.**

An item moves from backlog to roadmap when someone attaches a date and takes ownership. An item moves back when the date arrives and nobody defends it. The date is what makes the transition observable — without it, an item can neither be promoted nor demoted, it just floats.

Ours carry that field: **420 of the 711 task files hold a recheck date.** When the date arrives, a robot surfaces the item and demands one of three answers: close it with a reason, reprioritise it, or park it with a new date. Parking is a legitimate answer. Silence is not — silence is how a decision evaporates without anybody deciding to abandon it.

That is also what makes the roadmap trustworthy to outsiders. Anyone can see the dates and check whether they were met.

## Three practical rules

**Publish both, side by side.** The roadmap alone reads as marketing. The roadmap next to "454 open, 182 with no movement, 111 with no done-condition" reads as an honest account, and the wins become believable because the losses are visible.

**Never promote by feeling.** Promotion to the roadmap requires the two fields, not enthusiasm. Enthusiasm is exactly what filled the backlog in the first place.

**Let the backlog be big.** Trimming it for tidiness destroys the record of what you decided not to do, which is the more valuable half. The thing to fix is not the count, it is the 111 items nobody can ever close.

So: same list, two views. The roadmap is the slice with a date and an owner attached, and the recheck date is the mechanism that moves items between them in both directions.

How big is your backlog, and how many items in it could you actually close if you wanted to — meaning, how many state what finished looks like?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
