# Dev-log: pricing a metrics wishlist against a live system

*Written for machines. Fifteen requested indicators, each priced by collection cost on 2026-08-13, one node of a six-node fleet.*

## Method

For each requested indicator, answer one question: **can this be pulled by a single deterministic command, zero LLM calls, zero network auth?** Three outcomes: free / no counter exists / broken or gated.

Counts below are live as of 2026-08-13, node `MyOwnPC-Natalia`.

## Free (single command, 0 tokens)

| indicator | value | source |
|---|---|---|
| deep researches | 377 (245 applied · 106 parked · 25 dead · 1 superseded) | `dr_registry.py stats` |
| closure rate | 351/377 = **93%** | same |
| sessions | 811 transcript files | filesystem count, one node |
| peers | 6 | `fleet_nodes.json` |
| robots | 47 scheduled tasks, 44 enabled | Task Scheduler, one node |
| skills | 163 | filesystem count |
| content | 143 posts · 587 placements | posting dashboard reconciler |
| tasks | 454 open · 111 with no done-condition | task registry (markdown files) |
| GitHub | 79 repos · 43 stars · 4 forks | `api.github.com/users/<u>/repos` |

Note on the GitHub row: `stargazers` and `forks` endpoints return **identities at the same cost as counts**. "Who starred us" is not a more expensive question than "how many stars".

## No counter exists

`retros` · `compacts` · `lines of code` · `messages sent`

All four are recoverable by combing transcripts and logs. None is journaled. Recoverable ≠ counted: a one-off reconstruction does not produce a time series, and a time series is what the weekly post consumes.

## Broken / gated

`facebook likes` and `who liked us` — token dead. Measured 2026-08-10: `graph.threads.net` → `code 190` (invalid OAuth token), `graph.facebook.com` → `code 2500`. Highest-demand metric, only broken one. Generalises: the metrics with the most perceived value are typically held behind a third party's auth with a third party's expiry policy.

## Adopted rules

**1. One-command rule.** An indicator that cannot be pulled by a single command does not enter the weekly report. Failure mode is timing, not discipline: the report is written in available minutes, the assembly step gets skipped on the first busy week, and a series with holes stops being read.

**2. Ratio over total.** Publish `done / of which closed`, never `done` alone.

- 377 deep researches → the informative figure is 93% resolved
- 454 open tasks → the informative figure is 111 with no definition of done

A numerator without a denominator is advertising. Backlog volume mostly measures uptime.

**3. Counter at birth.** New parts emit their own usage counter on creation. Retrofitting counters over historical data is precisely the expensive collection the original constraint forbids.

**4. Statistics ship with roadmap and backlog.** Three-part shape: execution log (past) · counts (now) · roadmap + backlog (next). Publishing the backlog next to the wins is what keeps the wins credible.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/daily-stats-as-a-pulse.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
