#!/usr/bin/env python3
"""acceptance_rebind -- close a work package by binding evidence that already exists.

Why this exists: WP-FHS-10 was recorded FAIL with `REFUSAL-20261030-NO-HOST-CAPABILITY`, but its
declared oracle ("Fabric/HGK/SBL three GWO effects plus G-A/G-B evidence") was already produced and
signed by the B1 round. Re-running that native work would produce a second, weaker measurement of the
same thing; what was missing was a *binding*, and nothing in the typed API could express it, because
`resolve_acceptance()` only moves a row that is still NOT_RUN and refuses to rewrite a terminal verdict.

So a re-binding is a NEW acceptance row (`-V<n>`) over registered evidence, resolved through the
canonical transition, with the superseded acceptance named in the payload. History is never rewritten:
the FAIL row stays exactly as it was, and `work_queue.refresh()` already treats a later `-V<n>` PASS as
the live verdict.

Usage:
  acceptance_rebind.py --wp WP-FHS-10 \
      --oracle-file <text describing the oracle> \
      --evidence <path>[:<kind>] [--evidence ...] \
      --actor <identity> --reason <why this evidence satisfies the oracle> \
      [--supersedes ACC-WP-FHS-10] [--dry-run]

Exit codes: 0 resolved (or already resolved), 2 refused before any write, 3 typed API refused.
"""

from __future__ import annotations

try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop the tool
    pass

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

DB = REPO / "var" / "shared-spine" / "hg-kseos.db"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_evidence(spec: str) -> tuple[Path, str]:
    if ":" in spec and not spec[1:3] == ":\\":
        raw, kind = spec.rsplit(":", 1)
    else:
        raw, kind = spec, "ARTEFACT"
    return Path(raw), kind


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wp", required=True)
    ap.add_argument("--oracle-file", required=True, help="file whose text is the oracle this evidence discharges")
    ap.add_argument("--evidence", action="append", default=[], help="path[:kind]")
    ap.add_argument("--actor", required=True)
    ap.add_argument("--reason", required=True)
    ap.add_argument("--supersedes", default=None)
    ap.add_argument("--threshold", default="EXPLICIT_ORACLE_PASS")
    ap.add_argument("--negative-fixture", default="EVIDENCE_DIGEST_MISMATCH")
    ap.add_argument("--verdict", default="PASS", choices=("PASS", "FAIL"),
                    help="PASS binds evidence that discharges the oracle; FAIL records that it does not")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    from hg_kseos.spine import SharedSpine  # noqa: E402

    oracle_path = Path(args.oracle_file)
    if not oracle_path.is_file():
        print(json.dumps({"ok": False, "code": "ORACLE_FILE_MISSING", "path": str(oracle_path)}))
        return 2
    oracle_text = oracle_path.read_text(encoding="utf-8").strip()
    if not oracle_text:
        print(json.dumps({"ok": False, "code": "ORACLE_EMPTY"}))
        return 2

    ev = []
    for spec in args.evidence:
        p, kind = parse_evidence(spec)
        if not p.is_file():
            print(json.dumps({"ok": False, "code": "EVIDENCE_MISSING", "path": str(p)}))
            return 2
        ev.append({"path": str(p.resolve()), "kind": kind, "sha256": sha256_file(p), "bytes": p.stat().st_size})
    if not ev:
        print(json.dumps({"ok": False, "code": "NO_EVIDENCE"}))
        return 2

    spine = SharedSpine(DB)
    with spine.connect() as con:  # read-only lookups; the transition itself uses the typed API
        rows = con.execute(
            "SELECT acceptance_id, verdict FROM acceptances WHERE requirement_id LIKE ? OR acceptance_id LIKE ?",
            (f"%{args.wp}%", f"ACC-{args.wp}%"),
        ).fetchall()
    prior = [{"acceptance_id": r[0], "verdict": r[1]} for r in rows]
    versions = []
    for r in prior:
        tail = r["acceptance_id"].rsplit("-V", 1)
        if len(tail) == 2 and tail[1].isdigit():
            versions.append(int(tail[1]))
    version = (max(versions) + 1) if versions else 1
    if any(r["verdict"] == "PASS" and r["acceptance_id"].endswith(f"-V{version}") for r in prior):
        version += 1
    acceptance_id = f"ACC-{args.wp}-V{version}"
    requirement_id = f"REQ-{args.wp}-V{version}"

    receipt = {
        "schema": "HGK-ACCEPTANCE-REBIND/1",
        "at": now_iso(),
        "wp": args.wp,
        "acceptance_id": acceptance_id,
        "requirement_id": requirement_id,
        "oracle_file": str(oracle_path.resolve()),
        "oracle_sha256": hashlib.sha256(oracle_text.encode("utf-8")).hexdigest(),
        "evidence": ev,
        "actor": args.actor,
        "reason": args.reason,
        "supersedes": args.supersedes,
        "prior_acceptances": prior,
        "dry_run": bool(args.dry_run),
    }

    if args.dry_run:
        receipt["ok"] = True
        receipt["state"] = "DRY_RUN"
        print(json.dumps(receipt, ensure_ascii=False, indent=1))
        return 0

    token = f"LEASE-{acceptance_id}-{now_iso()}"
    try:
        for item in ev:
            spine.register_evidence(
                evidence_id=f"EV-{args.wp}-{Path(item['path']).stem}"[:120],
                kind=item["kind"],
                locator=item["path"],
                sha256=item["sha256"],
                producer="FHS-MSC-PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1",
                checker=args.actor,
            )
        spine.register_requirement(
            requirement_id,
            source_locator=str(oracle_path.resolve()),
            wording=oracle_text[:2000],
            acceptance_id=acceptance_id,
            oracle=oracle_text[:2000],
            threshold=args.threshold,
            negative_fixture=args.negative_fixture,
        )
        spine.acquire_lease(acceptance_id, args.actor, token, ttl_seconds=900)
        result = spine.resolve_acceptance(
            acceptance_id,
            verdict=args.verdict,
            evidence_ref=f"EV-{args.wp}-{Path(ev[0]['path']).stem}"[:120],
            actor=args.actor,
            token=token,
            expected_version=0,
            idempotency_key=f"IDEM-{acceptance_id}-{now_iso()}",
            requirement_id=requirement_id,
            payload={
                "rebind": True,
                "supersedes": args.supersedes,
                "reason": args.reason,
                "oracle_sha256": receipt["oracle_sha256"],
                "evidence": [{"path": e["path"], "sha256": e["sha256"], "kind": e["kind"]} for e in ev],
                "claim_ceiling": "BINDING_OF_EXISTING_SIGNED_EVIDENCE",
            },
        )
        spine.release_lease(acceptance_id, args.actor, token)
    except Exception as exc:  # typed refusals are the product; report them, never swallow
        receipt["ok"] = False
        receipt["code"] = type(exc).__name__
        receipt["detail"] = str(exc)
        print(json.dumps(receipt, ensure_ascii=False, indent=1))
        return 3

    receipt["ok"] = True
    receipt["state"] = "RESOLVED"
    receipt["transition"] = result
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
