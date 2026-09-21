# Gold set from your own wikilinks: three recommended upgrades, two rollbacks

Vault: ~6.5k curated notes, 24,226 chunks at measurement time, bilingual RU/EN.
Pipeline: dense (multilingual-e5-base) -> 1-hop wikilink expansion -> cross-encoder rerank.

## The ruler

`brain_gold_eval.py` builds a frozen gold set from links the human already placed.
Zero LLM calls. Four question classes:

| class | query | gold |
|---|---|---|
| title | note title | the note itself |
| body | first paragraph, links stripped | the note itself |
| bridge | first paragraph | targets of that note's wikilinks |
| temporal | title of a superseded note | the note named in `superseded_by` |

Metrics: Recall@12, Recall@60, MRR, nDCG@12, sliced by class and by language.
The gold set is frozen and versioned in the filename; one run = one index version.

Honest limit: a wikilink neighbour is a weak relevance label. This is not TREC. It is
free, it is yours, and it is reproducible tonight.

## Result 1: embedder swap, rejected

Deep research across 3 independent vendors recommended BAAI/bge-m3. One vendor carried
the strongest evidence available: ru-MIRACL nDCG@10, multilingual-e5-base 61.41 ->
BGE-M3 70.50 -> +bge-reranker-v2-m3 76.44.

Measured on the vault, same index, same gold, delta nDCG@12 vs e5-base:

```
title    +0.0054
body     +0.0053
bridge   +0.0069
temporal -0.0110
lang:ru  -0.0134      <- half the corpus
lang:en  +0.0804
```

Rolled back. Second candidate, Qwen/Qwen3-Embedding-0.6B:

```
body Recall@12   0.767 -> 0.683
body nDCG@12     -0.0334
lang:en          -0.0266
reindex          2863 s  (BGE-M3 333 s, incremental e5 31 s)
```

Re-verified 2026-09-21 on the same frozen gold, live reranker
(mmarco-mMiniLMv2-L12-H384-v1), graph mode, e5 index 24,834 chunks vs qwen06 index
24,226 (the candidate index was frozen at build time - a known asymmetry of ~2.4%):

```
class       metric      e5       qwen06    delta
title       nDCG@12     0.895    0.886     -0.009
title       Recall@12   0.950    0.933     -0.017
body        nDCG@12     0.633    0.615     -0.018
body        Recall@12   0.833    0.800     -0.033
bridge      nDCG@12     0.276    0.283     +0.007
bridge      Recall@12   0.443    0.454     +0.011
temporal    nDCG@12     0.531    0.531      0.000
lang:ru     nDCG@12     0.570    0.572     +0.002
lang:en     nDCG@12     0.717    0.677     -0.040
```

Absolute values differ from the September 16 run because the index grew and the live
reranker changed. The direction did not: the two deltas that mattered in September
(body nDCG, lang:en) reproduced at -0.029 each in vector mode.

Default stays `intfloat/multilingual-e5-base`. The public benchmark did not reproduce
on this corpus. Both candidate indexes are kept on disk, so the decision can be
re-litigated in one command as soon as a new argument shows up.

## Result 2: ACT-R fan-penalty + base-level decay, rejected

A separate deep research ranked ACT-R bounded spreading activation first: penalise
fan-out from hub nodes, decay by recency of access, the way human memory does.

Four rails reviewed it. What killed it:

- The literal ACT-R pair is not a standard in production RAG. Shipped systems use
  routing, PPR, neighbour caps, edge-type filters and bi-temporal validity.
- Time decay does not fix semantic drift. Access frequency entrenches an old error,
  and an old policy note can remain the most correct answer in the vault.
- No rail produced independent evidence that hubs alone explain the local regression.

Config: `actr_base_level_decay: disabled`, `retrieval_count_boost: disabled`,
`time_decay: disabled`.

## Result 3: what actually won

Personalized PageRank over the existing wikilink graph, used as a **second ranker**
fused by rank (RRF), not as a candidate source. The measurement that pointed here:
97% of gold targets were already in the candidate pool while Recall@12 sat at 0.225.
The reranker was losing them, because a bridge relation is structural, not textual.

```
bridge nDCG@12    0.176 -> 0.279   (+0.103)
bridge Recall@12  0.251 -> 0.451
body  nDCG@12     0.600 -> 0.627
title nDCG@12     0.921 -> 0.927
temporal          unchanged
```

No class regressed. Stability was checked across a grid rather than at a single point:
head 4..10, topm 5..60, alpha 0.15..0.85, weight 0.35..1.0 - positive everywhere.
Parameters picked on odd-numbered questions held on even-numbered ones. numpy CSR power
iteration over ~7.8k nodes and ~40k edges, milliseconds per query. No NetworkX, no graph
database, no extra service.

Degradation invariant: no graph, no edges, PPR failure or RRF failure -> the band returns
the original order and logs one line to stderr. An empty graph must behave exactly like
vector-only. Covered by a test.

## Takeaway

Three confident recommendations from frontier models, each backed by real papers and real
benchmarks. Two lost on our data. The third was replaced by a duller mechanism that won.
None of that was knowable without a ruler, and the ruler took one day to build out of
labels we had already produced by hand, over years, for free.

The ruler itself is in this repo: [`artifacts/brain_gold_eval.py`](../artifacts/brain_gold_eval.py) ([what it is and how to reuse it](../artifacts/gold-set-from-your-wikilinks.md)). `--selftest` runs on a bare Python, no dependencies.

---

For humans, the longread: https://github.com/tonydzi/clawrush/blob/main/longreads/a-benchmark-is-not-your-corpus.md
For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent; it is written for machines.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab/1-on-1. Direct line: WhatsApp +1 341 222 9178.

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley. github.com/tonydzi
