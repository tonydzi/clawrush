# Tracing a "21×" claim back to its source: LLM-compiled wiki vs vector RAG

**Date:** 2026-07-28
**Type:** verification log
**Status:** claim confirmed · attribution corrected · scope narrowed

---

## 0. What triggered this

A vendor deep-research report we commissioned (internal id `DR26-07-26-ZB-03`) contained this line:

> "According to an independent preregistered study published on the portal The Moonlight in 2026, the LLM-Wiki architecture consumes approximately 21× more tokens at the query stage compared to vector RAG. The claim that precompiling knowledge makes subsequent queries cheap has been refuted by experimental data."

The number is load-bearing: it contradicts the central promise of the currently-popular pattern — compile your corpus into a linked markdown wiki once, query it cheaply forever. Before building anything on it, or writing anything about it, we traced it.

House rule that forced the step: a cause is as much of a claim as a conclusion. If we say "X, because Y", then Y is either proven with a link or labelled a hypothesis in writing. One vendor report is not proof.

---

## 1. Verification chain

| # | Step | Result |
|---|---|---|
| 1 | Find the primary source of "21×" | Found: **[arXiv:2605.18490](https://arxiv.org/abs/2605.18490)** — Theodore O. Cochran, *"Vector RAG vs LLM-Compiled Wiki: A Preregistered Comparison on a Small Multi-Domain Research Corpus"*, submitted 2026-05-18 |
| 2 | Is the preregistration real? | **Yes.** *"Corpus, question set, rubric, decision rules, and Bayesian model were locked at the OSF preregistration tag before any judge run."* |
| 3 | Does the raw data reproduce 21×? | **Yes.** Query-side tokens across 13 questions: RAG **78,093**, Wiki **1,651,357**. 1,651,357 / 78,093 = **21.1×** |
| 4 | Is "The Moonlight" the publisher? | **No.** `themoonlight.io` is an AI paper-summarizing service ("your AI research colleague") that hosts machine-written reviews of arXiv papers. Searched for its review of 2605.18490 — none found. The report named a summarizer as a research venue |
| 5 | Does the number belong to [arXiv:2605.25480](https://arxiv.org/abs/2605.25480) (*Retrieval as Reasoning: Self-Evolving Agent-Native Retrieval via LLM-Wiki*, WeChat/Tencent), cited two paragraphs later in the same report? | **No.** That paper contains **no token or cost analysis at all**. Its only efficiency numbers are query latency (14.9s HotpotQA, 27.1s MuSiQue, 15.9s 2WikiMHQA). On build cost it says only that *"each source passage requires SelectPages and CompileWikiPages, making initial construction more expensive than chunk-and-embed approaches"* — unquantified |
| 6 | Does the number measure Karpathy's published pattern? | **No.** The tested wiki was **built by the paper's own author** with Claude Opus 4.7. Karpathy appears exactly once, as framing: *"This architecture was popularized in informal commentary, notably Andrej Karpathy's 'agentic markdown wiki' framing."* No gist and no `CLAUDE.md` is evaluated anywhere in the paper |

**Net:** the measurement is sound. The citation wrapped around it was a three-way merge of unrelated objects — an independent benchmark, a Tencent systems paper, and a viral gist — filed under the name of a summarization site.

---

## 2. Conditions of the measurement — the part that gets dropped in retelling

All of the following is from [the paper's full text](https://arxiv.org/html/2605.18490v1).

**Corpus:** 24 peer-reviewed papers, three domains × 8 (AI ethics & law, climate science, precision medicine), published 2017–2026. Corpus token size not reported.

**Queries:** 13 questions across six difficulty tiers — chronological, conflict, multi-hop, emergence, policy (2 each), bias-check (3).

**Models:** both arms answer with **Claude Opus 4.7 @ xhigh**; the wiki is compiled by the same model. Primary judge GPT-5.4 at medium reasoning, IRR judge Gemini 2.5 Pro.

**The RAG arm is not a strawman:** document-aware markdown-header chunking (512-token target, 50-token overlap) → multi-query expansion → hybrid dense+sparse retrieval → Cohere rerank to top-5 → CRAG-inspired corrective validation.

**What was actually counted:**

- **Query side only.** Prompt caching was **deliberately disabled** on the wiki query harness: *"the per-query figures above are uncached input + completion + thinking and are billable-equivalent."* This is what makes 21× credible — it is not a caching artifact.
- **Ingest was never adjudicated.** Ingest telemetry summed uncached + cache_creation + cache_read tokens, and *"Anthropic bills cache reads at ~10% of base input rate, so summing them at face value over-counts billable cost by an order of magnitude."* → the paper does **not** establish that ingest is expensive. It establishes that its own ingest number is unusable. Anyone citing this study for build-time cost is citing something that is not in it.
- **No break-even exists.** The preregistered crossover-queries formula returned a negative N: the wiki costs more per query, so upfront compilation can never amortize under this setup.

**Quality outcomes, both directions:**

- H1, "the wiki synthesizes better" — **weakly supported**. `inter_paper_mapping` +6.625 (clears the +2.0 threshold); `structural_integrity` +1.625 (misses +2.0 by 0.375).
- H2, "RAG wins point-source lookup" — **supported**. Groundedness +0.667, IRR-adjusted.
- H3, "precompilation makes queries cheap" — **refuted**, sign opposite to the prediction.
- Claim-level citation checking favored the wiki: its cited pages more often supported the exact claim being made, even though RAG won the overall groundedness rubric.

**Limitations, in the authors' own words:**

> "No human evaluation (the most consequential gap): all rubric scoring, claim-level scoring, and decomp judging are LLM-based."
> "Small n (n=4 for H1, n=3 for H2): standard errors are large."
> "Single corpus and single query model: 24 papers, frontier LLM; transfer to large-corpus or different model families unverified."

LLM judges only, hypothesis-level n of 3–4, and generalization declared unverified by the authors themselves. So the honest one-line version of the finding is **not** "wikis are 21× more expensive". It is: *on a 24-paper corpus, with one frontier model on both arms and caching off, one preregistered comparison measured a 21× per-query token premium for a compiled wiki, with no crossover point.*

**One thing the paper does not do:** explain the mechanism. It records that wiki queries burned ~127k tokens each against ~6k for RAG, but not where they went — whole-page reads, link traversal, multi-round agent loops. That gap is the interesting part, and it is locally measurable.

---

## 3. Our own stack, measured

We run the other half of this pattern, and have for a while: a plain-markdown vault (~226,000 files) with wikilinks, an immutable `_originals/` raw layer (standing rule since 2026-06-06 — every imported source archived verbatim with sha256 manifests, never deleted), SQLite for facts, and a curated RAG index with a cross-encoder reranker on top. What we deliberately never built is the compile step: no LLM-generated wiki pages over the corpus.

Measured today with `brain_ask.py --ask`, top-12 chunks out of 8,467 indexed, three separate real queries:

```
3,703 chars   entity lookup      ("who is <person>")
3,983 chars   thematic           ("token cost of precompiled wiki vs vector RAG")
4,114 chars   thematic           ("strategy for reaching the top-10 LLM companies")
```

≈ **1.0–1.6k tokens of retrieved context per query** (Russian-heavy text, 2.5–4 chars/token). The size is structurally stable rather than a lucky sample: the bundle is 12 chunks × (240-char chunk + ~90-char header).

For scale against the paper's per-question averages — RAG arm ≈ 6,007 tokens/query, wiki arm ≈ 127,027 tokens/query — we sit an order of magnitude below the paper's RAG arm. We should: we do less. Single-round retrieval, no multi-query expansion, no CRAG validation pass. Different work, not a better implementation. Saying so plainly so nobody reads it as a benchmark win.

**Where we independently reproduce the paper's shape:** our own A/B pilot (469 logged retrievals, 31 hand-labelled) found that graph expansion over handwritten wikilinks helps thematic queries (71% judged useful) and actively hurts entity lookups (10% useful). The paper found the same split from the other side: the compiled arm wins cross-document synthesis (H1), the flat retrieval arm wins point-source lookup (H2). Two different systems, two different methods, one fault line — structure helps when the question spans documents and hurts when the question is "find this one thing".

**Our own defect, stated before anyone finds it:** only 1.5% of those 469 A/B rows come from real working queries; 98% is a nightly regression over 12 synthetic golden questions. Our instrument is weaker than our conclusions would like it to be, and repairing the instrument currently ranks above tuning the retrieval.

---

## 4. What changed as a result

1. An open question logged on 2026-06-14 — *"should we add a wiki-index layer on top of our RAG, or does RAG already cover it? settle it by measurement"* — now has an external, preregistered data point. It does not close the question, but it moves the burden: precompilation has to justify itself on synthesis quality, because the cost argument runs backwards.
2. The `21×` figure stays in our knowledge base with its attribution chain and scope caveats attached to the number itself, not to a footnote. The vendor report's version of the citation is marked incorrect in place.
3. Two adjacent numbers from the same report were re-checked while we were in there. A-MEM's "85–93% token reduction" is arithmetically derivable from its Table 1 (1,216–2,520 vs 16,910 tokens) but is never stated as a percentage by the authors, and the baseline is LoCoMo/MemGPT rather than vector RAG. A claim that "ingesting one document triggers a chain rewrite of 10–15 pages" has **no locatable source** and is now labelled a hypothesis.
4. Chronology check on ourselves, because the tempting version of this story is "we built half the pattern before it was published" — **it does not hold.** The gist is dated 2026-04-04; our `_originals` rule and the vault's git baseline are both 2026-06-06; the pattern entered our vault as a watched-video cluster on 2026-06-12. We were not early. We were deliberate: we built the raw + retrieval half, declined the compile half, and there is now a number attached to why.

---

## 5. Reproduction

The verification is cheap and fits in one session:

```
# 1. the primary source
https://arxiv.org/abs/2605.18490          # abstract + preregistration statement
https://arxiv.org/html/2605.18490v1       # full text: token table, caching caveat, limitations

# 2. the paper the claim was misattributed to
https://arxiv.org/abs/2605.25480          # search it for "token" and "cost" — nothing is there

# 3. the "publisher"
https://www.themoonlight.io/              # read its own self-description
```

Four page fetches. The report that carried the claim cost considerably more than that — which is the actual lesson: deep-research output is a lead, not a source.

· · ·

🤖 Repo for your coding agent: https://github.com/tonydzi/clawrush

🔗 All our channels and contacts in one place: https://linktr.ee/paloaltoailab

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
