#!/usr/bin/env python3
"""claude_desktop_gate_probe.py -- is a Claude Desktop feature gate on for THIS account?

Purpose: Claude Desktop (Code tab) ships built-in MCP servers (e.g. `ccd_sidebar`
with move_sessions / set_pinned / create_group) behind server-side feature gates.
The app pulls gate values from `/api/desktop/features` and caches them on disk.
This probe reads that cache and tells you whether a gate id is present and on.
No network, no LLM. Built for Anton's fleet -- adapt the cache path if needed.

Input : gate id(s) as argv (default: 2365358358 = ccd_sidebar, 1776348311 = ccd_session_mgmt PR tools)
Output: one line per gate: ON / OFF / ABSENT(default off) + cache age; exit 0 if all ON, 1 otherwise, 2 = cache unreadable
Who calls: /retro step 6a-quater (manual), task-2026-09-08-ccd-sidebar-gate-watch
Rail: local python, 0 tokens. updated: 2026-09-08
"""
import gzip, json, os, sys, time

MAGIC_LEN = 8  # b"CLF\x02\x00\x9a\xb7\xe2" then gzip
DEFAULT_GATES = {"2365358358": "ccd_sidebar (move_sessions/set_pinned/create_group)",
                 "1776348311": "ccd_session_mgmt PR tools"}

def cache_path():
    env = os.environ.get("CLAUDE_DESKTOP_FCACHE")
    if env:
        return env
    if sys.platform == "win32":
        return os.path.join(os.environ["APPDATA"], "Claude", "fcache")
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/Claude/fcache")
    return os.path.expanduser("~/.config/Claude/fcache")

def load(path):
    raw = open(path, "rb").read()
    if raw[:3] != b"CLF":
        raise ValueError("not a CLF cache: " + repr(raw[:8]))
    return json.loads(gzip.decompress(raw[MAGIC_LEN:]))

def main(argv):
    gates = argv or list(DEFAULT_GATES)
    try:
        d = load(cache_path())
    except Exception as e:
        print("CACHE-UNREADABLE", cache_path(), e); return 2
    feats = d.get("features", {})
    age_h = (time.time() * 1000 - d.get("timestamp", 0)) / 3.6e6
    print(f"cache: {cache_path()}  features={len(feats)}  age={age_h:.1f}h  mode={d.get('mode')}")
    all_on = True
    for g in gates:
        f = feats.get(g)
        if f is None:
            state = "ABSENT (default off)"; all_on = False
        elif f.get("on"):
            state = f"ON (source={f.get('source')})"
        else:
            state = f"OFF (source={f.get('source')})"; all_on = False
        print(f"{g}: {state}  {DEFAULT_GATES.get(g, '')}")
    return 0 if all_on else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
