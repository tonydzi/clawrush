# Cheaper Software Means More of It

*The paradox has a name and a two-hundred-year-old track record. We also ran it on ourselves, and the numbers are not flattering.*

Andrej Karpathy talks about a certain paradox: when technology becomes cheaper, users start using it even more.

The big question at the time was: will the programming profession survive, given that making software is becoming very cheap? He says yes, it will survive. Moreover, there may be even more of it. Why? Because software is now cheaper than before, and more of it will be made. Programmers will simply become orchestrators rather than programmers — but there will be far more of them, and far more software will be produced.

And I think he is right here.

Look, I once tried to buy a graphics card for local LLMs and got talking to a guy who had built a service like this on his own machine. A person comes along who needs a website and says: I need such-and-such a site, I have a hair salon, here are the photos, I would like a website. And his LLM, sitting on his seven-thousand-dollar Mac, generates a site for that user on request.

Say you have a pizzeria — in five minutes you have a site where people can order pizza online. A hair salon — in five minutes you have a site where people can book a haircut.

He says the market capacity is infinite. The volume of small businesses that need a site where you can easily order or book is enormous: hairdressers, manicures, dog grooming and so on. There is an endless number of them, and going to Wix or some platform and building a site was a genuine pain for them.

And here: the LLM asked the user for a few photos of the business — and made a site for the salon. You can book a haircut. Or a site for a farm that sells its own produce. Incredible: a site in five minutes.

And this guy says you still have to solve the user's hosting problem, everything else the user needs, and even payments. So from a single prompt the user gets a site: they land somewhere, there is a "buy" button, a "book" button, the whole payment flow.

That really is cool. And AI is exactly what makes it possible.

So yes: there will be even more software. And demand for engineers will not fall, engineers will just be doing slightly different things. Meanwhile the barrier to entry into engineering will drop, because almost anyone with prompts can write a prompt.

In short, engineers can relax a bit. You just need to get to grips with this very fast.

## The paradox has a name, and that makes it checkable

This is **Jevons paradox**, first described in 1865 about coal: more efficient steam engines did not reduce coal consumption, they increased it, because efficiency made coal worth using in places where it previously was not. The same shape recurs in lighting, in road capacity, in bandwidth.

Naming it matters because the named version comes with a caveat the optimistic version drops: **total consumption rises, but the individual unit's price collapses.** More software gets made, and each individual piece of it is worth less. Both halves are the same phenomenon.

## We ran it on ourselves, and it is unflattering

We are exactly the case in the post — generation got cheap for us. What happened to our consumption:

**36.8 million output tokens in one week on one machine.** Of that, **82% was mechanical work**: running shell commands, editing code, reading files back. Not thinking. Not deciding.

And the cost of merely starting: **median 103,574 tokens per session before any work happens**, growing week by week — 104k, 119k, 147k on the worst day.

That is Jevons in one household. Cheap generation did not free the time; it moved the time into producing more, and most of the "more" was mechanics.

The second half of the same bill: **95 gates we built that nothing ever invokes, and 19 of 25 recent rules with no caller at all.** Every one was cheap to build and correct on the day. Cheap creation produces abundance, and abundance produces a maintenance surface nobody budgeted for.

## The five-minute site is real, and the five minutes are the cheap part

The demo is genuine and the market observation is right. The part worth separating: **generating the site is the easy five minutes. Owning it is the business.**

Hosting, a domain, payments, the tax and refund rules for that payment flow, a booking system that does not double-book, the photo the owner wants swapped next Tuesday, and — the real one — **who fixes it in three months when something breaks and the owner does not know what a deploy is.**

That is not an argument against the idea; it is where the money and the durable work actually are. Which supports the post's conclusion by a different route: demand does not fall, it **moves** — from typing the thing into keeping the thing alive.

## What "orchestrator" actually means, practically

We live that role. What it turned out to consist of: choosing which rail runs which work, keeping the context small enough that the model still thinks well, and building the boring layer that wakes things and checks their output.

And the one thing that does not get cheaper: **knowing what to build.** When creation costs nothing, the binding constraint becomes judgement — which of the possible things deserves to exist, and who will read its output. We measured our own failure at that: 19 of 25 recent rules had no consumer. Producing them was free. Producing the right ones was not.

So: engineers can relax about supply, and should not relax about the maintenance surface they are about to create. The barrier to entry drops; the barrier to *finishing* does not move at all.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/cheaper-software-means-more-of-it.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/cheaper-software-means-more-of-it.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
