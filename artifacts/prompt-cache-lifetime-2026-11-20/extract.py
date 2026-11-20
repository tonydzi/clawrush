#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extract.py -- шаг 1 аудита контекста сессий: сырьё -> по строке JSON на сессию.

ВХОД: транскрипты Claude Code (*.jsonl) и Codex (rollout-*.jsonl) этой машины и
архива волта (_session-archive/live, transcripts). Только чтение.
ВЫХОД: <out>/sessions.jsonl, строка на сессию:
  sid, node, harness, path, size, entry, model, title, n_user,
  calls = [[ts, ctx, cache_read, cache_write_5m, cache_write_1h, fresh_in, out, after_user]]
  (ctx = весь вход вызова; after_user = 1 ход человека, строка = тег служебного хода, 0 = нет;
   последним полем ключ вызова: по нему analyze.py убирает копии истории в форках сессий)
Кто зовёт: analyze.py (шаг 2). Что ломается: смена формата usage в харнесах.
рельса: локально, 0 LLM.
Machine: MacStudioM4 · Agent: Claude Code (claude-fable-5-2) · Operator: Anton · 2026-11-20
"""
import json
import os
import sys
import time
from datetime import datetime
from multiprocessing import Pool

HOME = os.path.expanduser("~")
ARCH = os.path.join(HOME, "Obsidian", "Anton-Knowledge", "_session-archive")
SINCE = time.mktime((2026, 10, 20, 0, 0, 0, 0, 0, -1))


def roots():
    out = [("MacStudioM4", os.path.join(HOME, ".claude", "projects")),
           ("MacStudioM4", os.path.join(HOME, ".codex", "sessions"))]
    for sub in ("live", "transcripts"):
        base = os.path.join(ARCH, sub)
        if os.path.isdir(base):
            for n in sorted(os.listdir(base)):
                p = os.path.join(base, n)
                if os.path.isdir(p):
                    out.append((n.replace("Codex-", ""), p))
    return out


def _ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def _text(c):
    """Весь текст хода без ведущих блоков <system-reminder> (они есть и у человека, и у автомата)."""
    if isinstance(c, list):
        c = "\n".join(b["text"] for b in c if isinstance(b, dict)
                      and b.get("type") in ("text", "input_text") and b.get("text"))
    if not isinstance(c, str):
        return ""
    c = c.lstrip()
    while c.startswith("<system-reminder>") and "</system-reminder>" in c:
        c = c.split("</system-reminder>", 1)[1].lstrip()
    return c


def claude(path):
    calls, order, pending_user, n_user = {}, [], 0, 0
    entry = model = title = sid = ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"custom-title"' in line[:40] or '"ai-title"' in line[:40]:
                try:
                    d = json.loads(line)
                    title = d.get("customTitle") or title or d.get("aiTitle", "")
                except Exception:
                    pass
                continue
            if '"type":"user"' not in line and '"type":"assistant"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("isSidechain"):
                continue
            t = _ts(d.get("timestamp") or "")
            m = d.get("message") or {}
            entry = d.get("entrypoint") or entry
            sid = d.get("sessionId") or sid
            if d.get("type") == "user":
                if d.get("isMeta") or d.get("isCompactSummary"):
                    continue
                txt = _text(m.get("content")).lstrip()
                if txt.startswith("[Request interrupted"):
                    continue
                if txt and not txt.startswith("<"):
                    pending_user = 1
                    n_user += 1
                elif txt and pending_user != 1:  # служебный ход: запоминаю имя тега
                    pending_user = txt[1:40].split(">")[0].split(" ")[0] or 0
            elif d.get("type") == "assistant" and m.get("usage") and t:
                if m.get("model") == "<synthetic>":
                    continue
                u = m["usage"]
                cc = u.get("cache_creation") or {}
                w1h = cc.get("ephemeral_1h_input_tokens", 0) or 0
                w5 = cc.get("ephemeral_5m_input_tokens", 0) or 0
                wtot = u.get("cache_creation_input_tokens", 0) or 0
                if w1h + w5 == 0 and wtot:
                    w5 = wtot  # старый формат без разбивки
                rd = u.get("cache_read_input_tokens", 0) or 0
                inp = u.get("input_tokens", 0) or 0
                key = m.get("id") or d.get("requestId") or d.get("uuid")
                model = m.get("model") or model
                if key in calls:
                    calls[key][6] = max(calls[key][6], u.get("output_tokens", 0) or 0)
                else:
                    if inp + rd + wtot == 0:
                        continue
                    calls[key] = [round(t, 1), inp + rd + wtot, rd, w5, w1h, inp,
                                  u.get("output_tokens", 0) or 0, pending_user, key]
                    order.append(key)
                    pending_user = 0
    return {"sid": sid or os.path.basename(path)[:-6], "harness": "claude", "entry": entry,
            "model": model, "title": title, "n_user": n_user, "calls": [calls[k] for k in order]}


def codex(path):
    calls, pending_user, n_user, last_total = [], False, 0, None
    sid = model = entry = ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if ('token_count' not in line and 'task_started' not in line
                    and 'session_meta' not in line[:80] and 'turn_context' not in line[:80]):
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p = d.get("payload") or {}
            if d.get("type") == "session_meta":
                sid = p.get("id", "") or sid
                entry = p.get("originator") or p.get("source") or entry
                if not isinstance(entry, str):
                    entry = json.dumps(entry)[:40]
            elif d.get("type") == "turn_context":
                model = p.get("model") or model
            elif p.get("type") == "task_started":  # начало хода = пришло сообщение
                pending_user = True
                n_user += 1
            elif p.get("type") == "token_count":
                info = p.get("info") or {}
                lu = info.get("last_token_usage") or {}
                tot = (info.get("total_token_usage") or {}).get("total_tokens")
                t = _ts(d.get("timestamp") or "")
                if not lu.get("input_tokens") or not t or tot == last_total:
                    continue
                last_total = tot
                rd = lu.get("cached_input_tokens", 0) or 0
                ctx = lu["input_tokens"]
                calls.append([round(t, 1), ctx, rd, 0, 0, ctx - rd, lu.get("output_tokens", 0) or 0,
                              1 if pending_user else 0, f"{sid}:{len(calls)}"])
                pending_user = False
    return {"sid": sid or os.path.basename(path)[:-6], "harness": "codex", "entry": entry,
            "model": model, "title": "", "n_user": n_user, "calls": calls}


def work(item):
    node, path, size = item
    try:
        r = codex(path) if os.path.basename(path).startswith("rollout-") else claude(path)
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {e}", "path": path}
    r.update(node=node, path=path, size=size)
    return r


def main():
    out_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    items, seen = [], set()
    for node, root in roots():
        for dp, dn, fn in os.walk(root):
            if "subagents" in dp:
                dn[:] = []
                continue
            for f in fn:
                if not f.endswith(".jsonl"):
                    continue
                p = os.path.join(dp, f)
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                if st.st_mtime < SINCE or (st.st_ino, st.st_dev) in seen:
                    continue
                seen.add((st.st_ino, st.st_dev))
                items.append((node, p, st.st_size))
    print("files", len(items), "GB", round(sum(i[2] for i in items) / 1e9, 2), flush=True)
    best, errors, empty = {}, 0, 0
    with Pool(10) as pool:
        for i, r in enumerate(pool.imap_unordered(work, items, chunksize=8)):
            if "error" in r:
                errors += 1
                continue
            if not r["calls"]:
                empty += 1
                continue
            k = (r["harness"], r["sid"])
            if k not in best or len(r["calls"]) > len(best[k]["calls"]):
                best[k] = r
            if i % 1000 == 0:
                print("..", i, flush=True)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "sessions.jsonl"), "w", encoding="utf-8") as fh:
        for r in best.values():
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps({"files": len(items), "sessions": len(best), "errors": errors,
                      "no_calls": empty}))


if __name__ == "__main__":
    main()
