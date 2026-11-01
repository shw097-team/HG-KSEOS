"""Evidence index: every artefact this round rests on, with its digest and the verdict it carries.

A report that cites files by path is a reading list. This index gives each citation a digest, so a reader can prove
the file they open is the file that was measured — and so that "the receipt says PASS" can be checked rather than
believed.

Usage:
    python scripts/evidence_index.py --json ops/session-20261031/FHS-ALLPASS-20261031/EVIDENCE_INDEX.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
SESSION = REPO / "ops" / "session-20261031" / "FHS-ALLPASS-20261031"
VAR = pathlib.Path(r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031")
FAR = pathlib.Path(r"C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs")

ITEMS = [
    # (wp, kind, path, what it decides)
    ("WP-FHS-11", "table", SESSION / "WP-FHS-11" / "NINE_CELL_TABLE.json", "nine cells, three states, fail-closed"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "hermes-cells" / "HERMES_CELL_LITE.json", "Hermes LITE, model half"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "hermes-cells" / "HERMES_CELL_STANDARD.json", "Hermes STANDARD"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "hermes-cells" / "HERMES_CELL_ASSURED.json", "Hermes ASSURED"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "host-cells" / "CODEX_CELL_LITE.json", "Codex LITE, current manifest"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "host-cells" / "CODEX_CELL_STANDARD.json", "Codex STANDARD"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "host-cells" / "CODEX_CELL_ASSURED.json", "Codex ASSURED"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "host-cells" / "CLAUDE_CODE_CELL_LITE.json", "Claude Code LITE"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "host-cells" / "CLAUDE_CODE_CELL_STANDARD.json", "Claude Code STANDARD"),
    ("WP-FHS-11", "receipt", SESSION / "WP-FHS-11" / "host-cells" / "CLAUDE_CODE_CELL_ASSURED.json", "Claude Code ASSURED"),
    ("WP-FHS-12", "receipt", SESSION / "WP-FHS-12" / "RUNTIME_PATH_LAB.json", "three arms: product runtime, PATH shim, recovery entry"),
    ("WP-FHS-12", "receipt", SESSION / "WP-FHS-12" / "MAXPATH_CONTROLLED_REPRO.json", "identical bytes, 259 vs 260 characters"),
    ("WP-FHS-13", "oracle", VAR / "wp13" / "ORACLE_WP13.json", "the five clauses, registered before the check"),
    ("WP-FHS-13", "receipt", VAR / "wp13" / "HOTSWAP_ABI_RECEIPT.json", "the historical ABI swap (C5 not covered)"),
    ("WP-FHS-13", "receipt", VAR / "wp13" / "HOTSWAP_GRANT_BOUND_RECEIPT.json", "swap bound to a covering grant, ten checks"),
    ("WP-FHS-13", "receipt", VAR / "wp13" / "HOTSWAP_REFUSED_NONCOVERING_GRANT.json", "refusal: the old grant covers nothing here"),
    ("WP-FHS-20", "table", SESSION / "WP-FHS-20" / "SURFACE_INVENTORY.json", "192 cells, named reasons, no anonymous bucket"),
    ("E2E", "receipt", SESSION / "E2E_W18_E33_E42.json", "six cases measured, four refused by name"),
    ("O-1", "table", SESSION / "O1_MAIN_ONLY_CLASSIFICATION.json", "516 main-only files, content-first"),
    ("report", "document", SESSION / "FINAL_ENGINEERING_REPORT.md", "this round, with its refusals"),
    ("report", "document", SESSION / "RESUME_CHECKPOINT.md", "the opening instruction and the traps"),
    ("FAR", "run", FAR / "FAR-20261031-054-RUNTIME-IDENTITY-AND-MAXPATH" / "PLAN_RECEIPT.json", "PLAN lane, first attempt"),
    ("FAR", "run", FAR / "FAR-20261031-056-RUNTIME-DECISION" / "lane_output" / "WORKPACKAGE.md", "the decision document"),
]

VERDICT_PATHS = [("verdict",), ("state",), ("checks",), ("overall",), ("swap_exit",)]


def sha(p: pathlib.Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def peek(p: pathlib.Path) -> dict:
    """The fields a reader would check first, without pretending to summarise the file."""
    if p.suffix != ".json":
        return {"bytes": p.stat().st_size if p.exists() else None}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out = {}
    for key in ("verdict", "state", "overall", "denominator", "counts", "headline", "ok", "code"):
        if key in d:
            out[key] = d[key]
    if "checks" in d and isinstance(d["checks"], dict):
        out["checks_true"] = sum(1 for v in d["checks"].values() if v is True)
        out["checks_total"] = len(d["checks"])
    if "cells" in d and isinstance(d["cells"], list):
        out["cells"] = len(d["cells"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(SESSION / "EVIDENCE_INDEX.json"))
    args = ap.parse_args()

    rows, missing = [], []
    for wp, kind, path, what in ITEMS:
        if not path.exists():
            missing.append({"wp": wp, "path": str(path), "why": "absent"})
            continue
        rows.append({"wp": wp, "kind": kind, "path": str(path), "bytes": path.stat().st_size,
                     "sha256": sha(path), "what_it_decides": what, **peek(path)})

    doc = {"schema": "HGK-EVIDENCE-INDEX/1", "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "repo": str(REPO), "items": rows, "missing": missing,
           "rule": ("every claim in FINAL_ENGINEERING_REPORT.md names one of these rows; a row without its file is "
                    "listed under `missing` and the claim it supports is not made")}
    out = pathlib.Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"json": str(out), "items": len(rows), "missing": len(missing),
                      "missing_list": [m["path"] for m in missing]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
