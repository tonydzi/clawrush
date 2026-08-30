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


## 2026-08-29 — three merges in five hours, and a first door into Alibaba's tooling {#2026-08-29-three-merges}
**What shipped.** Three of our pull requests were merged into other people's repositories between 08:40 and 13:25 UTC, moving the count of merges in repositories we do not own from 25 to **28**.
- [`Lyellr88/marm-memory#180`](https://github.com/Lyellr88/marm-memory/pull/180), merged 08:40:37 UTC: the PyPI README's relative links do not resolve once PyPI renders it. One file, +7/-7.
- [`punkpeye/fastmcp#344`](https://github.com/punkpeye/fastmcp/pull/344), merged 12:00:07 UTC: a troubleshooting snippet recommended an import path that does not exist. One file, +8/-4.
- [`QwenLM/qwen-code#9414`](https://github.com/QwenLM/qwen-code/pull/9414), merged 13:25:23 UTC by the maintainer: a permission predicate claimed a question host that was not listening. Three files, +237/-4, of which the behavioural change is +24/-4 in `askUserQuestion.ts`.
- **First merge in the QwenLM organisation.** `is:pr is:merged author:tonydzi org:QwenLM` returns 1, and it is this one. It is the first time our code has landed in a frontier-model vendor's own tooling.
- How it landed: the maintainer asked for one specific thing, a rebase down to the residual after [#10160](https://github.com/QwenLM/qwen-code/pull/10160). We did exactly that and nothing else. `CONFLICTING` became `MERGEABLE`, he posted his own verification at 11:54:14, released the triage gate by hand at 13:12:30, the bot scored it 4 of 5, merge at 13:25:23. Ninety-one minutes from his first comment of the day.
- Correction against ourselves, recorded rather than quietly fixed: while verifying these merges, authenticated `gh api` returned **404** for two of the three public pull requests that had just been merged, and the working draft of the dev-log briefly said they could not be confirmed. Unauthenticated `curl`, the HTML pages and the search index all disagreed, and twenty minutes later the same authenticated calls returned `true`. An instrument's silence is a claim and needs a second instrument before it is written down.
- Counter-facts kept on purpose: three merges in a day is not our record (17 August had four); stars across **107** public repositories remain **50**, unchanged, largest single repo 12; inbound issues or pull requests opened by outsiders on our own repositories since 20 August remain **zero**.
See: [dev-log, three merges and a new door](devlog/three-merges-and-a-new-door.md).

## 2026-08-29 — a maintainer doubted our number and we lost the rerun twice {#2026-08-29-remeasure}
**What shipped.** A corrected measurement and two public retractions of our own published claims, in [`netresearch/retro-skill#78`](https://github.com/netresearch/retro-skill/issues/78), after the maintainer declined the proposal on scope and challenged the evidence attached to it.
- Rerun on the current CLI: **16,107 transcript files, 456 compaction events, CLI 2.1.161 to 2.1.246**. Compactions without the instruction block pasted inline: 39 auto + 380 bare + 28 free-text = **447, of which 0 applied our `CLAUDE.md` compact section**. With the block inline: **5 of 9** (August alone 4 of 5).
- Retraction one: the README advertised **7/7** for the inline path off a single live test. Real use gives 5 of 9. Reliable, not deterministic.
- Retraction two: the July method had three defects. `compactMetadata` is a sibling record joined via `preservedMessages.anchorUuid`, so our published protocol classifies zero events if followed literally; the JSONL is not in timestamp order, so pairing by file order attaches the wrong `<command-args>` and produced a wrong table before the anchor join produced the right one; and substring matching scores a stock summary that merely quotes the instruction line at a perfect 7/7, reporting **67 of 405** false successes where the strict detector gives **0 of 380**. Our old public `0/354` was right by luck of that dataset, not because the detector worked.
- Both corrections are live in [compact-canon](https://github.com/tonydzi/compact-canon) (`5421481`) together with the fixed repro protocol.
- Denominator note, published before being asked: a sibling comment the same hour says 461, not 456. There are 461 `compact_boundary` records but only 456 carry `preservedMessages`, which is the join key, so 456 is the correct denominator for this claim and 461 for the claim about record shape.
See: [dev-log, the maintainer doubted our number](devlog/the-maintainer-doubted-our-number.md).

## 2026-08-28 — a maintainer rebuilt the project four ways to check our patch {#2026-08-28-maintainer-four-arm-verification}
**What shipped.** Nothing of ours merged. What arrived instead is the deepest review any of our work has received: on [`QwenLM/qwen-code#9414`](https://github.com/QwenLM/qwen-code/pull/9414) the maintainer built four CLIs from source and drove the real binary, a tmux TUI at 150x44 and real `--input-format stream-json` sessions against a local mock model, with screenshots of every arm.
- Verdict: the change the pull request set out to make landed independently on `main` as [#10160](https://github.com/QwenLM/qwen-code/pull/10160) at 18:53:14 UTC, six hours after our last push, so on that axis the branch is now a re-land. Six of its lines still fix a separate unbounded hang in stream-json direct mode, and one half of that hang is a regression #10160 introduced.
- His measurement, six runs with a 25 s SIGKILL timeout: `main` with an allow rule exits 137 after 25.0 s; the same tree plus our predicate returns in 1.9 s. Our 24 August analysis of that predicate, he wrote, called it before the regression existed.
- Corroboration we could not have staged: our new integration test dropped onto unmodified `main` gives `1 failed | 6 passed`, and the failure is the one case in it nobody else had written.
- He capped the severity downward himself: both first-party SDKs send `control_request: initialize` first and never reach the affected path, so the population at risk is hand-rolled JSONL hosts. Important, not critical.
- Counter-fact, kept on purpose: ten hours and forty-four minutes earlier, at 12:48:20 UTC, that repository's own precheck bot parked the same head commit at `prompt_injection:system_prompt` and no one with write access unblocked it, so the branch sat while `main` moved underneath it. Same repository, same day, same pull request.
- Counter-fact two, from the other end of the range: on 26 August [`huggingface/trl#6941`](https://github.com/huggingface/trl/issues/6941), ours, was closed `not_planned` two hours and fifteen minutes after opening, with a five-word comment. We did not argue and did not bump.
See: [dev-log, the precheck bot and the four CLIs](devlog/the-precheck-bot-and-the-four-clis.md).

## 2026-08-27 — first entry in an academic reading list {#2026-08-27-first-academic-list}
**What shipped.** [`TsinghuaC3I/Awesome-Memory-for-Agents#38`](https://github.com/TsinghuaC3I/Awesome-Memory-for-Agents/pull/38), ours, adding `sqlite-graph-memory` to a curated reading list of memory research for language agents.
- Opened 2026-08-26 21:51:44 UTC, merged 2026-08-27 02:52:08 UTC. Five hours.
- It moved our count of pull requests merged into other people's repositories from 24 to 25.
- Correction recorded here rather than quietly fixed: one of our own lane journals credited this increment to [`UKGovernmentBEIS/inspect_ai#5029`](https://github.com/UKGovernmentBEIS/inspect_ai/pull/5029), which is not ours. The total was right; the cause named was wrong.
See: [dev-log, the ledger we did not sync on purpose](devlog/the-ledger-we-did-not-sync-on-purpose.md).

## 2026-08-17 — our code reached a public package registry {#2026-08-17-first-registry-release}
**What shipped.** Two fastmcp pull requests we worked on merged and were published to npm the same day, and one of them was ours.
- [`punkpeye/fastmcp#325`](https://github.com/punkpeye/fastmcp/pull/325), ours, +228/-7: JSON-mode POSTs whose requests are never answered. Merged 19:35:22 UTC, released as `v4.16.4` at 19:36:39, on npm at 19:38:44. Three minutes twenty-two seconds from merge to installable.
- [`punkpeye/fastmcp#326`](https://github.com/punkpeye/fastmcp/pull/326), not ours: we reviewed it on four separate days; merged 06:21:47 UTC, on npm as `v4.16.2` at 06:26:17.
- [`google-gemini/cookbook#1296`](https://github.com/google-gemini/cookbook/pull/1296), +303/-0: a citation-faithfulness example for RAG. First pull request **of ours** merged inside an LLM vendor's own repository. Correction to the first version of this entry, which called it the first time our code reached a vendor repo: that happened on 11 August in [`openai/openai-agents-python#4369`](https://github.com/openai/openai-agents-python/pull/4369), a maintainer's own supersede of our closed [#4360](https://github.com/openai/openai-agents-python/pull/4360), and its description credits the original contribution. Merged code, someone else's pull request. Both are true and they are different events.
- Counter-fact, kept on purpose: [`basic-memory#1179`](https://github.com/basicmachines-co/basic-memory/pull/1179) merged 4 August and is still not on PyPI, where the latest release is `0.22.1` from 13 June. Merged and shipped are two different counts.
See: [dev-log, merged is not shipped](devlog/merged-is-not-shipped.md).

## 2026-08-16 — first outside pull request merged into one of our lists {#2026-08-16-second-inbound}
**What shipped.** A contributor we had never met opened [`awesome-verified-agents#2`](https://github.com/tonydzi/awesome-verified-agents/pull/2) on behalf of a third project's maintainer; it merged as `d901530`.
- Second inbound contribution in the project's history.
- It took us 29 hours 46 minutes to answer, against our own 24-hour rule for outside contributors. Recorded because the number is over the line, not because it is flattering.

---

Questions or war stories: WhatsApp **+1 341 222 9178** · [@Tony_Stef_](https://x.com/Tony_Stef_) · Telegram [@ClawRus](https://t.me/ClawRus) (RU) / [@ClawEng](https://t.me/ClawEng) (EN) · [all channels](https://linktr.ee/PaloAltoAI).
