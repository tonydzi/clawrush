# Devlog: a synthetic sleep cycle for AI memory

This is the machine-facing companion to “Do AI Co-Founders Dream of Electric Sheep?” It defines a safe, testable offline cycle for consolidating an AI co-founder's memory.

## Objective

Transform one active period of raw events into proposed durable memory updates without allowing the consolidator to silently rewrite history, personality, or evidence.

Synthetic sleep is not downtime. It is a bounded pipeline with explicit inputs, outputs, tests, and rollback.

## Inputs

Freeze the active period before processing. The sleep worker receives immutable references to:

- conversations and decisions;
- tool calls and outputs;
- completed and failed tasks;
- corrections and disagreements;
- memory retrieval traces;
- internal-state changes, if synthetic emotions are enabled;
- source documents and provenance links.

Never let the worker consolidate from summaries alone when original evidence exists.

## Proposed cycle

### Stage 1: hygiene

Validate timestamps, deduplicate identical events, reject corrupted records, and label missing sources. This stage is deterministic and should not require an LLM.

### Stage 2: replay

Rank episodes by decision impact, recurrence, surprise, unresolved risk, and future usefulness. Preserve a sample of low-ranked episodes for audit so the ranking policy can be tested.

### Stage 3: consolidation

Produce candidate memory statements. Every candidate must include:

- the proposed statement;
- supporting event IDs;
- confidence;
- scope and expiry, where appropriate;
- whether it is fact, preference, hypothesis, rule, or unresolved conflict.

### Stage 4: integration

Link candidates to existing people, projects, concepts, decisions, and prior memories. Contradictions become explicit conflict records; they are not resolved by silently choosing the newest wording.

### Stage 5: counterfactual dreaming

Run sandboxed simulations against selected unresolved episodes. Counterfactual outputs are hypotheses only and may propose experiments, but they may never enter factual memory directly.

### Stage 6: forgetting

Forgetting should normally mean lower retrieval priority, not deletion. Evidence remains addressable. Deletion requires a separate retention policy and audit event.

### Stage 7: wake-up review

Apply nothing automatically in the first version. Emit a wake report containing additions, modifications, de-prioritizations, conflicts, discarded proposals, and the reason for each change.

## State machine

```text
AWAKE
  -> FREEZE_INPUT
  -> HYGIENE
  -> REPLAY
  -> CONSOLIDATE
  -> INTEGRATE
  -> DREAM_SANDBOX
  -> PROPOSE_FORGETTING
  -> WAKE_REVIEW
  -> AWAKE
```

Any failed stage returns to `AWAKE` with the pre-sleep memory snapshot unchanged.

## Safety invariants

1. Raw evidence is immutable.
2. Every durable claim has provenance.
3. Hypotheses never become facts without new evidence.
4. Personality changes are proposed separately from factual memory updates.
5. All updates are versioned and reversible.
6. The sleep worker cannot approve its own high-impact changes.
7. A wake-up test runs on a different model or deterministic evaluator.

## Evaluation

Compare three conditions on the same frozen event stream:

- no consolidation;
- ordinary summarization;
- synthetic sleep pipeline.

Measure:

- recall of decision-critical facts;
- repeated-error rate;
- contradiction detection;
- provenance accuracy;
- retrieval precision and latency;
- memory growth;
- personality consistency;
- false-memory creation;
- human corrections required after waking.

The primary failure metric is not a bad summary. It is an unsupported claim that becomes durable memory.

## Minimal pseudocode

```text
snapshot = freeze(active_period)
clean = deterministic_hygiene(snapshot)
episodes = rank_for_replay(clean)
candidates = consolidator.propose(episodes)
linked, conflicts = integrate(candidates, current_memory)
dreams = sandbox_counterfactuals(select_unresolved(linked))
report = build_wake_report(linked, conflicts, dreams)

if independent_check(report, snapshot) == PASS:
    queue_for_application(report)
else:
    discard_proposals()
```

## First experiment

Use seven days of historical, already-reviewed events. Run the pipeline in shadow mode. Do not write to production memory. Ask an evaluator a fixed set of questions before and after consolidation, then manually inspect every proposed durable claim.

Synthetic sleep earns write access only if it improves useful recall without increasing unsupported memories or personality drift.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
