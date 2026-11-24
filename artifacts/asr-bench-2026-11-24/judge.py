r"""judge.py -- «судья на слух»: аудио-модель слушает голосовую и оценивает слепые расшифровки.

Вход: runs.jsonl (bench.py) + папка аудио. Выход: judge_<судья>.jsonl, по строке на файл:
reference (эталон, собранный судьёй по звуку), scores[engine] = {omitted, wrong, hallucinated, score}.
Слепота: кандидаты под буквами A..G, порядок перемешан детерминированно от id файла;
названия моделей судья не видит. Судьи: or:<model> (OpenRouter), oa:<model> (OpenAI chat audio).
Author: Mycroft (Claude Code) and Tony Dzi, Palo Alto AI Research Lab, 2026-11-24.
"""
import base64, hashlib, json, os, random, re, sys, time, requests
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
def okey():
    return os.environ["OPENAI_API_KEY"]

ENGINES = ["whisper-1", "gpt-4o-mini-transcribe", "gpt-4o-transcribe", "gpt-transcribe",
           "gpt-transcribe+hints", "gpt-4o-transcribe@60s", "gpt-transcribe@60s"]
PROMPT = """You are an expert Russian/English transcription auditor. Listen to the attached voice message carefully (Russian speech with English tech terms, speaker Anton).
Below are {n} candidate transcripts labeled {labels}. They were produced by different speech-to-text systems; their order is random.

Tasks:
1. Write REFERENCE: your own best verbatim transcript of the audio, using the candidates only as help; trust your ears over them. Keep the original language; drop filler sounds (э-э, ммм).
2. For EACH label, count against the audio: omitted = number of words of real speech missing; wrong = words misheard/substituted (names and terms matter); hallucinated = words present that were never said (including repetition loops). Then score 0-10 for fidelity (10 = perfect, 0 = useless).

Return ONLY JSON: {{"reference": "...", "scores": {{"A": {{"omitted": int, "wrong": int, "hallucinated": int, "score": number, "note": "short"}}, ...}}}}

{cands}"""


def labelled(fid, texts):
    order = list(texts); random.Random(int(hashlib.md5(str(fid).encode()).hexdigest(), 16)).shuffle(order)
    labels = [chr(65 + i) for i in range(len(order))]
    return dict(zip(labels, order))


def call(judge, audio_b64, prompt, keys):
    content = [{"type": "text", "text": prompt}, {"type": "input_audio", "input_audio": {"data": audio_b64, "format": "ogg"}}]
    if judge.startswith("or:"):
        url, key, model = "https://openrouter.ai/api/v1/chat/completions", keys["or"], judge[3:]
        body = {"model": model, "messages": [{"role": "user", "content": content}], "usage": {"include": True},
                "response_format": {"type": "json_object"}, "reasoning": {"effort": "low"}}
    else:
        url, key, model = "https://api.openai.com/v1/chat/completions", keys["oa"], judge[3:]
        content[1]["input_audio"]["format"] = "mp3"
        body = {"model": model, "modalities": ["text"], "messages": [{"role": "user", "content": content}]}
    r = requests.post(url, headers={"Authorization": "Bearer " + key}, json=body, timeout=600)
    if r.status_code != 200:
        raise RuntimeError("HTTP %s %s" % (r.status_code, r.text[:300]))
    j = r.json(); txt = j["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", txt, re.S)
    return json.loads(m.group(0)), j.get("usage")


def main(judge, audio_dir, ff=None):
    runs = {}
    for l in open(os.path.join(D, "runs.jsonl")):
        x = json.loads(l)
        if not x.get("err") and x["engine"] in ENGINES:
            runs.setdefault(x["id"], {})[x["engine"]] = x["text"]
    out = os.path.join(D, "judge_%s.jsonl" % re.sub(r"[^\w.-]", "_", judge))
    done = {json.loads(l)["id"] for l in open(out)} if os.path.exists(out) else set()
    keys = {"oa": okey() if judge.startswith("oa:") else None,
            "or": next(l.split("=", 1)[1].strip().strip('"\'') for l in ["OPENROUTER_API_KEY=" + os.environ.get("OPENROUTER_API_KEY", "")]
                       if l.startswith("OPENROUTER_API_KEY"))}
    for fid, texts in sorted(runs.items()):
        only = os.environ.get("ONLY_IDS")
        if only and str(fid) not in only.split(","):
            continue
        if fid in done or len(texts) < len(ENGINES):
            continue
        lab = labelled(fid, ENGINES)
        cands = "\n\n".join("=== %s ===\n%s" % (L, texts[e]) for L, e in lab.items())
        p = os.path.join(audio_dir, "%s.ogg" % fid)
        if judge.startswith("oa:"):   # OpenAI chat audio accepts wav/mp3 only
            import subprocess, tempfile
            mp3 = os.path.join(tempfile.mkdtemp(), "a.mp3")
            subprocess.run([ff, "-loglevel", "error", "-y", "-i", p, "-b:a", "48k", mp3], check=True); p = mp3
        b = base64.b64encode(open(p, "rb").read()).decode()
        t = time.time()
        for attempt in range(3):
            try:
                res, use = call(judge, b, PROMPT.format(n=len(lab), labels=", ".join(lab), cands=cands), keys); break
            except Exception as ex:
                err = repr(ex)[:300]; time.sleep(10 * (attempt + 1))
        else:
            print(fid, "FAIL", err); continue
        scores = {lab[L]: v for L, v in res.get("scores", {}).items() if L in lab}
        row = {"id": fid, "judge": judge, "sec": round(time.time() - t, 1), "labels": lab,
               "reference": res.get("reference", ""), "scores": scores, "usage": use}
        with open(out, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(fid, judge, "ok", {e: s.get("score") for e, s in scores.items()})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
