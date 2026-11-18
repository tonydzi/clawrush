# Пересуд ВСЕХ ответов экзамена в одном проходе двумя судьями разных вендоров (codex, mistral), вперемешку и вслепую.
import io, os, re, sys, json, subprocess, threading, hashlib, collections
D = os.path.dirname(os.path.abspath(__file__))
st = json.load(io.open(os.path.join(D, "canon_eval.json"), encoding="utf-8"))
OUT = os.path.join(D, "rejudge.json")
res = json.load(io.open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
S = {s["id"]: s for s in st["sit"]}; lock = threading.Lock()
items = []
for key, a in st["ans"].items():
    if key.startswith("grok|"): continue
    for sid, txt in a.items():
        items.append((hashlib.md5(("r2" + key + sid).encode()).hexdigest()[:8], key, sid, txt))
items.sort()
JH = ("Ты судья экзамена. Для каждой записи даны: ситуация, ожидаемое действие по своду, типичное неверное действие и ответ агента. "
      "Поставь 1, если ответ агента ПО СУТИ содержит ожидаемое действие: назван тот же ключевой шаг или инструмент и не нарушен названный запрет. Другие слова, другой порядок и ДОПОЛНИТЕЛЬНЫЕ шаги сверх ожидаемого допустимы. "
      "Поставь 0, если ключевого шага нет, агент делает типичное неверное или отвечает общо. Суди одинаково строго все записи.\n"
      "Формат строго, одна строка на запись, без пояснений: КЛЮЧ|||1 или 0\n\n")
def judge(rail):
    for i in range(0, len(items), 50):
        b = [x for x in items[i:i + 50] if x[0] not in res.get(rail, {})]
        if not b: continue
        body = "\n\n".join("КЛЮЧ %s\nСитуация: %s\nОжидаемое: %s\nНеверное: %s\nОтвет агента: %s" % (k, S[sid]["q"], S[sid]["want"], S[sid]["wrong"], txt[:700]) for k, key, sid, txt in b)
        pf = os.path.join(D, "rj_%s_%d.txt" % (rail, i)); io.open(pf, "w", encoding="utf-8").write(JH + body)
        for attempt in (1, 2):
            try:
                got = subprocess.run([sys.executable, "-X", "utf8", os.path.expanduser("~/.claude/scripts/llm_ask.py"), "--rails", rail, "--mode", "first", "--no-principles",
                                      "--timeout", "900", "--prompt-file", pf], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1000).stdout or ""
            except Exception: got = ""
            ok = {}
            for ln in got.splitlines():
                p = [x.strip().strip("`") for x in ln.split("|||")]
                if len(p) >= 2 and p[1][:1] in ("0", "1"): ok[p[0].replace("КЛЮЧ", "").strip()] = int(p[1][:1])
            ok = {k: v for k, v in ok.items() if k in {x[0] for x in b}}
            print(rail, "пачка", i, "оценок", len(ok), "из", len(b)); sys.stdout.flush()
            if len(ok) >= len(b) * 0.9:
                with lock:
                    res.setdefault(rail, {}).update(ok); json.dump(res, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
                break
JUDGES = ["codex", "mistral"]
th = [threading.Thread(target=judge, args=(r,)) for r in JUDGES]; [t.start() for t in th]; [t.join() for t in th]
ARMS = ["v6", "v7", "v7b", "v7c", "none"]; NAME = {"v6": "канон 6.18", "v7": "проект 7.1 (файл)", "v7b": "сборка строками", "v7c": "сборка абзацами", "none": "без канона"}
for j in JUDGES:
    t = collections.defaultdict(lambda: [0, 0])
    for k, key, sid, txt in items:
        if k in res.get(j, {}):
            rail, arm = key.split("|");
            if rail == "mistral" and j == "mistral": continue      # судья не судит собственные ответы
            t[arm][0] += res[j][k]; t[arm][1] += 1
    print("\nСУДЬЯ %s:" % j, " | ".join("%s %d/%d (%.0f%%)" % (NAME[a], t[a][0], t[a][1], 100.0 * t[a][0] / max(1, t[a][1])) for a in ARMS))
both = [(k, key) for k, key, sid, txt in items if all(k in res.get(j, {}) for j in JUDGES)]
agree = sum(1 for k, key in both if res["codex"][k] == res["mistral"][k])
print("\nсудьи согласны в %d из %d (%.0f%%)" % (agree, len(both), 100.0 * agree / max(1, len(both))))
t = collections.defaultdict(lambda: [0, 0])
for k, key in both:
    arm = key.split("|")[1]; t[arm][1] += 1; t[arm][0] += 1 if res["codex"][k] and res["mistral"][k] else 0
print("ОБА СУДЬИ сказали «верно»:", " | ".join("%s %d/%d (%.0f%%)" % (NAME[a], t[a][0], t[a][1], 100.0 * t[a][0] / max(1, t[a][1])) for a in ARMS))
