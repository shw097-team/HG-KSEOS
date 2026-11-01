#!/usr/bin/env python3
"""The publication state machine: a synthesis exists, a study does not.

Three states, and only one of them may be cited:

    CANDIDATE      ResearchSynthesis.md exists. Nothing else. Anyone can produce this by writing a file.
    LANES_SERVED   PLAN, EXECUTE and VERIFY_SECURITY each left a receipt that passes far_lane_gate.py.
    PUBLISHED      LANES_SERVED plus an explicit promotion, recorded with who promoted and when.

Why a state and not a flag. Twenty FAR runs existed and every one of them read as a finished study, because the only
thing that distinguished a routed study from a hand-written one was invisible: one had receipts on disk and the other
did not. A state machine makes the difference the artefact itself, so "is this published" stops being a question about
provenance and becomes a field.

Usage:
    python scripts/far_publish.py --status <run>        # what state is it in, and why
    python scripts/far_publish.py --promote <run> --by "<owner id>" --note "..."
    python scripts/far_publish.py --list                # every run and its state

Promotion never invents a receipt. If the gate refuses, promotion refuses with the gate's own reasons.
Exit: 0 ok, 1 refused, 2 run not found.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

K = pathlib.Path(__file__).resolve().parent.parent
RUNS = pathlib.Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\runs")
GATE = K / "scripts" / "far_lane_gate.py"


def gate_verdict(run_dir: pathlib.Path) -> dict:
    p = subprocess.run([sys.executable, str(GATE), str(run_dir)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"verdict": "GATE_UNREADABLE", "raw": (p.stdout or p.stderr)[-400:]}


def state_of(run_dir: pathlib.Path) -> dict:
    if not run_dir.is_dir():
        return {"run": run_dir.name, "state": "MISSING"}
    synth = (run_dir / "ResearchSynthesis.md").exists()
    g = gate_verdict(run_dir)
    publish = run_dir / "PUBLICATION.json"
    published = None
    if publish.exists():
        try:
            published = json.loads(publish.read_text(encoding="utf-8"))
        except Exception:
            published = {"error": "unreadable"}
    if published and published.get("state") == "PUBLISHED":
        state = "PUBLISHED"
    elif g.get("verdict") == "PUBLISHABLE":
        state = "LANES_SERVED"
    elif synth:
        state = "CANDIDATE"
    else:
        state = "EMPTY"
    return {"run": run_dir.name, "state": state, "gate": g.get("verdict"),
            "receipts": sorted((g.get("receipts") or {}).keys()),
            "synthesis": synth, "publication": published}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--status")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--promote")
    ap.add_argument("--by", default=None)
    ap.add_argument("--note", default="")
    args = ap.parse_args(argv)

    if args.list:
        rows = [state_of(p) for p in sorted(RUNS.iterdir()) if p.is_dir() and p.name.startswith("FAR-")]
        for r in rows:
            print(f"{r['state']:12} {r['run'][:52]:54} gate={r.get('gate')} receipts={r.get('receipts')}")
        counts: dict[str, int] = {}
        for r in rows:
            counts[r["state"]] = counts.get(r["state"], 0) + 1
        print("\n" + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        return 0

    target = args.promote or args.status
    if not target:
        ap.error("give --status RUN, --list, or --promote RUN")
    run_dir = RUNS / target
    s = state_of(run_dir)
    if s["state"] == "MISSING":
        print(json.dumps(s, ensure_ascii=False, indent=1))
        return 2

    if not args.promote:
        print(json.dumps(s, ensure_ascii=False, indent=1))
        return 0

    # promotion is a state transition, not an assertion: it cannot create the receipts it requires
    if s["state"] != "LANES_SERVED":
        print(json.dumps({"ok": False, "code": "PROMOTION_REFUSED", "state": s["state"],
                          "why": "only LANES_SERVED may be promoted; the gate has not passed for this run",
                          "gate": s["gate"], "receipts": s["receipts"]}, ensure_ascii=False, indent=1))
        return 1
    if not args.by:
        print(json.dumps({"ok": False, "code": "PROMOTION_NEEDS_PROMOTER",
                          "why": "a promotion records who made it; an anonymous promotion is not a decision"},
                         ensure_ascii=False, indent=1))
        return 1
    rec = {"schema": "HGK-FAR-PUBLICATION/1", "run": target, "state": "PUBLISHED",
           "promoted_by": args.by, "note": args.note,
           "promoted_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "gate_verdict_at_promotion": s["gate"], "receipts": s["receipts"]}
    (run_dir / "PUBLICATION.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1),
                                              encoding="utf-8", newline="")
    print(json.dumps({"ok": True, "state": "PUBLISHED", "run": target}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
