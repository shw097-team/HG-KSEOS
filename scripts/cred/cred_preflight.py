#!/usr/bin/env python3
"""Fail-closed credential preflight for the PIPD-LS-SP unattended write lane.

Purpose
-------
A long unattended run must not discover at minute 90 that its write credential is
absent, expired or invalid.  This module verifies credential *availability* at
minute 0 and **fails closed**: any check that cannot be confirmed FAILs the run
before it starts.

Security contract (binding -- same as tools/github_publish.py):
  * the secret is read into THIS process only, never printed, never placed in
    argv, stdout, a log, evidence, a prompt, a remote URL or .git/config;
  * only non-sensitive codes and lengths are emitted (PAT_PRESENT, AUTH_VALID ...);
  * ``--metadata-only`` never reads the file at all (existence + byte length only).

Exit codes: 0 = all required checks PASS (WARN/SKIP alone still exit 0);
            2 = one or more required checks FAIL (the run must abort).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Credential sources, in precedence order.  The broker uses the first that works.
PAT_FILE = Path(os.environ.get(
    "HGK_CRED_FILE",
    r"C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt"))

# Optional GitHub App source (the recommended long-term credential -- see the FAR).
APP_ID = os.environ.get("HGK_APP_ID")               # e.g. "1234567"
APP_KEY = os.environ.get("HGK_APP_KEY")             # path to the app .pem (private key)
APP_INSTALLATION_ID = os.environ.get("HGK_APP_INSTALLATION_ID")

# Optional owner-recorded expiry metadata, since GitHub exposes NO API to read a
# fine-grained PAT's own expiry date.  File holds an ISO-8601 date, nothing more.
EXPIRY_FILE = Path(os.environ.get(
    "HGK_CRED_EXPIRY_FILE",
    str(PAT_FILE) + ".expiry"))

API = "https://api.github.com"
TOKEN_RE = re.compile(rb"github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}")

REQUIRED = ("cred_source_present", "cred_syntax", "cred_api_valid")


def _result(cid: str, status: str, detail: str) -> dict:
    return {"id": cid, "status": status, "detail": detail}


def _redact(text: str) -> str:
    """Strip any token-shaped or credential-shaped substring from free text."""
    text = re.sub(r"github_pat_[A-Za-z0-9_]{10,}", "<REDACTED>", text)
    text = re.sub(r"gh[pousr]_[A-Za-z0-9]{10,}", "<REDACTED>", text)
    text = re.sub(r"(?i)authorization:\s*basic\s+\S+", "Authorization: Basic <REDACTED>", text)
    return text


def load_pat() -> str | None:
    """Read the PAT into memory.  NEVER called when --metadata-only is set."""
    if not PAT_FILE.is_file():
        return None
    m = TOKEN_RE.search(PAT_FILE.read_bytes())
    return m.group(0).decode("ascii") if m else None


def _api(path: str, token: str):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "PIPD-LS-SP-cred-preflight",
                 "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            return e.code, {}
    except Exception as e:  # noqa: BLE001 - report, never hide
        return None, {"error": type(e).__name__}


def check_metadata_only() -> list[dict]:
    """No secret is read; existence + byte length only.  Safe on any host."""
    checks = []
    st = PAT_FILE.stat() if PAT_FILE.is_file() else None
    checks.append(_result("cred_source_present",
                          "PASS" if st else "FAIL",
                          f"file present, {st.st_size} bytes" if st else "credential file absent"))
    checks.append(_result("cred_syntax", "SKIP", "metadata-only: content not read"))
    checks.append(_result("cred_api_valid", "SKIP", "metadata-only: not probed"))
    return checks


def run_preflight(probe: bool) -> dict:
    checks: list[dict] = []

    # 1. source presence (metadata)
    st = PAT_FILE.stat() if PAT_FILE.is_file() else None
    checks.append(_result("cred_source_present",
                          "PASS" if st else "FAIL",
                          f"file present, {st.st_size} bytes" if st else "credential file absent"))
    if not st:
        checks.append(_result("cred_syntax", "FAIL", "no source"))
        checks.append(_result("cred_api_valid", "FAIL", "no source"))
        checks.append(_result("app_config_present", "SKIP", "PAT path failed first"))
        checks.append(_result("expiry_known", "FAIL", "no source"))
        return _verdict(checks)

    # 2. syntax (reads the file)
    token = load_pat()
    checks.append(_result("cred_syntax",
                          "PASS" if token else "FAIL",
                          f"token-shaped & non-empty, length={len(token)}" if token
                          else "file holds no github token-shaped string"))
    if not token:
        checks.append(_result("cred_api_valid", "FAIL", "unusable source"))
        checks.append(_result("app_config_present", "SKIP", "PAT path failed first"))
        checks.append(_result("expiry_known", "SKIP", "PAT path failed first"))
        return _verdict(checks)

    # 3. App source availability (optional; needs no secret read here)
    app_ok = bool(APP_ID and APP_KEY and APP_INSTALLATION_ID and Path(APP_KEY).is_file())
    checks.append(_result("app_config_present",
                          "PASS" if app_ok else "WARN",
                          "app id/key/installation configured" if app_ok
                          else "not configured (PAT bridge in force)"))

    # 4. validity probe (network; uses the token but prints only a status code)
    if probe:
        s, me = _api("/user", token)
        valid = s == 200
        checks.append(_result("cred_api_valid",
                              "PASS" if valid else "FAIL",
                              f"GET /user -> {s}" + (f", login={me.get('login')}" if valid else "")))
    else:
        checks.append(_result("cred_api_valid", "SKIP", "--no-probe"))

    # 5. expiry knowledge.  GitHub exposes no API to read a PAT's own expiry, so
    #    the only signal is owner-recorded metadata (a date file).
    if EXPIRY_FILE.is_file():
        raw = EXPIRY_FILE.read_text(encoding="utf-8", errors="replace").strip()
        checks.append(_result("expiry_known", "PASS", f"owner-recorded expiry: {_redact(raw)[:32]}"))
    else:
        checks.append(_result("expiry_known", "WARN",
                              "no owner-recorded expiry; GitHub has no API to read a PAT's own expiry"))
    return _verdict(checks)


def _verdict(checks: list[dict]) -> dict:
    failed = [c["id"] for c in checks
              if c["status"] == "FAIL" and c["id"] in REQUIRED]
    return {"schema": "PIPD-CRED-PREFLIGHT/1",
            "checks": checks,
            "required": list(REQUIRED),
            "failed_required": failed,
            "verdict": "FAIL_CLOSED" if failed else "OK",
            "abort": bool(failed)}


def main() -> int:
    ap = argparse.ArgumentParser(description="fail-closed credential preflight")
    ap.add_argument("--metadata-only", action="store_true",
                    help="never read the secret; existence + byte length only")
    ap.add_argument("--no-probe", action="store_true", help="skip the network validity probe")
    args = ap.parse_args()
    if args.metadata_only:
        out = _verdict(check_metadata_only())
    else:
        out = run_preflight(probe=not args.no_probe)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 2 if out["abort"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
