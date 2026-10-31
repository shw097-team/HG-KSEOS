#!/usr/bin/env python3
"""far_lane_gate — a FAR research run is not a research run until the lanes produced it.

Why this exists
---------------
Measured 2026-10-31: eight FAR run directories from one session, `C:\\wg\\queue` holding 18 EXECUTE receipts and only
**two** PLAN receipts all week, and no FAR run carrying a PLAN or VERIFY receipt at all. Every report had been written
by the interactive session, whose pinned arm is `opencode-go/deepseek-v4.1-flash` — the EXECUTE arm. So the mandate's
"PLAN: gpt-6.1-sol, VERIFY: gpt-6.1-sol" was satisfied on paper only, and nothing noticed, because a research report
has no required provenance: any file in `runs/<name>/` reads as a finished study.

The obligation therefore has to live in the artefact's own admission rule, not in the operator's memory:

    a FAR run is VALID_RESEARCH only if it carries
      PLAN_RECEIPT.json    --lane PLAN, served openai-codex/gpt-6.1-sol, nonce echoed
      VERIFY_RECEIPT.json  --lane VERIFY_SECURITY, served openai-codex/gpt-6.1-sol, nonce echoed
    both passing scripts/lane_evidence_gate.py, and a synthesis that cites them.

Usage:
    python scripts/far_lane_gate.py <run-dir> [--json]
Exit 0 = VALID_RESEARCH; 3 = INVALID_RESEARCH (prints which receipt is missing or why it does not pass).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:  # every child of this process must be consoleless
    import winproc as _winproc  # noqa: E402

    _winproc.install()
except Exception:
    pass

K = Path(__file__).resolve().parent.parent
GATE = K / "scripts" / "lane_evidence_gate.py"
CASES = {
    "PLAN": ("PLAN_RECEIPT.json", "openai-codex/gpt-6.1-sol"),
    "VERIFY_SECURITY": ("VERIFY_RECEIPT.json", "openai-codex/gpt-6.1-sol"),
}


def _gate(receipt: Path, lane: str) -> dict:
    r = subprocess.run([sys.executable, str(GATE), str(receipt), "--lane", lane],
                       capture_output=True, text=True, timeout=300, creationflags=0x08000000)
    out = (r.stdout or "").strip()
    try:
        parsed = json.loads(out.splitlines()[-1]) if out else {}
    except json.JSONDecodeError:
        parsed = {"raw": out[-400:]}
    return {"exit": r.returncode, "gate": parsed}


def check(run: Path) -> dict:
    findings, receipts = [], {}
    for lane, (fname, expect_model) in CASES.items():
        p = run / fname
        if not p.exists():
            findings.append({"lane": lane, "problem": f"{fname} ABSENT — the lane never produced this run"})
            continue
        receipts[lane] = str(p)
        try:
            d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError as exc:
            findings.append({"lane": lane, "problem": f"{fname} unreadable: {exc}"})
            continue
        # asked == served, on the pinned arm, and the child echoed the nonce
        attempts = d.get("attempts") if isinstance(d.get("attempts"), list) else []
        served = None
        nonce_seen = False
        for a in attempts:
            if isinstance(a, dict):
                served = served or a.get("model") or a.get("served_model")
                nonce_seen = nonce_seen or bool(a.get("nonce_present"))
        served = served or d.get("served_model") or d.get("model")
        if served and expect_model.split("/")[-1] not in str(served):
            findings.append({"lane": lane, "problem": f"served {served!r}, expected {expect_model!r}"})
        if not nonce_seen:
            findings.append({"lane": lane, "problem": "no attempt echoes the run nonce (nonce_present false)"})
        g = _gate(p, lane)
        if g["exit"] != 0:
            findings.append({"lane": lane, "problem": "lane_evidence_gate refused", "gate": g["gate"]})

    synthesis = [p for p in run.glob("*.md") if p.name.lower() not in ("plan_brief.md", "questions.md")]
    cites = []
    for s in synthesis:
        body = s.read_text(encoding="utf-8", errors="replace")
        cites.append({"file": s.name, "cites_plan": "PLAN_RECEIPT.json" in body,
                      "cites_verify": "VERIFY_RECEIPT.json" in body})
    if not synthesis:
        findings.append({"problem": "no synthesis file present"})
    for c in cites:
        if not (c["cites_plan"] and c["cites_verify"]):
            findings.append({"file": c["file"],
                             "problem": "synthesis does not cite both lane receipts (a report that cannot name its "
                                        "lanes is a session note)"})
    return {"run": run.name, "verdict": "VALID_RESEARCH" if not findings else "INVALID_RESEARCH",
            "receipts": receipts, "synthesis": cites, "findings": findings}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    run = Path(args.run_dir)
    if not run.is_dir():
        print(json.dumps({"verdict": "INVALID_RESEARCH", "problem": f"{run} is not a directory"}))
        return 3
    res = check(run)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["verdict"] == "VALID_RESEARCH" else 3


if __name__ == "__main__":
    sys.exit(main())
