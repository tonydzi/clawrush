r"""analyze.py -- сводка стенда: runs.jsonl + judge_*.jsonl -> results.json + results.md. 0 LLM.

Метрики на движок: средний балл судей (0-10), CER против эталона каждого судьи (символы, нормализованные:
нижний регистр, только буквы/цифры/пробел), доля пропущенных слов, «провалы» (балл <=3 хоть у одного судьи),
цена по фактическому usage и прайсу OpenAI на 24.11.2026, медианная задержка.
Author: Mycroft (Claude Code) and Tony Dzi, Palo Alto AI Research Lab, 2026-11-24.
"""
import glob, json, os, re, statistics as st
D = os.path.dirname(os.path.abspath(__file__))
PRICE_MIN = {"whisper-1": 0.006, "gpt-transcribe": 0.0045}          # $/мин (прайс 24.11.2026)
PRICE_TOK = {"gpt-4o-transcribe": (2.5, 10.0), "gpt-4o-mini-transcribe": (1.25, 5.0)}  # $/1M in,out


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^\w ]", " ", (t or "").lower().replace("ё", "е"))).strip()


def lev(a, b):
    if len(a) < len(b): a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** 0.5
    return round(num / den, 3) if den else None


def cost(engine, row):
    base = engine.split("@")[0].split("+")[0]
    u = row.get("usage") or {}
    if base in PRICE_MIN:
        sec = u.get("seconds") or row["dur"]
        return PRICE_MIN[base] * sec / 60
    if base in PRICE_TOK:
        if "input_tokens" in u:
            i, o = PRICE_TOK[base]; return (u["input_tokens"] * i + u["output_tokens"] * o) / 1e6
        return 0.006 * row["dur"] / 60 if base == "gpt-4o-transcribe" else 0.003 * row["dur"] / 60
    return None


def main():
    runs = {}
    for l in open(os.path.join(D, "runs.jsonl")):
        x = json.loads(l)
        if not x.get("err"): runs.setdefault(x["engine"], {})[x["id"]] = x
    judges = {}
    for f in glob.glob(os.path.join(D, "judge_*.jsonl")):
        for l in open(f):
            x = json.loads(l); judges.setdefault(x["judge"], {})[x["id"]] = x
    common = set.intersection(*[set(j) for j in judges.values()]) if judges else set()
    total_min = sum(runs["whisper-1"][i]["dur"] for i in common) / 60
    out = {"files": len(common), "audio_minutes": round(total_min, 2), "judges": sorted(judges), "engines": {}}
    for e, rows in runs.items():
        if not all(i in rows for i in common): continue
        sc, cer, omit, fails, lat, usd = [], {}, [], 0, [], 0.0
        for i in common:
            r = rows[i]; lat.append(r["sec"]); usd += cost(e, r) or 0
            per = []
            for jn, J in judges.items():
                s = J[i]["scores"].get(e)
                if not s: continue
                per.append(float(s["score"]))
                ref = norm(J[i]["reference"]); hyp = norm(r["text"])
                cer.setdefault(jn, []).append(lev(hyp, ref) / max(1, len(ref)))
                omit.append(int(s.get("omitted", 0)) / max(1, len(ref.split())))
            sc.extend(per)
            if per and min(per) <= 3: fails += 1
        out["engines"][e] = {
            "score_mean": round(st.mean(sc), 2), "score_median": round(st.median(sc), 2),
            "cer_by_judge": {jn: round(st.mean(v) * 100, 1) for jn, v in cer.items()},
            "omitted_share_pct": round(st.mean(omit) * 100, 1), "catastrophic_files": fails,
            "latency_median_s": round(st.median(lat), 2), "usd_total": round(usd, 4),
            "usd_per_min": round(usd / total_min, 5)}
    # согласие судей: корреляция рангов движков по файлу
    if len(judges) == 2:
        a, b = list(judges.values()); agree = []
        for i in common:
            ka = a[i]["scores"]; kb = b[i]["scores"]; es = [e for e in ka if e in kb]
            pa = sorted(es, key=lambda e: -float(ka[e]["score"]))[0]; pb = sorted(es, key=lambda e: -float(kb[e]["score"]))[0]
            agree.append(pa == pb)
        out["judges_same_winner_pct"] = round(100 * sum(agree) / len(agree), 1)
        flat = [(float(a[i]["scores"][e]["score"]), float(b[i]["scores"][e]["score"])) for i in common for e in a[i]["scores"] if e in b[i]["scores"]]
        out["judges_score_pearson"] = pearson([x for x, _ in flat], [y for _, y in flat])
    json.dump(out, open(os.path.join(D, "results.json"), "w"), indent=1, ensure_ascii=False)
    lines = ["| engine | score (0-10) | CER % per judge | omitted % | catastrophic files | median latency s | $/min |", "|---|---|---|---|---|---|---|"]
    for e, v in sorted(out["engines"].items(), key=lambda kv: -kv[1]["score_mean"]):
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (e, v["score_mean"], " / ".join(str(x) for x in v["cer_by_judge"].values()),
                     v["omitted_share_pct"], v["catastrophic_files"], v["latency_median_s"], v["usd_per_min"]))
    md = "files=%s, audio=%s min, judges=%s\n\n" % (out["files"], out["audio_minutes"], ", ".join(out["judges"])) + "\n".join(lines)
    open(os.path.join(D, "results.md"), "w").write(md + "\n"); print(md); print({k: v for k, v in out.items() if k.startswith("judges_")})


if __name__ == "__main__":
    main()
