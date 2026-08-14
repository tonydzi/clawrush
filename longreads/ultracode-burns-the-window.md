# One Ultracode Session Eats the Whole Window

*"Does Claude burn tokens faster than Codex?" We measured our own side of that question, and most of the answer is not about the model.*

I tried burning Fable tokens through effort on ultracode.

When you set effort to ultracode, it is not just fun, it is better than Goethe's Faust.

The most important thing is that the request be specific, as all-encompassing as possible. So those guys who advise giving Claude as much context as possible, meaning dictating a long, long message where everything is thought through — they are right. Because the more you explain to Claude what is required, the better it manages to produce something for you.

In short, ultracode is great.

Shame that one ultracode session and that is it, the five-hour limit is done.

And another thing: it seems to me Claude burns through tokens fast compared to Codex.

Have you noticed the same?

## Before you type a single word, the session already costs ~100k tokens

This is the part that is invisible and dominant, so it is worth putting a number on.

We measure the cost of a session's *first request* — the context loaded before any work happens. Across **180 sessions over 14 days: median 103,574 tokens.** Minimum 71,157, maximum 149,106. Today's median was **146,835**, our highest yet.

That is not the conversation. That is the standing instructions, the always-loaded files, the tool definitions, the connectors — the rent paid at the start of every single session, whatever you then ask.

And it grows, because every improvement adds a line somewhere: 104k on 3 August, 119k on the 6th, 123k on the 9th, 147k today. Nobody decided to make sessions more expensive. Each addition was individually small and individually justified.

So "Claude burns through tokens fast" is partly true and mostly mis-attributed. A large share of the burn happens before the model does anything you asked for.

## The second part: language costs money

Measured on our own corpus: **Russian text runs about 2.17 characters per token, Latin about 2.81.** Same length of text, roughly **1.3× more tokens in Russian**.

That applies to everything — the standing instruction files, the prompts, the long detailed message the post recommends writing. A rule written in Russian is a third more expensive to keep loaded than the same rule in English, forever, on every session.

## The third part, and the one that actually answers the comparison

Here is the honest version, and it is uncomfortable.

We measured a week of output on one node: **36.8 million tokens, of which 82% was mechanical work** — shell commands 54.4%, code 15.6%, reading files back 12.4%. Not judgement, not writing, not decisions. Running things and reading them back.

All of that ran on one vendor. Meanwhile the paid Codex bucket sat at **4% utilisation**, and two other paid subscriptions had **never been measured at all**.

So the comparison "Claude runs out faster than Codex" is real, and the cause is largely routing: we sent nearly everything to one rail, including the boring mechanical work that any rail could do. It is not a fair race when one runner carries the luggage.

What we changed: every new part now declares in its passport **which paid bucket it burns**. "Claude, because I am Claude" counts as an architecture defect. Mechanical work — shell, file reading, drafts, extraction — is routed to whichever paid rail has the most headroom, and orchestration, judgement and voice stay where they belong.

## About the advice to write a long, exhaustive prompt

The advice is right, with one correction that costs nothing to apply.

A long prompt is worth it when the length carries **specifics** — file paths, actual numbers, the constraint, what "done" looks like, what not to touch. It is expensive and useless when the length is restating the goal three ways. The failure is not verbosity, it is unspecific verbosity, and it costs the same per token as the good kind.

The cheap discipline: put the facts and constraints in, leave the encouragement out.

## And on burning a five-hour window in one session

That is a real trade and worth naming as one. Maximum effort on a single big request buys depth on that request and spends the window. It is the right call when the task is genuinely one hard indivisible problem, and the wrong call when the task is ten mechanical steps in a trench coat — those should have gone to a cheaper rail, and the window kept for the thing only the expensive rail can do.

The question worth asking before setting effort to maximum is not "will this be better" — it will. It is "is this the one thing today that deserves the window".

Have you measured what a session costs you before you type anything? Most people have not, and it is usually the largest line.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/ultracode-burns-the-window.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/ultracode-burns-the-window.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
