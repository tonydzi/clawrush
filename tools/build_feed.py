# -*- coding: utf-8 -*-
"""Generate feed.xml (RSS 2.0) from the longreads/ essays.

  python tools/build_feed.py           # rewrite feed.xml
  python tools/build_feed.py --check   # verify only, change nothing (exit 1 if stale)

Why it exists: the profile README on github.com/tonydzi pulls
the latest essays automatically (blog-post-workflow), and any feed reader can
subscribe. The essays live here, so the feed is generated here — one owner, no
copies.

Title  = the first `# ` heading of the file.
Date   = the commit that ADDED the file (git log --diff-filter=A), not mtime:
         mtime is rewritten by every clone and by Syncthing.
Link   = the file on github.com (this repo has no Pages site).

Zero dependencies: stdlib + git only.
"""
import argparse
import html
import os
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = "longreads"
OUT = os.path.join(ROOT, "feed.xml")

REPO_URL = "https://github.com/tonydzi/clawrush"
BLOB = REPO_URL + "/blob/main/"
FEED_TITLE = "ClawRush — building an AI digital twin in public"
FEED_DESC = ("English essays from running a fleet of Claude machines as one organism: "
             "what was built, what broke, what was learned.")
MAX_ITEMS = 40
SUMMARY_CHARS = 300


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args),
                          capture_output=True, text=True).stdout.strip()


def added_at(relpath):
    """ISO date of the commit that first added the file; None if never committed."""
    out = git("log", "--diff-filter=A", "--follow", "--format=%aI", "--", relpath)
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else None


def parse_post(text):
    """(title, summary) from a markdown essay. Title = first '# ' heading."""
    title, summary = None, ""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            rest = lines[i + 1:]
            break
    else:
        return None, ""
    for para in "\n".join(rest).split("\n\n"):
        para = para.strip()
        if not para or para.startswith(("#", ">", "|", "---", "```", "!")):
            continue
        summary = strip_markdown(para)
        break
    if len(summary) > SUMMARY_CHARS:
        summary = summary[:SUMMARY_CHARS].rsplit(" ", 1)[0] + "…"
    return title, summary


def strip_markdown(s):
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)   # links / images
    s = re.sub(r"[*_`]{1,3}", "", s)                     # emphasis, code ticks
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def collect():
    posts = []
    src = os.path.join(ROOT, SRC_DIR)
    for name in sorted(os.listdir(src)):
        if not name.endswith(".md") or name == "README.md":
            continue
        rel = "%s/%s" % (SRC_DIR, name)
        with open(os.path.join(src, name), encoding="utf-8") as fh:
            title, summary = parse_post(fh.read())
        if not title:
            print("  skip (no '# ' heading): %s" % rel, file=sys.stderr)
            continue
        iso = added_at(rel)
        if not iso:
            print("  skip (not committed yet): %s" % rel, file=sys.stderr)
            continue
        # quote() only: the slug is one path segment, and "/" must stay a separator.
        posts.append({"title": title, "summary": summary,
                      "link": BLOB + urllib.parse.quote(rel), "iso": iso})
    # Sort on the parsed instant, NOT on the ISO string: commits come from machines
    # in different timezones, and "…T01:00+14:00" sorts after "…T23:00-10:00" as text
    # while being three hours EARLIER in real time.
    posts.sort(key=lambda p: datetime.fromisoformat(p["iso"]).astimezone(timezone.utc),
               reverse=True)
    return posts[:MAX_ITEMS]


def rfc822(iso):
    return format_datetime(datetime.fromisoformat(iso).astimezone(timezone.utc))


def render(posts, built_at):
    e = html.escape
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
           "  <channel>",
           "    <title>%s</title>" % e(FEED_TITLE),
           "    <link>%s</link>" % REPO_URL,
           "    <description>%s</description>" % e(FEED_DESC),
           "    <language>en</language>",
           "    <lastBuildDate>%s</lastBuildDate>" % built_at,
           '    <atom:link href="%s/raw/main/feed.xml" rel="self" type="application/rss+xml"/>'
           % REPO_URL]
    for p in posts:
        out += ["    <item>",
                "      <title>%s</title>" % e(p["title"]),
                "      <link>%s</link>" % e(p["link"]),
                '      <guid isPermaLink="true">%s</guid>' % e(p["link"]),
                "      <pubDate>%s</pubDate>" % rfc822(p["iso"]),
                "      <description>%s</description>" % e(p["summary"]),
                "    </item>"]
    out += ["  </channel>", "</rss>", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify feed.xml is current; change nothing")
    args = ap.parse_args()

    posts = collect()
    if not posts:
        print("ERROR: no posts found in %s/ — refusing to write an empty feed" % SRC_DIR)
        return 1

    old = ""
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            old = fh.read()

    # lastBuildDate alone must never count as a change, or the nightly job
    # would commit a no-op diff every single night.
    keep = re.search(r"<lastBuildDate>(.*?)</lastBuildDate>", old)
    built_at = keep.group(1) if keep else rfc822(posts[0]["iso"])
    new = render(posts, built_at)

    if new == old:
        print("feed.xml up to date (%d items)" % len(posts))
        return 0
    if args.check:
        print("feed.xml is STALE — run: python tools/build_feed.py")
        return 1

    new = render(posts, format_datetime(datetime.now(timezone.utc)))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(new)
    print("feed.xml written: %d items, newest %s" % (len(posts), posts[0]["title"][:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
