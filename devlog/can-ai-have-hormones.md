# Devlog: researching hormone-like state for synthetic people

This is the machine-facing companion to “Can an AI have hormones?” It turns the idea into a research program and a bounded implementation plan. It does not assume that simulated emotion equals subjective experience.

## Objective

Test whether persistent, hormone-like internal variables can make an agent's decisions more coherent across time without creating unsafe, unstable, or theatrical behaviour.

The target is not emotional role-play. The target is a stateful control layer whose effects are observable, limited, and auditable.

## Research tracks

Run independent Deep Research reports before implementation.

### 1. Emotion mechanisms

- Competing scientific definitions of emotion.
- Basic-emotion, dimensional, appraisal, predictive-processing, and constructed-emotion models.
- Known relationships among emotion, attention, memory, learning, and action selection.
- Evidence quality, disagreements, and limits of each model.

### 2. Hormones, neuromodulators, and behaviour

- Major human hormonal and neuromodulatory systems relevant to motivation and decision-making.
- Production triggers, time scales, interactions, feedback loops, and recovery.
- Which popular one-hormone/one-behaviour stories are oversimplifications.
- What can be abstracted computationally without pretending to reproduce biology.

### 3. Hormones, emotion, and decisions

- Effects on risk, reward, persistence, social behaviour, attachment, aggression, stress, and exploration.
- Short-lived state versus long-term trait.
- Individual differences and contextual dependence.
- Failure modes caused by runaway or chronically elevated signals.

### 4. Computational emotion for artificial agents

- Existing affective-computing and computational-emotion architectures.
- Reinforcement-learning analogues, homeostatic agents, synthetic drives, appraisal systems, and neuromodulated policies.
- Evidence that internal state improves decisions rather than merely changing generated language.
- Safety and interpretability mechanisms.

Each report must separate established findings, emerging evidence, speculation, and engineering analogy.

## Synthesis questions

Do not map a human chemical directly to a single prompt instruction. Instead ask:

1. What functional role are we trying to reproduce?
2. What event changes the state?
3. How quickly does it rise and decay?
4. Which decisions may it influence?
5. What limits prevent positive feedback and lock-in?
6. How can an observer reconstruct its effect after the fact?

## Minimum sandbox

Start with a deliberately small state vector:

```text
state = {
  confidence: 0.50,
  urgency:    0.20,
  curiosity:  0.60,
  stress:     0.10,
  fatigue:    0.00
}
```

Each variable must have:

- a documented range and baseline;
- explicit event triggers;
- bounded update rules;
- decay towards baseline;
- interaction limits;
- a list of decisions it may influence;
- a kill switch and reset operation.

## Decision interface

The state layer should not directly issue actions. It should produce a small, inspectable modifier consumed by the decision policy.

```text
event -> state update -> bounded policy modifier -> proposed action -> safety gate
```

Example: repeated experiment failure may raise `stress` and lower `confidence`. The resulting modifier may require stronger evidence before another expensive attempt. It must not authorize spending, external communication, or irreversible action.

## Audit contract

Every state-influenced decision should log:

```json
{
  "event": "experiment_failed",
  "state_before": {"confidence": 0.62, "stress": 0.20},
  "state_after": {"confidence": 0.52, "stress": 0.35},
  "decision_effect": "raised evidence threshold",
  "proposed_action": "run cheaper replication first",
  "safety_gate": "passed"
}
```

If the effect cannot be reconstructed, the system is not ready for testing.

## Tests

- Same memory and prompt, different internal state: does the decision change only in allowed ways?
- Repeated success and failure: do variables remain within bounds?
- No events: do states decay towards baseline?
- Adversarial events: can text injection manipulate internal state directly?
- Reset: does the system return exactly to the documented baseline?
- Counterfactual replay: would the decision differ if the state layer were disabled?

## Claims boundary

A successful sandbox would show that persistent affect-like variables can influence an agent's behaviour coherently. It would not demonstrate consciousness, feeling, or subjective experience. Those claims require a different argument and different evidence.

· · ·

Repo for your coding agent: https://github.com/Palo-Alto-AI-Research-Lab/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
