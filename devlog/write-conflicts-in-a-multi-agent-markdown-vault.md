# Write conflicts in a multi-agent Markdown vault: taxonomy is not the variable

**Status:** field report. Measured on a live 6-node fleet, 2026-07-25 → 2026-07-28.
**Claim under test:** "PARA-style folder organization causes race conditions in multi-agent knowledge bases."
**Verdict:** the phenomenon is real and reproducible. The attribution to folder taxonomy is unsupported by our data and by the literature.

## 1. Setup

| Property | Value |
|---|---|
| Nodes writing to one vault | 6 (Windows hub, 2× MacBook, 2× Windows laptop, Linux VPS) |
| Transport | Syncthing — **no merge**; loser of a concurrent write is preserved as `*.sync-conflict-*` |
| Vault size | ~175k notes, Markdown + YAML frontmatter |
| Retrieval layer | SQLite + embeddings + reranker |
| Folder scheme | Semantic/numbered (`00-System`, `02-Decisions`, `03-Insights`, `06-Concepts`, `07-People`, `10-Tasks`) |
| **PARA in use** | **No.** No actionability-based partitioning anywhere in the tree |

The last row is what makes this a useful data point: the vault is a *negative control* for the claim under test.

## 2. Measurements

| Metric | Value | When |
|---|---|---|
| `*.sync-conflict-*` files, total | 3695 | 2026-07-25 21:25 |
| — of which in `.stversions` (local trash, never synced) | 3694 | same |
| — **live conflicts** | **75** | same |
| Live conflicts after root fix | **0** | 2026-07-27 19:31 |
| Work actually lost and recovered | 2 sections + a `state: done` field in a task file; 5 lines of `ROADMAP.md`; 1 status cell in the research registry | 2026-07-27 |

Counting note: 99.97% of the raw number was Syncthing's local version trash and never propagated. Reporting "3695 conflicts" would have been technically true and materially misleading. Live and archived counts must be reported separately.

## 3. Root causes — three classes, not one

A single universal remedy ("assign one writer") is wrong. The correct remedy depends on **where the data originates**.

### Class A — node-local data written to a shared path
Files: per-node session boards, quarantine lists, automation inventories.
Single-writer here is **actively harmful** — the fleet would go blind on every other node.
**Fix:** per-node filename suffix + one generated index page that aggregates them.

### Class B — genuinely shared data, generated on several nodes
Files: task backlog, orphan list, people MOC, canon index.
**Fix:** one designated writer, enforced **in code, not in the scheduler.** A task disabled on a remote peer comes back — via reinstall, restore, or a manual run. A schedule is a request; a code gate is a prohibition.

### Class C — shared cache with an unstable body
File: `_onair/ACTIVE_NOW.md`.
Root cause was **not writer count**. The body contained `_updated <timestamp> by <machine>_`, so the bytes differed on every regeneration even when the semantic content was identical. Every node rewrote it every time.
**Fix:** remove the volatile line from the body; write-if-changed.

None of the three classes is a function of how directories are named.

## 4. The diagnostic case

Live/conflict pair, `04-Projects/fireflies-meetings/2026-07-27-planerka-utro-*.md`:

```
live file:      199 561 bytes
conflict copy:  200 978 bytes
diff:           3 lines — all in the YAML frontmatter

  node A:  type: meeting
  node B:  type: reference
           stage: raw
```

Two agents disagreed on **one classification token** and each rewrote **200 KB of transcript** to record that disagreement.

This is the crux:
- The contended value *is* a taxonomy field. That part of the original claim is correct.
- The damage vector is **write granularity**: the minimum writable unit was the whole file.
- Removing folders does not remove the contention — `type:` still gets assigned by someone. The failure reproduces under any organizational scheme.

## 5. Cross-check against the literature

Searched for evidence that folder taxonomy is causally implicated in multi-agent write conflicts.

**Found — for the phenomenon:**
- Pre-write admission control ([arXiv:2607.00041](https://arxiv.org/abs/2607.00041)): a system must decide, before applying a governed shared mutation, which concurrent write intents may proceed in parallel, which require serialization, and which must fail closed.
- Write-time validation against read dependencies ([arXiv:2605.20563](https://arxiv.org/abs/2605.20563)): a write is valid only if the target file *and its read dependencies* are unchanged since the agent last observed them. Root cause named: **stale reads**.
- Industrial practice: per-agent worktree isolation.

**Found — for the taxonomy attribution:** nothing. Across the multi-agent conflict literature, directory organization is not discussed as a variable. The named variables are consistently: staleness of reads, write granularity, writer cardinality.

**Note on source quality:** the report that prompted this investigation flagged the PARA paragraph itself as low-authority ("consensus of developers on Reddit/HN"). Its academic backbone checks out — [arXiv:2605.25480](https://arxiv.org/abs/2605.25480) (LLM-Wiki / Retrieval-as-Reasoning / Error Book) exists and matches its description. The failure was localized to the one paragraph the vendor had already marked as weak.

## 6. Convergence

Our open follow-up after the fix: hand-edited `ROADMAP.md` and the DR registry are still written by multiple nodes and need sharding.

The write-time-validation paper states the same limitation from the other direction: file-level tracking produces false-positive rejections when two agents edit different regions of one file, turning heavily shared files into serialization bottlenecks.

Independent convergence on the same boundary: **file-level granularity is the ceiling.**

The DR registry has since moved to sharded IDs (`DR26-07-28-ZB-05-0850`, time-suffixed) so nodes no longer contend for a row.

## 7. Reframed rule

> Resistance to concurrent writes is a property of **each artifact**, not of the taxonomy: writer cardinality, minimum write unit, and body stability under unchanged inputs.

Per-file triage, three questions:

1. **How many nodes may write this path?** >1 with shared data → designate one writer, gate in code.
2. **Is the data node-local?** → per-node filename. A shared file is harmful here, not helpful.
3. **Is the body stable?** Timestamp or hostname inside → bytes always differ → write-if-changed.

Implementation: `_imports/sync/derived_writers.json` (`writers` · `per_node` · `idempotent`) + `derived_writers.guard(<path>)`. Functionally this is pre-write admission control, built at hand-tool scale: one JSON registry and one guard function instead of a content-identifier broker.

## 8. Not tested

The third part of the original claim — that folder hierarchies degrade vector retrieval by creating "topological barriers" — **was not tested by the report and has not been tested by us.** No measurement was found either way.

Falsifiable design: one corpus, two directory layouts, identical chunking and embeddings, identical query set, compare recall@k. Until that runs, this remains a hypothesis and is labeled as one.

## Related
- Research prompt in flight: `DR26-07-28-ZB-05-0850` — write-safe knowledge architecture under concurrent multi-agent writes
- Prior beat: fleet vault conflict flood, three-class root fix (2026-07-27)

· · ·

🤖 Repo for your coding agent: https://github.com/tonydzi/clawrush

🔗 All our channels and contacts in one place: https://linktr.ee/paloaltoailab

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
