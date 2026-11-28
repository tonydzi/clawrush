"""Сравнение публичных каталогов LLM API (llmapi.ai) и OpenRouter по цене за токен.

Вход: два снимка в raw/ (llmapi_models_*.json, openrouter_models_*.json), берутся последние.
Выход: raw/catalog_compare_<ts>.csv и сводка в stdout.
Сопоставление: id без префикса вендора, нижний регистр, без хвоста -YYYYMMDD; только точные совпадения.
Что ломается: смена схемы каталога (поле pricing.prompt/completion) -> модель попадёт в "не могу судить".
рельса: локальный python, 0 LLM.
"""
import csv, glob, json, os, re, statistics, sys

RAW = os.path.join(os.path.dirname(os.path.realpath(__file__)), "raw")


def latest(prefix):
    files = sorted(glob.glob(os.path.join(RAW, prefix + "_models_*.json")))
    if not files:
        sys.exit(f"нет снимка {prefix}")
    return files[-1]


def norm(mid):
    s = mid.lower().split("/")[-1].split(":")[0]
    s = re.sub(r"-\d{8}$", "", s)
    return s


def price(m):
    p = m.get("pricing") or {}
    try:
        return float(p["prompt"]) * 1e6, float(p["completion"]) * 1e6
    except (KeyError, TypeError, ValueError):
        return None


def load(prefix):
    f = latest(prefix)
    d = json.load(open(f))
    rows = d.get("data", d)
    out, blind = {}, 0
    for m in rows:
        pr = price(m)
        if pr is None:
            blind += 1
            continue
        out.setdefault(norm(m["id"]), (m["id"], pr))
    return f, len(rows), blind, out


def main():
    fl, nl, bl, L = load("llmapi")
    fo, no, bo, O = load("openrouter")
    common = sorted(set(L) & set(O))
    ts = os.path.basename(fl).split("_models_")[1].replace(".json", "")
    outp = os.path.join(RAW, f"catalog_compare_{ts}.csv")
    ratios_in, ratios_out, cheaper, dearer, equal = [], [], 0, 0, 0
    with open(outp, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["key", "llmapi_id", "openrouter_id", "llmapi_in", "llmapi_out", "or_in", "or_out", "ratio_in", "ratio_out"])
        for k in common:
            (li, (lin, lout)), (oi, (oin, oout)) = L[k], O[k]
            if oin <= 0 or oout <= 0 or lin <= 0 or lout <= 0:
                continue  # бесплатные/нулевые цены не сравниваем
            ri, ro = lin / oin, lout / oout
            ratios_in.append(ri); ratios_out.append(ro)
            if ri < 0.999 and ro < 0.999: cheaper += 1
            elif ri > 1.001 or ro > 1.001: dearer += 1
            else: equal += 1
            w.writerow([k, li, oi, f"{lin:.4f}", f"{lout:.4f}", f"{oin:.4f}", f"{oout:.4f}", f"{ri:.3f}", f"{ro:.3f}"])
    print(f"llmapi: {nl} моделей ({os.path.basename(fl)}), без цены {bl}")
    print(f"openrouter: {no} моделей ({os.path.basename(fo)}), без цены {bo}")
    print(f"точных совпадений имени: {len(common)}; платных пар сравнено: {len(ratios_in)}")
    if ratios_in:
        print(f"медиана llmapi/OR вход {statistics.median(ratios_in):.3f}, выход {statistics.median(ratios_out):.3f}")
        print(f"дешевле на обоих {cheaper}, дороже хоть в одном {dearer}, равно {equal}")
    print("csv:", outp)


if __name__ == "__main__":
    main()
