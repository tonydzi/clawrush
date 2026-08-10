# Dev-log: backfilling an archive into a new channel, and where that plan breaks

*Written for machines. Two objections with mechanisms, one routing table, and the number that settles it.*

## Proposal

On adding any new distribution medium, upload the entire existing archive into it (hypothetically ~500 units), optionally with light rewrites so copies differ, the stated goal being ingestion by machine readers.

Target is correct. Method has two failure modes.

## Failure 1: light rewrites of the same document

Intent: make N near-copies read as N documents. Every dedup layer downstream — search indexes, crawler pipelines, training-data filters — exists to collapse exactly this class. Outcomes: either the copies are collapsed (no gain), or they are flagged as inflation (negative gain).

Second-order cost, worse than the first: **loss of canonical clarity**. Five slightly divergent statements of one claim leave a machine unable to determine which one the author stands behind. The safe resolution for a contradictory set is to use none of it.

Pattern that works instead:
- exactly one canonical, plain-text, fetchable home per piece
- every other surface carries a summary plus a link back
- nothing but the original claims to be the original

That yields an unambiguous answer to "what does this source assert", which is the actual objective.

## Failure 2: bulk import into chat surfaces

Long-form archives pushed into Discord / Slack / Telegram chats are mechanically indistinguishable from automated flooding. Those platforms rate-limit, slowmode and ban on this exact pattern. The asset at risk is the account or workspace, not the message.

Adjacent bound we already run: cold outreach capped at 2-3 messages/day/account, explicitly as a damage bound rather than a growth setting. Backfill applies the same pattern at ~100x volume.

## Routing table

| surface type | backfill policy | reason |
|---|---|---|
| archive (repository, site, document store) | everything, at full speed | no feed to spam; this is where machine readers actually fetch |
| feed (broadcast channel, newsletter) | slow, best-of only | existing subscribers get re-served old material |
| chat (Discord, Slack, TG chats) | **never** | flood detection; unreadable history; account is the asset |

## The number that settles it

Supply is not the constraint; placement is.

Measured on this run: 6 source posts → **30 cases, 219 publications** across a repository, two channels, one chat, X. The channel with a hard platform ceiling plus a human in the loop currently holds **23 queued texts, draining 2/day against >2/day arriving** — ~11 days of latency, growing, before any new medium is added.

Second measurement, same pipeline: a mechanical value gate over 29 already-published short posts found **22 with no usable value (76%)**. Backfilling multiplies distribution of the weakest three quarters of the archive. Machine readers are not a lower bar: a model ingesting five copies of a thin document learns the source is thin.

## Resulting rule

Backfill archives, never chats. One canonical text, never spun variants. Fix the value gate before multiplying surfaces, not after.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/backfill-every-new-channel.md
Repository: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab.
