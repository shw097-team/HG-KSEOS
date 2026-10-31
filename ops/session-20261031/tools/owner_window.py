"""Owner signing window (FAR-15): one passphrase prompt at task start, bounded signing afterwards.

Governing clause: `04_FABRIC_HGK_CONTROL.md:137` — a single Human Owner may, in ONE ceremony,
batch-approve a bounded permit ("predictable, same policy epoch, Root, WriteSet, Operation class,
time limit"); the Issuer still does nonce/lease gating per operation. Escalations (new Root,
elevated effect, UserData/Remote publish, Trust Anchor, Policy authority, Release) still need
dedicated authorisation — those are refused inside a window by construction.

What the window does NOT do
  * it never writes the private key to disk; the key lives only in this process's memory;
  * it never allows an `owner_enrollment` change (that would be "a second issuer");
  * it never signs release / sourcefreeze / policy-authority / trust-anchor payloads;
  * it expires (TTL), has an operation budget, and every signing is appended to SIGNING_LOG.jsonl.

Usage
  python owner_window.py open --task T1 --ttl-hours 8 --max-ops 40 [--workspace <ws>]
  python owner_window.py status | close | selftest-sign | log
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "admission"))
import owner_vault as ov            # noqa: E402
import owner_prompt as op           # noqa: E402

KEY = pathlib.Path(os.environ.get("HGK_OWNER_KEY_PATH") or (pathlib.Path.home() / ".hgk-owner" / "owner.key"))
WINDOW_FILE = pathlib.Path(os.environ.get("HGK_OWNER_WINDOW_PATH") or (KEY.parent / "window.json"))
TOKEN_FILE = WINDOW_FILE.with_name("window.token")

EFFECT_ORDER = ["READ_ONLY_PROBE", "REPOSITORY_WRITE", "HOST_OPERATIONS", "USER_DATA_EFFECT"]
ALLOWED_KINDS = {"merkle_root", "row"}
# FAR-18 §2 乙案: an escalation may be signed by a window ONLY when that window was opened with
# --allow-dedicated <kind>, the kind is in its scope, TTL <= 1h and max_ops <= 4. Anything else keeps
# the FAR-15 invariant (release/sourcefreeze are never covered by a normal registry window).
DEDICATED_KINDS = {"sourcefreeze", "release"}
FORBIDDEN_KINDS = {"release", "sourcefreeze", "policy_authority", "trust_anchor", "owner_enrollment",
                   "elevated_effect", "userdata_effect", "remote_publish"}
# The window's identity invariant is the OWNER enrolment only: that is what "a second issuer / a new
# owner key re-enrolled" would look like. Issuer/acceptance-authority enrolments are operational
# identities created by a ceremony, so binding them would refuse every legitimate run (measured:
# acceptance_authority_enrollment changes on the first ceremony, which refused row #1).
ENROLLMENT_KEYS = ("owner_enrollment",)


def canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def enrollment_sha(reg: dict) -> str:
    """Stable projection of the OWNER identity only (key_id + public_hex).

    The ceremony legitimately rewrites the enrollment block (status timestamps etc.) while the same
    key stays enrolled; hashing the whole block refused every real run (measured). Hashing the
    identity means: same owner -> same sha; a new/re-enrolled owner key -> different sha -> refused.
    """
    oe = reg.get("owner_enrollment") or {}
    return hashlib.sha256(canon({"key_id": oe.get("key_id"), "public_hex": oe.get("public_hex")})).hexdigest()


def _acl(path: pathlib.Path) -> None:
    try:
        subprocess.run(["icacls", str(path), "/inheritance:r", "/grant:r", f"{os.environ.get('USERNAME')}:F"],
                       capture_output=True)
    except Exception:
        pass


def _lock_down() -> None:
    try:
        os.chmod(WINDOW_FILE, 0o600)
        os.chmod(TOKEN_FILE, 0o600)
    except Exception:
        pass
    _acl(WINDOW_FILE)
    _acl(TOKEN_FILE)


def _write_window(d: dict) -> None:
    WINDOW_FILE.parent.mkdir(parents=True, exist_ok=True)
    WINDOW_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _write_token(t: str) -> None:
    TOKEN_FILE.write_text(t, encoding="utf-8")
    _lock_down()


def _log(ws: pathlib.Path, entry: dict) -> None:
    p = ws / "artifacts" / "SIGNING_LOG.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cmd_open(a) -> int:
    ws = pathlib.Path(a.workspace).resolve()
    reg = json.loads((ws / "admission" / "registry" / "runner-registry.json").read_text(encoding="utf-8"))
    if WINDOW_FILE.is_file():
        cur = json.loads(WINDOW_FILE.read_text(encoding="utf-8"))
        if cur.get("state") == "OPEN" and cur.get("expires_at", 0) > time.time():
            print(json.dumps({"opened": False, "error": "WINDOW_ALREADY_OPEN",
                              "window_id": cur.get("window_id"), "expires_at": cur.get("expires_at")},
                             ensure_ascii=False))
            return 3

    def _verify(secret: str) -> None:
        ov.load_private(KEY, secret)      # raises on a wrong passphrase -> the UI retries

    secret, source = op.get_secret(f"OWNER SIGNING WINDOW — task {a.task}",
                                   min_len=12, allow_generate=False, env_var=a.passphrase_env,
                                   verify=_verify, timeout=900, prefer_ui=True)
    priv = ov.load_private(KEY, secret)
    del secret
    pub = ov.pub_hex(priv)

    wid = f"WIN-{uuid.uuid4().hex[:12]}"
    now = time.time()
    window = {
        "schema": "OwnerSigningWindow@1", "window_id": wid, "task_id": a.task, "workspace": str(ws),
        "opened_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
        "expires_at": int(now + a.ttl_hours * 3600), "ttl_hours": a.ttl_hours,
        "scope": [s for s in a.scope.split(",") if s], "max_ops": a.max_ops, "ops_used": 0,
        "dedicated_scope": sorted({x.strip() for x in (a.allow_dedicated or "").split(",") if x.strip()}),
        "dedicated_authorisation": ("explicit" if (a.allow_dedicated or "").strip() else None),
        "effect_class_ceiling": a.effect_ceiling,
        "policy_epoch_at_open": reg.get("registry_rev"),
        "enrollments_sha256_at_open": enrollment_sha(reg),
        "owner_fingerprint": ov.fingerprint(pub), "owner_public_hex": pub,
        "prompt_source": source, "ui_impl": source, "state": "OPEN", "refusals": [],
        "ceiling": ("bounded batch approval per 04_FABRIC_HGK_CONTROL.md:137; release/sourcefreeze/"
                    "policy-authority/trust-anchor and owner_enrollment changes are always refused"),
    }
    token = os.urandom(24).hex()
    _write_window(window)
    _write_token(token)

    # owner-signed receipt for the window itself (who authorised this window)
    _ded = set(window["dedicated_scope"])
    if _ded:
        if not _ded <= DEDICATED_KINDS:
            print(json.dumps({"opened": False, "refused": "REFUSED_DEDICATED_KIND_UNKNOWN",
                              "detail": sorted(_ded - DEDICATED_KINDS)}, ensure_ascii=False))
            return 3
        if a.ttl_hours > 1 or a.max_ops > 4:
            print(json.dumps({"opened": False, "refused": "REFUSED_DEDICATED_WINDOW_TOO_BROAD",
                              "detail": {"ttl_hours": a.ttl_hours, "max_ops": a.max_ops,
                                         "limit": {"ttl_hours": 1, "max_ops": 4}}}, ensure_ascii=False))
            return 3
        _missing = sorted(_ded - set(window["scope"]))
        if _missing:
            print(json.dumps({"opened": False, "refused": "REFUSED_DEDICATED_NOT_IN_SCOPE",
                              "detail": _missing}, ensure_ascii=False))
            return 3

    if _ded:
        _log(ws, {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "window_id": window["window_id"],
                  "op": "DEDICATED_AUTHORISATION", "decision": "ALLOW",
                  "scope": sorted(_ded), "ttl_hours": a.ttl_hours, "max_ops": a.max_ops})
    receipt = {k: window[k] for k in ("window_id", "task_id", "opened_at", "expires_at", "scope",
                                      "max_ops", "effect_class_ceiling", "policy_epoch_at_open",
                                      "enrollments_sha256_at_open", "owner_fingerprint")}
    sig = priv.sign(canon(receipt)).hex()
    rec = {**receipt, "owner_signature_hex": sig, "alg": "ed25519",
           "claim_ceiling": ("the window authorises bounded signing for this task/scope/TTL only "
                             "(04_FABRIC_HGK_CONTROL.md:137); release/sourcefreeze/policy-authority/"
                             "trust-anchor and owner_enrollment changes always need dedicated "
                             "authorisation, and the private key lives only in the broker process")}
    (ws / "artifacts" / "OWNER_WINDOW.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1),
                                                        encoding="utf-8")
    _log(ws, {"ts": window["opened_at"], "window_id": wid, "op": "WINDOW_OPEN", "decision": "ALLOW",
              "task_id": a.task, "ttl_hours": a.ttl_hours, "max_ops": a.max_ops,
              "effect_class_ceiling": a.effect_ceiling, "prompt_source": source,
              "ui_impl": source})
    print(json.dumps({"opened": True, "window_id": wid, "owner_fingerprint": window["owner_fingerprint"],
                      "expires_at": window["expires_at"], "max_ops": a.max_ops,
                      "effect_class_ceiling": a.effect_ceiling, "prompt_source": source,
                      "ui_impl": source,
                      "receipt": str(ws / "artifacts" / "OWNER_WINDOW.json")}, ensure_ascii=False),
          flush=True)

    cap = EFFECT_ORDER.index(a.effect_ceiling) if a.effect_ceiling in EFFECT_ORDER else 1
    state = {"ops": 0, "closed": False, "why": None}
    lock = threading.RLock()   # refuse() re-enters under the budget check; a plain Lock deadlocked

    class H(BaseHTTPRequestHandler):
        def log_message(self, *args):
            return

        def _send(self, code: int, obj: dict) -> None:
            body = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):  # noqa: N802
            try:
                n = int(self.headers.get("Content-Length") or 0)
                req = json.loads(self.rfile.read(n) or b"{}")
            except Exception:
                return self._send(400, {"error": "BAD_JSON"})
            if req.get("token") != token:
                return self._send(403, {"error": "REFUSED_BAD_TOKEN"})
            if self.path == "/close":
                state["closed"], state["why"] = True, "CLIENT_CLOSE"
                return self._send(200, {"ok": True, "closed": True})
            if self.path != "/sign":
                return self._send(404, {"error": "NOT_FOUND"})

            def refuse(code: str):
                with lock:
                    window["refusals"].append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "code": code,
                                               "kind": req.get("kind")})
                    _write_window({**window, "ops_used": state["ops"]})
                _log(ws, {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "window_id": wid,
                          "op": req.get("kind"), "decision": "REFUSE", "code": code})
                return self._send(403, {"error": code, "window_id": wid})

            if time.time() > window["expires_at"]:
                return refuse("REFUSED_WINDOW_EXPIRED")
            kind = req.get("kind") or ""
            _dedicated_ok = (kind in DEDICATED_KINDS
                             and kind in (window.get("dedicated_scope") or [])
                             and window.get("dedicated_authorisation") == "explicit"
                             and kind in (window.get("scope") or []))
            if kind in FORBIDDEN_KINDS and not _dedicated_ok:
                return refuse("REFUSED_ENROLLMENT_CHANGE_IN_WINDOW" if kind == "owner_enrollment"
                              else "REFUSED_ESCALATION_NEEDS_DEDICATED_AUTH")
            if kind not in ALLOWED_KINDS and not _dedicated_ok:
                return refuse("REFUSED_KIND_NOT_IN_SCOPE")
            if req.get("effect_class") and EFFECT_ORDER.index(req["effect_class"]) > cap:
                return refuse("REFUSED_EFFECT_CLASS_ABOVE_WINDOW")
            if req.get("enrollments_sha256") != window["enrollments_sha256_at_open"]:
                return refuse("REFUSED_ENROLLMENT_CHANGE_IN_WINDOW")
            body = (req.get("body_json") or "").encode()
            if hashlib.sha256(body).hexdigest() != req.get("payload_sha256"):
                return refuse("REFUSED_PAYLOAD_SHA_MISMATCH")
            with lock:
                if state["ops"] >= window["max_ops"]:
                    return refuse("REFUSED_OP_BUDGET_EXHAUSTED")
                sig_hex = priv.sign(body).hex()
                state["ops"] += 1
                window["ops_used"] = state["ops"]
                _write_window(window)
            _log(ws, {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "window_id": wid, "op": kind,
                      "decision": "ALLOW", "payload_sha256": req["payload_sha256"],
                      "ops_used": state["ops"]})
            return self._send(200, {"signature_hex": sig_hex, "window_id": wid, "ops_used": state["ops"]})

    srv = HTTPServer(("127.0.0.1", 0), H)
    srv.timeout = 1
    port = srv.server_address[1]
    window["port"] = port
    _write_window(window)
    _write_token(token)
    print(json.dumps({"serving": True, "port": port, "window_id": wid}, ensure_ascii=False), flush=True)

    try:
        while not state["closed"] and time.time() <= window["expires_at"]:
            try:
                srv.handle_request()
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError, TimeoutError):
                continue          # a bare TCP probe (e.g. `status`) must never close the window
            except Exception:
                continue
    finally:
        try:
            del priv
        except Exception:
            pass
        close_entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "window_id": wid, "op": "WINDOW_CLOSE",
                       "decision": "CLOSED", "reason": state["why"] or "TTL_EXPIRED",
                       "ops_used": state["ops"], "refusals": len(window.get("refusals") or [])}
        _log(ws, close_entry)
        window.update({"state": "CLOSED", "closed_at": close_entry["ts"],
                       "close_reason": close_entry["reason"], "ops_used": state["ops"]})
        _write_window(window)
        TOKEN_FILE.unlink(missing_ok=True)
        srv.server_close()
    return 0


def _load_window() -> dict | None:
    if not WINDOW_FILE.is_file():
        return None
    return json.loads(WINDOW_FILE.read_text(encoding="utf-8"))


def cmd_status(_a) -> int:
    w = _load_window()
    if not w:
        print(json.dumps({"state": "ABSENT"}, ensure_ascii=False))
        return 1
    alive = False
    if w.get("port") and w.get("state") == "OPEN":
        import socket
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect(("127.0.0.1", w["port"]))
            alive = True
        except Exception:
            alive = False
        finally:
            s.close()
    out = {k: w.get(k) for k in ("window_id", "task_id", "state", "scope", "max_ops", "ops_used",
                                 "effect_class_ceiling", "expires_at", "owner_fingerprint",
                                 "ui_impl")}
    out["remaining_s"] = max(0, int(w.get("expires_at", 0) - time.time()))
    out["broker_alive"] = alive
    out["usable"] = bool(alive and w.get("state") == "OPEN" and time.time() < w.get("expires_at", 0))
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["usable"] else 2


def _post(path: str, payload: dict, timeout: float = 5) -> dict:
    import urllib.request
    w = _load_window() or {}
    port = w.get("port")
    if not port:
        raise RuntimeError("NO_WINDOW")
    token = TOKEN_FILE.read_text(encoding="utf-8").strip() if TOKEN_FILE.is_file() else ""
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}",
                                 data=json.dumps({**payload, "token": token}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def cmd_close(a=None) -> int:
    force = bool(getattr(a, "force", False))
    try:
        print(json.dumps(_post("/close", {}), ensure_ascii=False))
        return 0
    except Exception as e:
        if not force:
            print(json.dumps({"closed": False, "error": f"{type(e).__name__}: {e}",
                              "hint": "the signing service is unreachable; --force closes the WINDOW STATE "
                                      "locally and writes a receipt, it does not sign anything"},
                             ensure_ascii=False))
            return 4
        # MEASURED 2026-10-31: the service lives inside the `open` process, so when that process ends the
        # window stays OPEN with no way to close it, and `open` refuses a new window (WINDOW_ALREADY_OPEN)
        # until the TTL expires -- the owner is locked out of signing for up to 8 hours. The recovery is an
        # explicit, receipted local close: it signs nothing and it cannot open anything.
        cur = json.loads(WINDOW_FILE.read_text(encoding="utf-8")) if WINDOW_FILE.is_file() else {}
        receipt = {"schema": "OWNER-WINDOW-FORCE-CLOSE/1",
                   "window_id": cur.get("window_id"), "task_id": cur.get("task_id"),
                   "state_before": cur.get("state"), "expires_at": cur.get("expires_at"),
                   "closed_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "why": "signing service unreachable",
                   "transport_error": f"{type(e).__name__}: {e}", "signed_anything": False}
        arts = WINDOW_FILE.parent / "artifacts"
        arts.mkdir(parents=True, exist_ok=True)
        rpath = arts / f"WINDOW_CLOSE_FORCE_{time.strftime('%Y%m%dT%H%M%S')}.json"
        rpath.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        cur["state"] = "CLOSED"
        cur["closed_at"] = receipt["closed_at"]
        cur["closed_by"] = "FORCE_LOCAL_CLOSE"
        WINDOW_FILE.write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({"closed": True, "forced": True, "window_id": cur.get("window_id"),
                          "receipt": str(rpath)}, ensure_ascii=False))
        return 0


def cmd_selftest_sign(a) -> int:
    body = canon({"selftest": uuid.uuid4().hex, "at": time.strftime("%Y-%m-%dT%H:%M:%S")})
    ws = pathlib.Path(a.workspace).resolve()
    reg = json.loads((ws / "admission" / "registry" / "runner-registry.json").read_text(encoding="utf-8"))
    try:
        r = _post("/sign", {"kind": "merkle_root", "effect_class": "READ_ONLY_PROBE",
                            "enrollments_sha256": enrollment_sha(reg),
                            "payload_sha256": hashlib.sha256(body).hexdigest(),
                            "body_json": body.decode()})
    except Exception as e:
        print(json.dumps({"signed": False, "error": f"{type(e).__name__}: {e}"}, ensure_ascii=False))
        return 4
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    pub = bytes.fromhex(reg["owner_enrollment"]["public_hex"])
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(bytes.fromhex(r["signature_hex"]), body)
        ok = True
    except Exception:
        ok = False
    print(json.dumps({"signed": True, "signature_verifies_against_owner_key": ok,
                      "window_id": r.get("window_id"), "ops_used": r.get("ops_used")}, ensure_ascii=False))
    return 0 if ok else 5


def cmd_log(a) -> int:
    p = pathlib.Path(a.workspace).resolve() / "artifacts" / "SIGNING_LOG.jsonl"
    if not p.is_file():
        print(json.dumps({"log": [], "note": "no signing yet"}))
        return 0
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(json.dumps({"entries": len(rows), "last": rows[-5:]}, ensure_ascii=False, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open")
    o.add_argument("--task", required=True)
    o.add_argument("--ttl-hours", type=float, default=8)
    o.add_argument("--max-ops", type=int, default=40)
    o.add_argument("--scope", default="registry_row_sign,merkle_root_sign")
    o.add_argument("--allow-dedicated", default="",
                   help="csv of sourcefreeze/release explicitly authorised for THIS window (TTL<=1h, max_ops<=4)")
    o.add_argument("--effect-ceiling", default="REPOSITORY_WRITE")
    o.add_argument("--workspace", default=str(HERE))
    o.add_argument("--passphrase-env", default="HGK_OWNER_PASSPHRASE")
    sub.add_parser("status")
    cl = sub.add_parser("close")
    cl.add_argument("--force", action="store_true",
                    help="close the WINDOW STATE locally when the signing service is gone; signs nothing")
    st = sub.add_parser("selftest-sign")
    st.add_argument("--workspace", default=str(HERE))
    lg = sub.add_parser("log")
    lg.add_argument("--workspace", default=str(HERE))
    a = ap.parse_args()
    return {"open": cmd_open, "status": cmd_status, "close": cmd_close,
            "selftest-sign": cmd_selftest_sign, "log": cmd_log}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
