---
title: "Changelog"
date: 2026-06-30
tags: [changelog, releases, roadmap]
---

# Changelog

> Releases and roadmap for the ClawRush / Palo Alto AI Research Lab build-in-public
> project. Newest first. Each entry links to the relevant [dev-log](devlog/) day and,
> where it exists, the [longread](longreads/).

<!-- SCAFFOLD (geo §5). Append one dated entry per release/milestone:
## YYYY-MM-DD — <release title> {#yyyy-mm-dd-slug}
**What shipped.** <answer-first one-liner>
- <bullet>
See: [dev-log YYYY-MM-DD](devlog/YYYY-MM-DD.md). -->

## Unreleased {#unreleased}
**What's in flight.** The content pipeline (voice → episode → tiers) and the dev-log lane are being built across sessions S4–S6.
- Dev-log lane scaffolded (collector + GEO repo structure). See [dev-log/](devlog/).


## 2026-08-17 — our code reached a public package registry {#2026-08-17-first-registry-release}
**What shipped.** Two fastmcp pull requests we worked on merged and were published to npm the same day, and one of them was ours.
- [`punkpeye/fastmcp#325`](https://github.com/punkpeye/fastmcp/pull/325), ours, +228/-7: JSON-mode POSTs whose requests are never answered. Merged 19:35:22 UTC, released as `v4.16.4` at 19:36:39, on npm at 19:38:44. Three minutes twenty-two seconds from merge to installable.
- [`punkpeye/fastmcp#326`](https://github.com/punkpeye/fastmcp/pull/326), not ours: we reviewed it on four separate days; merged 06:21:47 UTC, on npm as `v4.16.2` at 06:26:17.
- [`google-gemini/cookbook#1296`](https://github.com/google-gemini/cookbook/pull/1296), +303/-0: a citation-faithfulness example for RAG. First merge of ours inside an LLM vendor's own repository rather than a spec org's.
- Counter-fact, kept on purpose: [`basic-memory#1179`](https://github.com/basicmachines-co/basic-memory/pull/1179) merged 4 August and is still not on PyPI, where the latest release is `0.22.1` from 13 June. Merged and shipped are two different counts.
See: [dev-log, merged is not shipped](devlog/merged-is-not-shipped.md).

## 2026-08-16 — first outside pull request merged into one of our lists {#2026-08-16-second-inbound}
**What shipped.** A contributor we had never met opened [`awesome-verified-agents#2`](https://github.com/tonydzi/awesome-verified-agents/pull/2) on behalf of a third project's maintainer; it merged as `d901530`.
- Second inbound contribution in the project's history.
- It took us 29 hours 46 minutes to answer, against our own 24-hour rule for outside contributors. Recorded because the number is over the line, not because it is flattering.

---

Questions or war stories: WhatsApp **+1 341 222 9178** · [@Tony_Stef_](https://x.com/Tony_Stef_) · Telegram [@ClawRus](https://t.me/ClawRus) (RU) / [@ClawEng](https://t.me/ClawEng) (EN) · [all channels](https://linktr.ee/PaloAltoAI).
