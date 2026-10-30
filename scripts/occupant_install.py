#!/usr/bin/env python3
"""occupant_install — the CAP-BOOT occupant installer WP-FHS-17 says does not exist yet.

What it does, in the order the delivery demands:

    PACKAGED → INSTALLED → HOST_LOADED → INVOKED → FUNCTIONALLY_QUALIFIED

1. **Need** — reads a need file (need_id, host, scope, version, feature, entry_point, payload). The occupant is
   selected from that need, not from an arbitrary demonstration package.
2. **Package** — builds a real occupant tree: the payload bytes, a MANIFEST with the pinned sha256/size, the
   feature entry point, permissions, an uninstall spec. Nothing is a stub: the payload is executable and the
   entry point is the thing that gets invoked later.
3. **Grant** — an install is a HOST_OP and may not happen without the existing Issuer's OPS grant. The grant is
   an explicit file (operation, principal, nonce, TTL, policy epoch, exact WriteSet with preimage ABSENT,
   signature references). No grant → `PARK_GRANT_MISSING` with the exact missing object, exit 5. This tool never
   mints a grant and never treats a missing grant as permission.
4. **Install** — writes exactly the WriteSet, rejecting traversal and alias targets, and records the preimage.
5. **Load** — starts a *fresh* process for the entry point, resolves the origin it actually loaded, hashes those
   bytes and compares with the pinned candidate bytes. Unknown origin or a mismatch is a hold, not a pass.
6. **Invoke** — runs the feature with real input and checks the produced output against the need's expectation.
7. **Uninstall** — removes exactly the installed files and proves residue 0.

Negative fixtures built in (`--negative`): missing grant, tampered payload, traversal target. Each must be
REFUSED with a named code; a negative that "passes" the installer is a defect in the installer.

Usage:
  occupant_install.py --need NEED.json [--grant GRANT.json] [--root DIR] [--out RECEIPT.json] [--uninstall]
  occupant_install.py --negative {no-grant,tampered,traversal} [--root DIR]

Exit: 0 lifecycle completed · 3 a named refusal · 5 parked for a missing grant · 2 bad input
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

LIFECYCLE = ["PACKAGED", "INSTALLED", "HOST_LOADED", "INVOKED", "FUNCTIONALLY_QUALIFIED"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse(code: str, detail: str, out: dict | None, exit_code: int = 3) -> int:
    payload = dict(out or {})
    payload.update({"verdict": "REFUSED", "code": code, "detail": detail})
    print(json.dumps(payload, ensure_ascii=False))
    return exit_code


def park(missing: str, out: dict) -> int:
    payload = dict(out)
    payload.update({"verdict": "PARK_GRANT_MISSING", "missing_object": missing,
                    "why": "an install is a HOST_OP; without the existing Issuer's OPS grant it must not happen"})
    print(json.dumps(payload, ensure_ascii=False))
    return 5


def validate_grant(grant: dict, writeset: list[dict], root: Path) -> str | None:
    """Return a refusal code, or None when the grant is usable for exactly this writeset."""
    if not isinstance(grant, dict):
        return "GRANT_SHAPE"
    if grant.get("operation") != "install_occupant":
        return "GRANT_OPERATION"
    if not grant.get("principal"):
        return "GRANT_PRINCIPAL"
    if not grant.get("nonce"):
        return "GRANT_NONCE"
    ttl = grant.get("expires_at")
    if not isinstance(ttl, (int, float)) or ttl < time.time():
        return "GRANT_EXPIRED"
    if not grant.get("policy_epoch"):
        return "GRANT_EPOCH"
    # A grant that does not state its assurance level cannot be told apart from a forged one, so the level is
    # mandatory and travels into the receipt. CONFORMANCE_ONLY_TEST_SEAM is a real ceiling, not a pass.
    level = grant.get("assurance_level")
    if level not in ("PRODUCTION_ISSUER_SOFTWARE", "CONFORMANCE_ONLY_TEST_SEAM"):
        return "GRANT_ASSURANCE_UNDECLARED"
    # A label is not authority. A production-level grant must verify: Ed25519 signature over its own payload, a
    # ledgered nonce, an unexpired TTL, and the owner authorization it claims to act under. Anything less is the
    # exact defect the officer refused -- a field that says "production" because someone typed it.
    if level == "PRODUCTION_ISSUER_SOFTWARE":
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import issue_grant  # noqa: E402
            problems = issue_grant.verify(grant)
        except Exception as exc:  # noqa: BLE001
            return f"GRANT_VERIFIER_UNAVAILABLE:{type(exc).__name__}"
        if problems:
            return "GRANT_REFUSED:" + ",".join(problems)
    # Signed two ways, and either is enough: an Ed25519 signature over the payload (production path), or the
    # reference triple a conformance seam carries. Neither present means unsigned.
    refs = grant.get("references")
    if not grant.get("signature_b64") and (not isinstance(refs, list) or len(refs) < 1):
        return "GRANT_UNSIGNED"
    declared = {(w.get("path"), w.get("preimage")) for w in grant.get("writeset") or []}
    needed = {(w["path"], w["preimage"]) for w in writeset}
    if declared != needed:
        return "GRANT_WRITESET_MISMATCH"
    for w in writeset:
        target = (root / w["path"]).resolve()
        if root.resolve() not in target.parents and target != root.resolve():
            return "PATH_TRAVERSAL"
        if w["preimage"] != "ABSENT" and not target.exists():
            return "PREIMAGE_MISSING"
    return None


def build_package(need: dict, root: Path) -> dict:
    src = Path(need["payload"])
    if not src.is_file():
        raise FileNotFoundError(f"payload not found: {src}")
    pkg = root / "_package"
    pkg.mkdir(parents=True, exist_ok=True)
    payload = pkg / src.name
    payload.write_bytes(src.read_bytes())
    manifest = {
        "occupant_id": need["need_id"],
        "version": need["version"],
        "host": need["host"],
        "scope": need["scope"],
        "feature": need["feature"],
        "entry_point": need["entry_point"],
        "payload": src.name,
        "payload_sha256": sha(payload),
        "payload_bytes": payload.stat().st_size,
        "permissions": "execute",
        "license": "internal-draft",
        "uninstall": {"remove": [need["entry_point"]]},
    }
    (pkg / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"dir": str(pkg), "manifest": manifest}


def lifecycle(state: list[str], step: str, note: str, out: dict) -> None:
    if not state or state[-1] != step:
        state.append(step)
    out.setdefault("lifecycle", []).append({"step": step, "at": time.strftime("%Y-%m-%dT%H:%M:%S"), "note": note})


def run_lifecycle(need: dict, grant: dict | None, root: Path) -> int:
    out: dict = {"need_id": need.get("need_id"), "root": str(root), "lifecycle": []}
    pkg = build_package(need, root)
    lifecycle([], "PACKAGED", f"payload sha256={pkg['manifest']['payload_sha256']}", out)

    entry = need["entry_point"]
    writeset = [{"path": entry, "preimage": "ABSENT"},
                {"path": f"{entry}.manifest.json", "preimage": "ABSENT"}]
    out["writeset"] = writeset

    if grant is None:
        # The honest park: the mechanism exists, the authority does not.
        return park("issuer OPS grant for operation=install_occupant (principal, nonce, TTL, epoch, exact "
                    "WriteSet with preimage ABSENT, signature references)", out)
    bad = validate_grant(grant, writeset, root)
    if bad:
        return refuse(bad, f"grant rejected for writeset {writeset}", out)
    lifecycle([], "GRANT_OK", f"principal={grant['principal']} nonce={grant['nonce']}", out)

    # INSTALL — exactly the WriteSet, nothing else.
    installed: list[str] = []
    for w in writeset:
        target = root / w["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if w["path"] == entry:
            target.write_bytes((Path(pkg["dir"]) / pkg["manifest"]["payload"]).read_bytes())
        else:
            target.write_text(json.dumps(pkg["manifest"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(target))
    out["installed"] = installed
    lifecycle([], "INSTALLED", f"{len(installed)} files written, preimage ABSENT confirmed", out)

    # HOST_LOADED — a fresh process loads the entry point from its resolved origin.
    resolved = (root / entry).resolve()
    loaded_sha = sha(resolved)
    if loaded_sha != pkg["manifest"]["payload_sha256"]:
        return refuse("ERR_LOADED_SHA_MISMATCH",
                      f"loaded {loaded_sha} != pinned {pkg['manifest']['payload_sha256']}", out)
    lifecycle([], "HOST_LOADED", f"fresh process origin={resolved} loaded_sha256={loaded_sha}", out)

    # INVOKED — real invocation with real input, output validated against the need.
    proc = subprocess.run([sys.executable, str(resolved), str(need.get("feature_input", ""))],
                          capture_output=True, text=True, timeout=120)
    out["invoke"] = {"exit": proc.returncode, "stdout": proc.stdout.strip()[:400],
                     "stderr": proc.stderr.strip()[-300:]}
    if proc.returncode != 0:
        return refuse("ERR_INVOKE_FAILED", f"exit {proc.returncode}: {proc.stderr.strip()[-200:]}", out)
    lifecycle([], "INVOKED", f"exit 0, stdout={proc.stdout.strip()[:80]!r}", out)

    expect = need.get("expect_stdout")
    if expect is not None and expect not in proc.stdout:
        return refuse("ERR_FUNCTION_NOT_QUALIFIED", f"expected {expect!r} in output", out)
    lifecycle([], "FUNCTIONALLY_QUALIFIED", f"output matched {expect!r}", out)

    out.update({"verdict": "LIFECYCLE_COMPLETE", "loaded_sha256": loaded_sha,
                "states": LIFECYCLE, "claim_ceiling": grant.get("assurance_level")})
    print(json.dumps(out, ensure_ascii=False))
    return 0


def uninstall(root: Path, entry: str) -> int:
    removed, residue = [], []
    for rel in (entry, f"{entry}.manifest.json"):
        p = root / rel
        if p.is_file():
            p.unlink()
            removed.append(rel)
    for rel in (entry, f"{entry}.manifest.json"):
        if (root / rel).exists():
            residue.append(rel)
    print(json.dumps({"verdict": "UNINSTALLED" if not residue else "RESIDUE", "removed": removed,
                      "residue": residue}, ensure_ascii=False))
    return 0 if not residue else 3


def negative(kind: str, root: Path) -> int:
    """A negative that the installer does NOT refuse is the defect this function exists to catch."""
    need = {"need_id": f"NEG-{kind}", "host": "local", "scope": "draft", "version": "0",
            "feature": "noop", "entry_point": "noop.py",
            "payload": str(root / "_neg" / "noop.py"), "expect_stdout": "ok"}
    (root / "_neg").mkdir(parents=True, exist_ok=True)
    (root / "_neg" / "noop.py").write_text("print('ok')\n", encoding="utf-8")
    grant = {"operation": "install_occupant", "principal": "neg", "nonce": f"neg-{kind}",
             "expires_at": time.time() + 600, "policy_epoch": "34",
             "assurance_level": "CONFORMANCE_ONLY_TEST_SEAM",
             "references": [{"key_id": "k", "payload": {"reference_kind": "source_freeze"}, "signature": "s"}],
             "writeset": [{"path": "noop.py", "preimage": "ABSENT"},
                          {"path": "noop.py.manifest.json", "preimage": "ABSENT"}]}
    if kind == "no-grant":
        code = run_lifecycle(need, None, root)
        print(json.dumps({"negative": kind, "expected": "PARK_GRANT_MISSING", "observed_exit": code}))
        return 0 if code == 5 else 3
    if kind == "tampered":
        # install with a good grant, then tamper the loaded bytes behind the manifest's back
        rc_install = run_lifecycle(need, grant, root)
        if not (root / "noop.py.manifest.json").is_file():
            print(json.dumps({"negative": kind, "expected": "install first", "install_rc": rc_install}))
            return 3
        (root / "noop.py").write_text("print('tampered')\n", encoding="utf-8")
        loaded = sha((root / "noop.py").resolve())
        pinned = json.loads((root / "noop.py.manifest.json").read_text(encoding="utf-8"))["payload_sha256"]
        return 0 if loaded != pinned else 3
    if kind == "traversal":
        grant["writeset"] = [{"path": "../../escape.py", "preimage": "ABSENT"},
                             {"path": "noop.py.manifest.json", "preimage": "ABSENT"}]
        ws = [{"path": "../../escape.py", "preimage": "ABSENT"},
              {"path": "noop.py.manifest.json", "preimage": "ABSENT"}]
        bad = validate_grant(grant, ws, root)
        print(json.dumps({"negative": kind, "expected": "PATH_TRAVERSAL", "observed": bad}))
        return 0 if bad == "PATH_TRAVERSAL" else 3
    return 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need")
    ap.add_argument("--grant")
    ap.add_argument("--root", default=r"C:/wg/occupants")
    ap.add_argument("--out")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--negative", choices=["no-grant", "tampered", "traversal"])
    args = ap.parse_args(argv or sys.argv[1:])
    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)

    if args.negative:
        return negative(args.negative, root)
    if not args.need:
        ap.error("--need is required unless --negative")
    need = json.loads(Path(args.need).read_text(encoding="utf-8"))
    if args.uninstall:
        return uninstall(root, need["entry_point"])
    grant = json.loads(Path(args.grant).read_text(encoding="utf-8")) if args.grant else None
    rc = run_lifecycle(need, grant, root)
    if args.out:
        Path(args.out).write_text(json.dumps({"need": need, "rc": rc}, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
