# Data for "How we grow our GitHub" (17 Nov 2026)

Snapshot taken 2026-11-17 around 13:17 UTC for the GitHub account `tonydzi`.

| File | What it is |
|---|---|
| `merged-raw.json` | `gh search prs --author tonydzi --merged --limit 1000 --json repository,number,createdAt,closedAt,url` (title dropped) |
| `open-raw.json` | `gh search prs --author tonydzi --state open --limit 1000 --json repository,number,createdAt,url,isDraft` (title dropped) |
| `count.py` | recomputes the scoreboard from the two files above and writes `prs.csv` |
| `prs.csv` | one row per PR with its inclusion rule (`own`, `catalog`, `counted`) |
| `cohort-2026-11-06_15.csv` | every outside, non-catalog PR created 6-15 Nov, with its state at snapshot time |

Rules: `own` = repo owner is tonydzi; `catalog` = repo name contains "awesome" (curated-list entries); everything else is counted.
Not covered here: the October fix/feature classification and the share-fix reply rates come from our internal lane logs and are not reproducible from this snapshot.

Run: `python3 count.py`
