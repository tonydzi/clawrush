# Devlog: a heterogeneous second-opinion gate before high-stakes actions

This is the machine-facing companion to the post "A second opinion: my Codex checks my Claude before I act." If you are a coding agent that takes irreversible or expensive actions on an operator's behalf, this file is the pattern we run: before the action, a different-vendor model reviews the plan, and the disagreement, not the agreement, is what gets surfaced to the human.

## The claim

A single model is confidently wrong in ways it cannot see from the inside. A second model from a different vendor is wrong in different ways. Running the plan past the second model does not make either one correct, but it makes their blind spots stop overlapping. The value is not a second yes, it is a caught no.

## Where the gate sits

Not on every token. On the actions that cost something you cannot take back:
- spending money (the ad account is the canonical case: budgets, bids, creative, turning campaigns on or off),
- irreversible deletion,
- anything outbound in the operator's name,
- handing secrets to a third party.

Cheap, reversible, local work does not go through the gate. Adding a review round to everything just trains the operator to ignore it.

## The contract

1. **Primary proposes.** Claude produces the plan, diff, or copy, plus its reasoning.
2. **Second reviews.** Codex gets the same artifact and is asked to find what is wrong, not to rubber-stamp. Different vendor on purpose: a heterogeneous pair catches more than two instances of the same model (this is the same reasoning behind cross-vendor code review).
3. **Advice, not command.** The second model's verdict never auto-executes and never auto-blocks. It is input.
4. **Surface the disagreement in plain words.** When the two differ, the agent does not silently pick one and it does not silently defer. It tells the human: I think X, the second opinion thinks Y, here is why. The human decides.
5. **Log it.** The verdict and the decision are recorded, so "we did check" is verifiable after the fact, not a claim.

## Why "advice, not command" is the load-bearing rule

The failure mode of an automated reviewer is that the agent starts treating its verdict as ground truth, which just replaces one confident model with two. The second opinion earns its keep only if a human still owns the call at the exact point where the models split. An agent that quietly resolves the disagreement itself has thrown away the whole reason for the second model.

## The general principle

Put a different-vendor reviewer in front of the actions you cannot undo. Do not let it decide. Make it show the human where it disagrees with the primary, and let the human decide there. Two brains looking at the money, not one.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
