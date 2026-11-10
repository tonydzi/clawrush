# -*- coding: utf-8 -*-
"""bench_zepruler.py: LoCoMo by Zep's own ruler, applied to our memory arms (v2 after Codex review 2028898).

Written on the lab hub, 2026-11-10

What "Zep's ruler" means here (pinned to getzep/zep-papers@4b7f26cc, kg_architecture_agent_memory/locomo_eval):
  * dataset  snap-research/locomo data/locomo10.json, 10 conversations, categories 1-4 (category 5 = adversarial,
             excluded by Zep: zep_locomo_search.py `if qa.get('category') == 5: continue`), N = 1540 questions
  * context  Zep: 20 facts (edges, cross-encoder) + 20 entities (nodes, rrf) in TEMPLATE; every arm here gets the
             same budget K = 20 retrieved units (Graphiti: 20 edges + 20 nodes in the same TEMPLATE)
  * reader   zep_locomo_responses.py: system_prompt + user prompt, loaded byte-exact from the pinned file,
             gpt-4o-mini, temperature 0
  * judge    zep_locomo_eval.py: system_prompt + ACCURACY_PROMPT byte-exact, structured output Grade
             {is_correct, reasoning}, gpt-4o-mini, temperature 0; label rule upstream: is_correct.lower()=='correct'
  * score    correct / 1540; per-category labels follow snap-research/locomo (Zep's README swaps 2/3):
             1 multi-hop · 2 temporal · 3 open-domain · 4 single-hop

Arms:
  zep       Zep Cloud's own published search contexts (upstream/data/zep_locomo_search_results.json), our reader+judge
  zepans    Zep's published gpt-4o-mini answers re-judged by our judge (calibration vs their 1157/1540 grades)
  mem0      Mem0 OSS 2.2.1 infer=True, Qdrant stores built 08.11 (../memory-over-time-bench-20261108/full/mem0_rN)
  graphiti  Graphiti 0.31.2 + Kuzu graphs built 08.11, edges+nodes hybrid RRF (no cross-encoder on hand)
  ours      time-stamped turn log, dense E5 top-K (our fact_history shape, no extraction)
  full      whole conversation with session dates (upper bound, no memory system)

Model backends: READER_MODEL / JUDGE_MODEL env. `gpt-4o-mini` (Zep's exact models) goes to api.openai.com and
needs OAI_KEY + ALLOW_OPENAI=1 (paid API, Tier-2 until Anton says yes); any other name goes through the
local CLIProxy (our subscriptions). Every stage is resumable (jsonl keyed by qid); OUT_DIR holds the outputs;
QLIMIT=n = smoke (first n questions per conversation).
рельса: reader/judge по env (дефолт gpt-6-sol / grok-4.20 через CLIProxy; точная копия Zep = gpt-4o-mini).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import statistics
import sys
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOT = HERE.parent / "memory-over-time-bench-20261108"
sys.path.insert(0, str(MOT))
os.environ.setdefault("LOCOMO", str(MOT / "locomo10.json"))
import bench_mot as mot  # noqa: E402  (parse_date/human/session_text/embed/proxy_key/write/done_ids/PROXY/timezone)

OUT = Path(os.environ.get("OUT_DIR", HERE / "out"))
STORES = Path(os.environ.get("STORES", MOT / "full"))
UP = HERE / "upstream"  # getzep/zep-papers@4b7f26cc kg_architecture_agent_memory/locomo_eval/*.py + data/*.json
K = int(os.environ.get("TOPK", "20"))
READER_MODEL = os.environ.get("READER_MODEL", "gpt-6-sol")
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "grok-4.20-0309-non-reasoning")
CATS = {1: "multi-hop", 2: "temporal", 3: "open-domain", 4: "single-hop"}
N_EXPECTED = 1540
UPSTREAM_SHA12 = {"zep_locomo_search.py": "5d659ffa05e7", "zep_locomo_responses.py": "6873a7ed3a5f",
                  "zep_locomo_eval.py": "191246ca4a33"}


# ---------------- Zep prompts, byte-exact from the pinned upstream scripts ----------------
def _upstream(name: str) -> str:
    b = (UP / name).read_bytes()
    h = hashlib.sha256(b).hexdigest()[:12]
    assert h == UPSTREAM_SHA12[name], f"{name}: sha {h} != pinned {UPSTREAM_SHA12[name]}"
    return b.decode("utf-8")


def _literal(src: str, var: str) -> str:
    """The triple-quoted literal assigned to `var` (plain or f-string), exactly as written in the source."""
    m = re.search(r'^[ \t]*' + re.escape(var) + r'\s*=\s*f?"""(.*?)"""', src, re.S | re.M)
    assert m, var
    return m.group(1)


TEMPLATE = _literal(_upstream("zep_locomo_search.py"), "TEMPLATE")            # {facts} {entities}
_resp = _upstream("zep_locomo_responses.py")
READER_SYS = _literal(_resp, "system_prompt")
READER_PROMPT = _literal(_resp, "prompt")                                      # {context} {question}
_eval = _upstream("zep_locomo_eval.py")
JUDGE_SYS = _literal(_eval, "system_prompt")
JUDGE_PROMPT = _literal(_eval, "ACCURACY_PROMPT")                              # {question} {gold_answer} {response}
GRADE_SCHEMA = {"type": "object",
                "properties": {"is_correct": {"type": "string", "description": "CORRECT or WRONG"},
                               "reasoning": {"type": "string", "description": "Explain why the answer is correct or incorrect."}},
                "required": ["is_correct", "reasoning"], "additionalProperties": False}


# ---------------- data ----------------
def load_all():
    """All conversations with every category-1..4 question. qid = <sample_id>#<index in qa>, same as bench_mot."""
    d = json.loads(Path(os.environ["LOCOMO"]).read_text(encoding="utf-8-sig"))
    convs = []
    for c in d:
        conv = c["conversation"]
        sessions = []
        for n in range(1, 60):
            if f"session_{n}" not in conv:
                continue
            sessions.append({"n": n, "date": mot.parse_date(conv[f"session_{n}_date_time"]),
                             "turns": [{"id": t["dia_id"], "speaker": t["speaker"], "text": t["text"]
                                        + (f" (description of attached image: {t['blip_caption']})" if t.get("blip_caption") else "")}
                                       for t in conv[f"session_{n}"]]})
        qs = [{"qid": f"{c['sample_id']}#{i}", "question": q["question"], "gold": str(q["answer"]),
               "category": q["category"], "evidence": q.get("evidence", [])}
              for i, q in enumerate(c["qa"]) if q.get("category") in CATS]
        convs.append({"id": c["sample_id"], "sessions": sessions, "qs": qs})
    if os.environ.get("QLIMIT"):  # smoke: first N questions per conversation, no completeness assert
        for c in convs:
            c["qs"] = c["qs"][:int(os.environ["QLIMIT"])]
        return convs
    n = sum(len(c["qs"]) for c in convs)
    assert n == N_EXPECTED, f"expected {N_EXPECTED} questions in categories 1-4, got {n}"
    return convs


def qindex():
    return {q["qid"]: q for c in load_all() for q in c["qs"]}


# ---------------- LLM backends ----------------
def chat(model: str, messages: list, max_tokens: int, schema: dict | None = None) -> str:
    if model.startswith("gpt-4o"):
        if os.environ.get("ALLOW_OPENAI") != "1" or not os.environ.get("OAI_KEY"):
            raise SystemExit("gpt-4o* = paid OpenAI API: needs ALLOW_OPENAI=1 and OAI_KEY (Tier-2, ask Anton)")
        url, key = "https://api.openai.com/v1/chat/completions", os.environ["OAI_KEY"]
        body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens}
    else:
        url, key = mot.PROXY + "/chat/completions", mot.proxy_key()
        body = {"model": model, "messages": messages}
        if model.startswith("gpt-"):
            body["max_completion_tokens"] = max_tokens
        else:
            body["temperature"] = 0; body["max_tokens"] = max_tokens
    if schema:  # Zep: client.beta.chat.completions.parse(response_format=Grade) = strict JSON schema
        body["response_format"] = {"type": "json_schema", "json_schema": {"name": "Grade", "strict": True, "schema": schema}}
    data = json.dumps(body).encode()
    err = None
    for a in range(6):
        try:
            req = urllib.request.Request(url, data=data, headers={"Authorization": "Bearer " + key,
                                                                 "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                j = json.loads(r.read())
            txt = (j["choices"][0]["message"].get("content") or "").strip()
            if txt:
                return txt
            err = "empty"
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {str(e)[:200]}"
        time.sleep(5 * (a + 1))
    raise RuntimeError(f"{model}: {err}")


# ---------------- contexts ----------------
def ctx_ours():
    out = OUT / "ctx_ours.jsonl"; have = mot.done_ids(out)
    for c in load_all():
        if all(q["qid"] in have for q in c["qs"]):
            continue
        rows = [{"date": mot.human(s["date"]), "speaker": t["speaker"], "text": t["text"], "id": t["id"]}
                for s in c["sessions"] for t in s["turns"]]
        vec = mot.embed([f"[{r['date']}] {r['speaker']}: {r['text']}" for r in rows])
        for q in c["qs"]:
            if q["qid"] in have:
                continue
            t0 = time.perf_counter()
            qv = mot.embed([q["question"]], "query")[0]
            sc = sorted(((sum(a * b for a, b in zip(qv, v)), i) for i, v in enumerate(vec)), reverse=True)[:K]
            hits = [rows[i] for _, i in sc]
            ms = (time.perf_counter() - t0) * 1000
            ctx = "\n".join(f"- [{h['date']}] {h['speaker']}: {h['text']}" for h in hits)
            mot.write(out, {"qid": q["qid"], "ctx": ctx, "retr_ms": round(ms, 2),
                            "evidence_hit": bool(set(q["evidence"]) & {h["id"] for h in hits})})
        print("ours", c["id"], flush=True)


def ctx_full():
    out = OUT / "ctx_full.jsonl"; have = mot.done_ids(out)
    for c in load_all():
        text = "\n\n".join(mot.session_text(s) for s in c["sessions"])
        for q in c["qs"]:
            if q["qid"] not in have:
                mot.write(out, {"qid": q["qid"], "ctx": text, "retr_ms": 0})
        print("full", c["id"], len(text), flush=True)


def ctx_mem0(run: str):
    """Query the Mem0 stores built on 08.11 (no re-ingestion)."""
    sys.path.insert(0, os.environ.get("MEM0_DIR_CODE", str(MOT)))
    os.environ.update(MEM0_TELEMETRY="False", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false")
    from mem0.utils.factory import EmbedderFactory
    from mem0.embeddings.base import EmbeddingBase
    from mem0 import Memory

    class HttpE5(EmbeddingBase):
        def __init__(self, config=None):
            super().__init__(config); self.config.embedding_dims = 768

        def embed(self, text, memory_action=None):
            return mot.embed([text], "query" if memory_action == "search" else "passage")[0]

        def embed_batch(self, texts, memory_action="add"):
            return mot.embed(list(texts), "query" if memory_action == "search" else "passage") if texts else []
    sys.modules[__name__].HttpE5 = HttpE5
    EmbedderFactory.provider_to_class["huggingface"] = f"{__name__}.HttpE5"
    out = OUT / f"ctx_mem0_{run}.jsonl"; have = mot.done_ids(out)
    for c in load_all():
        if all(q["qid"] in have for q in c["qs"]):
            continue
        base = STORES / f"mem0_{run}" / c["id"]
        assert (base / "qdrant").exists(), f"missing store {base}"
        m = Memory.from_config({
            "embedder": {"provider": "huggingface", "config": {"model": "intfloat/multilingual-e5-base", "embedding_dims": 768}},
            "llm": {"provider": "openai", "config": {"model": "unused", "api_key": "x", "openai_base_url": mot.PROXY}},
            "vector_store": {"provider": "qdrant", "config": {"path": str(base / "qdrant"), "collection_name": "c",
                                                               "on_disk": True, "embedding_model_dims": 768}},
            "history_db_path": str(base / "history.sqlite")})
        for q in c["qs"]:
            if q["qid"] in have:
                continue
            t1 = time.perf_counter()
            res = m.search(q["question"], filters={"user_id": c["id"]}, top_k=K, threshold=0.0)["results"]
            ms = (time.perf_counter() - t1) * 1000
            ctx = "\n".join(f"- [{(h.get('metadata') or {}).get('session_date', '?')}] {h.get('memory', '')}" for h in res)
            mot.write(out, {"qid": q["qid"], "ctx": ctx, "retr_ms": round(ms, 1), "n": len(res)})
        print("mem0", run, c["id"], flush=True)


def ctx_graphiti(run: str):
    """Query the Kuzu graphs built on 08.11: 20 edges + 20 nodes, hybrid RRF, Zep's TEMPLATE."""
    import asyncio
    os.environ.setdefault("GRAPHITI_TELEMETRY_ENABLED", "false")
    from graphiti_core import Graphiti
    from graphiti_core.cross_encoder.client import CrossEncoderClient
    from graphiti_core.driver.kuzu_driver import KuzuDriver
    from graphiti_core.embedder.client import EmbedderClient
    from graphiti_core.llm_client.config import LLMConfig
    from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
    from graphiti_core.search.search_config_recipes import EDGE_HYBRID_SEARCH_RRF, NODE_HYBRID_SEARCH_RRF

    class E5(EmbedderClient):
        async def create(self, input_data):
            t = input_data if isinstance(input_data, str) else " ".join(map(str, input_data))
            return (await asyncio.to_thread(mot.embed, [t], "query"))[0]

        async def create_batch(self, input_data_list):
            return await asyncio.to_thread(mot.embed, list(input_data_list), "query")

    class NoRerank(CrossEncoderClient):
        async def rank(self, query, passages):
            return [(p, 1.0) for p in passages]

    out = OUT / f"ctx_graphiti_{run}.jsonl"; have = mot.done_ids(out)
    ecfg = EDGE_HYBRID_SEARCH_RRF.model_copy(deep=True); ecfg.limit = K
    ncfg = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True); ncfg.limit = K

    def human_dt(x):
        return mot.human(x if x.tzinfo else x.replace(tzinfo=mot.timezone.utc)) if x else "unknown"

    async def one(c):
        if all(q["qid"] in have for q in c["qs"]):
            return
        dbp = STORES / f"graphiti_{run}" / f"{c['id']}.kuzu"
        assert dbp.exists(), f"missing graph {dbp}"
        import kuzu
        from unittest.mock import patch
        _orig = kuzu.Database
        with patch.object(kuzu, "Database", side_effect=lambda *a, **kw: _orig(
                *a, **{**kw, "buffer_pool_size": int(os.environ.get("KUZU_POOL_MB", "512")) * 1024 * 1024})):
            # not read_only: KuzuDriver.setup_schema() issues CREATE ... IF NOT EXISTS on open; nothing else writes here
            driver = KuzuDriver(str(dbp))
        llm = OpenAIGenericClient(config=LLMConfig(api_key="unused", base_url=mot.PROXY, model="unused"))  # search never calls it
        g = Graphiti(graph_driver=driver, llm_client=llm, embedder=E5(), cross_encoder=NoRerank())
        for q in c["qs"]:
            if q["qid"] in have:
                continue
            t1 = time.perf_counter()
            er, nr = await asyncio.gather(g.search_(q["question"], config=ecfg), g.search_(q["question"], config=ncfg))
            ms = (time.perf_counter() - t1) * 1000
            facts = [f"  - {e.fact} (event_time: {human_dt(e.valid_at)})" for e in er.edges]
            ents = [f"  - {n.name}: {n.summary}" for n in nr.nodes]
            mot.write(out, {"qid": q["qid"], "ctx": TEMPLATE.format(facts="\n".join(facts), entities="\n".join(ents)),
                            "retr_ms": round(ms, 1), "n_edges": len(er.edges), "n_nodes": len(nr.nodes)})
        print("graphiti", run, c["id"], flush=True)
        await g.close()

    async def main():
        for c in load_all():  # sequential: one Kuzu buffer pool at a time
            await one(c)
    asyncio.run(main())


# ---------------- Zep's published artefacts (same pin) ----------------
def _zep_groups():
    """Map Zep's per-user lists (filtered category != 5, file order) onto our qids (sample_id#index)."""
    d = json.loads((UP / "locomo.json").read_text(encoding="utf-8-sig"))
    return [[f"{c['sample_id']}#{i}" for i, q in enumerate(c["qa"]) if q.get("category") != 5] for c in d]


def ctx_zep():
    """Arm `zep`: Zep Cloud's own published search contexts (20 facts + 20 entities), our reader/judge on top."""
    sr = json.loads((UP / "zep_locomo_search_results.json").read_text(encoding="utf-8-sig"))
    out = OUT / "ctx_zep.jsonl"; have = mot.done_ids(out); qi = qindex(); n = 0
    for gi, qids in enumerate(_zep_groups()):
        items = sr[f"locomo_experiment_user_{gi}"]
        assert len(items) == len(qids), (gi, len(items), len(qids))
        for qid, it in zip(qids, items):
            if qid in qi and qid not in have:
                mot.write(out, {"qid": qid, "ctx": it["context"], "retr_ms": round(it.get("duration_ms", 0), 1)}); n += 1
    print("zep ctx written", n, flush=True)


def import_zep_answers():
    """ans_zepans_r1.jsonl = Zep's published gpt-4o-mini answers; judging them with our judge calibrates the judge
    against Zep's published grades (jud_zepans_upstream_r1.jsonl, 1157/1540 CORRECT upstream)."""
    rs = json.loads((UP / "zep_locomo_responses.json").read_text(encoding="utf-8-sig"))
    gr = json.loads((UP / "zep_locomo_grades.json").read_text(encoding="utf-8-sig"))
    out = OUT / "ans_zepans_r1.jsonl"; ref = OUT / "jud_zepans_upstream_r1.jsonl"
    have = mot.done_ids(out); qi = qindex(); n = 0
    for gi, qids in enumerate(_zep_groups()):
        items = rs[f"locomo_experiment_user_{gi}"]; grades = gr[f"locomo_experiment_user_{gi}"]
        assert len(items) == len(qids) == len(grades), (gi, len(items), len(qids), len(grades))
        for qid, it, g in zip(qids, items, grades):
            if qid not in qi:
                continue
            assert it["question"] == qi[qid]["question"] == g["question"], qid
            if qid not in have:
                mot.write(out, {"qid": qid, "answer": it["answer"], "model": "gpt-4o-mini@zep-published", "ms": round(it.get("duration_ms", 0))})
                mot.write(ref, {"qid": qid, "label": "CORRECT" if g["grade"] else "WRONG", "model": "gpt-4o-mini@zep-published"}); n += 1
    print("zep answers imported", n, flush=True)


# ---------------- reader & judge ----------------
def answer(system: str, run: str):
    ctxf = OUT / (f"ctx_{system}.jsonl" if system in ("ours", "full", "zep") else f"ctx_{system}_{run}.jsonl")
    ctx = {json.loads(l)["qid"]: json.loads(l)["ctx"] for l in ctxf.read_text(encoding="utf-8-sig").splitlines()}
    tag = os.environ.get("TAG", "")
    out = OUT / f"ans{tag}_{system}_{run}.jsonl"
    have = mot.done_ids(out); qi = qindex()

    def one(qid):
        q = qi[qid]
        t0 = time.perf_counter()
        a = chat(READER_MODEL, [{"role": "system", "content": READER_SYS},
                                {"role": "user", "content": READER_PROMPT.format(context=ctx[qid], question=q["question"])}],
                 max_tokens=int(os.environ.get("READER_MAX", "1500")))
        mot.write(out, {"qid": qid, "answer": a, "model": READER_MODEL, "ms": round((time.perf_counter() - t0) * 1000)})
    todo = [k for k in ctx if k not in have and k in qi]
    with cf.ThreadPoolExecutor(int(os.environ.get("PAR", "6"))) as ex:
        for f in cf.as_completed([ex.submit(one, k) for k in todo]):
            f.result()
    print("answer", system, run, len(todo), flush=True)


def judge(system: str, run: str):
    tag = os.environ.get("TAG", "")
    ans = {json.loads(l)["qid"]: json.loads(l)["answer"]
           for l in (OUT / f"ans{tag}_{system}_{run}.jsonl").read_text(encoding="utf-8-sig").splitlines()}
    out = OUT / f"jud{tag}{os.environ.get('JUDGE_TAG', '')}_{system}_{run}.jsonl"
    have = mot.done_ids(out); qi = qindex()

    def one(qid):
        q = qi[qid]
        v = chat(JUDGE_MODEL, [{"role": "system", "content": JUDGE_SYS},
                               {"role": "user", "content": JUDGE_PROMPT.format(question=q["question"], gold_answer=q["gold"], response=ans[qid])}],
                 max_tokens=300, schema=GRADE_SCHEMA)
        try:
            g = json.loads(v)
            is_correct = str(g.get("is_correct", "")); reasoning = str(g.get("reasoning", ""))[:300]; parsed = True
        except Exception:  # noqa: BLE001
            is_correct, reasoning, parsed = "", v[:300], False  # unparsable = WRONG (upstream: anything but 'correct')
        mot.write(out, {"qid": qid, "label": "CORRECT" if is_correct.strip().lower() == "correct" else "WRONG",
                        "is_correct": is_correct, "reasoning": reasoning, "parsed": parsed, "model": JUDGE_MODEL})
    todo = [k for k in ans if k not in have and k in qi]
    with cf.ThreadPoolExecutor(int(os.environ.get("PAR", "6"))) as ex:
        for f in cf.as_completed([ex.submit(one, k) for k in todo]):
            f.result()
    print("judge", system, run, len(todo), flush=True)


def aggregate():
    qi = qindex(); tag = os.environ.get("TAG", ""); jt = os.environ.get("JUDGE_TAG", "")
    smoke = bool(os.environ.get("QLIMIT"))
    res = {}; models = {}
    for f in sorted(OUT.glob(f"jud{tag}{jt}_*_r*.jsonl")):
        system, run = f.stem[len(f"jud{tag}{jt}_"):].rsplit("_", 1)
        rows = {}
        for l in f.read_text(encoding="utf-8-sig").splitlines():
            r = json.loads(l); rows[r["qid"]] = r  # one grade per qid; duplicates never inflate the count
        rows = [r for r in rows.values() if r["qid"] in qi]
        n = len(rows)
        if n != N_EXPECTED and not smoke:
            print(f"⚠️ {f.name}: {n}/{N_EXPECTED} unique graded qids, skipped", flush=True); continue
        jm = {r.get("model") for r in rows}
        af = OUT / f"ans{tag}_{system.replace('_upstream', '')}_{run}.jsonl"
        if not af.exists():
            print(f"⚠️ {f.name}: no answer file {af.name}, skipped", flush=True); continue
        arows = {json.loads(l)["qid"]: json.loads(l) for l in af.read_text(encoding="utf-8-sig").splitlines()}
        rm = {r.get("model") for r in arows.values()}
        if {r["qid"] for r in rows} != set(arows) & set(qi):
            print(f"⚠️ {f.name}: graded qids != answered qids, skipped", flush=True); continue
        if len(jm) != 1 or len(rm) != 1 or None in jm or None in rm:
            print(f"⚠️ {f.name}: mixed or empty models judge={jm} reader={rm}, skipped", flush=True); continue
        pair = {"reader": rm.pop(), "judge": jm.pop()}
        per = defaultdict(lambda: [0, 0])
        for r in rows:
            cat = qi[r["qid"]]["category"]; per[cat][1] += 1; per[cat][0] += r["label"] == "CORRECT"
        tot = sum(v[0] for v in per.values())
        # runs are grouped by (system, reader, judge): runs of one system under different model pairs never average
        key = f"{system}@{pair['reader']}/{pair['judge']}"
        models[key] = pair
        res.setdefault(key, []).append({"run": run, "n": n, "correct": tot, "overall": 100 * tot / n, **pair,
                                        **{CATS[c]: (100 * per[c][0] / per[c][1] if per[c][1] else None) for c in CATS}})
    summary = {}
    for s_, runs in res.items():
        summary[s_] = {"system": s_.split("@", 1)[0]}
        for k in ["overall"] + list(CATS.values()):
            vals = [r[k] for r in runs if r[k] is not None]
            summary[s_][k] = {"mean": round(statistics.mean(vals), 2) if vals else None,
                              "sd": round(statistics.pstdev(vals), 2) if len(vals) > 1 else None, "runs": len(vals)}
        summary[s_]["models"] = models[s_]
    out = {"ruler": "getzep/zep-papers@4b7f26cc locomo_eval", "n_expected": N_EXPECTED, "smoke": smoke, "K": K, "tag": tag + jt,
           "reference_zep_blog": {"zep_cloud": 75.14, "gpt-4o-mini_full_context": 72.90,
                                  "mem0_graph_from_mem0_paper": 68.44, "mem0_from_mem0_paper": 66.88},
           "runs": res, "summary": summary}
    (OUT / f"results{tag}{jt}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["ctx-ours", "ctx-full", "ctx-mem0", "ctx-graphiti", "ctx-zep", "import-zep-answers",
                                      "answer", "judge", "aggregate"])
    ap.add_argument("--run", default="r1")
    ap.add_argument("--system", default="ours")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    {"ctx-ours": ctx_ours, "ctx-full": ctx_full, "ctx-mem0": lambda: ctx_mem0(a.run),
     "ctx-graphiti": lambda: ctx_graphiti(a.run), "ctx-zep": ctx_zep, "import-zep-answers": import_zep_answers,
     "answer": lambda: answer(a.system, a.run), "judge": lambda: judge(a.system, a.run), "aggregate": aggregate}[a.stage]()


if __name__ == "__main__":
    main()
