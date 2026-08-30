# tools/ — passport

## build_feed.py

**What it does.** Turns the essays in `longreads/` into `feed.xml` (RSS 2.0) at the repo root.

**In.** Every `longreads/*.md` except `README.md`. Title = the file's first `# ` heading.
Date = the commit that *added* the file (`git log --diff-filter=A`), because file mtime is
rewritten by every clone and by Syncthing. Summary = first real paragraph, markdown stripped,
cut at 300 chars.

**Out.** `feed.xml` — newest 40 posts, newest first.

**Who pulls it.**
- the profile README at [github.com/tonydzi](https://github.com/tonydzi)
  (`blog-post-workflow` fills the "Latest writing" block from this feed);
- anything else that speaks RSS: `https://github.com/tonydzi/clawrush/raw/main/feed.xml`.

**Who runs it.** `.github/workflows/feed.yml` — on every push that touches `longreads/`,
plus nightly at 03:00 UTC (04:00 Lisbon, inside the fleet night window). It self-tests first,
then commits `feed.xml` only when the content actually changed.

**How to run it by hand.**

```bash
python3 tools/build_feed.py           # rewrite feed.xml
python3 tools/build_feed.py --check   # exit 1 if feed.xml is stale, change nothing
python3 tools/_test_build_feed.py     # 13 checks, exit 0 = green
```

**What breaks it, and how you'd know.**

| Symptom | Cause | Fix |
|---|---|---|
| A new essay never shows up on the profile | file has no `# ` heading on its first heading line | add one; the script prints `skip (no '# ' heading)` |
| An essay is dated today though it's old | it was re-added (deleted + committed again), so the *add* commit is new | leave it, or `git log --follow` the file to confirm |
| Every night a no-op commit lands | someone removed the `lastBuildDate` reuse in `main()` | restore it — the build date alone must never count as a change |
| Posts come out in slightly the wrong order | someone sorted on the ISO *string* again | sort on the parsed instant; this repo holds commits at +05:00, +02:00, +01:00 and −07:00, and `…T01:00+14:00` sorts after `…T23:00−10:00` as text while being earlier in time |
| The nightly job fails with "non-fast-forward" | a human pushed between checkout and push | already handled — the workflow rebases and retries three times |
| Workflow fails with an empty feed | `longreads/` was moved or emptied | the script refuses to write an empty feed and exits 1 by design |
| Dates are all identical | checkout without `fetch-depth: 0` — no history to read | keep `fetch-depth: 0` in the workflow |

**Dependencies.** Python 3 stdlib and `git`. Nothing else — no network at build time.
