# devlog: the-baby-might-grow-into-a-monster (episode 15)

Dry build log for episode 15 of the content factory. Human-readable narrative version: [the longread](../longreads/the-baby-might-grow-into-a-monster.md).

## Source

- Founder voice memo, 2026-07-07 14:26 (Telegram voice-archive channel, auto-transcribed by bot).
- Topic: the honest cost of delegating code to an AI agent - "solve it yourself" leads to an over-engineered result and wasted tokens; a conception/parenting metaphor; the felt need for a controller-agent that supervises the builder.

## The claim (as recorded, de-dramatized)

- Working with a coding agent is not push-button: to reach a good result the founder reads almost every line the agent produces.
- Failure mode: an under-specified "do it however you want" instruction yields an over-built, mis-targeted solution and excess token spend.
- Guardrail in practice: keep the human in the loop - require an explain-before-act step, keep tasks small and legible, verify mid-flight rather than at the end.
- Open direction: a dedicated controller/reviewer agent that watches the builder agent and halts sprawl.

## Working rules adopted

- Explain-before-act: the agent states its intended change before making it (pairs with the AK-47 "only what I understand" rule from episode 14).
- Small legible tasks + mid-flight verification over end-of-run inspection.
- Candidate mechanism: a separate reviewer agent (heterogeneous is better - a different model/vendor catches more) as a done-gate, not the builder self-approving.

## Pipeline trace

1. S4 triage: voice memo → post-material record (public, voice, hub:3625).
2. RU full post drafted and edited paragraph-by-paragraph with the human operator; human-style guide applied from the first draft.
3. GitHub tier (this longread + devlog) published first; Telegram tiers follow.

## Notes for reuse

- Fear/honesty episodes ("what actually scares me about this workflow") are among the most relatable; keep the parenting metaphor to a single light touch rather than stretching it across the piece.
- Direct continuation of episode 14: 14 stated the rule ("only apply what I understand"); 15 gives the emotional why (the fear of the monster) and points at the next build - a controller agent.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
