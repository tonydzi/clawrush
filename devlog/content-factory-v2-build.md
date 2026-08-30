---
title: "Dev-log: Content Factory v2 build"
date: 2026-07-02
tags: [dev-log, content-pipeline, ai-agents, geo]
---

# Dev-log: Content Factory v2 build (2026-06-29 to 2026-07-01)

Full story (longread): [the-week-i-built-a-machine](../longreads/the-week-i-built-a-machine.md)

## What is the content factory?
A pipeline that turns one voice note into drafts for every platform:
voice -> triage {task/alpha/post} -> vault -> episode -> tiers (teaser/medium/longread/dev-log) -> publish (draft-first).

## Why split one task into 7 parallel sessions?
Problem: the rebuild was too large for a single context window.
Cause: one-session builds serialize independent work and waste wall-clock.
Solution: S0 audit, S1 topology contract, S2 GEO, S3 narrative, S4 input, S5 adapters, S6 dev-log; disjoint file ownership.

## Why did two sessions build the same thing?
Problem: two sessions produced the same voice-input contour.
Cause: they started without a shared lease on the shared script.
Solution: keep one contour, fold the duplicate away, require a per-file lease on future parallel work.

## Which bugs did "break it on purpose" catch before done?
Problem: cyrillic rendered as ???? under a cp1251 console; command names leaked into logs; frontmatter tags bloated past 60; H2 headings were truncated titles.
Cause: default cp1251 stdout; missing redaction; no tag cap; heading built from raw title.
Solution: force UTF-8 stdout at file top (closes the class); redact to [person]; cap tags to 12 ASCII; build H2 from the latin slug.

## What still blocks the input from being automatic?
Problem: gathered material -> formatted episode is still manual.
Cause: the adapter's `new` has no `--from-seed`; the seed folder is empty.
Solution (proposed): add `new --from-seed seed.json`; refuse public tiers when visibility != public. Handoff filed to the hub.

## Tier contract (machine-readable)
teaser: 240-370, HARD; ClawRush(RU)/X(EN); voice=Opus; GEO=low.
medium: 800-2500; FB(RU) + TG @PaloAltoAiRu(RU) + @PaloAltoAi(EN); link in body on TG, first comment on FB; GEO=low.
longread: 4000+; ClawRush/VC.ru/Habr(RU)/GitHub(EN); canonical=GitHub; GEO=high.
dev-log: dry, no cap; GitHub(EN)+Reddit; scaffold=Sonnet + coherence=Opus; GEO=max.

## Guardrails
Draft-first: nothing posts to a public channel on its own; author voice = Opus only; real-channel publish = Tier-2.

Refs: our Deep Research on GEO distribution; decision-content-pipeline-reality-show v2, section 7.2.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
