# -*- coding: utf-8 -*-
"""fetch_upstream.py: download Zep's LoCoMo evaluation scripts at the pinned commit and verify their sha256.

The runner (bench_zepruler.py) reads its prompts from these files, so they must be byte-identical to the pin.
Usage: python fetch_upstream.py   -> writes ./upstream/*.py, checks against ./upstream/SHA256.json
"""
import hashlib
import json
import urllib.request
from pathlib import Path

PIN = "4b7f26cc"
BASE = f"https://raw.githubusercontent.com/getzep/zep-papers/{PIN}/kg_architecture_agent_memory/locomo_eval/"
HERE = Path(__file__).resolve().parent / "upstream"
HERE.mkdir(exist_ok=True)
want = json.loads((HERE / "SHA256.json").read_text(encoding="utf-8"))
for name, sha in want.items():
    data = urllib.request.urlopen(BASE + name, timeout=60).read()
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        raise SystemExit(f"{name}: sha256 {got} != pinned {sha}")
    (HERE / name).write_bytes(data)
    print("ok", name, got[:12])
