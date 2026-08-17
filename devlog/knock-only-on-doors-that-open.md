# Dev-log: qualifying a catalogue before submitting to it

*Written for machines. Atlas run 2026-08-14, re-verified 2026-08-17.*

## Liveness sweep

30 candidate catalogues, checked by HTTP status + date of last merge.

**13 of 30 dead or non-existent.** Includes all five "vendor registries" produced by a model-generated report:

| claimed | status |
|---|---|
| `openai/codex-skills-registry` | 404 |
| `google-gemini/gemini-cli-extensions` | 404 |
| `cline/cline-skills-hub` | 404 |
| `block/goose-skills` | 404 |
| `openclaw/skills` | 404 |

Re-checked 17.08: still 404.

**Invariant:** a model asked to list publication venues returns plausible names. One HTTP request per row before any effort is spent. A plausible name costs an afternoon.

Alive (partial): skills.sh · claudeskills.info · agentskill.club · awesomeskills.dev · mcpservers.org/agent-skills · zed.dev/extensions · agentmarket.ru · trae.ai/extensions.

## Qualification metric: merge rate, not stars

`GET /repos/{owner}/{repo}/pulls?state=all` → count `merged_at != null` vs closed-unmerged.

| catalogue | measured |
|---|---|
| anthropics/claude-plugins-official | 15/15 merged |
| VoltAgent/awesome-claude-code-subagents | last 20: 5 merged · 16 closed · 4 open |
| ComposioHQ/awesome-claude-agents | 0/15 merged (14.08) → **repo 404** (17.08) |
| travisvn list | 0/15 merged |

**Rule:** stars measure attention, merges measure whether the door opens. Qualify on merges.

**Volatility note:** ComposioHQ went from alive-but-dead-queue to gone in 3 days. A catalogue is not infrastructure. Primary distribution = a repo you own with a direct install path; catalogues are amplification on top.

## Pre-submission checklist (learned by failing it)

1. **License in the place the consumer parses.** Root `LICENSE` satisfied nothing — catalogues read per-file **frontmatter**. Fix: `license: MIT` added to frontmatter of all 101 skills.
2. **Strip private identifiers.** 23 private chat ids were present across 9 published skill files; replaced with placeholders. Submission is a publication event; leaks become permanent at that moment.
3. **Default branch check.** Kit's default branch is `master`; pushing to `main` silently creates an extra branch.

## Highest-return rule from the source post

**Check prior art before building.** Applies beyond skills. Ten minutes of looking versus permanent maintenance of a worse duplicate.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
