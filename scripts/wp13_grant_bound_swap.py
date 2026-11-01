"""Re-demonstrate WP-FHS-13 C5 on a fresh fixture, under a grant that actually covers the swap.

The independent checker's finding on the original receipt was not a technicality: the only grant in the tree was
issued 100 s after the ABI swap, and its writeset named abi.py and hotswap.py — neither of them the target. The
structural cause was that `hotswap.py` had no way to accept a grant at all, so no swap it ran could bind one.

This script therefore does the whole chain in order, on a fixture nobody has touched:

    1. build target_grant/occupant.py (cap-attest-v1) and candidate_grant.py (cap-attest-v2)
    2. write the writeset for exactly those two paths, with live preimages
    3. ISSUE the grant (so issued_at precedes the effect by construction, not by luck)
    4. swap under the grant, and record the binding in the receipt

Usage:
    python scripts/wp13_grant_bound_swap.py --json <receipt.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import time

WP13 = pathlib.Path(r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp13")
FIXTURE = WP13 / "target_grant"
GRANT = WP13 / "grant_wp13_bound.json"
WRITESET = WP13 / "writeset_wp13_bound.json"
HOTSWAP = pathlib.Path(r"C:/Projects/Agent_Workspace/PIPD/tools/hotswap.py")
ISSUER = pathlib.Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/scripts/issue_grant.py")

OCCUPANT = '''import sys
if "--identity" in sys.argv:
    print("cap-attest-v1")
    raise SystemExit(0)
'''


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    args = ap.parse_args()

    FIXTURE.mkdir(parents=True, exist_ok=True)
    entry = FIXTURE / "occupant.py"
    entry.write_text(OCCUPANT, encoding="utf-8", newline="")
    candidate = WP13 / "candidate_grant.py"
    candidate.write_text(OCCUPANT.replace("cap-attest-v1", "cap-attest-v2"), encoding="utf-8", newline="")

    writeset = {"writeset": [{"path": str(entry), "preimage": sha(entry)},
                             {"path": str(candidate), "preimage": sha(candidate)}]}
    WRITESET.write_text(json.dumps(writeset, indent=1), encoding="utf-8")

    nonce = f"WP13-BOUND-{int(time.time())}"
    issue = subprocess.run([sys.executable, str(ISSUER), "issue", "--writeset", str(WRITESET),
                            "--operation", "REPOSITORY_WRITE", "--principal", "owner",
                            "--subject", "WP-FHS-13", "--nonce", nonce, "--epoch", "40",
                            "--candidate-sha", sha(candidate),
                            "--scope", "WP-FHS-13 C5: install occupant under a covering writeset",
                            "--out", str(GRANT)],
                           capture_output=True, text=True, errors="replace", encoding="utf-8")
    if issue.returncode != 0:
        print(json.dumps({"stage": "issue", "exit": issue.returncode, "out": issue.stdout[-800:],
                          "err": issue.stderr[-800:]}, ensure_ascii=False))
        return 1
    issued = json.loads(issue.stdout.strip().splitlines()[-1])

    swap = subprocess.run([sys.executable, str(HOTSWAP), "--root", str(FIXTURE), "--candidate", str(candidate),
                           "--expect-old", "cap-attest-v1", "--expect-new", "cap-attest-v2",
                           "--grant", str(GRANT), "--grant-verifier", str(ISSUER), "--out", args.json],
                          capture_output=True, text=True, errors="replace", encoding="utf-8")

    rec = json.loads(pathlib.Path(args.json).read_text(encoding="utf-8")) if pathlib.Path(args.json).is_file() else {}
    grant_block = rec.get("grant", {})
    checks = {
        "swap_exit_zero": swap.returncode == 0,
        "grant_bound": bool(grant_block.get("nonce")),
        "grant_issued_before_effect": grant_block.get("issued_before_effect") is True,
        "writeset_covers_target": grant_block.get("covers_entry") is True,
        "writeset_covers_candidate": grant_block.get("covers_candidate") is True,
        "issuer_verified_signature": grant_block.get("issuer_verifier_exit") == 0,
        "no_grant_problems": not grant_block.get("problems"),
        "control_old_served": (rec.get("control") or {}).get("identity") == "cap-attest-v1",
        "pos_new_served": (rec.get("pos") or {}).get("identity") == "cap-attest-v2",
        "neg_old_not_served": (rec.get("neg") or {}).get("identity") != "cap-attest-v1",
    }
    out = {"schema": "HGK-WP13-GRANT-BOUND-SWAP/1", "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "fixture": str(FIXTURE), "candidate": str(candidate), "grant": str(GRANT),
           "grant_nonce": issued.get("nonce"), "swap_exit": swap.returncode,
           "swap_stdout": swap.stdout.strip()[-600:], "swap_stderr": swap.stderr.strip()[-600:],
           "checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL",
           "receipt": str(args.json), "receipt_sha256": sha(pathlib.Path(args.json)) if pathlib.Path(args.json).is_file() else None}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
