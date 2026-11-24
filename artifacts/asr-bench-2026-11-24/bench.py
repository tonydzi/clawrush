r"""bench.py -- ASR-стенд: одни и те же голосовые Антона через несколько моделей.

Вход: папка с <id>.ogg и meta.json (id, dur). Выход: runs.jsonl (одна строка = файл x модель:
text, sec, usage, err). Идемпотентно: готовые пары пропускает. 0 LLM-судей тут, только расшифровка.
Кто зовёт: человек/сессия руками. Ключи: env OPENAI_API_KEY, OPENROUTER_API_KEY.
Author: Mycroft (Claude Code) and Tony Dzi, Palo Alto AI Research Lab, 2026-11-24.
"""
import base64, json, os, sys, time, requests
from concurrent.futures import ThreadPoolExecutor
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
def okey():
    return os.environ["OPENAI_API_KEY"]

KEYWORDS = ["Claude", "Codex", "n8n", "OpenAI", "OpenRouter", "Майкрофт", "Майк", "Сиренка", "Syncthing",
            "NotebookLM", "Obsidian", "Telegram", "GitHub", "Gemini", "Grok", "GLM", "Hermes", "Mac Studio", "хаб"]
OPENAI = {
    "whisper-1": {"model": "whisper-1"},
    "gpt-4o-mini-transcribe": {"model": "gpt-4o-mini-transcribe"},
    "gpt-4o-transcribe": {"model": "gpt-4o-transcribe"},
    "gpt-transcribe": {"model": "gpt-transcribe"},
    "gpt-transcribe+hints": {"model": "gpt-transcribe", "hints": True},
    "gpt-4o-transcribe@60s": {"model": "gpt-4o-transcribe", "chunk": 60},
    "gpt-transcribe@60s": {"model": "gpt-transcribe", "chunk": 60},
    "gpt-transcribe@120s": {"model": "gpt-transcribe", "chunk": 120},
    "gpt-transcribe@30s": {"model": "gpt-transcribe", "chunk": 30},
}
FF = os.environ.get("FFMPEG", "ffmpeg")
OR_MODELS = {"or:gemini-3.8-flash": "google/gemini-3.8-flash"}
OR_PROMPT = ("Transcribe this voice message verbatim in its original language (mostly Russian with English "
             "tech terms). Output only the transcript text, no comments.")


def chunked(path, cfg, key):
    """Режем на куски по cfg['chunk'] с (ffmpeg -c copy), хвост прошлого куска = prompt следующего."""
    import glob, subprocess, tempfile
    tmp = tempfile.mkdtemp()
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", path, "-f", "segment", "-segment_time", str(cfg["chunk"]),
                    "-c", "copy", os.path.join(tmp, "c_%03d.ogg")], check=True)
    parts, prev, sec = [], "", 0
    for p in sorted(glob.glob(os.path.join(tmp, "c_*.ogg"))):
        txt, use, err = openai_run(p, {"model": cfg["model"]}, key, prompt=prev[-300:])
        if err:
            return None, None, err
        parts.append(txt); prev = txt
        sec += (use or {}).get("seconds", 0)
    return " ".join(parts), {"chunks": len(parts), "seconds": sec}, None


def openai_run(path, cfg, key, prompt=""):
    if cfg.get("chunk"):
        return chunked(path, cfg, key)
    data = [("model", cfg["model"]), ("response_format", "json")]
    if prompt:
        data.append(("prompt", prompt))
    if cfg.get("hints"):
        data += [("languages[]", "ru"), ("languages[]", "en")] + [("keywords[]", k) for k in KEYWORDS]
    with open(path, "rb") as f:
        r = requests.post("https://api.openai.com/v1/audio/transcriptions", headers={"Authorization": "Bearer " + key},
                          files={"file": (os.path.basename(path), f, "audio/ogg")}, data=data, timeout=300)
    if r.status_code != 200:
        return None, None, "HTTP %s %s" % (r.status_code, r.text[:300])
    j = r.json(); return j.get("text", ""), j.get("usage"), None


def or_run(path, model, key):
    b = base64.b64encode(open(path, "rb").read()).decode()
    body = {"model": model, "messages": [{"role": "user", "content": [
        {"type": "text", "text": OR_PROMPT}, {"type": "input_audio", "input_audio": {"data": b, "format": "ogg"}}]}],
        "usage": {"include": True}}
    r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": "Bearer " + key},
                      json=body, timeout=300)
    if r.status_code != 200:
        return None, None, "HTTP %s %s" % (r.status_code, r.text[:300])
    j = r.json(); return j["choices"][0]["message"]["content"].strip(), j.get("usage"), None


def main(audio_dir, only=None):
    meta = json.load(open(os.path.join(audio_dir, "meta.json")))
    out = os.path.join(D, "runs.jsonl")
    done = set()
    if os.path.exists(out):
        for l in open(out):
            x = json.loads(l)
            if not x.get("err"): done.add((x["id"], x["engine"]))
    okk = okey()
    ork = next(l.split("=", 1)[1].strip().strip('"\'') for l in ["OPENROUTER_API_KEY=" + os.environ.get("OPENROUTER_API_KEY", "")]
               if l.startswith("OPENROUTER_API_KEY"))
    jobs = [(m, e) for m in meta for e in list(OPENAI) + list(OR_MODELS)
            if (m["id"], e) not in done and (not only or e in only)]

    def one(job):
        m, e = job; p = os.path.join(audio_dir, "%s.ogg" % m["id"]); t = time.time()
        try:
            txt, use, err = openai_run(p, OPENAI[e], okk) if e in OPENAI else or_run(p, OR_MODELS[e], ork)
        except Exception as ex:
            txt, use, err = None, None, repr(ex)[:300]
        return {"id": m["id"], "dur": m["dur"], "engine": e, "sec": round(time.time() - t, 2), "text": txt, "usage": use, "err": err}

    with ThreadPoolExecutor(6) as ex, open(out, "a") as f:
        for row in ex.map(one, jobs):
            f.write(json.dumps(row, ensure_ascii=False) + "\n"); f.flush()
            print(row["id"], row["engine"], row["sec"], (row["err"] or "")[:120] or len(row["text"] or ""))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2].split(",") if len(sys.argv) > 2 else None)
