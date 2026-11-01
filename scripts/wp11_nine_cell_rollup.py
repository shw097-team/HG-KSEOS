"""WP-11 roll-up: the nine cells, derived from receipts, and fail-closed about what it cannot see.

Rewrite history first, because it explains the shape of this file. Version 3 of the table was hand-edited
twice: one cell went FAIL on a single model answer that omitted a line, then back to PASS on a second sample.
Version 4 was derived, but it still *copied* the six Codex/Claude rows out of the previous table and counted
them as PASS without opening their receipts. The independent checker convicted exactly that: with the prior
receipts made unavailable the roll-up still reported 9 PASS, so its "9/9" was arithmetic over a memory rather
than over evidence.

This version has three states per cell and no fourth:

  MEASURED_THIS_ROUND  a receipt written in this round, with its own measured fields (the three Hermes cells)
  CARRIED_PRIOR_ROUND  a row from the previous round, counted ONLY when the receipt files it names are present,
                       readable and still PASS — and reported separately from the measured ones
  UNMEASURED           no receipt: the cell is not a pass, and the script exits non-zero

The totals are then printed as three numbers, never as one. A caller that wants a single "9/9" has to say which
nine it means.

Usage:
    python scripts/wp11_nine_cell_rollup.py [--wp11 DIR] [--out FILE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_WP11 = REPO / "ops" / "session-20261031" / "FHS-ALLPASS-20261031" / "WP-FHS-11"
PROFILES = ["LITE", "STANDARD", "ASSURED"]
PRIOR_RECEIPTS = {
    "codex": ["CODEX_CELL_RECEIPT.json", "clean_codex_cell.json", "clean_cell_runs.json"],
    "claude": ["CLAUDE_CELL_RECEIPT.json", "clean_cell_runs.json"],
}


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: pathlib.Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wp11", default=str(DEFAULT_WP11))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    wp11 = pathlib.Path(args.wp11)
    out = pathlib.Path(args.out) if args.out else wp11 / "NINE_CELL_TABLE.json"

    prior_table = load(out) or {}
    prior_cells = {(c.get("host"), c.get("sp")): c for c in prior_table.get("cells", [])}

    cells, sources, missing = [], [], []

    # --- carried rows: counted only when their receipts are on disk and still say PASS ---
    for host in ("codex", "claude"):
        files = [wp11 / f for f in PRIOR_RECEIPTS[host]]
        present = [f for f in files if f.is_file()]
        receipts_ok = bool(present)
        evidence = []
        for f in present:
            d = load(f) or {}
            # A prior receipt is only usable if it exists, parses, and does not itself say it failed.
            ok = bool(d) and str(d.get("verdict", "PASS")).upper() != "FAIL"
            evidence.append({"file": f.name, "sha256": sha(f), "parsed": bool(d), "self_failed": not ok})
        receipts_ok = receipts_ok and all(e["parsed"] and not e["self_failed"] for e in evidence)
        for sp in PROFILES:
            old = prior_cells.get((host, sp))
            if old and old.get("verdict") == "PASS" and receipts_ok:
                cells.append({**old, "evidence_state": "CARRIED_PRIOR_ROUND",
                              "evidence": [e["file"] for e in evidence]})
                sources.extend(str(f) for f in present)
            else:
                reason = ("no PASS row for this cell in the previous table" if not old
                          else f"prior receipts missing or unreadable: {[f.name for f in files]}")
                cells.append({"host": host, "sp": sp, "verdict": "UNMEASURED", "evidence_state": "UNMEASURED",
                              "why": reason})
                missing.append(f"{host}/{sp}: {reason}")

    # --- measured rows: this round's Hermes receipts ---
    for sp in PROFILES:
        f = wp11 / "hermes-cells" / f"HERMES_CELL_{sp}.json"
        r = load(f)
        if not r:
            cells.append({"host": "hermes", "sp": sp, "verdict": "UNMEASURED", "evidence_state": "UNMEASURED",
                          "why": f"no receipt at {f}"})
            missing.append(f"hermes/{sp}: no receipt at {f}")
            continue
        served = r.get("served", {})
        cells.append({
            "host": "hermes",
            "sp": sp,
            "verdict": r.get("verdict"),
            "digest": r.get("digest"),
            "badge": r.get("badge"),
            "negative_clean": r.get("negative", {}).get("token_present_after_uninstall") is False,
            "archive_prefix": (r.get("archive_sha256") or "")[:12],
            "served": served.get("model"),
            "served_completed": served.get("completed"),
            "served_api_calls": served.get("api_calls"),
            "evidence_state": "MEASURED_THIS_ROUND",
            "receipt": f.name,
            "receipt_sha256": sha(f),
        })
        sources.append(str(f))

    order = {"codex": 0, "claude": 1, "hermes": 2}
    cells.sort(key=lambda c: (order.get(c["host"], 9),
                              PROFILES.index(c["sp"]) if c.get("sp") in PROFILES else 9))

    measured = [c for c in cells if c.get("evidence_state") == "MEASURED_THIS_ROUND"]
    carried = [c for c in cells if c.get("evidence_state") == "CARRIED_PRIOR_ROUND"]
    unmeasured = [c for c in cells if c.get("evidence_state") == "UNMEASURED"]

    table = {
        "schema": "HGK-WP11-NINE-CELLS/5",
        "denominator": len(cells),
        "counts": {
            "measured_this_round": len(measured),
            "measured_pass": sum(1 for c in measured if c.get("verdict") == "PASS"),
            "carried_prior_round": len(carried),
            "carried_pass": sum(1 for c in carried if c.get("verdict") == "PASS"),
            "unmeasured": len(unmeasured),
        },
        "headline": (f"{len(measured)} cells measured in this round "
                     f"({sum(1 for c in measured if c.get('verdict') == 'PASS')} PASS); "
                     f"{len(carried)} carried from the prior round with their receipts present; "
                     f"{len(unmeasured)} unmeasured"),
        "derived_from": sorted(set(sources)),
        "rule": ("MEASURED_THIS_ROUND comes from a receipt written now; CARRIED_PRIOR_ROUND is counted only when "
                 "the prior receipts are present and still PASS, and is reported apart from the measured cells; "
                 "anything else is UNMEASURED and the script exits non-zero"),
        "note": ("Hermes cells: the loader half is the skill index entry (the body is fetched on demand by the "
                 "host's own skill_view), so the model half is measured as 'load the body with the host loader "
                 "and report the two facts', with the same skill removed for the negative."),
        "cells": cells,
    }
    out.write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"out": str(out), "sha256": sha(out), **table["counts"], "headline": table["headline"],
                      "missing": missing}, ensure_ascii=False))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
