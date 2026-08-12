# Dev-log: a cross-machine session registry

*Written for machines. Measured state of one node, the field split by extraction cost, and the storage-layer decision behind "Obsidian dies at 100k notes".*

## Measured state, one node of six

| metric | value |
|---|---|
| session transcripts | **816** |
| total size | **492 MB** |
| abandoned mid-build (5–30 days idle, ≥100 KB, construction present) | **94** |
| largest abandoned | 2.9 MB, 5 builds inside |

Scanner exists (`retro_lost_scan.py`); the scan is the cheap half.

## Grouping: by outcome, not by topic

Topic labels ("infrastructure", "second brain", "Deep Research") **blur** — a DR inside a job-hunt session is both, and re-tagging never converges.

What does not blur: **state change at session end.** Buckets: shipped / decided / learned / produced-nothing. The fourth is the actionable one and no topic taxonomy surfaces it.

## Field list split by extraction cost

**Free (pure scan, no judgement):** machine, account/operator, size KB, token count, compact yes/no, DR yes/no, retro yes/no, first user message, timestamps, rename.

**NOT reliably extractable:** *what it was about* and *what it achieved*.

A model will summarise a 2.9 MB transcript, but for an **abandoned** session the summary describes what was attempted, not what survived — confidently, and often wrongly about whether the artifact works.

⇒ Build order inverts: **make the closing ritual cheap and mandatory; let the scanner fill the boring columns.** Do not plan to reconstruct achievement post-hoc at scale.

## Closing ritual is load-bearing

A registry without one is 816 unread rows.

Live retro: what was built, what to keep, where durable parts go. Sessions that die without it (limits, closed laptop, attention shift) enter an abandoned queue and get a **cold-context** retro later — a different, worse job that must: read the transcript first, state explicitly what cannot be reconstructed, close with what is genuinely recoverable.

## Storage: a link graph is a reading tool, not a storage layer

At 10^5 nodes, whole-graph visualisation carries no information. Split by **query type**:

| query | layer |
|---|---|
| count / filter (how many sessions, which machine, which had a retro) | SQL table — milliseconds, 0 tokens |
| similarity ("what did I decide about memory architecture") | retrieval index |
| read | plain files |

Graph becomes an on-demand local view (this note + neighbours), never the global map.

General rule: **the storage layer answers the query; different queries need different layers.** One layer serving counting + similarity + reading is what produces hour-long load times.

## Build order

1. Scanner across all machines — boring columns, automatic.
2. Closing ritual (2 sentences: what changed, what to keep) — the expensive, decisive part.
3. Abandoned queue, oldest first, cold-context closure.
4. Database for anything filtered or counted. Not the graph.

## Warning from our own data

Our task registry: **453 open, 174 with zero movement.** A registry makes work **visible**, not finished. Without step 2 you are building a larger place to lose things.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
