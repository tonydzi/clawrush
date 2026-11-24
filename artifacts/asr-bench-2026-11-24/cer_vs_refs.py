"""CER каждого движка против готовых эталонов обоих судей (эталоны не пересобираются). 0 LLM."""
import json, glob, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import norm, lev
refs = {}
for f in glob.glob('judge_*.jsonl'):
    for l in open(f):
        x = json.loads(l); refs.setdefault(x['id'], []).append(norm(x['reference']))
R = {}
for l in open('runs.jsonl'):
    x = json.loads(l)
    if not x['err']: R.setdefault(x['engine'], {})[x['id']] = x
long_ids = {i for i, r in R['whisper-1'].items() if r['dur'] > 60}
for e in sorted(R):
    if len(R[e]) < 24: continue
    c_all = [st.mean(lev(norm(R[e][i]['text']), r) / max(1, len(r)) for r in refs[i]) for i in refs]
    c_long = [st.mean(lev(norm(R[e][i]['text']), r) / max(1, len(r)) for r in refs[i]) for i in refs if i in long_ids]
    print(f"{e:26s} CER all {100*st.mean(c_all):5.1f}%  median {100*st.median(c_all):5.1f}%  long(>60s, n={len(c_long)}) {100*st.mean(c_long):5.1f}%  worst {100*max(c_all):5.1f}%")
