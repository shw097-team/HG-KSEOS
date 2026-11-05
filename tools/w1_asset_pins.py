#!/usr/bin/env python3
"""WP-FHS-17 asset side — what the 24 W1 AssetSlots actually pin, install and fit.

`CAP-BOOT` is not only about the binaries a host happens to have. The W1 package names 24 asset
slots (§5.1 Native20 + §5.2 Default30); this tool reads the extracted decision registry and reports,
per asset and in total, exactly what the source states:

  * does the pin contain a concrete digest, or is it a HOLD/sentinel literal;
  * is anything recorded as installed / loaded / invoked;
  * is the Windows host fit resolved, or still `..._PENDING`.

Nothing is upgraded: a sentinel pin stays a sentinel, `PROPOSED_NOT_INSTALLED` stays that, and an
unresolved host fit is counted as unresolved rather than assumed to pass on Windows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

DIGEST = re.compile(r"\b[0-9a-f]{40}\b")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", required=True, help="assets_24.json extracted from the W1 package")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    src = json.loads(Path(args.assets).read_text(encoding="utf-8"))
    assets = src["assets"]

    rows = []
    for a in assets:
        pin = str(a.get("pin") or "")
        ladder = a.get("status_ladder") or {}
        fit = str(a.get("windows_fit") or "")
        rows.append({
            "asset_id": a.get("asset_id"),
            "asset_name": a.get("asset_name"),
            "need_key": a.get("need_key"),
            "selected_occupant": a.get("selected_occupant"),
            "pin": pin,
            "pin_has_concrete_digest": bool(DIGEST.search(pin)),
            "pin_state": "PINNED" if DIGEST.search(pin) else "HOLD_LITERAL",
            "license": a.get("license"),
            "status_ladder": ladder,
            "installed": ladder.get("installed", "NOT_RECORDED"),
            "loaded": ladder.get("loaded", "NOT_RECORDED"),
            "invoked": ladder.get("invoked", "NOT_RECORDED"),
            "overall_status": ladder.get("overall_status", "NOT_RECORDED"),
            "windows_fit": fit,
            "windows_fit_state": "RESOLVED" if fit and "PENDING" not in fit.upper() else "PENDING",
            "host_bound": a.get("host_bound"),
            "hotswap_candidate": a.get("hotswap_candidate"),
            "source_ref": a.get("source_ref"),
        })

    counts = {
        "assets": len(rows),
        "pinned_with_digest": sum(1 for r in rows if r["pin_has_concrete_digest"]),
        "hold_literal_pins": sum(1 for r in rows if not r["pin_has_concrete_digest"]),
        "installed_recorded": sum(1 for r in rows if r["installed"] not in ("NOT_OBSERVED", "NOT_RECORDED")),
        "loaded_recorded": sum(1 for r in rows if r["loaded"] not in ("NOT_OBSERVED", "NOT_RECORDED")),
        "windows_fit_resolved": sum(1 for r in rows if r["windows_fit_state"] == "RESOLVED"),
        "hotswap_candidates": sum(1 for r in rows if r["hotswap_candidate"]),
    }
    record = {
        "schema": "FHS.W1.WP17.AssetPins@1",
        "source": {"path": args.assets,
                   "sha256": hashlib.sha256(Path(args.assets).read_bytes()).hexdigest(),
                   "declared_count": src.get("count")},
        "counts": counts,
        "state": ("ASSETS_NOT_INSTALLED__PINS_MOSTLY_HELD"
                  if counts["installed_recorded"] == 0 else "ASSETS_PARTIALLY_OBSERVED"),
        "first_fail": "WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION",
        "resume_predicate": ("per asset: a concrete owner pin + a resolved Windows host-fit readback + "
                             "the installer's own installed/loaded receipt"),
        "assets": rows,
        "claim_ceiling": "AUTHOR_STATIC_ASSET_DECISIONS_ONLY",
        "not_claimed": ["installed", "loaded", "Windows fit", "hotswap executed"],
    }
    record["record_sha256"] = hashlib.sha256(
        json.dumps({k: v for k, v in record.items() if k != "record_sha256"},
                   sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(out), "counts": counts, "state": record["state"],
                      "sha256": record["record_sha256"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
