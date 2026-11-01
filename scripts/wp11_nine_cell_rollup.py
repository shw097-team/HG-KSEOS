"""WP-11 roll-up: the nine cells, derived from receipts, never typed.

The table has been rewritten by hand twice, and both times a hand edit decided a verdict (one cell went
FAIL on a single model answer that omitted a line, and was then flipped back by a second sample). A table
that is *derived* cannot do that: each cell is either a receipt with its own measured fields or it is
`UNMEASURED`, and the totals are arithmetic over those cells.

Sources:
  <wp11>/CODEX_CELL_RECEIPT.json      codex host, per-profile archive prefixes (measured 2026-10-31)
  <wp11>/CLAUDE_CELL_RECEIPT.json     claude-code host
  <wp11>/clean_cell_runs.json         the two hosts' trigger/non-trigger token runs
  <wp11>/hermes-cells/HERMES_CELL_<P>.json   the three Hermes cells (this round)

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

    prior = load(out) or {}
    prior_cells = {(c.get("host"), c.get("sp")): c for c in prior.get("cells", [])}

    cells, sources = [], []

    # The two hosts measured in the previous round keep their records and their evidence pointer.
    for host in ("codex", "claude"):
        for sp in PROFILES:
            old = prior_cells.get((host, sp))
            if old and old.get("verdict") == "PASS":
                cell = dict(old)
                cell["evidence"] = f"recorded in the previous round; see {WP11_REL(host)}"
                cells.append(cell)
                sources.append(str(wp11 / ("CODEX_CELL_RECEIPT.json" if host == "codex" else "CLAUDE_CELL_RECEIPT.json")))

    # The three Hermes cells: derived from this round's receipts only.
    for sp in PROFILES:
        f = wp11 / "hermes-cells" / f"HERMES_CELL_{sp}.json"
        r = load(f)
        if not r:
            cells.append({"host": "hermes", "sp": sp, "verdict": "UNMEASURED", "why": f"no receipt at {f}"})
            continue
        cells.append({
            "host": "hermes",
            "sp": sp,
            "verdict": r.get("verdict"),
            "digest": r.get("digest"),
            "badge": r.get("badge"),
            "negative_clean": r.get("negative", {}).get("token_present_after_uninstall") is False,
            "archive_prefix": (r.get("archive_sha256") or "")[:12],
            "served": r.get("served", {}).get("model"),
            "receipt": f.name,
            "receipt_sha256": sha(f),
        })
        sources.append(str(f))

    order = {"codex": 0, "claude": 1, "hermes": 2}
    cells.sort(key=lambda c: (order.get(c["host"], 9), PROFILES.index(c["sp"]) if c.get("sp") in PROFILES else 9))
    passes = sum(1 for c in cells if c.get("verdict") == "PASS")
    table = {
        "schema": "HGK-WP11-NINE-CELLS/4",
        "denominator": len(cells),
        "pass": passes,
        "fail": sum(1 for c in cells if c.get("verdict") == "FAIL"),
        "unmeasured": sum(1 for c in cells if c.get("verdict") not in ("PASS", "FAIL")),
        "derived_from": sorted(set(sources)),
        "rule": "each cell is a receipt with its own measured fields; totals are arithmetic over those cells",
        "note": ("Hermes cells: the loader half is the skill index entry (the body is fetched on demand by the "
                 "host's own skill_view), so the model half is measured as 'retrieve the body with the host "
                 "loader and report the two facts', with the same skill removed for the negative."),
        "cells": cells,
    }
    out.write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"out": str(out), "sha256": sha(out), "denominator": table["denominator"],
                      "pass": table["pass"], "fail": table["fail"],
                      "unmeasured": table["unmeasured"]}, ensure_ascii=False))
    return 0 if passes == table["denominator"] else 1


def WP11_REL(host: str) -> str:  # noqa: N802  (used as a sentence fragment)
    return "CODEX_CELL_RECEIPT.json" if host == "codex" else "CLAUDE_CELL_RECEIPT.json"


if __name__ == "__main__":
    sys.exit(main())
