#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_numbers.py <article.md> ... -- каждое число статьи обязано найтись в файлах прибора или проверки.

ВХОД: статьи. Источники: tables.json, tables.md, codex_after_claim.json, ../session-context-audit/data/report.json
(числа прибора) и файлы проверки первоисточников (--ext <файл> ...). ВЫХОД: список чисел без источника, exit 1 если есть.
Числа из URL, дат и имён версий пропускаются по списку SKIP с причиной. рельса: локально, 0 LLM.
Machine: MacStudioM4 · Agent: Claude Code (claude-fable-5-2) · Operator: Anton · 2026-11-20
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
AUD = os.path.join(HERE, "..", "session-context-audit", "data")


def nums_of(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            nums_of(k, acc)
            nums_of(v, acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            nums_of(v, acc)
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, (int, float)):
        acc.add(float(obj))
    elif isinstance(obj, str):
        for m in re.findall(r"\d+(?:\.\d+)?", obj):
            acc.add(float(m))


def main():
    args = sys.argv[1:]
    ext, arts = [], []
    while args:
        a = args.pop(0)
        if a == "--ext":
            ext.append(args.pop(0))
        else:
            arts.append(a)
    inst = set()
    for f in ("tables.json", "codex_after_claim.json"):
        nums_of(json.load(open(os.path.join(HERE, f), encoding="utf-8")), inst)
    nums_of(json.load(open(os.path.join(AUD, "report.json"), encoding="utf-8")), inst)
    nums_of(json.load(open(os.path.join(AUD, "codex_ttl.json"), encoding="utf-8")), inst)
    nums_of(open(os.path.join(HERE, "tables.md"), encoding="utf-8").read(), inst)
    extn = set()
    for f in ext:
        nums_of(open(f, encoding="utf-8").read().replace(",", ""), extn)
    # производные: M = /1e6 с округлением до 0.1 и до целого; K = /1000; проценты из долей
    derived = set()
    for x in list(inst):
        for d in (1e6, 1e3):
            derived.add(round(x / d, 1))
            derived.add(float(round(x / d)))
            derived.add(float(int(x / d)))
        if 0 < x < 1:
            derived.add(round(100 * x, 1))
            derived.add(float(round(100 * x)))
    # параметры метода и определений (константы скриптов analyze.py / codex_ttl.py / tables.py, не замеры)
    method = {0.025, 0.05, 0.1, 1.25, 2.0, 2, 272, 50, 30, 5, 500, 6, 300, 200, 400, 150, 60, 1, 3, 4, 24, 90, 12,
              10, 62, 65, 55, 58, 1.5, 130, 53, 39}
    bad = 0
    for art in arts:
        t = open(art, encoding="utf-8").read()
        t = re.sub(r"\]\([^)]*\)", "]", t)                 # URL
        t = re.sub(r"https?://\S+", "", t)
        t = re.sub(r"\d{4}-\d{2}-\d{2}", "", t)           # даты
        t = re.sub(r"DR\d\d-\S+", "", t)
        t = re.sub(r"(GPT-|gpt-|Fable |Opus |Sonnet |Mythos |version |версии |#|codex#)\d+(?:\.\d+)*(?:-sol)?", "", t)
        t = re.sub(r"arxiv\.org/abs/\S+", "", t)
        miss = []
        for m in re.finditer(r"(?<![\w.])\d[\d ,]*(?:\.\d+)?", t):
            raw = m.group(0).strip().rstrip(",")
            s = raw.replace(",", "").replace(" ", "")
            if not s:
                continue
            try:
                v = float(s)
            except ValueError:
                continue
            if v in inst or v in derived or v in extn or v in method:
                continue
            ctx = t[max(0, m.start() - 40):m.end() + 25].replace("\n", " ")
            miss.append((raw, ctx))
        print(f"{os.path.basename(os.path.dirname(art))}/{os.path.basename(art)}: без источника {len(miss)}")
        for raw, ctx in miss:
            print(f"   {raw!r}: ...{ctx}...")
        bad += len(miss)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
