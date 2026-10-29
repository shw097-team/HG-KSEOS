#!/usr/bin/env python3
"""A3 / TT-R20-10: record the drift between the assignment snapshot a delivery pins and the live host.

Measured during R20: the branch pinned `config/model-lane-assignment.json` rev 35 (registry_epoch 34) while
the host had already moved to rev 36 (epoch 36) -- PLAN and VERIFY_SECURITY `transport_model` changed from
`opencode-go/deepseek-v4.1-flash` to `gpt-6.1-sol`. The receipts of lane passes 3-5 quote rev 36; the
committed file is rev 35. Re-baselining the evidence onto rev 36 would be a lie: the earlier phases never
ran against it. So the drift is EMITTED as data, with a stated rule for what it does and does not affect.

Usage:
    python tools/config_drift.py --repo <path/to/branch assignment.json> --host <path/to/host assignment.json>
Exit: 0 = recorded (drift or none), 4 = a file could not be read.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Fields whose change alters WHICH MODEL a lane actually reaches. A change here can invalidate a claim
# about lane identity; a change to a decorative field cannot.
IDENTITY_FIELDS = ("assigned_provider", "assigned_model")


def rows(data: dict) -> dict:
    out = {}
    for row in data.get("assignment") or []:
        label = str(row.get("role") or row.get("lane_group") or "").upper()
        if label:
            out[label] = row
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    try:
        repo = json.loads(Path(a.repo).read_text(encoding="utf-8"))
        host = json.loads(Path(a.host).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"unreadable assignment file: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4

    r, h = rows(repo), rows(host)
    fields, lanes = [], []
    for role in sorted(set(r) | set(h)):
        rr, hh = r.get(role, {}), h.get(role, {})
        for key in sorted(set(rr) | set(hh)):
            if key in ("authority",):
                continue
            if rr.get(key) != hh.get(key):
                fields.append({"role": role, "field": key, "repo": rr.get(key), "host": hh.get(key)})
                if key in IDENTITY_FIELDS:
                    lanes.append(role)
    identity_changed = bool(lanes)
    doc = {
        "schema": "R20.CONFIG_DRIFT/1",
        "repo": {"path": str(a.repo), "revision": repo.get("revision"),
                 "registry_epoch": repo.get("registry_epoch")},
        "host": {"path": str(a.host), "revision": host.get("revision"),
                 "registry_epoch": host.get("registry_epoch")},
        "same": not fields,
        "field_count": len(fields),
        "fields": fields,
        "lanes_with_identity_change": sorted(set(lanes)),
        # The rule, stated once so a reader does not have to re-derive it: a transport_model change that
        # leaves assigned_model alone does NOT invalidate a receipt whose lane gate compared assigned_model
        # (the R20 gates do exactly that). An assigned_model change DOES: the lane could not have served it.
        "affects_issued_evidence": identity_changed,
        "rule": ("transport-only drift leaves assigned_model unchanged, so a receipt that gated on "
                 "assigned_model still describes the lane it was issued for; an assigned_model change "
                 "does invalidate such receipts and they must be re-issued, not re-baselined"),
        "note": "the branch pins the repo snapshot; this file records the drift, it never rewrites evidence",
    }
    text = json.dumps(doc, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(text + "\n", encoding="utf-8", newline="\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
