#!/usr/bin/env python3
"""Mandate gate for a governed round: make lane disobedience unshippable.

    mandate_gate.py check --role PLAN|EXECUTE|VERIFY
        exit 0 only when that role has a lane receipt with ok=true and a nonce,
        served_arm == require_arm, and the served model matches MANDATE_<round>.json.

    mandate_gate.py audit
        exit 0 only when every DONE ledger row names a lane receipt for its role.

Both read var/<round>/MANDATE_*.json and var/<round>/receipts/*.json.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUND = "R15-MODEL-FALLBACK-20261023"
RDIR = ROOT / "var" / ROUND


def mandate() -> dict:
    for p in RDIR.glob("MANDATE_*.json"):
        return json.loads(p.read_text(encoding="utf-8"))
    raise SystemExit("ERR mandate file missing")


def receipts() -> list[dict]:
    out = []
    for p in sorted(glob.glob(str(RDIR / "receipts" / "**" / "*.json"), recursive=True)):
        try:
            d = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            continue
        d["_path"] = str(Path(p).relative_to(ROOT)).replace("\\", "/")
        out.append(d)
    return out


def lane_of_role(m: dict, role: str) -> str:
    return "VERIFY_SECURITY" if role == "VERIFY" else role


def check(role: str) -> int:
    m = mandate()
    lane = lane_of_role(m, role)
    spec = m["planes"]["lane_plane"].get(lane)
    if spec is None:
        print(f"ERR no lane spec for {lane}")
        return 2
    need_arm = spec.get("require_arm")
    need_model = spec.get("model")
    ok = []
    for r in receipts():
        if (r.get("lane") or "").upper() != lane:
            continue
        served = r.get("served_arm") or ""
        model_field = r.get("model") or served.split("/")[-1]
        if r.get("ok") is True and r.get("nonce") and served == need_arm and model_field == need_model:
            ok.append(r)
    if ok:
        r = ok[-1]
        print(f"PASS {lane}: receipt={r['_path']} served_arm={r.get('served_arm')} nonce={str(r.get('nonce'))[:12]}…")
        return 0
    print(f"FAIL {lane}: no receipt with ok=true, nonce, served_arm=={need_arm}, model=={need_model}")
    print(f"     receipts seen: {[x['_path'] for x in receipts()] or 'none'}")
    return 1


def audit() -> int:
    m = mandate()
    ledger = json.loads((RDIR / "LEDGER_R15.json").read_text(encoding="utf-8"))
    required_roles = {"O08": "EXECUTE", "O13": "VERIFY"}
    bad = []
    for row in ledger["rows"]:
        if row["state"] != "DONE":
            continue
        role = required_roles.get(row["id"])
        if role is None:
            continue
        lane = lane_of_role(m, role)
        spec = m["planes"]["lane_plane"][lane]
        bound = [p for p in row["evidence"]
                 if any((r.get("_path") or "").endswith(p) and r.get("lane", "").upper() == lane
                        and r.get("served_arm") == spec.get("require_arm") for r in receipts())]
        if not bound:
            bad.append((row["id"], lane))
    if bad:
        for rid, lane in bad:
            print(f"FAIL {rid}: DONE without a bound {lane} receipt (bypass would have shipped)")
        return 1
    print("PASS audit: every DONE row that requires a lane is bound to a served receipt")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["check", "audit"])
    ap.add_argument("--role", default="PLAN")
    a = ap.parse_args(argv)
    return check(a.role) if a.action == "check" else audit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
