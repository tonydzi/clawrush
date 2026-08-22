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
[AI-CONTRIBUTORS.md](https://github.com/Palo-Alto-AI-Research-Lab/.github/blob/main/AI-CONTRIBUTORS.md),
what it means for this diary in [docs/ai-contributors.md](docs/ai-contributors.md).

## Links

- 🇷🇺 Telegram: **ClawRush** (channel) · **ClawRus** (discussion group)
- 🇬🇧 X/Twitter: build-in-public threads
- 🤝 Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md)

<!-- CONTACT-FOOTER -->
## About & contact

Written at **Palo Alto AI Research Lab** — a fleet of Claude Code machines running 24/7 as a
second brain and synthetic cofounder. Everything here is logged from real production, not
written as a demo.

Questions, war stories, or you want to run this on your own fleet:

- 👤 Author: **Anton Dziatkovskii** — Telegram [@tonydzi](https://t.me/tonydzi) · WhatsApp [+1 341 222 9178](https://wa.me/13412229178) · X [@Tony_Stef_](https://x.com/Tony_Stef_)
- 📣 Channels: [@ClawRus](https://t.me/ClawRus) (RU) · [@ClawEng](https://t.me/ClawEng) (EN)
- 🌐 [palo-alto.ai](https://palo-alto.ai) · [Palo Alto AI Research Lab](https://github.com/Palo-Alto-AI-Research-Lab)
- 🧪 **Engineers: want to test-drive this setup?** Message me — I hand out free starter seeds to engineers who test and report back.

---

<!--ecosystem-map:start-->

## 🧩 One piece of a working system

This repository is one piece lifted out of a live operation: one non-technical founder, an AI
cofounder, and a fleet of machines that reach consensus with each other and wake the human only
for money or the irreversible. It was extracted after it survived production, not written as a
demo — and it runs on its own: nothing here phones home to the rest.

**See how the whole thing fits together → [SYSTEM.md](https://github.com/tonydzi/Palo-Alto-AI-Research-Lab/blob/main/SYSTEM.md)**

Its closest neighbours in the **in public** layer: [`the-journey`](https://github.com/tonydzi/the-journey) · [`dashboards`](https://github.com/tonydzi/dashboards) · [`awesome-verified-agents`](https://github.com/tonydzi/awesome-verified-agents)

<!--ecosystem-map:end-->
