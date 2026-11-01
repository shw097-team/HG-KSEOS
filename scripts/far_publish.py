#!/usr/bin/env python3
"""Read and promote the publication state of a FAR research round.

``PUBLICATION.json`` is a promotion record, never proof by itself. Every status read re-runs the
evidence gate against typed lane summaries and their raw in-run dispatcher receipts. Promotion is
allowed only from a current ``LANES_SERVED`` result and the gate is rechecked immediately before the
typed publication record is written.

States: MISSING, EMPTY, CANDIDATE, LANES_SERVED, EVIDENCE_INVALID, PUBLISHED.
Exit: 0 ok, 1 refused, 2 run not found.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import time

K = pathlib.Path(__file__).resolve().parent.parent
RUNS = pathlib.Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\runs")
GATE = K / "scripts" / "far_lane_gate.py"
PUBLICATION_SCHEMA = "HGK-FAR-PUBLICATION/2"


def _safe_run_target(value: str) -> bool:
    return (
        value.startswith("FAR-")
        and pathlib.PurePath(value).name == value
        and all(char.isalnum() or char in "-_." for char in value)
    )


def gate_verdict(run_dir: pathlib.Path) -> dict:
    try:
        p = subprocess.run([sys.executable, str(GATE), str(run_dir), "--json"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=300)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"verdict": "GATE_UNREADABLE", "findings": [{"problem": str(exc)}]}
    try:
        value = json.loads(p.stdout)
    except (json.JSONDecodeError, TypeError):
        return {"verdict": "GATE_UNREADABLE",
                "findings": [{"problem": (p.stdout or p.stderr)[-400:]}]}
    if not isinstance(value, dict):
        return {"verdict": "GATE_UNREADABLE", "findings": [{"problem": "gate output is not an object"}]}
    return value


def _read_publication(path: pathlib.Path) -> tuple[dict | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{exc.__class__.__name__}: {exc}"
    if not isinstance(value, dict):
        return None, "JSON root is not an object"
    return value, None


def _publication_problem(run_id: str, publication: dict | None, gate: dict) -> str | None:
    if publication is None:
        return "PUBLICATION.json is absent"
    if publication.get("schema") != PUBLICATION_SCHEMA:
        return f"PUBLICATION.json schema mismatch: {publication.get('schema')!r}"
    if publication.get("run") != run_id:
        return f"PUBLICATION.json run mismatch: {publication.get('run')!r} != {run_id!r}"
    if publication.get("state") != "PUBLISHED":
        return f"PUBLICATION.json state is {publication.get('state')!r}"
    if gate.get("verdict") != "PUBLISHABLE":
        return "current evidence gate does not pass"
    if publication.get("gate_verdict_at_promotion") != "PUBLISHABLE":
        return "publication does not record a passing gate"
    if publication.get("question_sha256") != gate.get("question_sha256"):
        return "publication question digest is stale or foreign"
    if publication.get("receipts") != gate.get("receipts"):
        return "publication receipt evidence is stale or foreign"
    return None


def state_of(run_dir: pathlib.Path) -> dict:
    if not run_dir.is_dir():
        return {"run": run_dir.name, "state": "MISSING"}
    synth = (run_dir / "ResearchSynthesis.md").is_file()
    gate = gate_verdict(run_dir)
    publication_path = run_dir / "PUBLICATION.json"
    publication_exists = publication_path.is_file()
    publication = None
    publication_problem = None
    if publication_exists:
        publication, publication_problem = _read_publication(publication_path)

    gate_ok = gate.get("verdict") == "PUBLISHABLE"
    if publication_exists:
        publication_problem = publication_problem or _publication_problem(
            run_dir.name, publication, gate)
        if publication_problem:
            state = "EVIDENCE_INVALID"
        else:
            state = "PUBLISHED"
    elif gate_ok:
        state = "LANES_SERVED"
    elif synth:
        state = "CANDIDATE"
    else:
        state = "EMPTY"

    return {
        "run": run_dir.name,
        "state": state,
        "gate": gate.get("verdict"),
        "question_sha256": gate.get("question_sha256"),
        "receipts": gate.get("receipts") or {},
        "synthesis": synth,
        "publication": publication,
        "publication_problem": publication_problem,
        "findings": gate.get("findings") or [],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--status")
    group.add_argument("--list", action="store_true")
    group.add_argument("--promote")
    ap.add_argument("--by", default=None)
    ap.add_argument("--note", default="")
    args = ap.parse_args(argv)

    if args.list:
        rows = [state_of(p) for p in sorted(RUNS.iterdir())
                if p.is_dir() and p.name.startswith("FAR-")]
        for row in rows:
            print(f"{row['state']:16} {row['run'][:52]:54} gate={row.get('gate')} "
                  f"receipts={sorted((row.get('receipts') or {}).keys())}")
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["state"]] = counts.get(row["state"], 0) + 1
        print("\n" + "  ".join(f"{key}={value}" for key, value in sorted(counts.items())))
        return 0

    target = args.promote or args.status
    if not target:
        ap.error("give --status RUN, --list, or --promote RUN")
    if not _safe_run_target(target):
        ap.error("RUN must be one safe FAR directory name")
    run_dir = RUNS / target
    current = state_of(run_dir)
    if current["state"] == "MISSING":
        print(json.dumps(current, ensure_ascii=False, indent=1))
        return 2

    if not args.promote:
        print(json.dumps(current, ensure_ascii=False, indent=1))
        return 0

    if current["state"] != "LANES_SERVED":
        print(json.dumps({
            "ok": False,
            "code": "PROMOTION_REFUSED",
            "state": current["state"],
            "why": "only a current LANES_SERVED result may be promoted",
            "gate": current["gate"],
            "findings": current["findings"],
            "publication_problem": current["publication_problem"],
        }, ensure_ascii=False, indent=1))
        return 1
    if not args.by:
        print(json.dumps({
            "ok": False,
            "code": "PROMOTION_NEEDS_PROMOTER",
            "why": "a promotion records who made it; an anonymous promotion is not a decision",
        }, ensure_ascii=False, indent=1))
        return 1

    # Close the check-to-write race: re-run the complete gate immediately before promotion.
    recheck = gate_verdict(run_dir)
    if recheck.get("verdict") != "PUBLISHABLE":
        print(json.dumps({
            "ok": False,
            "code": "PROMOTION_REFUSED_EVIDENCE_CHANGED",
            "gate": recheck.get("verdict"),
            "findings": recheck.get("findings") or [],
        }, ensure_ascii=False, indent=1))
        return 1

    record = {
        "schema": PUBLICATION_SCHEMA,
        "run": target,
        "state": "PUBLISHED",
        "promoted_by": args.by,
        "note": args.note,
        "promoted_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "gate_verdict_at_promotion": recheck["verdict"],
        "question_sha256": recheck["question_sha256"],
        "receipts": recheck["receipts"],
    }
    encoded = json.dumps(record, ensure_ascii=False, indent=1)
    (run_dir / "PUBLICATION.json").write_text(encoded, encoding="utf-8", newline="")
    # Critical state is read back, not assumed from a successful write call.
    readback = (run_dir / "PUBLICATION.json").read_text(encoding="utf-8")
    if hashlib.sha256(readback.encode("utf-8")).digest() != hashlib.sha256(encoded.encode("utf-8")).digest():
        print(json.dumps({"ok": False, "code": "PUBLICATION_READBACK_MISMATCH"}, indent=1))
        return 1
    print(json.dumps({"ok": True, "state": "PUBLISHED", "run": target}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
