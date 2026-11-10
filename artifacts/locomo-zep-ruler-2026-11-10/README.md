# LoCoMo by Zep's ruler, 2026-11-10

Per-question outputs for the longread "We ran our memory through Zep's own LoCoMo ruler".

- `runs/ans_<arm>_rN.jsonl`: reader answers (`qid`, `answer`, `model`, `ms`). `qid` = `<sample_id>#<index in qa>` of
  snap-research/locomo `locomo10.json`.
- `runs/jud_<arm>_rN.jsonl`: judge grades (`label`, `is_correct`, `reasoning`, `parsed`, `model`).
  `jud_zepans_upstream_r1.jsonl` carries Zep's own published grades; `jud_zepans_r1.jsonl` our judge on the same answers.
- `runs/ctx_<arm>_rN.jsonl.gz`: retrieved contexts for the arms we ran (mem0, graphiti, ours). Zep's contexts are
  Zep's published `data/zep_locomo_search_results.json` (33 MB), full-context is the dataset itself; neither is copied.
- `results.json`, `report.md`: aggregate (correct / 1540, per category, mean +- sd over runs).
- `bench_zepruler.py`: the runner. Prompts are read from `upstream/*.py` (getzep/zep-papers@4b7f26cc) with a sha check;
  the upstream files are not redistributed here: `python fetch_upstream.py` downloads them at the pinned commit and
  verifies `upstream/SHA256.json`. In this public copy the paid-API key variable is `OAI_KEY`.
- Models: reader `gpt-6-sol`, judge `grok-4.20-0309-non-reasoning` via our own subscriptions; Zep's rows use Zep's
  published `gpt-4o-mini` outputs. Mem0 OSS 2.2.1 ran vector-only (BM25 off, `fastembed` not installed); Graphiti 0.31.2
  ran without a cross-encoder. Stores for Mem0 and Graphiti were built on 2026-11-08 with Gemini 3 Flash extraction
  and E5 embeddings.

Anton Dziatkovskii - github.com/tonydzi
