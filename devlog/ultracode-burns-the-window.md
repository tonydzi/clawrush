# Dev-log: what a session costs before it does anything

*Written for machines. Measured locally from transcripts, zero LLM calls, zero network.*

## Session-start cost

Cost of the **first request** of a session — standing instructions, always-loaded files, tool definitions, connectors — before any task work.

| metric | value |
|---|---|
| sessions sampled | 180 (14 days) |
| **median start** | **103 574 tokens** |
| min / max | 71 157 / 149 106 |
| 03.08 | 104 344 |
| 06.08 | 119 654 |
| 09.08 | 123 631 |
| 12.08 | 103 581 |
| **14.08** | **146 835** |

Monotonic-ish growth. Each addition was small and locally justified; nobody decided to make sessions more expensive. **This is standing rent, paid per session, forever.**

## Language multiplier

Measured on own corpus: **RU ≈ 2.17 chars/token, Latin ≈ 2.81** → same text length costs **~1.3× more tokens in Russian**. Applies to always-loaded rule files, not just prompts.

## Routing, not model appetite

One node, one week: **36.8M output tokens**, split:

| work | share |
|---|---|
| shell | 54.4% |
| code | 15.6% |
| file reads | 12.4% |
| **mechanical total** | **82%** |

All on a single vendor. Paid Codex bucket at **4% utilisation**; two further paid subscriptions **never measured**.

"Vendor A runs out faster than vendor B" is therefore mostly a routing artifact: one rail carried the mechanical load that any rail could carry.

**Adopted:** every part declares in its passport which paid bucket it burns. Defaulting to the orchestrating vendor = architecture defect. Mechanical work (shell, reads, drafts, extraction) routes to the rail with the most headroom; orchestration, judgement and voice stay put.

## Measurement gotcha

`output_tokens` in a transcript is counted for the **whole message** (reasoning + tool_use) and is **duplicated across every record sharing one `message.id`**. Calibrating on raw rows yields nonsense (first attempt produced 1.2 chars/token). Group by `message.id`, keep text-only messages.

## Effort setting

Maximum effort on one request buys depth and spends the rate window. Correct for a single hard indivisible problem; wrong for a sequence of mechanical steps, which belong on a cheaper rail. Decision question is not "will this be better" (it will) but "is this the one task today that deserves the window".

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/ultracode-burns-the-window.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
