"""Recompute the scoreboard of 'How we grow our GitHub' (17 Nov 2026) from the raw snapshots.

Inputs (taken 2026-11-17 ~13:17 UTC):
  merged-raw.json  gh search prs --author tonydzi --merged --limit 1000 --json repository,number,createdAt,closedAt,url (titles dropped)
  open-raw.json    gh search prs --author tonydzi --state open --limit 1000 --json repository,number,createdAt,url,isDraft (titles dropped)
Output: prs.csv (one row per PR with the inclusion decision) and the counts on stdout.

Rules:
  own        repo owner is tonydzi -> excluded (our own projects)
  catalog    repo name contains 'awesome' -> excluded (one-line list entries, not code or docs work)
  counted    everything else
Window cohorts for the November comparison: created 2026-11-06..2026-11-15, outcome as of the snapshot.
"""
import csv, json

def decide(p):
    owner, name = p["repository"]["nameWithOwner"].split("/")
    if owner.lower() == "tonydzi":
        return "own"
    if "awesome" in name.lower():
        return "catalog"
    return "counted"

merged = json.load(open("merged-raw.json"))
opened = json.load(open("open-raw.json"))
rows = []
for p in merged:
    rows.append(dict(url=p["url"], repo=p["repository"]["nameWithOwner"], state="merged",
                     created=p["createdAt"][:10], closed=p["closedAt"][:10], draft="", rule=decide(p)))
for p in opened:
    rows.append(dict(url=p["url"], repo=p["repository"]["nameWithOwner"], state="open",
                     created=p["createdAt"][:10], closed="", draft=str(p.get("isDraft", "")), rule=decide(p)))
rows.sort(key=lambda r: (r["state"], r["created"]))
with open("prs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

m = [r for r in rows if r["state"] == "merged" and r["rule"] == "counted"]
cat = [r for r in rows if r["state"] == "merged" and r["rule"] == "catalog"]
o = [r for r in rows if r["state"] == "open" and r["rule"] == "counted"]
nov = [r for r in m if r["closed"] >= "2026-11-01"]
first = min(r["closed"] for r in m)
print("merged counted:", len(m), "in", len({r["repo"] for r in m}), "projects; first merge", first)
print("merged catalog entries excluded:", len(cat))
print("open counted:", len(o), "of them drafts:", sum(r["draft"] == "True" for r in o))
print("november merged:", len(nov), "in", len({r["repo"] for r in nov}), "projects")
