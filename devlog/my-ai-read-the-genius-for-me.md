# Dev-log: LLM-assisted expertise transfer (expert articles -> layman's production)

**Context:** a non-programmer applied expert-level LLM-optimization articles by having his AI read and adapt them. Canonical story: [longread](../longreads/my-ai-read-the-genius-for-me.md).

## What was the problem?

Expert engineering articles (LLM workflow optimization, Habr) were relevant but not actionable for a non-engineer operator. Reading did not transfer into implementation.

## What was the method?

1. Hand the full article set to the operator's own Claude instance ("read everything this author writes").
2. Claude maps article content against the operator's existing stack and its known unsolved problems.
3. Claude extracts only the applicable techniques and implements/adapts them directly.
Result: transfer chain shortened from expert->expert to expert->AI->production.

## What was the headline technique adopted?

Recurring service tasks must not invoke the LLM on every trigger. Checks, gates, stop-conditions, routine detectors = deterministic code (0 tokens, instant). LLM is reserved for judgment: synthesis, evaluation, language. Applied as a general token-spend rule across the stack.

## What was the immediate outcome?

- Several token-spend optimizations shipped, derived from the articles.
- At least 4 specific points queued for a detailed breakdown episode (with before/after numbers).
- Verdict from the AI after reading: the author solves problems the operator's stack had left unsolved for months.

## Why does this matter beyond one case?

- Expertise-access shift: expert content becomes consumable by non-experts via their AI (write deep -> machines parse -> humans ship).
- For authors: audience is no longer bounded by reader expertise (GEO implication: AIs read and cite deep content).

## Open

- Detailed 4-point breakdown with metrics: pending, next episode.
- Habr invite for first-party publishing: pending (community ask).

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
