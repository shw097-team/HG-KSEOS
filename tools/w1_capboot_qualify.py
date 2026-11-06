#!/usr/bin/env python3
"""WP-FHS-17 — CAP-BOOT occupant qualification for the capabilities W1 actually consumes.

Each need is resolved to a REAL occupant on this host (binary or installed distribution), probed for
version/digest/license/Windows fit, and cross-checked against the owner-signed B1 runner registry.
Four states, and no fifth:

  QUALIFIED_WITH_ROUTE     real occupant + an OWNER_SIGNED route covering it
  QUALIFIED_LOCAL_ONLY     real occupant, no signed route  → usable for READ/LOCAL_DRAFT, not HOST_OP
  CAPABILITY_GAP_HOLD      the route exists in `not_registered` → named gap, never "installed"
  CAPABILITY_NOT_QUALIFIED the probe itself failed (the occupant is not there)

A file existing is never `INSTALLED`; `loaded_consumer` is only true when this round actually invoked
the occupant and the evidence file is named.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as md
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REGISTRY = Path(r"C:/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027/admission/registry/runner-registry.json")


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def probe_binary(name: str) -> dict:
    found = shutil.which(name)
    if not found:
        return {"found": False}
    p = Path(found)
    out = {"found": True, "path": str(p), "sha256": sha_file(p) if p.is_file() else "",
           "bytes": p.stat().st_size if p.is_file() else 0}
    try:
        v = subprocess.run([found, "--version"], capture_output=True, text=True, timeout=30)
        out["version"] = (v.stdout or v.stderr).strip().splitlines()[0][:120]
    except Exception as exc:
        out["version_error"] = str(exc)[:120]
    return out


def probe_dist(name: str, host_site: Path | None = None) -> dict:
    """Probe a distribution in THIS interpreter, then in an explicit host site-packages."""
    try:
        dist = md.distribution(name)
        meta = dist.metadata
        files = list(dist.files or [])
        return {"found": True, "interpreter": sys.executable, "version": dist.version,
                "license": (meta.get("License") or "")[:80],
                "license_expression": (meta.get("License-Expression") or "")[:80],
                "requires_python": meta.get("Requires-Python") or "",
                "files": len(files), "location": str(dist.locate_file(""))}
    except md.PackageNotFoundError:
        pass
    if host_site and host_site.is_dir():
        for info in sorted(host_site.glob(f"{name.replace('-', '_')}*.dist-info")):
            meta = {}
            for line in (info / "METADATA").read_text(encoding="utf-8", errors="replace").splitlines():
                if ": " in line:
                    k, v = line.split(": ", 1)
                    meta.setdefault(k, v)
            return {"found": True, "interpreter": str(host_site.parents[1] / "Scripts" / "python.exe"),
                    "version": meta.get("Version", ""), "license": meta.get("License", "")[:80],
                    "license_expression": meta.get("License-Expression", "")[:80],
                    "requires_python": meta.get("Requires-Python", ""),
                    "files": len(list((info.parent / name.replace("-", "_")).rglob("*")))
                    if (info.parent / name.replace("-", "_")).is_dir() else 0,
                    "location": str(host_site), "probe": "host venv site-packages dist-info"}
    return {"found": False}


def registry_index(reg: dict) -> tuple[dict, set]:
    """Index the SIGNED rows first.

    `rows` is the owner-signed set (rev 10: 30 rows); `runners` is an older, narrower shape (12).
    `not_registered` is a to-do list the ceremony consumes but never clears, so a route that already
    has a signed row IS registered regardless of what that list still says. The previous precedence
    (`not_registered` first, over `runners` only) reported two owner-signed routes as NOT_REGISTERED.
    """
    rows: dict = {}
    for r in (reg.get("rows") or []):
        if r.get("route_id"):
            rows[r["route_id"]] = r
    for r in (reg.get("runners") or []):
        rows.setdefault(r.get("route_id"), r)
    missing = set()
    for entry in reg.get("not_registered") or []:
        # the list mixes plain route ids with typed entries {route_id, why}
        rid = entry.get("route_id") if isinstance(entry, dict) else str(entry)
        if rid and rid not in rows:
            missing.add(rid)
    return rows, missing


def qualify(need: str, route: str, probe: dict, rows: dict, missing: set,
            invoked: str | None) -> dict:
    row = rows.get(route)
    rec = {"need": need, "route": route, "probe": probe, "invoked_this_round": invoked}
    if not probe.get("found"):
        rec["state"] = "CAPABILITY_NOT_QUALIFIED"
        rec["first_fail"] = "WP-FHS-17.FIRST_FAIL:CAPABILITY_NOT_QUALIFIED"
        return rec
    rec["windows_fit"] = platform.system() == "Windows" and platform.machine().lower() in (
        "amd64", "x86_64", "arm64")
    rec["occupant_state"] = "PRESENT"
    if row is not None:
        rec["registry"] = {"route_id": route, "state": row.get("status") or row.get("state"),
                           "permission_scope": row.get("permission_scope"),
                           "owner_signed": bool((row.get("owner_signature") or {}).get("value"))}
        rec["route_state"] = "REGISTERED"
        signed = rec["registry"]["owner_signed"]
        rec["state"] = "QUALIFIED_WITH_ROUTE" if (signed and rec["windows_fit"]) else "QUALIFIED_LOCAL_ONLY"
        return rec
    if route in missing:
        rec["state"] = "CAPABILITY_GAP_HOLD"
        rec["first_fail"] = "CAPABILITY_GAP_HOLD"
        rec["registry"] = "NOT_REGISTERED"
        rec["route_state"] = "NOT_REGISTERED"
        rec["owner"] = "Original HGK Issuer / Installer"
        rec["resume_predicate"] = ("an owner-signed route for this occupant exists in the registry and "
                                  "the host load is read back")
        return rec
    rec["registry"] = "NO_ROUTE"
    rec["route_state"] = "NO_ROUTE"
    rec["state"] = "QUALIFIED_LOCAL_ONLY" if rec["windows_fit"] else "CAPABILITY_NOT_QUALIFIED"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--registry", default=str(REGISTRY))
    ap.add_argument("--host-venv", default=r"C:/Projects/Agent_Workspace/FHS_W1_Engineering_Execution/hosts/win-py311-sbl")
    args = ap.parse_args()
    reg = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    rows, missing = registry_index(reg)
    host_site = Path(args.host_venv) / "Lib" / "site-packages"

    needs = []
    needs.append(qualify("python.runtime (>=3.11)", "OWNER_REGISTERED::root_probe",
                         probe_binary("python"), rows, missing,
                         "evidence/WP11_SP_HOST_MATRIX.json"))
    needs.append(qualify("git.repo.read", "OWNER_REGISTERED::repo_context_probe",
                         probe_binary("git"), rows, missing,
                         "evidence/WP11_SP_HOST_MATRIX.json"))
    needs.append(qualify("hermes.agent.runtime", "OWNER_REGISTERED::hermes_queue",
                         probe_binary("hermes"), rows, missing,
                         "evidence/WP04_RUNTIME_BINDING.json"))
    needs.append(qualify("sp.host.load", "OWNER_REGISTERED::sp_host_load",
                         probe_dist("sbl-v01", host_site), rows, missing,
                         "evidence/WP11_SP_HOST_MATRIX.json"))
    needs.append(qualify("openspec.change.validate", "OWNER_REGISTERED::openspec_validate",
                         probe_binary("openspec"), rows, missing, None))
    for dist in ("jsonschema", "pyyaml", "cryptography"):
        needs.append(qualify(f"python.dist:{dist}", "OWNER_REGISTERED::" + dist,
                             probe_dist(dist, host_site), rows, missing,
                             "evidence/WP11_SP_HOST_MATRIX.json"))

    summary = {}
    for n in needs:
        summary[n["state"]] = summary.get(n["state"], 0) + 1
    record = {
        "schema": "FHS.W1.WP17.CapBootQualification@1",
        "host": {"platform": platform.platform(), "python": sys.version.split()[0],
                 "executable": sys.executable},
        "registry": {"path": args.registry, "registry_rev": reg.get("registry_rev"),
                     "signed_rows": sum(1 for r in reg.get("runners") or []
                                        if (r.get("owner_signature") or {}).get("value")),
                     "not_registered": sorted(missing)[:40]},
        "needs": needs,
        "summary": summary,
        "claim_ceiling": "HOST_BOUND_PROBE_WITH_NAMED_GAPS",
        "not_claimed": ["installer privilege", "host install of a new occupant", "policy active",
                        "release"],
    }
    record["qualification_sha256"] = hashlib.sha256(
        json.dumps(record, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(out), "summary": summary,
                      "states": {n["need"]: n["state"] for n in needs},
                      "sha256": record["qualification_sha256"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
