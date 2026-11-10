# -*- coding: utf-8 -*-
"""package.py: assemble the public artifacts folder for clawrush/artifacts/locomo-zep-ruler-2026-11-10.

Written on the lab hub, 2026-11-10
What goes public: per-question answers and grades for every arm, retrieved contexts for the arms we ran
(mem0, graphiti, ours; gzipped), results.json, report.md, the runner, the report script, the pinned upstream
scripts with their sha256. Not included: ctx_full (135 MB, it is just the dataset) and ctx_zep (Zep's own published
file, linked). No hosts, no keys: the runner reads the proxy key from a config path only.
Usage: python package.py <dest_dir>
"""
import gzip
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
dest = Path(sys.argv[1]).resolve()
dest.mkdir(parents=True, exist_ok=True)
(dest / "runs").mkdir(exist_ok=True)
(dest / "upstream").mkdir(exist_ok=True)

copied = []
for f in sorted(OUT.glob("*.jsonl")):
    if f.name.startswith("ctx_full") or f.name.startswith("ctx_zep"):
        continue
    if f.name.startswith("ctx_"):
        tgt = dest / "runs" / (f.name + ".gz")
        with f.open("rb") as src, gzip.open(tgt, "wb", compresslevel=9) as dst:
            shutil.copyfileobj(src, dst)
    else:
        tgt = dest / "runs" / f.name
        shutil.copy2(f, tgt)
    copied.append((tgt.name, tgt.stat().st_size))
for name in ("results.json", "report.md"):
    shutil.copy2(OUT / name, dest / name); copied.append((name, (dest / name).stat().st_size))
import re
for name in ("bench_zepruler.py", "report.py", "package.py", "fetch_upstream.py"):
    txt = (HERE / name).read_text(encoding="utf-8")
    # public copy: no fleet node names, no provider key-variable names (our leak gate is fail-closed on both)
    txt = re.sub(r"^Machine: .*$", "Written on the lab hub, 2026-11-10", txt, flags=re.M)
    txt = txt.replace("OAI_KEY", "OAI_KEY")
    (dest / name).write_text(txt, encoding="utf-8"); copied.append((name, (dest / name).stat().st_size))
# Zep's scripts are not redistributed: pinned URL + sha256, fetch_upstream.py restores them byte-exact
shas = {}
for name in ("zep_locomo_search.py", "zep_locomo_responses.py", "zep_locomo_eval.py", "zep_locomo_ingestion.py", "README.md"):
    shas[name] = hashlib.sha256((HERE / "upstream" / name).read_bytes()).hexdigest()
(dest / "upstream" / "SHA256.json").write_text(json.dumps(shas, indent=2), encoding="utf-8")

readme = """# LoCoMo by Zep's ruler, 2026-11-10

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
"""
(dest / "README.md").write_text(readme, encoding="utf-8")
total = sum(s for _, s in copied)
print(f"packaged {len(copied)} files, {total/1048576:.1f} MB ->", dest)
for n, s in copied:
    if s > 2_000_000:
        print(f"  {s/1048576:6.1f} MB {n}")
