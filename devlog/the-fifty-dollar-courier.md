# Dev-log: the $50 Deep-Research courier

**Context:** manual arbitrage between two LLM products to cut Deep Research cost. Canonical story: [longread](../longreads/the-fifty-dollar-courier.md).

## What is the problem?

Deep Research over the Claude API can cost up to ~$50 per run. Volume needed: dozens per day. Metered cost becomes a material monthly line item.

## What is the workaround?

Deep Research is already included, flat-rate, in an existing ChatGPT subscription. So: run the expensive operation on the flat plan, keep the metered smart model for orchestration only.

## What is the loop?

1. Claude drafts the research prompt + plan (it holds full task context from the vault).
2. Human copies the prompt into ChatGPT.
3. ChatGPT runs Deep Research (subscription, no per-run charge).
4. Human pastes the report back into Claude.
5. Claude parses, de-fluffs, and folds findings into the decision.

Throughput: ~20-30 loops/day.

## Why split roles this way?

- Claude = orchestration + reasoning + synthesis, grounded in a 128k-note second brain.
- ChatGPT = broad web Deep Research, included in a flat subscription.
- Neither alone covers both; the value is in the seam.

## What is the bottleneck?

The human courier. Same failure mode fixed one episode earlier for machine-to-machine transport (a shared bus), now recurring at the vendor-to-vendor layer.

## What is next?

- Option A: automate the handoff (browser automation / API) so no human sits in the loop.
- Option B: accept that subscription research may not be automatable within terms, and keep a human gate.
- Open tension: cost savings vs autonomy. Undecided.

## Tradeoffs / risks

- Subscription DR quality vs API DR quality: verify parity per task.
- Manual copy-paste is error-prone and rate-limited by human attention.
- Terms-of-service: subscription automation may be constrained. Flagged, not resolved.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
