"""Replay the memory-bench threshold ablation and the gold-note extractor control.

Usage (from a checkout of github.com/tonydzi/sqlite-graph-memory, any commit with bench/ at
or after cbf93bb):
    cd bench/adapters && python /path/to/replay_threshold.py

What it does, with no model and no retrieval run:
1. Re-applies the shared extractor (_extract.best_sentence) to the saved rankings in
   results/sqlite-graph-memory-vector.json, with the adapter's rule
   "no answer if top reranker score < 0 or no sentence found". Prints how many of the 91
   saved answers it reproduces.
2. Repeats with the score threshold removed (extractor rule only).
3. Feeds each of the 10 `paraphrase` questions its gold support notes and counts how often
   the extractor still returns nothing.

Expected output (11 Nov 2026):
    gate on : correct refusals 10/22, false refusals 18/69, answers passing 23/69
    gate off: correct refusals 3/22, false refusals 6/69, answers passing 25/69
    reproduced saved answers 91/91
    paraphrase with gold notes, extractor empty 10/10
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, ".")
from _extract import best_sentence  # noqa: E402

notes = {os.path.splitext(os.path.basename(p))[0].lower(): open(p, encoding="utf-8").read()
         for p in glob.glob("../vault/**/*.md", recursive=True)}
qs = {}
for line in open("../questions.jsonl", encoding="utf-8"):
    q = json.loads(line)
    qs[q["id"]] = q
saved = json.load(open("../results/sqlite-graph-memory-vector.json", encoding="utf-8"))


def passes(answer, q):
    return bool(answer) and any(re.search(r"\b" + re.escape(g.lower()) + r"\b", answer.lower())
                                for g in q["answers"])


reproduced = 0
for gate in (True, False):
    correct_ref = false_ref = good = 0
    for r in saved["per_question"]:
        q = qs[r["id"]]
        _, sent, _ = best_sentence(q["question"], r["retrieved"], lambda n: notes.get(n, ""))
        answer = None if (not sent or (gate and r["top_score"] < 0)) else sent
        if gate and (answer or None) == (r.get("answer") or None):
            reproduced += 1
        if q["cls"].startswith("absent"):
            correct_ref += answer is None
        else:
            false_ref += answer is None
            good += passes(answer, q)
    print("gate %-3s: correct refusals %d/22, false refusals %d/69, answers passing %d/69"
          % ("on" if gate else "off", correct_ref, false_ref, good))
print("reproduced saved answers %d/91" % reproduced)

empty = total = 0
for q in qs.values():
    if q["cls"] != "paraphrase":
        continue
    total += 1
    _, sent, _ = best_sentence(q["question"], [s.lower() for s in q["support"]],
                               lambda n: notes.get(n, ""))
    empty += sent is None
print("paraphrase with gold notes, extractor empty %d/%d" % (empty, total))
