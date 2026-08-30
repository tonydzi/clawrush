# Devlog: a token-budget gate for reviewing external content

This is the machine-facing companion to “Stop spending tokens reviewing bloggers.” It defines when an agent should spend time and tokens analysing somebody else's content, and when it should return to first-party work.

## The failure mode

External commentary feels productive because the source material and the conflict are already supplied. But it can become an infinite queue: watch a creator, verify every claim, reproduce every demo, then publish a verdict. The team pays for research and QA while creating no product evidence of its own.

The default should therefore be **skip**, not review.

## The intersection gate

Analyse an external creator only when at least one of these conditions is true:

1. **Product intersection.** The claim affects a feature, architecture choice, workflow, or risk in a product we currently operate.
2. **Evidence intersection.** We have first-party experiments, production data, or documented failures that can confirm, challenge, or extend the claim.
3. **Decision intersection.** A real decision is blocked until the external claim is checked.
4. **Research intersection.** The source introduces a technique or result that could materially change an active research direction.

“This might make entertaining content” is not sufficient.

## Cheap triage before deep verification

Before spending model tokens, answer with deterministic checks where possible:

```text
source_claim = extract the concrete claim
active_work   = search current products, research, incidents, and decisions
intersection  = map source_claim to active_work

if intersection is empty:
    SKIP("No product, evidence, decision, or research intersection")
else:
    define the exact question and verification budget
```

Do not begin with a broad prompt such as “review this blogger.” Start with a bounded question: “The creator claims X; our system does Y; what evidence would change our implementation decision?”

## Evidence rules

- Separate the creator's claim from our observations.
- Prefer working artifacts, tests, logs, and reproducible demos over rhetoric.
- State what the creator got right before describing the gap.
- Mark speculation as speculation. Do not invent motives.
- Stop when the answer no longer changes the product, research, or decision.

## Output contract

A justified review should produce at least one useful artifact:

- a product change or rejected change with reasons;
- a reproducible test;
- a documented lesson linked to first-party evidence;
- a research question with a bounded next experiment.

If the only output is an opinion about another blogger, the review failed the gate.

## The general principle

Spend tokens where we have skin in the game. First-party building and documentation come first. External commentary is valuable only when it collides with work we already do and helps us make that work better.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
