# Cover Everything With Tests, on Subscriptions That Are Idle Anyway

*We ran the coverage map before starting. 1,260 parts, 194 tested, 1,106 documented. The gap between those two numbers is the whole story.*

Recently, for fun, I asked Claude to start writing tests for everything we produce.

Meaning: everything we have written needs tests. Or at least the most-used things. Just so that I have everything covered by tests. Okay, maybe not everything, but at least a little, so that I simply start doing it.

And to write those tests, I have a pile of LLMs and subscriptions just sitting idle: Grok, Codex, Gemini and so on.

So: I will get test coverage. I will verify it works. And possibly I will arrive at the task of writing documentation.

Those are the two things I would like to do across several of my products, and then turn it into a repeatable skill: writing documentation and test coverage.

## We measured the starting position before writing a single test

You cannot report progress on coverage without a number to start from, so here is ours, taken today across the whole system.

**1,260 parts total. 1,118 alive, 142 dead. Of the alive ones: 194 carry a test, 1,106 carry documentation, 12 have neither.**

That is **17% tested and 99% documented**, and the asymmetry is the interesting part. Documentation happened because we made it a birth requirement — a part is not finished until its passport is written, in the file itself. Tests did not, and so they did not happen.

By zone the picture sharpens:

| zone | alive | tested | documented |
|---|---|---|---|
| scripts | 441 | 136 (31%) | 438 |
| imports | 675 | 56 (8%) | 666 |
| engine | 2 | 2 | 2 |

The imports zone is where data flows through, and it is the least tested. That is the normal shape: the parts that are easiest to test are the ones you also understand best, and the ones that most need testing are the ones nobody wants to touch.

## Three rules that decide whether coverage is real

We learned these expensively, and they are what separates a coverage number from a coverage claim.

**A test that never runs is not a test.** Our rule is blunt: a test with no schedule and no visible run date within thirty days counts as non-existent. A repository full of green files nobody executes produces exactly the confidence of having no tests, minus the honesty.

**A test that does not redden on mutation is decoration.** Every test we add gets checked by deliberately breaking the code it guards. If it stays green, it was testing nothing. We caught this on ourselves twice: a test that verified a *function* worked but never checked that the function was *called* — the wiring was missing, and the test could not see it. Then a second time, a length test whose sample was too short for the limit to ever trigger.

**Test the consequence, not the action.** Verifying "the script ran" proves nothing. Verifying "the artifact the script writes has a fresh timestamp inside it, at the consumer" proves the thing you actually care about. Exit code zero is a claim by the same program you are testing.

## On the idle subscriptions — that instinct is right, and we measured why

The observation that several paid LLM subscriptions sit unused is not a minor efficiency note. We measured it: over one week on one node, **82% of output tokens went to mechanical work** — shell 54.4%, code 15.6%, reading files back 12.4% — and all of it ran on one vendor, while another vendor's paid bucket was at **4% utilisation** and two more had never been measured at all.

An unused subscription is not saved money, it is spent money producing nothing. And test-writing is close to the ideal workload for those idle rails: mechanical, verifiable, and the output is checkable by a machine rather than by taste. If a generated test does not redden on mutation, it fails, regardless of which model wrote it.

The rule we adopted from this: every new part names, in its passport, **whose paid bucket burns when it runs**. "Claude, because I am Claude" counts as an architecture defect.

## And documentation — one thing worth deciding upfront

Docs and tests are usually planned as two projects. They are cheaper as one, if the documentation lives **inside the code file** rather than beside it.

Ours is a docstring at the top of each part: what it does, input and output, who calls it, which rail it burns, and the name of its test. One file, one truth. A separate markdown retelling the same thing is not documentation, it is a second thing to keep in sync, and it will be wrong within a month.

The reason that matters more than tidiness: **documentation that lies is more expensive than documentation that is missing.** We paid for that one directly. A passport claimed the dashboard generator called a reconciler before drawing; the call did not exist in the code at all. The dashboard quietly showed a five-day-old picture and 100 placements went missing, because everybody trusted the document instead of the file.

## What we would tell someone starting the same task

Take the coverage number before you write anything, so you can prove movement later. Put the test on the consequence, not the action. Break the code on purpose to check the test can see it. Give the mechanical work to the subscriptions you are already paying for. And write the documentation inside the file, because the copy beside it is the one that starts lying.

What is your real coverage number — measured, not estimated? And when did your tests last actually run?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
