"""Живой парный бенчмарк: LLM API (llmapi.ai) против OpenRouter, одни и те же задания.

Вход: ключи OPENROUTER_API_KEY (~/.claude/secrets/openrouter.env) и LLM_API_KEY (~/.claude/secrets/llmapi.env).
Выход: raw/live_<ts>.jsonl (строка на запрос) + сводка в stdout.
Метод (по projects/lnap-eval/codex-method-review.md): 12 заданий с проверяемым ответом × модели × повторы,
порядок платформ в паре перемешан с seed, stream=True, TTFT = первый непустой content delta,
ошибки остаются в знаменателе. Без ключа платформы её строки пишутся как error=no_key.
Что ломается: сменился формат SSE или имя модели -> error_class в jsonl, не тишина.
"""
import argparse, datetime, hashlib, json, os, random, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.realpath(__file__))
SECRETS = os.path.expanduser("~/.claude/secrets")

PLATFORMS = {
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "openrouter.env", "OPENROUTER_API_KEY"),
    "llmapi": ("https://api.llmapi.ai/v1/chat/completions", "llmapi.env", "LLM_API_KEY"),
}
# явная таблица соответствия имён (одинаковые цены в каталоге 19.11)
MODELS = {
    "claude-sonnet-5": {"openrouter": "anthropic/claude-sonnet-5", "llmapi": "claude-sonnet-5"},
    "gpt-6.1-terra": {"openrouter": "openai/gpt-6.1-terra", "llmapi": "gpt-6.1-terra"},
}
# задания с однозначным проверяемым ответом
TASKS = [
    ("arith1", "What is 487 * 236? Reply with the number only.", "114932"),
    ("arith2", "What is 2**20 - 1? Reply with the number only.", "1048575"),
    ("date1", "What weekday was 2000-01-01? Reply with one English word.", "saturday"),
    ("cap1", "Capital of Australia? One word.", "canberra"),
    ("rev1", "Reverse the string 'gateway' exactly. Reply with the result only.", "yawetag"),
    ("count1", "How many letters 'r' are in 'strawberry'? Reply with a digit only.", "3"),
    ("json1", 'Return only JSON {"a":1,"b":[2,3]} with b reversed. No prose.', '{"a":1,"b":[3,2]}'),
    ("prime1", "Is 221 a prime number? Reply yes or no.", "no"),
    ("unit1", "How many seconds are in 3 hours? Number only.", "10800"),
    ("code1", "In Python, what does len(set('mississippi')) return? Number only.", "4"),
    ("sort1", "Sort ascending: 9, 2, 7, 4. Reply as comma-separated numbers, no spaces.", "2,4,7,9"),
    ("logic1", "If all bloops are razzies and all razzies are lazzies, are all bloops lazzies? yes or no.", "yes"),
]


def key_for(env_file, var):
    p = os.path.join(SECRETS, env_file)
    if os.environ.get(var):
        return os.environ[var]
    if os.path.exists(p):
        for line in open(p):
            if line.startswith(var + "="):
                return line.split("=", 1)[1].strip().strip('"')
    return None


def check(out, want):
    o = re.sub(r"\s+", "", (out or "").lower()).strip(".`")
    w = re.sub(r"\s+", "", want.lower())
    return o == w or o.endswith(w) and len(o) <= len(w) + 12


def call(platform, model, prompt, key, max_tokens):
    url = PLATFORMS[platform][0]
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": max_tokens, "stream": True, **({} if os.environ.get("BENCH_NO_TEMP") else {"temperature": 0}),
                       "stream_options": {"include_usage": True}}).encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {key}",
                                 "Content-Type": "application/json"})
    r = {"http_status": None, "error_class": None, "ttft_s": None, "total_s": None, "text": "",
         "usage": None, "returned_model": None, "provider": None, "request_id": None, "finish_reason": None}
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            r["http_status"] = resp.status
            r["request_id"] = resp.headers.get("x-request-id") or resp.headers.get("x-generation-id")
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    ev = json.loads(data)
                except ValueError:
                    continue
                r["returned_model"] = ev.get("model") or r["returned_model"]
                r["provider"] = ev.get("provider") or r["provider"]
                r["request_id"] = r["request_id"] or ev.get("id")
                if ev.get("usage"):
                    r["usage"] = ev["usage"]
                for ch in ev.get("choices") or []:
                    c = (ch.get("delta") or {}).get("content")
                    if c:
                        if r["ttft_s"] is None:
                            r["ttft_s"] = round(time.monotonic() - t0, 4)
                        r["text"] += c
                    r["finish_reason"] = ch.get("finish_reason") or r["finish_reason"]
    except urllib.error.HTTPError as e:
        r["http_status"], r["error_class"] = e.code, f"http_{e.code}"
        r["text"] = e.read()[:300].decode("utf-8", "replace")
    except Exception as e:  # сеть, таймаут
        r["error_class"] = type(e).__name__
    r["total_s"] = round(time.monotonic() - t0, 4)
    if r["error_class"] is None and not r["text"]:
        r["error_class"] = "empty"
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--tasks", type=int, default=len(TASKS))
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--platforms", default="openrouter,llmapi")
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--max-tokens", type=int, default=1024)  # 64 давал пустой ответ sonnet (finish=length, замер 19.11)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    plats = a.platforms.split(",")
    keys = {p: key_for(PLATFORMS[p][1], PLATFORMS[p][2]) for p in plats}
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = os.path.join(HERE, "raw", f"live_{ts}.jsonl")
    n = 0
    with open(out, "w") as fh:
        for rep in range(a.repeats):
            for tid, prompt, want in TASKS[: a.tasks]:
                for mk in a.models.split(","):
                    order = plats[:]
                    rnd.shuffle(order)
                    for pos, p in enumerate(order):
                        base = {"run_id": ts, "ts_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                "prompt_id": tid, "prompt_sha": hashlib.sha256(prompt.encode()).hexdigest()[:12],
                                "repeat": rep, "pair_pos": pos, "platform": p, "model_key": mk,
                                "requested_model": MODELS[mk][p], "seed": a.seed}
                        if not keys[p]:
                            rec = {**base, "error_class": "no_key"}
                        else:
                            r = call(p, MODELS[mk][p], prompt, keys[p], a.max_tokens)
                            rec = {**base, **r, "correct": check(r["text"], want) if not r["error_class"] else None}
                            rec["text"] = rec["text"][:200]
                        fh.write(json.dumps(rec, ensure_ascii=False) + "\n"); fh.flush()
                        n += 1
    print(f"строк: {n} -> {out}")
    summarize(out)


def summarize(path):
    rows = [json.loads(l) for l in open(path)]
    import statistics as st
    for p in sorted({r["platform"] for r in rows}):
        for mk in sorted({r["model_key"] for r in rows}):
            g = [r for r in rows if r["platform"] == p and r["model_key"] == mk]
            ok = [r for r in g if not r.get("error_class")]
            tt = [r["ttft_s"] for r in ok if r.get("ttft_s")]
            tot = [r["total_s"] for r in ok]
            cor = sum(1 for r in ok if r.get("correct"))
            print(f"{p:10} {mk:16} n={len(g)} ошибок={len(g)-len(ok)} верно={cor}/{len(g)} "
                  f"TTFT med={st.median(tt) if tt else '-'} total med={st.median(tot) if tot else '-'}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--summarize":
        summarize(sys.argv[2])
    else:
        main()
