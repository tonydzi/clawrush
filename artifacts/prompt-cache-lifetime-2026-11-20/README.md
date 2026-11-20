# Prompt cache lifetime: Codex vs Claude Code (2026-11-20)

Instrument and aggregates behind the longread
[Our Claude Code calls go cold after 60 idle minutes. Our Codex calls go cold slowly, over a day.](../../longreads/prompt-cache-lifetime-codex-vs-claude-code-2026-11-20.md)
([RU](../../longreads-ru/prompt-cache-lifetime-codex-vs-claude-code-2026-11-20.md)).

Only aggregates are published here. Session logs, session titles and message text stay on our machines.

## Files

| File | What it is |
|---|---|
| `extract.py` | Reads local Claude Code (`~/.claude/projects`) and Codex (`~/.codex/sessions`) logs, writes one JSON row per session with per-call token usage. Paths at the top are ours; change them. |
| `analyze.py` | Cost in input equivalents, human returns by pause and context size, the threshold model. Writes `report.json` (not published: it carries machine names). |
| `codex_ttl.py` | Cold-call share by pause for Codex, from per-machine probe files. The probe that collected those files over ssh is not included. |
| `tables.py` | Builds `tables.json` and `tables.md`, the tables used in the article. Expects `extract.py` output in `../session-context-audit/data/`; adjust `AUD`. |
| `codex_after_claim.py` | Control run: Codex cold calls by pause, only for calls after 2026-10-22. |
| `check_numbers.py` | Fails if a number in the article is not found in the instrument output or in the fact-check notes. |
| `tables.json`, `tables.md`, `codex_after_claim.json` | The aggregates. |
| `dr/` | Deep research DR26-11-20-MACSTUDIOM4-01-0251: the prompt, the vendor reports as collected, and our synthesis with the list of what the reports got wrong. |

## Definitions

- Claude Code cold call: at least half of the call's input was not read from cache, context at least 50K tokens.
- Codex cold call: cached read is less than half of the previous call's context, previous context at least 30K tokens.
- Input equivalent: tokens weighted by API list price relative to fresh input. Weights are in the header of `analyze.py`.

## Limits

API list prices, not subscription limits. The saving is modeled. A cold call is not always an expired cache. Small counts near the 60-minute edge. One fleet. About 20,268 compressed Codex logs were not read.

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab.
