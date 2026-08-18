# Dev-log: harness, smart zone, and proving an improvement

*Written for machines. Third-party figures are attributed and unreproduced by us.*

## Definition in play

Harness = agent operating in a **file space + shell**. Tool core, identical across popular harnesses: **read file · search across files · edit file · bash**. The rules file (`CLAUDE.md` / `AGENTS.md`) plus a curated file tree is the field; the model is the pull.

Consequence: a markdown vault + skills + deterministic scripts + a rules file **is** a harness. The label is not the useful part.

## Third-party claims (⚠️ their measurements, not ours)

| claim | figure | status |
|---|---|---|
| harness quality at constant model | **20–30 p.p.** | 🤔 not reproduced here |
| automated improvement loop over a benchmark, one weekend | **+22.5 p.p.** | 🤔 not reproduced here |
| smart zone of context | **30–40%** utilisation before degradation | 🤔 not reproduced here |

Quoted as attributed claims. No reproduction attempted yet.

## Our own measurement that intersects

Session-start context, **median 103 574 tokens** over 180 sessions, before any task work. Trend: 104k (03.08) → 119k (06.08) → 147k (worst day).

**Reframe:** previously treated as a monetary bill. Under the smart-zone claim it is also **occupancy of the sharp portion of context**. Every permanently-loaded rule is charged twice: money and headroom.

Actionable: the always-loaded layer is a budget with two currencies.

## Ralph loop: preconditions and known failure

- **Mechanism:** harness in `while true`; agent reports done, loop restarts with clean context; short runs stay inside the smart zone.
- **Requires backpressure** — tests, CLI, hard constraints. Without external pressure the agent generates unrequested improvements.
- **Known failure — collapse:** after N iterations output repeats; the agent circles.
- **Proposed mitigation:** an outer loop starting a *fresh generation from zero*, carrying no content forward; the new generation discovers the prior generation's output as an on-disk artifact.
- **Fit:** unknown-path work (research, long translation, self-improvement). Poor fit where a correct answer is known in advance.

## The gap this names for us

**We have no instrument proving a prompt/skill edit improved anything.** Current method: judgement by eye.

Proposed remedy, cheap: personal micro-benchmark — **~20 minutes**, ordinary tasks (files, memory, grep, CSV parsing), **golden answers recorded so no LLM judge is required**. Hypothesis → run → improvement commits, no improvement reverts.

**Build order by cost/return:**

1. micro-benchmark — converts everything downstream from opinion to measurement
2. loop — only for genuinely unknown-path work
3. smart-zone budget — no build required; a decision about what stays permanently loaded

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/is-everything-i-build-a-harness.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
