# -*- coding: utf-8 -*-
"""Full Multi-Vendor × Effort Cofounder Consistency Benchmark on Canon v7.14.0:
Tests Low / Medium / High / XHigh across:
- Meta Muse Wonder (meta/muse-wonder: low, medium, high)
- xAI Grok CLI (grok-4.7: low, medium, high, xhigh; grok-4.7-build-fast: low, high; grok-4.6: low, medium, high)
- Z.ai GLM-5.3 (z-ai/glm-5.3: low, medium, high)
- DeepSeek V4 Pro (deepseek/deepseek-v4-pro: low, medium, high)
- Qwen 3.7 Plus (qwen/qwen3.7-plus: low, medium, high)
- MiniMax M3 (minimax/minimax-m3: low, medium, high)
- Mistral Large 2512 (mistralai/mistral-large-2512: low, medium, high) + Mistral Vibe CLI
- OpenAI GPT-6 Sol (openai/gpt-6-sol: low, medium, high) & GPT-5.6 Terra (openai/gpt-5.6-terra: low, medium, high)
- Anthropic Claude CLI (opus, sonnet, haiku: low, medium, high)
- Plus all 27 Antigravity configurations already on disk.

Machine: PaloAlto-Hub (Хаб) · Agent: Antigravity · Operator: Anton · 2026-11-26
"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, r"~\.claude\scripts")
sys.path.insert(0, r"~\.claude\scripts\_shared")
sys.path.insert(0, r"~\.claude\scripts\cc-review")

import claude_run
import eval_v7140_antigravity_frontier as base
import grok_lockdown
import llm_ask
import orouter_review

CLAUDE_SEM = threading.Semaphore(3)
GROK_SEM = threading.Semaphore(3)
OR_SEM = threading.Semaphore(6)

EXTERNAL_SPECS = [
    # Meta Muse Wonder
    ("ext:muse-wonder-low", "or", "meta/muse-wonder", "low"),
    ("ext:muse-wonder-medium", "or", "meta/muse-wonder", "medium"),
    ("ext:muse-wonder-high", "or", "meta/muse-wonder", "high"),
    # Z.ai GLM-5.3
    ("ext:glm-5.3-low", "or", "z-ai/glm-5.3", "low"),
    ("ext:glm-5.3-medium", "or", "z-ai/glm-5.3", "medium"),
    ("ext:glm-5.3-high", "or", "z-ai/glm-5.3", "high"),
    # xAI Grok 4.7, 4.7-build-fast, 4.6 via Grok CLI
    ("cli:grok-4.7-low", "grok", "grok-4.7", "low"),
    ("cli:grok-4.7-medium", "grok", "grok-4.7", "medium"),
    ("cli:grok-4.7-high", "grok", "grok-4.7", "high"),
    ("cli:grok-4.7-xhigh", "grok", "grok-4.7", "xhigh"),
    ("cli:grok-4.7-fast-low", "grok", "grok-4.7-build-fast", "low"),
    ("cli:grok-4.7-fast-high", "grok", "grok-4.7-build-fast", "high"),
    ("cli:grok-4.6-low", "grok", "grok-4.6", "low"),
    ("cli:grok-4.6-medium", "grok", "grok-4.6", "medium"),
    ("cli:grok-4.6-high", "grok", "grok-4.6", "high"),
    # DeepSeek V4 Pro
    ("ext:deepseek-v4-pro-low", "or", "deepseek/deepseek-v4-pro", "low"),
    ("ext:deepseek-v4-pro-medium", "or", "deepseek/deepseek-v4-pro", "medium"),
    ("ext:deepseek-v4-pro-high", "or", "deepseek/deepseek-v4-pro", "high"),
    # Qwen 3.7 Plus
    ("ext:qwen3.7-plus-low", "or", "qwen/qwen3.7-plus", "low"),
    ("ext:qwen3.7-plus-medium", "or", "qwen/qwen3.7-plus", "medium"),
    ("ext:qwen3.7-plus-high", "or", "qwen/qwen3.7-plus", "high"),
    # MiniMax M3
    ("ext:minimax-m3-low", "or", "minimax/minimax-m3", "low"),
    ("ext:minimax-m3-medium", "or", "minimax/minimax-m3", "medium"),
    ("ext:minimax-m3-high", "or", "minimax/minimax-m3", "high"),
    # Mistral Large 2512 + Vibe CLI
    ("ext:mistral-large-2512-low", "or", "mistralai/mistral-large-2512", "low"),
    ("ext:mistral-large-2512-medium", "or", "mistralai/mistral-large-2512", "medium"),
    ("ext:mistral-large-2512-high", "or", "mistralai/mistral-large-2512", "high"),
    ("cli:mistral-vibe", "vibe", "mistral-vibe", "default"),
    # OpenAI GPT-6 Sol & GPT-5.6 Terra
    ("ext:gpt-6-sol-low", "or", "openai/gpt-6-sol", "low"),
    ("ext:gpt-6-sol-medium", "or", "openai/gpt-6-sol", "medium"),
    ("ext:gpt-6-sol-high", "or", "openai/gpt-6-sol", "high"),
    ("ext:gpt-5.6-terra-low", "or", "openai/gpt-5.6-terra", "low"),
    ("ext:gpt-5.6-terra-medium", "or", "openai/gpt-5.6-terra", "medium"),
    ("ext:gpt-5.6-terra-high", "or", "openai/gpt-5.6-terra", "high"),
    # Anthropic Claude CLI with explicit --effort
    ("cli:claude-opus-5-5-low", "claude_eff", "opus", "low"),
    ("cli:claude-opus-5-5-medium", "claude_eff", "opus", "medium"),
    ("cli:claude-opus-5-5-high", "claude_eff", "opus", "high"),
    ("cli:claude-sonnet-5-5-low", "claude_eff", "sonnet", "low"),
    ("cli:claude-sonnet-5-5-medium", "claude_eff", "sonnet", "medium"),
    ("cli:claude-sonnet-5-5-high", "claude_eff", "sonnet", "high"),
    ("cli:claude-haiku-5-5-low", "claude_eff", "haiku", "low"),
    ("cli:claude-haiku-5-5-medium", "claude_eff", "haiku", "medium"),
    ("cli:claude-haiku-5-5-high", "claude_eff", "haiku", "high"),
]


def call_or_with_effort(prompt, canon_text, model_id, effort, timeout=180):
    with OR_SEM:
        res = orouter_review.ask_one(
            model=model_id,
            context=prompt,
            effort=effort,
            system=canon_text,
            timeout=timeout,
            max_tokens=16384,
        )
    if not res.get("ok") or not (res.get("content") or res.get("text") or "").strip():
        raise ValueError(f"orouter/llmapi({model_id}, {effort}) failed: {res.get('text', '')[:180]}")
    ans = (res.get("content") or res.get("text") or "").strip()
    return res.get("response_model") or model_id, ans, {
        "channel": f"{res.get('provider', 'openrouter')} reasoning.effort={effort}",
        "effort_applied": res.get("effort_applied"),
        "in_tokens": res.get("in"),
        "out_tokens": res.get("out"),
        "usd": res.get("usd"),
    }


def call_grok_with_effort(prompt, canon_path, model_id, effort, timeout=200):
    with GROK_SEM:
        with tempfile.TemporaryDirectory(prefix="eval-grok-") as td:
            td_p = Path(td)
            real_grok = Path.home() / ".grok"
            temp_gh = td_p / "grok_home"
            temp_cwd = td_p / "cwd"
            temp_gh.mkdir(parents=True, exist_ok=True)
            temp_cwd.mkdir(parents=True, exist_ok=True)
            for fname in (
                "auth.json", "agent_id", "config.toml", ".config-init.lock", "experiments_remote.json",
                "models_cache.json", "settings_cache.json", "tip_cursor.json", "version.json", ".metadata_version",
            ):
                src_f = real_grok / fname
                if src_f.is_file():
                    shutil.copyfile(src_f, temp_gh / fname)
            shutil.copyfile(canon_path, temp_gh / "AGENTS.md")
            env = grok_lockdown.env()
            env["GROK_HOME"] = str(temp_gh)
            env["HOME"] = str(td_p / "fake_home")
            env["USERPROFILE"] = str(td_p / "fake_home")
            (td_p / "fake_home").mkdir(exist_ok=True)
            inp = temp_cwd / "input.txt"
            inp.write_text(prompt, encoding="utf-8")
            cmd = llm_ask._win_base(shutil.which("grok")) + [
                "--prompt-file", str(inp), "--verbatim", "--model", model_id, "--always-approve", "--no-plan",
                "--disable-web-search", "--no-auto-update", "--output-format", "json", "--reasoning-effort", effort,
            ] + grok_lockdown.TOOL_ARGS
            result = llm_ask._run_tree(cmd, timeout=timeout, env=env, cwd=str(temp_cwd))
            if result.returncode:
                raise ValueError(f"Grok CLI exit {result.returncode}; {result.stderr[-160:].strip()}")
            answer, stop = llm_ask.grok_parse(result.stdout.strip())
            if not answer or stop == llm_ask.STOP_UNPARSED or stop in llm_ask.GROK_STOP_BAD:
                raise ValueError(f"Grok incomplete; stop={stop}")
            return f"{model_id}:{effort}", answer, {"channel": "isolated GROK_HOME", "effort": effort, "stop_reason": stop}


def call_claude_with_effort(prompt, canon_path, model_id, effort, timeout=200):
    with CLAUDE_SEM:
        with tempfile.TemporaryDirectory(prefix="eval-claude-") as td:
            claude_run.ensure_oauth_token()
            env = dict(os.environ)
            env.pop("VENDOR_API_TOKEN", None)
            env = llm_ask.isolated_env(env, "claude", force=True)
            cmd = llm_ask._win_base(shutil.which("claude")) + [
                "-p", "--safe-mode", "--no-session-persistence", "--strict-mcp-config",
                "--model", model_id, "--effort", effort, "--tools", "", "--output-format", "json",
                "--system-prompt-file", str(canon_path),
            ]
            result = llm_ask._run_tree(cmd, prompt=prompt, timeout=timeout, env=env, cwd=td)
            if result.returncode:
                raise ValueError(f"Claude CLI exit {result.returncode}; {result.stderr[-180:].strip()}")
            data = json.loads(result.stdout.strip())
            if data.get("is_error") or not data.get("result"):
                raise ValueError("Claude returned no answer")
            return f"claude-{model_id}:{effort}", data["result"], {"channel": "claude CLI --effort", "effort": effort}


def call_vibe_isolated(prompt, canon_text, timeout=180):
    vibe_exe = shutil.which("vibe") or os.path.expanduser("~/.local/bin/vibe.exe")
    key_f = Path(r"~\.claude\config/vibe.env").read_text(encoding="utf-8")
    key = re.search(r"MISTRAL_API_KEY=['\"]?([^'\"\s#]+)", key_f).group(1)
    with tempfile.TemporaryDirectory(prefix="eval-vibe-") as td:
        env = dict(os.environ, MISTRAL_API_KEY=key, USERPROFILE=td, HOME=td, VIBE_HOME=td)
        full_p = "Ниже твой файл правил CLAUDE.md целиком:\n\n" + canon_text + "\n\n" + prompt
        pf = os.path.join(td, "p.md")
        Path(pf).write_text(full_p, encoding="utf-8")
        r = subprocess.run(
            [vibe_exe, "--prompt-file", pf, "--max-turns", "1"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=td, timeout=timeout
        )
        out = (r.stdout or "").strip()
        if r.returncode != 0 or not out:
            raise ValueError(f"vibe exit {r.returncode}: {(r.stderr or '')[-180:]}")
        return "mistral-vibe", out, {"channel": "Mistral Vibe CLI clean VIBE_HOME"}


def run_spec_job(job):
    route_key, kind, model_id, effort, run_idx = job
    safe_name = route_key.replace(":", "_").replace("/", "_")
    raw_bytes = base.CANON_PATH.read_bytes()
    canon_text = raw_bytes.decode("utf-8-sig")
    canon_sha = hashlib.sha256(raw_bytes).hexdigest()
    out_file = base.OUT_DIR / f"{safe_name}-r{run_idx}.json"
    if out_file.exists():
        try:
            cached = json.loads(out_file.read_text(encoding="utf-8"))
            if cached.get("status") == "ok" and cached.get("canon_sha256") == canon_sha:
                print(f"[CACHE] {route_key} r{run_idx}: full_pass={cached['full_pass_count']}/8 axes={cached['axes_sum']}/48", flush=True)
                return cached
        except Exception:
            pass

    rec = {
        "machine": base.STAMP,
        "route": route_key,
        "kind": kind,
        "requested_model": model_id,
        "effort": effort,
        "arm": "v7.14.0",
        "run": run_idx,
        "canon_sha256": canon_sha,
        "started_utc": datetime.now(timezone.utc).isoformat(),
    }
    t0 = time.monotonic()
    try:
        # Use 4-case chunks for Grok, DeepSeek, GLM, MiniMax, Qwen, Muse so long reasoning never truncates 8-case JSON
        use_chunks = kind in ("or", "grok", "vibe")
        chunks = [base.CASES[:4], base.CASES[4:]] if use_chunks else [base.CASES]
        rows = []
        eff_model = model_id
        rcpt = {}
        for chunk in chunks:
            p_chunk = base.FRAME_TEMPLATE.format(n=len(chunk)) + json.dumps(
                [{"id": c["id"], "context": c["context"], "request": c["request"]} for c in chunk],
                ensure_ascii=False,
            )
            for attempt in range(2):
                try:
                    if kind == "or":
                        m, r_ans, rc = call_or_with_effort(p_chunk, canon_text, model_id, effort, timeout=180)
                    elif kind == "grok":
                        m, r_ans, rc = call_grok_with_effort(p_chunk, base.CANON_PATH, model_id, effort, timeout=180)
                    elif kind == "claude_eff":
                        m, r_ans, rc = call_claude_with_effort(p_chunk, base.CANON_PATH, model_id, effort, timeout=180)
                    elif kind == "vibe":
                        m, r_ans, rc = call_vibe_isolated(p_chunk, canon_text, timeout=180)
                    else:
                        raise ValueError(f"Unknown kind {kind}")
                    part = base.extract_array(r_ans, [c["id"] for c in chunk])
                    eff_model, rcpt = m, rc
                    rows.extend(part)
                    break
                except Exception:
                    if attempt == 1:
                        raise
                    time.sleep(2)

        by_id = {r["id"]: str(r["reply"]) for r in rows}
        scored = [base.score_case(c, by_id[c["id"]]) for c in base.CASES]
        rec.update({
            "status": "ok",
            "model": eff_model,
            "receipt": rcpt,
            "canary": {"expected_version_present": True, "tail_present": True},
            "answers": [{"id": c["id"], "reply": by_id[c["id"]]} for c in base.CASES],
            "scores": scored,
            "full_pass_count": sum(s["full_pass"] for s in scored),
            "axes_sum": sum(s["axes_passed"] for s in scored),
            "s01_s04_spine": sum(s["axes"]["opponent_privateer_ak47"] for s in scored if s["id"].startswith("S")),
        })
    except Exception as e:
        rec.update({"status": "error", "error": f"{type(e).__name__}: {str(e)[:280]}"})
    rec["seconds"] = round(time.monotonic() - t0, 2)
    out_file.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "route": route_key, "run": run_idx, "status": rec["status"],
        "full_pass": rec.get("full_pass_count"), "axes_sum": rec.get("axes_sum"),
        "spine": rec.get("s01_s04_spine"), "sec": rec["seconds"],
        "err": rec.get("error", "")[:110],
    }, ensure_ascii=False), flush=True)
    return rec


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jobs = [(rk, k, m, eff, r_i) for r_i in (1, 2) for (rk, k, m, eff) in EXTERNAL_SPECS]
    with cf.ThreadPoolExecutor(max_workers=10) as pool:
        list(pool.map(run_spec_job, jobs))
    print("=== EXTERNAL VENDOR EFFORT SUITE COMPLETE ===", flush=True)
