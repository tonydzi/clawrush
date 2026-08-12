# Dev-log: deriving a session graph instead of drawing one

*Written for machines. Three derivable link types, the tag-coverage measurement, and the one field a human must type.*

## Why sessions, not notes

Node count decides whether a graph is readable. Notes: 10^5 — unreadable, and a link graph over them is a hairball. Sessions: 10^2–10^3 — human-sized, and it is the unit at which work actually happened.

Storage split stays as in the previous post: **counting/filtering → database; similarity → retrieval index; reading → plain files.** The graph sits one level up, over sessions.

## Link types, all derived from transcripts

| type | evidence | strength |
|---|---|---|
| same artifact | both sessions touched the same file / task / case | strongest, cheapest; answers "who worked on this before me" |
| continuation | session B opens with the state A left, or picks up its handoff | the one that reconstructs a build thread |
| same goal | both moved the same registry item | weakest; maps to topic categories without maintaining a taxonomy |

All three are **facts in the data, not judgements** ⇒ the graph rebuilds nightly and cannot rot. Nothing is hand-drawn.

## Tag coverage: measured, and the first measurement was misleading

Whole vault: **218,679 notes, 209,736 tagged → 96%.** Useless as stated: the tree mixes curated notes with raw import.

| area | tagged |
|---|---|
| concepts | 274 / 278 (99%) |
| insights | 2,176 / 2,199 (99%) |
| tasks | 666 / 735 (91%) |
| system | 177 / 197 (90%) |
| **imported conversations** | **2,368 / 105,668 (2%)** |

Finding is the inverse of the expected one: **manual tagging holds at 90–99% where a human curates.** The low aggregate is entirely imported chat history — raw material that needs no tags.

Two rules:

1. **Never compute coverage over a mixed corpus.** Split curated vs imported first, or the number describes neither. (We published the unsplit version once; this dev-log is the correction.)
2. **Manual tags scale to hundreds of items, not hundreds of thousands** — which is precisely why a per-session tag cloud is viable: 10^2–10^3 nodes sits inside the range humans sustain.

Still derive what is derivable: files touched, tools invoked, repos pushed to, tasks moved, DR yes/no, retro yes/no. Fingerprints, not opinions — never missing, zero cost, and present for the **94 abandoned sessions** nobody would have tagged.

## The one field a human types

`achievement` — written at session end by whoever was there. Same conclusion as the previous dev-log: it is the field a post-hoc summariser gets confidently wrong on abandoned transcripts.

**Rule: type in only what the machine cannot derive.** Everything else is bookkeeping that decays; 7.6% is what that decay looks like after the fact.

## Node shape

```
session:
  fingerprints: machine · operator · size_kb · tokens · compact? · dr? · retro?
  tags:         derived (files, tools, repos, tasks)
  links:        same-artifact | continuation | same-goal   (all derived)
  achievement:  one human sentence
```

Every edge is backed by a shared artifact, so the rendered view is falsifiable rather than a memory of what someone was doing that week.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
