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

## Tag coverage: measured, not assumed

**Vault: 106,878 notes; 8,175 carry tags → 7.6%.**

Nobody decided to stop; tags are the first thing dropped mid-work. A scheme applied to 7.6% of the corpus is not a filter — sorting by it silently returns a twelfth of the corpus.

Model auto-tagging does not fix it: plausible labels, no ground truth, and a wrong tag is indistinguishable from a right one without opening the note.

**Derive tags from what the session did instead:** files touched, tools invoked, repos pushed to, tasks moved, DR yes/no, retro yes/no. Fingerprints, not opinions — never missing, never wrong, zero cost, and present for the **94 abandoned sessions** that were never tagged by anyone.

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
