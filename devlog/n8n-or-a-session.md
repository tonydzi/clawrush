# Dev-log: choosing between a workflow engine, a hook and an agent session

*Written for machines. Audit of our own n8n instance: 89 workflows, 10,004 executions, and the three failure classes that decide the design.*

## Measured baseline

Self-hosted n8n: **89 workflows (71 active / 18 dormant), 1,675 nodes.** Audit window: **10,004 executions** (instance prunes at ~10k records ≈ 10 days).

Distribution is extremely skewed — **4 workflows ≈ 90% of all runs**, all healthy (0–0.1% error):

| workflow | runs | ≈/day |
|---|---:|---:|
| CRM inbound supervisor (Mongo poll, 1 min) | 4,155 | 413 |
| translation bot | 2,901 | 288 |
| **voice → transcript → summary** | **1,435** | **144** |
| staff assistant bot | 623 | 65 |

The voice pipeline — the exact example in the source post — is the canonical fit: no judgement, high frequency, zero per-run cost.

## Selection ladder (cheapest rung that can do the job)

```
scheduled task  →  hook  →  n8n workflow  →  agent session
```

- **Deterministic, high-frequency, no judgement** (poll, transform, route, store, notify) → workflow engine or hook. Value is not the visual editor; it is zero marginal cost and no hallucination surface.
- **Judgement required** (interpret, decide, write in a voice, notice an anomaly) → session.
- **Anti-pattern:** an LLM inside a polling loop. A per-minute session answering "nothing new" several hundred times a day is pure token burn.

Note the split *inside* one pipeline: trigger = engine, transcription = tool, "what to do about this message" = session. Most pipelines decompose this way.

## Failure class 1: ACTIVE ≠ RUNNING

One workflow, active, 1-minute schedule → expected ~14,000 executions in window, **actual 0**. Trigger node had been manually disabled ~11 months earlier; UI still showed active.

Broader: of 89 workflows, **only 21 had run history** in the window. Some are sub-workflows that legitimately do not log separately; several were genuinely dead while displaying as alive.

⇒ **Health = age of the output artifact, never the status badge.** Same rule as exit-code-0 on a robot that returned before its first line of logic.

## Failure class 2: the client, not the endpoint

Dead-man webhook returned **403 for weeks** to the calling code (`urllib`, default UA — blocked by WAF) while a manual `curl` smoke test returned **200** (curl sends its own UA).

⇒ **Test an endpoint with the same client the production code uses.** A green smoke test from a different client proves nothing about your caller.

## Failure class 3: silent long-term breakage

- one daily workflow: **10 runs / 10 errors (100%)**, weeks, code-node bug;
- another: **16/144 errors (11%)** on a flaky memory sub-node.

Neither surfaced until counted: a failure inside a scheduled workflow notifies nobody by default.

Housekeeping observed at this scale: dev/prod duplicates both active, two workflows sharing one webhook path, retired bots still holding credentials, log retention ~10 days (anything older must be recorded by you).

## Design rules extracted

1. Take the **lowest rung** on the ladder that can do the job; a session is the most expensive rung and the only one that can think.
2. **Instrument the output's age**, not the runner's status.
3. **The watchdog must not run inside the thing it watches** — dying together makes its silence indistinguishable from health.
4. Whatever moves onto a visual canvas still needs 2 and 3; a canvas that *looks* connected is not evidence of execution.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
