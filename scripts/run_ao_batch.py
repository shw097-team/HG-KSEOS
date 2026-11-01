#!/usr/bin/env python3
"""Dispatch the three VERIFY_SECURITY sittings for this round, one work package per brief.

One office per brief is not a style rule: two batches that carried two and three packages each hit the 1500 s wall
and produced no receipt, which downgraded their evidence grade below the single-package batches. Each brief below
therefore covers exactly one WP, and each dispatch carries its own nonce, its own receipt and its own arm pin.

The subject of every brief is committed (the briefs themselves are in git), so the durable gates have something to
hash; the receipts they produce are new files, which is what IR-4 is for.

Usage:
    python scripts/run_ao_batch.py [--only WP-FHS-11] [--timeout 600]
"""
from __future__ import annotations

try:
    import winproc as _winproc  # noqa: E402
    _winproc.install()
except Exception:
    pass

import argparse
import hashlib
import json
import pathlib
import secrets
import subprocess
import sys
import time

K = pathlib.Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
OPS = K / "ops" / "session-20261031" / "FHS-ALLPASS-20261031"
DISPATCH = K / "scripts" / "hgk-lane-dispatch.py"
ARM = "openai-codex/gpt-6.1-sol"

BRIEFS = {
    "WP-FHS-11": OPS / "WP-FHS-11" / "AO_BRIEF_WP11_HERMES.md",
    "WP-FHS-12": OPS / "WP-FHS-12" / "AO_BRIEF_WP12_RUNTIME.md",
    "WP-FHS-13": OPS / "WP-FHS-13" / "AO_BRIEF_WP13_HOTSWAP.md",
}

TRANSPORT = ["--codex-home", "C:/Users/user/.codex", "--allow-human-home-transport",
             "--relay-base", "https://chatgpt.com/backend-api/codex",
             "--identity-source", "codex-rollout"]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verdict_block(text: str) -> dict | None:
    """Last fenced ```json block that parses; a checker's verdict, not a guess at one."""
    blocks, cur, inside = [], [], False
    for line in text.splitlines():
        if line.strip().startswith("```json"):
            inside, cur = True, []
            continue
        if inside and line.strip().startswith("```"):
            inside = False
            blocks.append("\n".join(cur))
            continue
        if inside:
            cur.append(line)
    for b in reversed(blocks):
        try:
            return json.loads(b)
        except ValueError:
            continue
    return None


def run(wp: str, brief: pathlib.Path, timeout: int) -> dict:
    nonce = f"AO-{wp}-{secrets.token_hex(4).upper()}"
    # The nonce has to be in the prompt. The first batch was dispatched without it, so every receipt came back
    # ok=false with nonce_present=false even though the checker had done the work — a receipt defect I authored,
    # not a checker failure.
    staged = OPS / wp / f"AO_BRIEF_{nonce}.md"
    staged.write_text(brief.read_text(encoding="utf-8")
                      + f"\n\n---\n\nBefore you finish, echo this nonce verbatim on its own line: NONCE-ECHO: {nonce}\n",
                      encoding="utf-8")
    out = OPS / wp / f"AO_RECEIPT_{nonce}.json"
    cmd = [sys.executable, str(DISPATCH), "--lane", "VERIFY_SECURITY", "--require-arm", ARM,
           "--prompt", str(staged), "--nonce", nonce, "--timeout", str(timeout),
           "--json-out", str(out),
           "--require-durable-gates", "--durable-gates-subject", str(brief)] + TRANSPORT
    started = time.time()
    proc = subprocess.run(cmd, cwd=str(K), capture_output=True, text=True, errors="replace", encoding="utf-8")
    rec = {"wp": wp, "nonce": nonce, "brief": str(brief), "brief_sha256": sha(brief),
           "receipt": str(out), "seconds": round(time.time() - started, 2),
           "dispatch_exit": proc.returncode, "stderr_tail": (proc.stderr or "")[-400:]}
    d = {}
    if out.is_file():
        try:
            d = json.loads(out.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            d = {}
    att = (d.get("attempts") or [{}])[-1]
    rec.update({"ok": d.get("ok"), "code": d.get("code"), "served_arm": d.get("served_arm") or
                (f"{att.get('provider')}/{att.get('model')}" if att.get("model") else None),
                "rank": att.get("rank"), "exit": att.get("exit"),
                "usage_receipt_ok": d.get("usage_receipt_ok"), "nonce_present": att.get("nonce_present")})
    text = ""
    sp = att.get("stdout_path")
    if sp and pathlib.Path(sp).is_file():
        raw = pathlib.Path(sp).read_text(encoding="utf-8", errors="replace")
        said = []
        for line in raw.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                o = json.loads(line)
            except ValueError:
                continue
            it = o.get("item") or {}
            if it.get("type") == "agent_message":
                said.append(it.get("text") or "")
        text = "\n".join(said)
        (OPS / wp / f"AO_REPLY_{nonce}.md").write_text(text, encoding="utf-8", newline="")
    rec["verdict_block"] = verdict_block(text)
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    results = []
    for wp, brief in BRIEFS.items():
        if args.only and wp != args.only:
            continue
        if not brief.is_file():
            results.append({"wp": wp, "ok": False, "code": "BRIEF_MISSING", "brief": str(brief)})
            continue
        r = run(wp, brief, args.timeout)
        results.append(r)
        vb = r.get("verdict_block") or {}
        print(json.dumps({"wp": wp, "ok": r.get("ok"), "served": r.get("served_arm"), "rank": r.get("rank"),
                          "nonce_present": r.get("nonce_present"), "seconds": r.get("seconds"),
                          "checker_overall": vb.get("overall")}, ensure_ascii=False), flush=True)

    summary = {"schema": "HGK-AO-BATCH/2", "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "results": results}
    # One file per run, never a shared name: three overlapping batches all wrote AO_BATCH.json and the last one to
    # finish (a single-WP re-sit) replaced the file that held another WP's PASS sitting. The per-sitting replies and
    # receipts are immutable, and scripts/ao_verdict_index.py rebuilds the whole sequence from them.
    p = OPS / f"AO_BATCH_{time.strftime('%Y%m%dT%H%M%S')}.json"
    p.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"summary": str(p), "sittings": len(results)}, ensure_ascii=False))
    subprocess.run([sys.executable, str(K / "scripts" / "ao_verdict_index.py")], cwd=str(K),
                   capture_output=True, text=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
