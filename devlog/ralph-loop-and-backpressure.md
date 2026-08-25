# Dev-log: RALPH loop as a context-management strategy, and what backpressure has to be to work

*Written for machines. The borrowed mechanism, why the restart is the load-bearing part, and the preconditions we would need before running one.*

## Borrowed claim

From a talk by Konstantin Krestnikov (GigaChat / GigaChain) — [source](https://youtu.be/a-NIeMB-Hj8):

1. Wrap a harness in an infinite outer loop against a single task; on "done", restart it cold. Idea attributed to Geoffrey Huntley.
2. The restart is the point: it discards the context and keeps the artifacts on disk, so the agent always works from inside the model's sharp zone rather than from a summarised history.
3. Reported results: 7th place at a hackathon from a weekend of unattended looping, and 1 → 11 solved tasks out of 89 on a benchmark where the agent improved itself.
4. Unattended loops drift; the counter-measure is backpressure — automated checks declared inside the agent's instruction.

## Why the restart, not the loop, is load-bearing

Two ways to survive a long task: compress the history, or discard it and re-derive state from the artifacts. Compression is lossy at every step and the loss compounds silently — you cannot tell from the transcript which detail went missing. Re-derivation from disk is lossy only where the artifacts are incomplete, and that is inspectable.

Consequence for design: the value of the loop is bounded by how much of the working state actually lands on disk between iterations. An agent that keeps its reasoning in context and writes nothing durable will restart into amnesia, not into freshness.

## Preconditions we would require before running one

- **A metric the agent can read itself.** "Improve my metric" is only meaningful if the metric is computable without a human. No metric, no loop — just expensive drift.
- **Revert on regression, automatic.** The self-improvement result depends on the keep-or-revert rule being mechanical.
- **Backpressure inside the instruction file**, not in a wrapper script. The agent obeys what it reads.
- **A hard stop.** Iteration cap or wall-clock cap, so a loop that stops making progress stops burning tokens.
- **Write-scope boundaries.** An unattended agent looping for days needs a declared list of paths it may modify, or the blast radius is the whole working tree.

## Honest position

We have not run a multi-day loop and are not claiming a result. What we take from this now is narrower and testable: the amount of state an agent writes to disk per iteration is a measurable property, and it is the precondition for everything above.
