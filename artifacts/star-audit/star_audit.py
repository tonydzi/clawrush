#!/usr/bin/env python3
"""Prototype star-event inspection. Read-only GitHub API and public GH Archive.
Input: owner/repo and optional GITHUB_TOKEN environment variable.
Output: bounded event/profile heuristics, not a bot classification or purchase claim.
No local credential discovery, uploads of private data, or telemetry.
API/archive coverage is limited; current profiles are not historical profiles.
"""
import argparse
import datetime as dt
import json
import os
import socket
import statistics
import sys
import urllib.error
import urllib.request
from collections import Counter

API = "https://api.github.com"
MIN_SAMPLE = 20          # меньше профилей = «не могу судить»
YOUNG_DAYS = 30          # аккаунт создан меньше чем за N дней до звезды
SUSPECT_SIGNALS = 3      # сколько признаков из 5 делают аккаунт подозрительным


# ---------- чистые функции (покрыты тестом) ----------

def parse_ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def user_signals(profile, starred_at):
    """Список признаков «пустого» аккаунта. profile = ответ /users/{login}."""
    sig = []
    if (profile.get("public_repos") or 0) == 0:
        sig.append("no_repos")
    if (profile.get("followers") or 0) == 0:
        sig.append("no_followers")
    if (profile.get("following") or 0) == 0:
        sig.append("no_following")
    if not any(profile.get(k) for k in ("bio", "blog", "company", "location", "name")):
        sig.append("empty_profile")
    created = profile.get("created_at")
    if created and starred_at:
        age = parse_ts(starred_at) - parse_ts(created)
        if age.days < YOUNG_DAYS:
            sig.append("young_at_star")
    return sig


def is_suspect(signals):
    return len(signals) >= SUSPECT_SIGNALS


def find_bursts(starred_ats, min_count=15, factor=5.0):
    """Часы, где звёзд в factor раз больше медианы непустых часов и не меньше min_count."""
    hours = Counter(parse_ts(t).strftime("%Y-%m-%d %H:00") for t in starred_ats)
    if not hours:
        return []
    med = statistics.median(hours.values())
    out = [(h, c) for h, c in hours.items() if c >= min_count and c >= factor * med]
    return sorted(out, key=lambda x: -x[1])


def verdict(n_checked, n_suspect, bursts):
    if n_checked < MIN_SAMPLE:
        return "не могу судить: проверено {} профилей, нужно ≥{}".format(n_checked, MIN_SAMPLE)
    share = n_suspect / n_checked
    if share >= 0.4 or (bursts and share >= 0.2):
        return "красный: много сигналов для ручной проверки ({:.0%} отмеченных профилей)".format(share)
    if share >= 0.15 or bursts:
        return "жёлтый: есть аномалии, смотреть руками ({:.0%} отмеченных)".format(share)
    return "зелёный: мало сигналов по этой эвристике ({:.0%} отмеченных)".format(share)


# ---------- сеть ----------





MAX_PAGE = 400


class RateLimited(Exception):
    pass


def get(path, accept="application/vnd.github+json"):
    req = urllib.request.Request(API + path, headers={
        "Accept": accept, "User-Agent": "star-audit",
        **({"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"]}
           if os.environ.get("GITHUB_TOKEN") else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise RateLimited("GitHub ответил 401; проверьте GITHUB_TOKEN "
                              "(fine-grained токен, только чтение публичных репо)")
        if e.code in (403, 429):
            raise RateLimited("GitHub отказал ({}): лимит запросов; задайте GITHUB_TOKEN".format(e.code))
        raise


GHARCHIVE = "https://play.clickhouse.com/?user=play"  # публичная копия GH Archive, без входа


def gharchive_stars(repo, limit):
    """Последние limit звёзд (WatchEvent) из GH Archive в формате ответа stargazers."""
    if not all(c.isalnum() or c in "-_./" for c in repo):
        raise ValueError("странное имя репо: " + repo)
    q = ("SELECT actor_login, formatDateTime(created_at, '%Y-%m-%dT%H:%i:%SZ') FROM github_events "
         "WHERE repo_name = '{}' AND event_type = 'WatchEvent' ORDER BY created_at DESC LIMIT {} "
         "FORMAT TSV").format(repo, int(limit))
    req = urllib.request.Request(GHARCHIVE, data=q.encode(), headers={"User-Agent": "star-audit"})
    with urllib.request.urlopen(req, timeout=120) as r:
        rows = [l.split("\t") for l in r.read().decode().splitlines() if "\t" in l]
    return [{"user": {"login": u}, "starred_at": t} for u, t in reversed(rows)]


def audit(repo, pages, sample):
    info = get("/repos/" + repo)
    total = info["stargazers_count"]
    stars, notes = [], []
    last_page = max(1, -(-total // 100))
    first = max(1, last_page - pages + 1)
    try:
        if last_page > MAX_PAGE:  # API не отдаёт дальше 400-й страницы: свежих звёзд не видно
            raise RateLimited("у репо {} звёзд, API показывает только первые {}".format(total, MAX_PAGE * 100))
        for p in range(first, last_page + 1):
            stars += get("/repos/{}/stargazers?per_page=100&page={}".format(repo, p),
                         accept="application/vnd.github.star+json")
    except (RateLimited, urllib.error.HTTPError) as e:
        # API error or pagination cap: fall back to a bounded public archive; cause is not inferred.
        notes.append("основная выборка API не получена ({}); звёзды взяты из GH Archive".format(
            getattr(e, "code", e)))
        stars = gharchive_stars(repo, pages * 100)
    stars = [s for s in stars if s.get("user")]
    bursts = find_bursts([s["starred_at"] for s in stars])
    checked, suspects = [], []
    step = max(1, len(stars) // sample) if sample else 1
    for s in stars[::step][:sample]:
        try:
            prof = get("/users/" + s["user"]["login"])
        except RateLimited as e:
            notes.append(str(e))
            break
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
            # Missing account is a separate signal, not evidence of a bot or purchased star.
            checked.append(s["user"]["login"])
            suspects.append({"login": s["user"]["login"], "signals": ["account_gone"]})
            continue
        sig = user_signals(prof, s["starred_at"])
        checked.append(s["user"]["login"])
        if is_suspect(sig):
            suspects.append({"login": s["user"]["login"], "signals": sig})
    return {
        "repo": repo, "stars_total": total, "stars_fetched": len(stars),
        "profiles_checked": len(checked), "suspects": suspects,
        "bursts": bursts[:10], "notes": sorted(set(notes)),
        "verdict": verdict(len(checked), len(suspects), bursts),
        "coverage": "звёзд прочитано {} из {}; профилей проверено {}".format(len(stars), total, len(checked)),
    }




def main(argv=None):
    ap = argparse.ArgumentParser(description="Проверка звёзд GitHub-репо на накрутку")
    ap.add_argument("repo", help="owner/repo")
    ap.add_argument("--pages", type=int, default=5, help="сколько последних страниц по 100 звёзд читать")
    ap.add_argument("--sample", type=int, default=60, help="сколько профилей проверить")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        r = audit(a.repo, a.pages, a.sample)
    except RateLimited as e:
        print("❌ " + str(e), file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print("Репозиторий: {} · звёзд всего {}".format(r["repo"], r["stars_total"]))
    print("Покрытие: " + r["coverage"])
    print("Вердикт: " + r["verdict"])
    if r["bursts"]:
        print("Всплески (час UTC: звёзд):")
        for h, c in r["bursts"]:
            print("  {}: {}".format(h, c))
    for s in r["suspects"][:15]:
        print("  подозрительный: {} ({})".format(s["login"], ", ".join(s["signals"])))
    for n in r["notes"]:
        print("⚠️ " + n)
    print("Помните: аномалия не доказывает, что звёзды купил владелец.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
