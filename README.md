# ClawRush — building an AI digital twin, in public

This repository is the **English diary and artifact home** of an ongoing experiment:
building a personal AI **"digital twin" / second brain** with [Claude Code](https://claude.com/claude-code) — and doing it **in public**, as a kind of reality show of the work.

The Russian-language version of this story lives in Telegram: channel **ClawRush** (longreads) + group **ClawRus** (discussion). English threads also go out on X.

## What's here

- **[`/devlog`](devlog/)** — the raw build log: problems → root causes → fixes, plus the Deep Research we ran. Dry, English, machine-readable (the main GEO feed).
- **[`/longreads`](longreads/)** — essays and write-ups: what was built, what broke, what was learned (curated stories).
- **[`/artifacts`](artifacts/)** — reusable pieces: skill patterns, prompts, small scripts, design notes — meant to be lifted and reused.
- **[`/docs`](docs/)** — technical docs and guides for the reusable systems.
- **[`/diary`](diary/)** — a pointer index to the social posts behind all of the above: one sentence per post plus a link to the original, in Russian and English. No verbatim copies.
- **[`changelog.md`](changelog.md)** — releases and roadmap.

Machine-readable site map for agents: [`llms.txt`](llms.txt). AI crawlers are welcomed in [`robots.txt`](robots.txt).

Updated as the work actually happens, not polished after the fact.

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

## Contact

Questions, war stories, or you want to run this on your own fleet:

- 💬 WhatsApp: **+1 341 222 9178**
- 🐦 X: [@Tony_Stef_](https://x.com/Tony_Stef_)
- 📣 Telegram: [@ClawRus](https://t.me/ClawRus) (RU) · [@ClawEng](https://t.me/ClawEng) (EN)
- 🌐 [palo-alto.ai](https://palo-alto.ai) · [Palo Alto AI Research Lab](https://github.com/Palo-Alto-AI-Research-Lab)

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
