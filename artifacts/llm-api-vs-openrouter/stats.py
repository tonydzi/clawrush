"""Сводка живого замера llmapi vs OpenRouter из сырых jsonl (0 LLM). Выход: stats.json рядом.
"""
import json, statistics as st, collections, pathlib, re
H = pathlib.Path(__file__).resolve().parent
A = [json.loads(l) for l in open(H / "raw/live_20261124T141600Z.jsonl", encoding="utf-8")]
B = [json.loads(l) for l in open(H / "raw/live_20261124T142153Z.jsonl", encoding="utf-8")]
def q(v, p):
    v = sorted(v); return v[min(len(v) - 1, int(round(p * (len(v) - 1))))] if v else None
def summ(rows):
    out = {}
    g = collections.defaultdict(list)
    for r in rows: g[(r["platform"], r["model_key"])].append(r)
    for (p, m), rs in sorted(g.items()):
        ok = [r for r in rs if not r["error_class"]]
        tt = [r["ttft_s"] for r in ok if r.get("ttft_s") is not None]
        to = [r["total_s"] for r in ok if r.get("total_s") is not None]
        def _c(u):
            u = u or {}
            if u.get("cost") is not None: return u["cost"]  # OpenRouter
            return (u.get("cost_usd_input") or 0) + (u.get("cost_usd_output") or 0)  # llmapi
        cost = sum(_c(r.get("usage")) for r in ok)
        out[f"{p}|{m}"] = {"n": len(rs), "errors": len(rs) - len(ok),
            "error_classes": dict(collections.Counter(r["error_class"] for r in rs if r["error_class"])),
            "http": dict(collections.Counter(r["http_status"] for r in rs)),
            "correct": sum(1 for r in ok if r.get("correct")),
            "ttft_med": round(st.median(tt), 3) if tt else None, "ttft_p90": round(q(tt, .9), 3) if tt else None,
            "total_med": round(st.median(to), 3) if to else None, "total_p90": round(q(to, .9), 3) if to else None,
            "cost_usd": round(cost, 5), "cost_reported": sum(1 for r in ok if (r.get("usage") or {}).get("cost") is not None or "cost_usd_input" in (r.get("usage") or {})),
            "providers": dict(collections.Counter(str(r.get("provider")) for r in rs)),
            "returned_models": dict(collections.Counter(str(r.get("returned_model")) for r in rs))}
    return out
def paired(rows, model):
    d = collections.defaultdict(dict)
    for r in rows:
        if r["model_key"] == model and not r["error_class"]:
            d[(r["prompt_id"], r["repeat"])][r["platform"]] = r
    pairs = [v for v in d.values() if len(v) == 2]
    llm_faster = sum(1 for v in pairs if v["llmapi"]["ttft_s"] < v["openrouter"]["ttft_s"])
    return {"pairs": len(pairs), "llmapi_ttft_faster": llm_faster,
            "same_correctness": sum(1 for v in pairs if v["llmapi"]["correct"] == v["openrouter"]["correct"])}
fails = collections.defaultdict(list)
for r in A:
    if r["model_key"] == "claude-sonnet-5" and not r["error_class"] and not r["correct"]:
        fails[r["prompt_id"]].append((r["platform"], r["repeat"], (r["text"] or "")[:80], r.get("finish_reason"), (r.get("usage") or {}).get("completion_tokens")))
err_terra = [ (r["http_status"], r["error_class"], str(r.get("text"))[:160]) for r in A if r["platform"]=="llmapi" and r["model_key"]=="gpt-6.1-terra"][:2]
res = {"run_A": {"id": "20261124T141600Z", "summary": summ(A), "paired_sonnet": paired(A, "claude-sonnet-5")},
       "run_B_no_temp": {"id": "20261124T142153Z", "summary": summ(B), "paired_terra": paired(B, "gpt-6.1-terra")},
       "sonnet_fails": fails, "llmapi_terra_errors_sample": err_terra}
json.dump(res, open(H / "stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(res, ensure_ascii=False, indent=1, default=str)[:6000])
