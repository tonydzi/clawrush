#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze.py -- шаг 2 аудита: размеры контекста, продолжения, лишние токены, пороги.

ВХОД: data/sessions.jsonl от extract.py. ВЫХОД: data/report.json + таблицы в stdout.
Единица счёта: «входной эквивалент» (вх.экв.) = токены, взвешенные ценой входа:
  свежий вход 1.0 · чтение кэша 0.1 · запись кэша 5 мин 1.25 · запись кэша 1 час 2.0
  (Codex: кэш 0.1, остальное 1.0, наценки за запись нет). Выход модели не считаем.
Модель «что было бы»: при возврате человека после паузы > GAP и контексте >= T сессию
выжимаем; новая стартует с S0 (замеренный стартовый контекст узла) + BRIEF.
Кто зовёт: человек/агент руками. рельса: локально, 0 LLM.
Machine: MacStudioM4 · Agent: Claude Code (claude-fable-5-2) · Operator: Anton · 2026-11-20
"""
import json
import os
import statistics
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(HERE, "data")
# Веса по официальным прайсам на 20.11.2026 (сверил проверяющий агент по докам Anthropic и OpenAI):
# чтение кэша 0.025 у Fable 5.1/5.2, 0.05 у Opus 5.5 и Sonnet 5.5, 0.1 у остальных Claude;
# запись кэша Claude 1.25 (5 мин) и 2.0 (1 час). Codex: чтение 0.05, некэшированный вход 1.25,
# весь вызов x2 при контексте больше 272K. Подписки тарифицируют иначе: это оценка по ценам API.
READ_W = (("fable-5-1", 0.025), ("fable-5-2", 0.025), ("mythos-5", 0.025),
          ("opus-5-5", 0.05), ("sonnet-5-5", 0.05))
DISTILL_W = 1.0  # цена чтения старой сессии для выжимки, если её читает платная модель


def read_w(model):
    for k, w in READ_W:
        if k in (model or ""):
            return w
    return 0.1
GAP = 3600
BRIEF = 5000
ROBOT = ("sdk-cli", "codex_exec", "n8n_voice_router", "codexdoor")
CTX_BINS = [0, 100, 150, 200, 300, 400, 500, 10 ** 6]
GAP_BINS = [(0, 300, "<5 мин"), (300, 3600, "5-60 мин"), (3600, 5 * 3600, "1-5 ч"),
            (5 * 3600, 86400, "5-24 ч"), (86400, 10 ** 9, ">24 ч")]
THRESHOLDS = [20, 100, 150, 200, 250, 300, 400, 500]
AUTO = ("0", "task-notification", "scheduled-task", "cross-session-message", "side-sessions-event")


def human(c):
    """Ход начал человек: текст, слэш-команда, вставка. Автомат: уведомление, расписание, без хода."""
    return str(c[7]) not in AUTO


def parts(s, c):
    """(цена чтения кэша, цена остального входа) одного вызова во вх.экв."""
    if s["harness"] == "codex":
        k = 2.0 if c[1] > 272000 else 1.0
        return c[2] * 0.05 * k, (c[1] - c[2]) * 1.25 * k
    return c[2] * s["rw"], c[5] + c[3] * 1.25 + c[4] * 2.0


def eq(s, c):
    a, b = parts(s, c)
    return a + b


def cbin(k):
    for a, b in zip(CTX_BINS, CTX_BINS[1:]):
        if k < b * 1000:
            return f"{a}-{b}K" if b < 10 ** 6 else f"{a}K+"


def gbin(g):
    for a, b, name in GAP_BINS:
        if a <= g < b:
            return name


def q(xs, p):
    xs = sorted(xs)
    return xs[min(int(len(xs) * p), len(xs) - 1)] if xs else 0


def baselines(S):
    """S0 = медиана контекста первого вызова, r0 = медиана цены токена первого вызова."""
    by = defaultdict(list)
    for s in S:
        c = s["calls"][0]
        if c[1] > 0 and s["own"][0]:
            by[(s["node"], s["harness"])].append((c[1], eq(s, c) / c[1]))
            by[("*", s["harness"])].append((c[1], eq(s, c) / c[1]))
    return {k: (statistics.median(x[0] for x in v), statistics.median(x[1] for x in v), len(v))
            for k, v in by.items()}


def simulate(S, base, T, gap=GAP):
    """Виртуальный мир с порогом T (токены). Возвращает сумму экономии и число блоков."""
    saved = foreign = rewrite = 0.0
    blocks = 0
    sess = set()
    for s in S:
        h = s["harness"]
        s0, r0, n = base.get((s["node"], h), (0, 0, 0))
        if n < 5:
            s0, r0, n = base[("*", h)]
        fresh = s0 + BRIEF
        off, prev = 0.0, None
        for c, own in zip(s["calls"], s["own"]):
            ctx = c[1]
            if not own:  # копия чужой истории в форке: только как «предыдущий вызов»
                prev = c
                continue
            if prev and ctx < prev[1] * 0.7:
                off = 0.0  # сжатие в реальном мире: миры сошлись
            off = min(off, max(ctx - fresh, 0))
            rd_eq, rest_eq = parts(s, c)
            rate = (rd_eq + rest_eq) / ctx if ctx else 0
            v = ctx - off
            if prev and human(c) and c[0] - prev[0] > gap and v >= T and v > fresh:
                blocks += 1
                sess.add(s["sid"])
                foreign += v
                saved += ctx * rate - fresh * r0
                rewrite += ctx * rate - fresh * r0
                off = ctx - fresh
            else:  # выброшенное = самый старый префикс: сперва по цене чтения кэша
                a = min(off, c[2])
                saved += (a * rd_eq / c[2] if c[2] else 0) + \
                         ((off - a) * rest_eq / (ctx - c[2]) if ctx > c[2] else 0)
            prev = c
    return {"T": T, "blocks": blocks, "sessions": len(sess), "saved_eq": round(saved),
            "saved_at_resume_eq": round(rewrite),
            "foreign_tokens": round(foreign)}


def analyze(S, name):
    R = {"set": name, "n": len(S)}
    t0 = min(s["calls"][0][0] for s in S)
    t1 = max(s["calls"][-1][0] for s in S)
    R["span_days"] = round((t1 - t0) / 86400, 1)
    R["first_last"] = [min(s["calls"][-1][0] for s in S), t1]
    R["by_node"] = Counter(f"{s['node']}/{s['harness']}" for s in S).most_common()
    peak = [max(c[1] for c in s["calls"]) for s in S]
    R["peak_q"] = {p: q(peak, p) for p in (0.25, 0.5, 0.75, 0.9, 0.95, 0.99)}
    R["peak_hist"] = Counter(cbin(k) for k in peak)
    R["start_q"] = {p: q([s["calls"][0][1] for s in S], p) for p in (0.25, 0.5, 0.75)}
    tot = defaultdict(float)
    cont = defaultdict(lambda: [0, 0, 0.0, 0.0])  # n, cold, eq, ctx
    drag = {t: 0.0 for t in THRESHOLDS}
    cold_other = defaultdict(lambda: [0, 0.0])
    for s in S:
        prev = None
        for c, own in zip(s["calls"], s["own"]):
            if not own:
                prev = c
                continue
            rd_eq, rest_eq = parts(s, c)
            e = rd_eq + rest_eq
            tot["eq"] += e
            tot["read_eq"] += rd_eq
            tot["write_eq"] += rest_eq
            tot["tokens"] += c[1]
            tot["calls"] += 1
            for t in THRESHOLDS:
                if c[1] > t * 1000:
                    drag[t] += (c[1] - t * 1000) * (e / c[1])
            cold = (c[1] - c[2]) >= 0.5 * c[1] and c[1] >= 50000
            if prev and human(c):
                k = (gbin(c[0] - prev[0]), cbin(prev[1]))
                x = cont[k]
                x[0] += 1
                x[1] += cold
                x[2] += e
                x[3] += c[1]
            elif prev and cold:
                x = cold_other[("пауза >1 ч" if c[0] - prev[0] > GAP else "пауза <1 ч") + ", " + str(c[7])]
                x[0] += 1
                x[1] += e
            prev = c
    R["totals"] = {k: round(v) for k, v in tot.items()}
    R["cont"] = {f"{k[0]}|{k[1]}": [v[0], v[1], round(v[2]), round(v[3])] for k, v in cont.items()}
    R["cold_not_after_user"] = {k: [v[0], round(v[1])] for k, v in cold_other.items()}
    R["drag_over_T_eq"] = {t: round(v) for t, v in drag.items()}
    base = baselines(S)
    R["baseline"] = {f"{k[0]}/{k[1]}": [round(v[0]), round(v[1], 2), v[2]] for k, v in base.items()}
    R["sim"] = [simulate(S, base, t * 1000) for t in THRESHOLDS]
    R["sim_gap5m"] = [simulate(S, base, t * 1000, 300) for t in (200, 300, 400)]
    return R


def show(R):
    M = 1e6
    print(f"\n===== {R['set']}: {R['n']} сессий за {R['span_days']} дн =====")
    print("узлы:", ", ".join(f"{k} {v}" for k, v in R["by_node"][:12]))
    print("пик контекста, квантили:", {k: f"{v // 1000}K" for k, v in R["peak_q"].items()})
    print("старт контекста, квантили:", {k: f"{v // 1000}K" for k, v in R["start_q"].items()})
    print("гистограмма пика:", {b: R["peak_hist"].get(b, 0) for b in
                                 [cbin(a * 1000) for a in CTX_BINS[:-1]]})
    t = R["totals"]
    print(f"всего вх.экв. {t['eq'] / M:.0f}M = чтение кэша {t['read_eq'] / M:.0f}M + запись кэша "
          f"и свежий вход {t['write_eq'] / M:.0f}M; вызовов {t['calls']}")
    print("\nпродолжения человеком: пауза x контекст до -> число (из них холодных) | вх.экв. M")
    cols = [cbin(a * 1000) for a in CTX_BINS[:-1]]
    print(f"{'пауза':>9} | " + " | ".join(f"{c:>16}" for c in cols))
    for _, _, g in GAP_BINS:
        row = []
        for c in cols:
            v = R["cont"].get(f"{g}|{c}", [0, 0, 0, 0])
            row.append(f"{v[0]:>4}({v[1]:>3}) {v[2] / M:>6.1f}M")
        print(f"{g:>9} | " + " | ".join(row))
    print("холодные перезаписи НЕ после хода человека (число, вх.экв.):",
          {k: f"{v[0]} / {v[1] / M:.1f}M" for k, v in sorted(R["cold_not_after_user"].items(), key=lambda x: -x[1][1])})
    print("налог на раздутость (вх.экв. на токены сверх T):",
          {f"{k}K": f"{v / M:.0f}M" for k, v in R["drag_over_T_eq"].items()})
    print("\nпорог T | блоков | сессий | экономия вх.экв. (в т.ч. в момент возврата) | на блок | доля от всего | "
          "чтение для выжимки | пол: возврат минус выжимка")
    for x in R["sim"]:
        per = x["saved_eq"] / x["blocks"] if x["blocks"] else 0
        print(f"{x['T'] // 1000:>5}K | {x['blocks']:>6} | {x['sessions']:>6} | {x['saved_eq'] / M:>10.1f}M ({x['saved_at_resume_eq'] / M:>7.1f}M) | "
              f"{per / 1000:>6.0f}K | {100 * x['saved_eq'] / t['eq']:>5.1f}% | {x['foreign_tokens'] / M:.1f}M | "
              f"{(x['saved_at_resume_eq'] - DISTILL_W * x['foreign_tokens']) / M:.1f}M")
    print("то же при паузе 5 мин:", [(x["T"] // 1000, x["blocks"], round(x["saved_eq"] / M, 1))
                                     for x in R["sim_gap5m"]])


def main():
    S = [json.loads(l) for l in open(os.path.join(DATA, "sessions.jsonl"), encoding="utf-8")]
    seen = set()
    for s in sorted(S, key=lambda s: s["calls"][0][0]):  # форк несёт копию истории родителя
        s["own"] = [c[8] not in seen for c in s["calls"]]
        seen.update(c[8] for c in s["calls"])
    S = [s for s in S if any(s["own"])]
    for s in S:
        s["rw"] = read_w(s["model"])
    for s in S:
        s["n_h"] = sum(1 for c, o in zip(s["calls"], s["own"]) if o and human(c))
    S.sort(key=lambda s: s["calls"][-1][0], reverse=True)
    dialog = [s for s in S if s["n_h"] >= 2 and s["entry"] not in ROBOT]
    sets = {"A: последние 500, все подряд": S[:500],
            "B: последние 500 диалоговых (2+ хода человека)": dialog[:500],
            "C: все диалоговые за месяц": [s for s in dialog if s["calls"][-1][0] > S[0]["calls"][-1][0] - 31 * 86400],
            "D: все сессии за месяц": [s for s in S if s["calls"][-1][0] > S[0]["calls"][-1][0] - 31 * 86400]}
    out = []
    for name, sub in sets.items():
        R = analyze(sub, name)
        out.append(R)
        show(R)
    with open(os.path.join(DATA, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
    print("\nbaseline B:", out[1]["baseline"])


if __name__ == "__main__":
    sys.exit(main())
