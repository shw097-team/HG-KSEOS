#!/usr/bin/env python3
"""Offline install-verification for the HG-KSEOS credential broker.

Runs the network-free subset of `selftest.py` against the INSTALLED copy, so a
host with `network_default: DENY` (config/project.json) can still prove the
install is intact and the security contract holds, WITHOUT reading the real
credential value and WITHOUT any network call.

  T1 fail-closed        : an absent credential file aborts the preflight (exit 2).
  T2 metadata-only      : presence + byte length reported with content NOT read.
  T3 header construction: the child-env extraheader is URL-scoped and base64-wrapped
                          with the raw token absent from the value.
  T4 redaction          : token-shaped text is stripped from free text.
  T5 wire plumbing      : SKIPPED here (needs network) -> reported INCONCLUSIVE,
                          never as PASS. Run `selftest.py` on a network-enabled
                          host to obtain T5.

Only DUMMY, correctly-shaped tokens are used. The real credential file is never
opened; cred_preflight.PAT_FILE is rebound to synthetic paths before any call.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ["HGK_CRED_FILE"] = str(HERE / "_verify_nonexistent")
import cred_preflight as pf  # noqa: E402
import cred_broker as cb    # noqa: E402

DUMMY = "github_pat_" + "A" * 30  # fake, correctly-shaped; NOT the real token
results: list[dict] = []


def rec(cid: str, status: str, detail: str) -> None:
    results.append({"id": cid, "status": status, "detail": detail})


# T1 -- fail closed on an absent credential file (no read, no network)
pf.PAT_FILE = Path(HERE / "_verify_nonexistent")
pre = pf.run_preflight(probe=False)
rec("T1_fail_closed", "PASS" if (pre["abort"] and pre["verdict"] == "FAIL_CLOSED") else "FAIL",
    f"verdict={pre['verdict']} failed={pre['failed_required']}")

# T2 -- metadata-only reports existence+length without reading content
with tempfile.TemporaryDirectory() as td:
    f = Path(td) / "cred.txt"
    f.write_text(DUMMY + "\n", encoding="utf-8")
    pf.PAT_FILE = f
    meta = pf._verdict(pf.check_metadata_only())
    present = any(c["id"] == "cred_source_present" and c["status"] == "PASS" for c in meta["checks"])
    skipped = any(c["id"] == "cred_syntax" and c["status"] == "SKIP" for c in meta["checks"])
    rec("T2_metadata_only", "PASS" if (present and skipped and meta["verdict"] == "OK") else "FAIL",
        "present+size read, syntax SKIP (content untouched)")

    # T3 -- header construction is URL-scoped and base64-wrapped
    env = cb._child_env(DUMMY)
    val = env["GIT_CONFIG_VALUE_0"]
    decoded = base64.b64decode(val.split("Basic ", 1)[1]).decode()
    rec("T3_header_construction",
        "PASS" if (env["GIT_CONFIG_KEY_0"] == "http.https://github.com/.extraheader"
                   and decoded == f"x-access-token:{DUMMY}"
                   and DUMMY not in val) else "FAIL",
        "key URL-scoped; value decodes to x-access-token:<token>; raw token absent from value")

# T4 -- redaction strips token-shaped text
red = pf._redact(f"failed with {DUMMY} and Authorization: Basic {base64.b64encode(b'x').decode()}")
rec("T4_redaction", "PASS" if (DUMMY not in red) else "FAIL", f"redacted -> {red[:60]}")

# T5 -- network-dependent; never claim PASS offline
rec("T5_wire_plumbing", "SKIP", "network call; INCONCLUSIVE offline -- run selftest.py on a networked host")

pf.PAT_FILE = Path(HERE / "_verify_nonexistent")
failed = [r for r in results if r["status"] == "FAIL"]
verdict = "FAIL" if failed else ("PASS" if all(r["status"] == "PASS" for r in results) else "PASS_OFFLINE_T5_UNPROVEN")
print(json.dumps({"schema": "HGK-CRED-VERIFY-OFFLINE/1", "results": results,
                  "verdict": verdict}, indent=1, ensure_ascii=False))
sys.exit(2 if failed else 0)
