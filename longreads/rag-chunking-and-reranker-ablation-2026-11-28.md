(Full Publication & CTO Outreach Draft)

# Why We Turned Off Our Cross-Encoder Reranker, Found 38.5% Silent Chunk Truncation, and Tested Mem0, Zep/Graphiti, and SQLite on Their Own Benchmarks

**By Anton Dzyatkovskiy · Palo Alto AI Research Lab**
*Code & Reproducible Benchmarks:* [`tonydzi/sqlite-graph-memory`](https://github.com/tonydzi/sqlite-graph-memory) · [`tonydzi/memory-over-time`](https://github.com/tonydzi/memory-over-time) · [`tonydzi/clawrush`](https://github.com/tonydzi/clawrush)

In recent conversations with engineering leaders building agent memory systems - including a great technical discussion with Mem0 CTO Deshraj Yadav - two practical questions kept coming up:
1. **"What should the chunk size be in the first place, and how many chunks (`top-k`) should you fetch during RAG?"**
2. **"Why do standard RAG best practices - like adding a cross-encoder reranker or fixed character chunking - often degrade retrieval on real personal and multi-agent memory corpora?"**

Over the past six months, we have run an always-on multi-agent memory layer in production across **111,532 curated knowledge chunks (~30,228 markdown documents)** and **832,113 agent session chunks**, backed by an open-source local engine (`sqlite-graph-memory`). Whenever a retrieval change is proposed, we test it against frozen real-world and synthetic benchmarks:
- **Vault Gold-184:** 184 real queries over 111.5K production chunks (`60 body`, `60 title`, `60 bridge`, `4 temporal`), evaluated with 10,000-iteration paired bootstrap.
- **`memory-bench v0.1`:** 91 queries (`69 answerable` across 5 reasoning classes + `22 unanswerable` abstention traps) over 202 notes.
- **DolphinBench Source-Session Retrieval (`mem0ai/dolphinbench`):** 50 tasks over `200`, `1,000`, and all `5,128` multi-turn sessions (~500K tokens).
- **LoCoMo (`1,540` questions, Categories 1-4):** evaluated under Zep's exact prompt protocol across 3 runs with independent reader/judge calibration.
- **Bitemporal Lifecycle (`Room 402` + `30 CRM as-of state queries`):** testing out-of-order updates and retraction of erroneous memories across 13 extraction LLMs.

Here are the four most counter-intuitive engineering lessons we measured - with exact numbers.

---

### 1. Why Our Cross-Encoder Reranker Degraded Retrieval Across Four Benchmarks (and Why We Turned It Off)

From June to November 2026, our second stage ran `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` (and later `BAAI/bge-reranker-v2-m3` and `Qwen/Qwen3-Reranker-0.6B`) over the top 60 dense candidates. When we finally audited the reranker against a no-reranker baseline across four datasets, **the cross-encoder lost on every single dataset**:

| Benchmark Dataset | Corpus Scale & Queries | Dense E5 (No Reranker) | Dense E5 + Cross-Encoder | Reranker Delta | Hybrid `Dense E5 + SQLite FTS5 BM25 (RRF)` (No Reranker) |
|---|---|---|---|---|---|
| **Real Vault Canary** | 40 notes, **24 queries** | `R@1 = 0.792`<br>**`R@5 = 0.958`** | `R@1 = 0.708`<br>**`R@5 = 0.875`** | **`-8.3 pp R@5`** | **`R@5 = 0.958`** (`10 ms` query) |
| **`memory-bench v0.1`** | 202 notes, **69 queries** | **`R@1 = 0.739`**<br>**`R@5 = 0.928`** | **`R@1 = 0.616`**<br>**`R@5 = 0.884`** | **`-12.3 pp R@1`**<br>(`paraphrase_bridge`: **`0.50 -> 0.08`**) | Beats even `RRF(dense, CE)` (`R@1 = 0.659, R@5 = 0.906`) |
| **DolphinBench (1K)** | 1,000 sessions, **50 tasks** | **`R@5 = 0.610`**<br>`Hit@5 = 68%` (`39 ms`) | **`R@5 = 0.480`**<br>`Hit@5 = 54%` (`2,775 ms`) | **`-13.0 pp R@5`**<br>(`71x` slower) | **`R@5 = 0.717 / R@10 = 0.843`**<br>`Hit@5 = 80%` (`48 ms`) |
| **DolphinBench (Full 5.1K)** | 5,128 sessions (~500K tok.), **50 tasks** | **`R@5 = 0.400`**<br>`Hit@5 = 46%` | **`R@5 = 0.220`**<br>`Hit@5 = 28%` | **`-18.0 pp R@5`** | **`R@5 = 0.540 / R@10 = 0.650`**<br>`Hit@5 = 60%` (`132 ms`) |
| **Vault Gold-184 (`body` slice)** | 111,532 chunks, **60 body queries** (184 total) | **`body R@12 = 0.983`**<br>(`nDCG = 0.911`, `2 min`) | **`body R@12 = 0.850`**<br>(`nDCG = 0.601`, `25 min`) | **`-13.3 pp R@12`**<br>**`-0.310 nDCG`** | Production (`BM25 RRF + PPR`, no CE):<br>`body R@12 = 0.933`, `bridge = 0.439`, `title = 0.933` |

On a 10,000-resample paired bootstrap over all 184 Gold queries, **every tested cross-encoder had a statistically significant negative 95% confidence interval** compared to no reranker (`bge-reranker-v2-m3` full chunk: `-0.074`, 95% CI `[-0.113, -0.037]`; `mmarco` snippet: `-0.114`, 95% CI `[-0.156, -0.073]`; `mmarco` full chunk: `-0.147`, 95% CI `[-0.191, -0.104]`).

#### The 4 Root Causes Behind the Reranker Failure
1. **Head-Snippet Blindness (`240 / 1500` chars = 16% visibility):** Initially, stage 2 passed `title + ". " + chunk[:240]` to the reranker while chunks were 1,500 characters long. Whenever the dense embedder found a chunk whose answer lay in characters `241..1500`, the cross-encoder read only the first 16% of the chunk, saw no lexical overlap, assigned a negative logit, and evicted the right document.
2. **The 512-Token Ceiling & Long-Passage Dilution (`0.967 -> 0.850` on 60 body queries):** When we fed the full 1,500-character chunk to the cross-encoder, our nightly 60-query `body` benchmark immediately dropped from `Recall@12 = 0.967` to `0.850` for six consecutive nights. Why? Because 1,500 characters of Russian/English technical markdown + title + query tokenizes to **550-700 XLM-R tokens** (`median = 599.5 tokens`, with **97% of full 1,500-char chunks exceeding the 512-token limit**). Worse, MS MARCO cross-encoders are trained on ~60-word web passages; feeding them 500-token multi-paragraph blocks dilutes cross-attention across unrelated sentences.
3. **Query-Type Mismatch (`paraphrase_bridge` collapsed from `0.50` to `0.08`):** On `memory-bench v0.1`, the cross-encoder slightly helped on short entity `bridge` queries (`0.87 -> 0.97`), hurt `paraphrase` (`1.00 -> 0.80`), and devastated `paraphrase_bridge` (`0.50 -> 0.08`). When a user asks a paraphrased question that shares zero surface keywords with the note, dense embeddings bridge the semantic gap, whereas an MS MARCO cross-encoder acts as a strict lexical gatekeeper and kills the candidate.
4. **Why Hybrid `Dense + SQLite FTS5 BM25 (RRF)` Fixed It Without a Reranker:** Unlike a cross-encoder that overwrites dense ranks, Reciprocal Rank Fusion (`RRF_K = 60`) with `SQLite FTS5` BM25 **only boosts** exact keyword matches across the entire un-truncated chunk in `2-11 ms` while never penalizing semantic paraphrases found by the dense vector lane.

---

### 2. Chunk Size & `top-k`: Why Fixed Character Windows Silently Truncate 38.5% of Chunks

To answer Deshraj Yadav's question (*"What should the chunk size be, and how many chunks to fetch?"*), we audited our production corpus (`111,532` vault chunks, mean `1,274.6` chars; `832,113` session chunks, mean `1,475.95` chars), which used a standard fixed character window of `CHUNK_CHARS = 1500` with `OVERLAP = 200` (`step = 1300` chars).

When we tokenized a random sample of **3,000 vault chunks (`seed=42`)** and **200 full 1,500-character chunks** using our dense embedder's actual tokenizer (`intfloat/multilingual-e5-base`, `max_seq_length = 512` tokens, input `"passage: " + title + ". " + body`), we found a silent killer:

| Corpus Sample (`"passage: " + title + ". " + body`) | Median Tokens | p90 Tokens | p99 Tokens | Max Tokens | Share of Chunks **> 512 Tokens** (Silently Truncated!) |
|---|---|---|---|---|---|
| **All Vault Chunks** ($n=3,000$ of $111,532$) | **489 tok.** (RU `480`, EN `403`) | **579 tok.** | **730 tok.** | **1,154 tok.** | **38.5%** (~42,940 chunks truncated by `e5-base`!) |
| **Full 1,500-Char Chunks** ($n=200$, typical of long notes & 832K session chunks) | **599.5 tok.** | **638 tok.** | **659 tok.** | **664 tok.** | **97.0%** (194 / 200 chunks lose their last `~88 tokens / ~250-350 chars`!) |

Because `OVERLAP = 200` characters is smaller than the `250-350` characters chopped off after token 512, every boundary between consecutive 1,500-character chunks in a 512-token embedder creates a **30-150 character dead zone that is never embedded in either chunk** (surviving only in the FTS5 BM25 index).

#### Why Naive Heading Prefixes (`H1 > H2 > H3`) Backfired (`-0.023 nDCG@12`)
We also tested prepending markdown heading breadcrumbs (`H1 › H2 › H3`) to every chunk on `Vault Gold-184`. Instead of improving retrieval, it **dropped `body nDCG@12` from `0.611` to `0.588` (`-0.023`) and `temporal nDCG@12` from `0.638` to `0.603` (`-0.035`)**. Even when restricted to continuation chunks (`chunk_idx > 0`) with title deduplication, `body nDCG@12` still dropped to `0.590`. Why? In structured knowledge bases, template headings (`Facts` 912x, `Log` 873x, `Alpha` 724x, `Why` 618x) repeat across thousands of unrelated files, pulling their embeddings toward a shared centroid while consuming precious tokens at the front of the 512-token window.

#### The Engineering Rule: Separate Three Windows Under a Fixed Token Budget
1. **Index Unit (Embedder Window):** Never define chunk size in raw characters without bounding it by the embedder's token limit. Split first on structural boundaries (`\n## `, `\n### `, blank lines `\n\n`, or chat turn boundaries), then cap each index chunk at **`320-384 tokens` (`~900-1,000 chars` for multilingual text, overlap `64 tokens`)** so **0% of chunks hit the 512-token wall** and each vector represents one atomic thought.
2. **File-Level Candidate Grouping (`CHUNKS_PER_FILE = 3`):** Fetch `TOPK_RETRIEVE = 60` chunks, keep up to `3` chunks per document during fusion/scoring, and deduplicate by document *after* RRF + graph scoring.
3. **Reader Unit & `top-k` (Pareto Frontier Under Fixed Token Budget $B$):** Don't compare `k=5` across different chunk sizes without holding the prompt token budget $B = k \times \text{chunk\_tokens}$ constant. On our `69-query` retrieval bench, `Recall@k` plateaus at **`k = 5` (`R@5 = 0.928` vs `R@10 = 0.942`)**: doubling `k` from 5 to 10 adds only `+1.4 pp` recall while doubling prompt tokens and distractor noise. Instead of returning raw `[:240]` heads, return a **query-centered window (`window_snippet`, `350-450 chars` around matched query stems) or expand the winning `320-token` child chunk to its parent section (`~600-800 tokens`) within a fixed `2,500-3,500` token budget (`top-k = 5..8` unique notes)**.

---

### 3. Auditing the Benchmarks: LoCoMo (`75.14% vs 68.44%`), DolphinBench, and Bitemporal Retraction

When evaluating external memory layers (Mem0, Zep Cloud, Graphiti, Anima Labs) alongside our SQLite engine, we found three structural blind spots in industry benchmarks:

#### A. LoCoMo Measures Reader + Judge Sensitivity as Much as Memory
In the public LoCoMo debate (Zep's `75.14 ± 0.17%` vs Mem0 Graph's `68.44%` across 1,540 questions in Categories 1-4), the benchmark scores an end-to-end pipeline: `Memory Retrieval -> LLM Reader -> LLM Judge ("be generous")`.
When we ran a controlled 3-run ablation on Zep's own 1,540 published contexts and answers (`locomo-zep-ruler-protocol-2026-11-10`):
- **Judge Shift (`-3.44 pp` on identical answers):** Scoring Zep's exact 1,540 published answers with `grok-4.20` instead of `gpt-4o-mini` (using Zep's verbatim judge prompt) shifted Zep's score from **`75.13%` (1157/1540) to `71.69%` (1104/1540)** ($\kappa = 0.84$) - half the entire published gap between Zep and Mem0!
- **Reader Shift (`+4.2 pp` on identical retrieved context):** Keeping the judge fixed at `grok-4.20` and swapping Zep's reader (`gpt-4o-mini`) for `gpt-6-sol` on Zep's exact retrieved contexts raised the score from **`71.69%` to `75.9%` (`+4.2 pp`)** without changing a single retrieved fact.
- **Zero-LLM Ingestion Baseline (`84.5%` Single-Hop):** Under the exact same reader and judge (`gpt-6-sol` + `grok-4.20`, 3 runs), passing the full ~16K-token conversation without any memory system scored **`86.6%`**, **Mem0 OSS 2.2.1 (`infer=True`)** scored **`78.6 ± 0.2%`** (`Single-Hop 83.8%`, `Temporal 67.0%`, `Multi-Hop 81.2%`), **Zep Cloud contexts** scored **`75.9 ± 0.4%`** (`Temporal 70.0%`), **our zero-LLM dated turn log (`Dense E5`)** scored **`72.1 ± 0.2%`** while **winning Single-Hop at `84.5%`**, and **Graphiti OSS 0.31.2 (edges+nodes without raw turns)** scored **`42.3 ± 0.5%`**. Mem0's real edge on dialogue LoCoMo is specifically in **Category 2 (`Temporal`: `67.0%` vs `44.9%`)**, where its write-time LLM resolves relative dates (*"last Tuesday"*) into absolute dates.

#### B. DolphinBench Door 1: Zero-LLM Hybrid Retrieval Beats Heavy Ingestion at 1/20th the Latency
On Mem0's DolphinBench (`Riley` persona, `1,000` sessions / `50` tasks), isolating pure `source_session_ids` retrieval shows that our zero-LLM **`SQLite FTS5 BM25 + Dense E5 (RRF)`** indexes 1,000 sessions in **`41.5 s` (vs `1,323 s` for Mem0 OSS)**, queries in **`48 ms` (vs `952 ms`)**, and achieves **`Recall@10 = 0.843` (`Hit@5 = 80%`) vs `0.743` (`Hit@5 = 72%`) for Mem0 OSS**.

#### C. Bitemporal Memory & The Write-Time Invalidation Trap (`getzep/graphiti#2165`)
For facts that change over time (e.g., CRM deal stages, role changes, or our `Room 402` bitemporal benchmark), systems like Graphiti (`0.31.2`) mutate the old edge at write time by setting `invalid_at` when a newer episode arrives.
- **What breaks:** When a newly ingested episode turns out to be an extraction error and is retracted via `remove_episode()`, the bad new edge is deleted, **but the prior edge remains permanently closed (`invalid_at` is never rolled back)** - leaving Room 402 empty (`2/3` on Room 402; reported in [`getzep/graphiti#2165`](https://github.com/getzep/graphiti/issues/2165)). Furthermore, across 30 `as-of` CRM state queries over 15 field updates, Graphiti's accuracy ranged from **`0/30` to `27/30`** across 13 extraction LLMs (~10 min ingest).
- **The AK-47 Fix (`Read-Time Interval Closure`):** Our 302-line append-only bitemporal log (`fact_history.py` / `brain_temporal.py`) never mutates past rows on write. Instead, it computes `valid_to[i] = valid_from[i+1]` dynamically at read time over non-retracted transactions (`retracted_tx IS NULL OR retracted_tx > tx_at`). It passes **`3/3` on Room 402 (including retraction)** and **`30/30 (100%)` on CRM `as-of` queries in `0.01 ms` median latency with `0` LLM calls**.
- **Bonus - Knowing When to Say "I Don't Know" in `0 ms`:** On `memory-bench v0.1` (`69` answerable + `22` unanswerable queries), a single deterministic cosine threshold (`max_score < 0.785` on `e5-base`) separates missing memories with **`F1 = 0.880` (`100%` abstention recall on unanswerable queries, `86.4%` specificity)** in `0 ms` with zero LLM calls - outperforming cross-encoder logit thresholding (`F1 = 0.567`).

---
