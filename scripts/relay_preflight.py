#!/usr/bin/env python3
"""IR-2 — the transport must outlive the session that started it.

The relay is a process. Twice now a round began, the relay was not running, and the lane "failed" with
a 401 that looked like a credential problem. Nothing in the loop checked that the thing the lanes talk
to was alive, and nothing restarted it after a reboot: `ocx status` reported
`Proxy: not running / Codex autostart: disabled / Service: not installed`.

This preflight answers one question before a spawn: is the transport that this turn will use answering?

Usage:
    python scripts/relay_preflight.py --base http://127.0.0.1:10101 [--json]
Exit: 0 alive · 5 RELAY_DOWN · 6 RELAY_MISCONFIGURED
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:10101")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    url = a.base.rstrip("/") + "/healthz"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read(400).decode("utf-8", "replace")
        out = {"verdict": "RELAY_ALIVE", "url": url, "status": 200, "body": body[:200]}
        print(json.dumps(out, ensure_ascii=False) if a.json else "RELAY_ALIVE")
        return 0
    except urllib.error.HTTPError as e:
        out = {"verdict": "RELAY_MISCONFIGURED", "url": url, "status": e.code,
               "detail": "the relay answered, but not with a healthy status"}
        print(json.dumps(out, ensure_ascii=False) if a.json else "RELAY_MISCONFIGURED")
        return 6
    except Exception as e:
        out = {"verdict": "RELAY_DOWN", "url": url, "detail": f"{type(e).__name__}: {e}",
               "fix": "ocx start --port 10101 (or restore the user-level startup entry)",
               "why_it_matters": "a lane turn that starts here reports a credential failure that is really a dead transport"}
        print(json.dumps(out, ensure_ascii=False) if a.json else "RELAY_DOWN")
        return 5


if __name__ == "__main__":
    sys.exit(main())
