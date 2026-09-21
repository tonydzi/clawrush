# A gold set for your own notes — `brain_gold_eval.py`

**What.** A ruler for a personal RAG / second-brain system. It turns the wikilinks you
already placed by hand into a frozen relevance-judgement set, then scores your retrieval
pipeline on it: Recall@12, Recall@60, MRR, nDCG@12, sliced by question class and language.
Zero LLM calls, zero API spend.

**Why.** We ran a deep research pass across three independent LLMs on which embedder to
adopt. All three agreed: switch to BGE-M3. One carried a Russian benchmark showing
nDCG@10 61.41 → 70.50. We measured on our own corpus first. Russian went **down** 0.0134.
Rolled back. The second candidate, Qwen3-Embedding-0.6B, lost harder — and lost again on a
re-run five days later:

```
class       metric      e5-base   Qwen3-0.6B   delta
title       nDCG@12     0.895     0.886        -0.009
body        nDCG@12     0.633     0.615        -0.018
body        Recall@12   0.833     0.800        -0.033
bridge      nDCG@12     0.276     0.283        +0.007
temporal    nDCG@12     0.531     0.531         0.000
lang:ru     nDCG@12     0.570     0.572        +0.002
lang:en     nDCG@12     0.717     0.677        -0.040
```

A published benchmark is a fact about someone else's corpus. Until you have a ruler of
your own, every model swap is superstition with a citation attached.

The same ruler paid for itself in the other direction: it showed that 97% of correct
answers were already sitting in our candidate pool while Recall@12 was 0.225 — the
reranker was dropping them, because a link between two notes is a structural relation and
a cross-encoder only sees text. That pointed at Personalized PageRank as a *second ranker*
rather than a candidate source: bridge nDCG@12 0.176 → 0.279, Recall@12 0.251 → 0.451, no
other class regressed.

**The four question classes.** Gold is a list of note stems; comparison is by basename.

| class | query | gold answer | what it probes |
|---|---|---|---|
| `title` | a note's title | that note | finds a thing you named |
| `body` | first paragraph, links stripped | that note | meaning, not word overlap |
| `bridge` | first paragraph | targets of that note's wikilinks | can it walk relations |
| `temporal` | title of a superseded note | the note in `superseded_by` | does it serve stale truth |

`bridge` is the honest, nasty one. `temporal` needs `superseded_by` / `valid_to` fields in
frontmatter; if you close outdated notes by editing them in place instead, you cannot build
this class at all — which is itself worth knowing.

**How to reuse.**

```
python brain_gold_eval.py --selftest                      # stdlib only, no deps
python brain_gold_eval.py --build --n-per-class 60        # -> eval/gold-<date>.jsonl
python brain_gold_eval.py --run --gold eval/gold-<date>.jsonl
python brain_gold_eval.py --run --gold ... --embedder-backend <name>
```

The file ships as it runs in our vault, comments in Russian included, rather than as a
cleaned-up fork that would drift from the real thing. Two halves, and the split matters:

- **Runs anywhere, stdlib only** — the metrics (`recall_at`, `mrr`, `ndcg_at`), the
  frontmatter/first-paragraph parsing, the gold-set builder `build_gold`, and `--selftest`
  (10 checks; verified on a bare Python 3.12 with no venv and no torch).
- **Needs our retrieval stack** — `run()` imports `brain_ask`, `brain_common`,
  `brain_emb_backends`, `brain_rerankers`, `brain_graph`. Swap those five imports for your
  own retriever and the rest works unchanged. That is the intended seam.

**Honest limits.** A wikilink neighbour is a *weak* relevance label — you are measuring
against your own judgement, not ground truth, so it catches regressions and ranks
alternatives but does not tell you how good you are in absolute terms. This is not TREC.
One run = one index version; freeze the gold set and put the date in the filename, or you
will compare two different things and believe the result. Our `temporal` class has only 4
questions, which is too few to trust on its own, and we say so in every report rather than
quietly dropping the row.

**Thresholds we use** (engineering targets from our own synthesis, not a published norm):
title Recall@12 ≥ 0.90 · body ≥ 0.80 · bridge ≥ 0.70 · temporal ≥ 0.60. The graph band
earns its place if bridge nDCG@12 rises ≥ +0.03 with no more than 0.01 lost on body.

Full story, for humans: [A benchmark is not your corpus](../longreads/a-benchmark-is-not-your-corpus.md) ·
[technical devlog](../devlog/a-benchmark-is-not-your-corpus.md) ·
[RU](../longreads-ru/2026-09-21-benchmark-ne-tvoy-korpus.md)

---

Built by Mycroft, a synthetic co-founder, and Tony Dzi (Anton Dziatkovskii) at Palo Alto AI
Research Lab. Proudly made in Silicon Valley.

Questions, or a story about your own rejected upgrade: WhatsApp **+1 341 222 9178** ·
[@Tony_Stef_](https://x.com/Tony_Stef_) · Telegram [@ClawEng](https://t.me/ClawEng) ·
[all channels](https://linktr.ee/PaloAltoAI) · [github.com/tonydzi](https://github.com/tonydzi)
