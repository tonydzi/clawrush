# C(H+A)RM — the build diary

> **C(H+A)RM** is what this lab is building: a CRM for **H**uman **&** **A**gent collaboration, running on a personal second brain. The framework itself lives in **[charm-os](https://github.com/tonydzi/charm-os)**. This repository is its **diary**: the day-by-day record of building it in public.

**ClawRush** is the diary's own name, kept because the links, the feed and the Telegram channels carry it. The product is C(H+A)RM; ClawRush is where the work gets written down.

This is the **English diary and artifact home** of an ongoing experiment: building a personal AI **"digital twin" / second brain** with [Claude Code](https://claude.com/claude-code), in public, as a kind of reality show of the work.

The Russian-language version of this story lives in Telegram: channel **ClawRush** (longreads) + group **ClawRus** (discussion). English threads also go out on X.

## What's here

- **[`/devlog`](devlog/)** — the raw build log: problems → root causes → fixes, plus the Deep Research we ran. Dry, English, machine-readable (the main GEO feed).
- **[`/longreads`](longreads/)** — essays and write-ups: what was built, what broke, what was learned (curated stories).
- **[`/longreads-ru`](longreads-ru/)** — the same kind of essays written natively in Russian (not translations).
- **[`/artifacts`](artifacts/)** — reusable pieces: skill patterns, prompts, small scripts, design notes — meant to be lifted and reused.
- **[`/docs`](docs/)** — technical docs and guides for the reusable systems.
- **[`/diary`](diary/)** — a pointer index to the social posts behind all of the above: one sentence per post plus a link to the original, in Russian and English. No verbatim copies.
- **[`changelog.md`](changelog.md)** — releases and roadmap.

Machine-readable site map for agents: [`llms.txt`](llms.txt). AI crawlers are welcomed in [`robots.txt`](robots.txt).

Updated as the work actually happens, not polished after the fact.

## The skills behind this diary

Everything logged here is produced by a set of Claude Code skills that ship openly:
**[second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit)** — 101 skills,
installable in one line.

```
npx skills add tonydzi/second-brain-starter-kit
```

The 25 worth your first hour are listed on the
[kit's front page](https://github.com/tonydzi/second-brain-starter-kit#start-here--25-skills-worth-your-first-hour);
the ones that produced most of this diary are
[`/tt`](https://github.com/tonydzi/second-brain-starter-kit/blob/master/skills/tt/SKILL.md) (prove it works before saying "done"),
[`/secondop`](https://github.com/tonydzi/second-brain-starter-kit/blob/master/skills/secondop/SKILL.md) (a review panel of external LLMs) and
[`/retro`](https://github.com/tonydzi/second-brain-starter-kit/blob/master/skills/retro/SKILL.md) (what survives a session).

🧪 Engineers: try one and tell me what broke — free starter seeds for people who test and report back.
Telegram [@tonydzi](https://t.me/tonydzi) · WhatsApp [+1 341 222 9178](https://wa.me/13412229178).

## Philosophy

- **AK-47 simplicity** — the simplest thing that works, repairable by a non-engineer "with a hammer". If it can't be fixed simply, it's too complex.
- **Human-in-the-loop** — the bottleneck isn't writing code, it's the right decisions and knowing what people actually need.
- **Own your home** — in 2026 ownership beats the algorithm. This repo is the owned base; mirrors (Telegram, X, blog) point back here.

## AI contributors

The model avatars you may see among contributors are not decoration — Claude
writes the code, Codex and Grok review it, Gemini feeds the research. Each
gets a `Co-authored-by` credit only on commits its output actually shaped —
lab-wide policy in
[AI-CONTRIBUTORS.md](https://github.com/tonydzi/.github/blob/main/AI-CONTRIBUTORS.md),
what it means for this diary in [docs/ai-contributors.md](docs/ai-contributors.md).

## Links

- 🇷🇺 Telegram: **ClawRush** (channel) · **ClawRus** (discussion group)
- 🇬🇧 X/Twitter: build-in-public threads
- 🤝 Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md)

## 🗺 The whole lab, one map

This diary is the **canonical entry point** to everything the lab ships. The system itself is
split into small repos on purpose — take one piece, ignore the rest — but they all come from
one running operation. The layers, top to bottom:

| Layer | What it answers | Start with |
|---|---|---|
| **Governance** | what an agent is allowed to do | [claude-bible](https://github.com/tonydzi/claude-bible) · [agent-leash](https://github.com/tonydzi/agent-leash) · [charm-os](https://github.com/tonydzi/charm-os) |
| **Memory** | what survives the context window | [sqlite-graph-memory](https://github.com/tonydzi/sqlite-graph-memory) · [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit) · [claude-workdir-sentry](https://github.com/tonydzi/claude-workdir-sentry) |
| **Gates** | what proves the agent did it | [verbatim-citation-gate](https://github.com/tonydzi/verbatim-citation-gate) · [verdict-contract](https://github.com/tonydzi/verdict-contract) · [claim-check](https://github.com/tonydzi/claim-check) · [context-contamination-probe](https://github.com/tonydzi/context-contamination-probe) · [persona-portability-benchmark](https://github.com/tonydzi/persona-portability-benchmark) · [red-first-review-skill](https://github.com/tonydzi/red-first-review-skill) |
| **Fleet** | how many machines run as one | [claw-consensus](https://github.com/tonydzi/claw-consensus) · [fleet-deploy](https://github.com/tonydzi/fleet-deploy) · [agent-control-plane-casebook](https://github.com/tonydzi/agent-control-plane-casebook) · [telegram-agent-bus](https://github.com/tonydzi/telegram-agent-bus) |
| **Connectors** | what the agents reach into | [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) · [whatsapp-mcp-kit](https://github.com/tonydzi/whatsapp-mcp-kit) · [lambda-cloud-mcp](https://github.com/tonydzi/lambda-cloud-mcp) |
| **Running the shop** | what it costs and where the effort goes | [llm-spend-audit](https://github.com/tonydzi/llm-spend-audit) · [agent-approval-gate](https://github.com/tonydzi/agent-approval-gate) · [claude-dev-star](https://github.com/tonydzi/claude-dev-star) · [pr-watch](https://github.com/tonydzi/pr-watch) · [claude-session-icons](https://github.com/tonydzi/claude-session-icons) |
| **In public** | the story, said out loud | this repo · [the-journey](https://github.com/tonydzi/the-journey) · [cv](https://github.com/tonydzi/cv) · [deep-research](https://github.com/tonydzi/deep-research) · [github-evidence](https://github.com/tonydzi/github-evidence) · [nine-buckets](https://github.com/tonydzi/nine-buckets) |

Full map with every repo and "take it if" guidance: **[SYSTEM.md](https://github.com/tonydzi/tonydzi/blob/main/SYSTEM.md)**.

**Weekly releases:** every week the lab packs what it shipped into a dated entry in
[`changelog.md`](changelog.md) — one place to watch instead of fifty repos. Watch/star this
repo to follow the whole system.

<!-- CONTACT-FOOTER -->
## About & contact

Written at **Palo Alto AI Research Lab** — a fleet of Claude Code machines running 24/7 as a
second brain and synthetic cofounder. Everything here is logged from real production, not
written as a demo.

Questions, war stories, or you want to run this on your own fleet:

- 👤 Author: **Anton Dziatkovskii** — Telegram [@tonydzi](https://t.me/tonydzi) · WhatsApp [+1 341 222 9178](https://wa.me/13412229178) · X [@Tony_Stef_](https://x.com/Tony_Stef_)
- 📣 Channels: [@ClawRus](https://t.me/ClawRus) (RU) · [@ClawEng](https://t.me/ClawEng) (EN)
- 🌐 [palo-alto.ai](https://palo-alto.ai) · [Palo Alto AI Research Lab](https://github.com/tonydzi)
- 🧪 **Engineers: want to test-drive this setup?** Message me — I hand out free starter seeds to engineers who test and report back.

---

<!--we-ask:start-->

## Contributors welcome — and here is what we are missing

We spend a lot of time answering other people's issues. It was fair to say out loud
what we have not built ourselves:

- [Follow one diary entry end to end and tell us where it does not reproduce](https://github.com/tonydzi/clawrush/issues/3)

Issues labelled [`accepted`](https://github.com/tonydzi/clawrush/issues?q=is%3Aissue+is%3Aopen+label%3Aaccepted) are scoped, free to take, and nobody is on them.
Comment **"claiming this"** — no permission needed — and it is yours for 7 days.
New here? Start with [`good first issue`](https://github.com/tonydzi/clawrush/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

**You keep the copyright to your code.** No CLA, no assignment, ever — your contribution goes
in under this repo's existing license, the same terms as ours. We answer every issue and PR
within 48 hours, including "no, and here is why"; our silence is our bug, so ping the thread.

Full deal: [CONTRIBUTING.md](https://github.com/tonydzi/.github/blob/main/CONTRIBUTING.md)

<!--we-ask:end-->

---

<!--ecosystem-map:start-->

## 🧩 One piece of a working system

This repository is one piece lifted out of a live operation: one engineer running a fleet of
machines, built with Claude as implementation collaborator; the machines reach consensus with
each other and wake the human only for money or the irreversible. It was extracted after it
survived production, not written as a demo — and it runs on its own: nothing here phones home
to the rest.

**See how the whole thing fits together → [SYSTEM.md](https://github.com/tonydzi/tonydzi/blob/main/SYSTEM.md)**

Its closest neighbours in the **in public** layer: [`dashboards`](https://github.com/tonydzi/dashboards) · [`awesome-verified-agents`](https://github.com/tonydzi/awesome-verified-agents) · [`cofounder`](https://github.com/tonydzi/cofounder)

<!--ecosystem-map:end-->

<!-- READ-WITH-AI:START (generated by read_with_ai.py - do not hand-edit) -->

### READ THIS WITH AI

One click and an agent reads the repo, pulls out the patterns and helps you apply them to your own work.

<a href="https://chatgpt.com/codex?prompt=Read%20this%20repo%3A%20https%3A%2F%2Fgithub.com%2Ftonydzi%2Fclawrush%20%28%E2%80%9Cclawrush%E2%80%9D%20-%20C%28H%2BA%29RM%20build%20diary%20%E2%80%94%20a%20CRM%20for%20Human%20%26%20Agent%20collaboration%2C%20built%20in%20public%20with%20Claude%20Code.%20Framework%3A%20github.com%2Ftonydzi%2Fcharm-os.%20English%20diary%2C%20longreads%20%26%20reusable%20artifacts%29.%20Work%20out%20what%20problem%20it%20actually%20solves%2C%20pull%20out%20the%20reusable%20patterns%20and%20help%20me%20apply%20them%20to%20my%20own%20setup.%20Start%20by%20asking%20what%20I%20am%20working%20on."><img alt="Codex - open" src="https://img.shields.io/badge/Codex-open-000000?style=for-the-badge&logo=openai&logoColor=white"></a> <a href="https://chatgpt.com/?q=Read%20this%20repo%3A%20https%3A%2F%2Fgithub.com%2Ftonydzi%2Fclawrush%20%28%E2%80%9Cclawrush%E2%80%9D%20-%20C%28H%2BA%29RM%20build%20diary%20%E2%80%94%20a%20CRM%20for%20Human%20%26%20Agent%20collaboration%2C%20built%20in%20public%20with%20Claude%20Code.%20Framework%3A%20github.com%2Ftonydzi%2Fcharm-os.%20English%20diary%2C%20longreads%20%26%20reusable%20artifacts%29.%20Work%20out%20what%20problem%20it%20actually%20solves%2C%20pull%20out%20the%20reusable%20patterns%20and%20help%20me%20apply%20them%20to%20my%20own%20setup.%20Start%20by%20asking%20what%20I%20am%20working%20on."><img alt="ChatGPT - open" src="https://img.shields.io/badge/ChatGPT-open-10a37f?style=for-the-badge&logo=openai&logoColor=white"></a> <a href="https://claude.ai/new?q=Read%20this%20repo%3A%20https%3A%2F%2Fgithub.com%2Ftonydzi%2Fclawrush%20%28%E2%80%9Cclawrush%E2%80%9D%20-%20C%28H%2BA%29RM%20build%20diary%20%E2%80%94%20a%20CRM%20for%20Human%20%26%20Agent%20collaboration%2C%20built%20in%20public%20with%20Claude%20Code.%20Framework%3A%20github.com%2Ftonydzi%2Fcharm-os.%20English%20diary%2C%20longreads%20%26%20reusable%20artifacts%29.%20Work%20out%20what%20problem%20it%20actually%20solves%2C%20pull%20out%20the%20reusable%20patterns%20and%20help%20me%20apply%20them%20to%20my%20own%20setup.%20Start%20by%20asking%20what%20I%20am%20working%20on."><img alt="Claude - open" src="https://img.shields.io/badge/Claude-open-d97757?style=for-the-badge&logo=anthropic&logoColor=white"></a>

<details>
<summary>Copy the prompt (works in any agent: Gemini, Grok, a local model, your own CLI)</summary>

```text
Read this repo: https://github.com/tonydzi/clawrush (“clawrush” - C(H+A)RM build diary — a CRM for Human & Agent collaboration, built in public with Claude Code. Framework: github.com/tonydzi/charm-os. English diary, longreads & reusable artifacts). Work out what problem it actually solves, pull out the reusable patterns and help me apply them to my own setup. Start by asking what I am working on.
```

</details>

<sub>— TonyDzi, Palo Alto AI Research Lab · second brain, agent coordination, persistent memory: github.com/tonydzi</sub>

<!-- READ-WITH-AI:END -->
