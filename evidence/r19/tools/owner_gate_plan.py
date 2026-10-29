"""Build the owner-gated registry revision plan for R19 (no authority is granted here).

WHY THIS FILE EXISTS
  A HOST_OP / REPO_WRITE / RELEASE work package can only obtain a native PERMIT when the protected
  registry at %ProgramData%\\HG-KSEOS\\native-admission\\registry.json already pre-authorises the exact
  request digest (native_admission.authorize -> REQUEST_SCOPE). That registry is written by an OWNER
  elevated step. An agent writing it would be issuing its own authority, so this tool stops at:

    * a dedicated execution root (git repo) with its exact head, root_identity and approved-file pins
    * the request digests for every gated work package
    * a plan JSON in the shape the owner installs, and the exact one-line elevated command

  It never writes the registry, never creates a key, never signs a reference.

OUTPUT  var/R19-FHS-20261029/owner_gate/REGISTRY_REVISION_PLAN.json
        var/R19-FHS-20261029/owner_gate/REQUEST_DIGESTS.json
        var/R19-FHS-20261029/owner_gate/OWNER_STEP.md
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
from ctypes import wintypes as w
from datetime import datetime, timezone

HGK_SRC = pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\src")
sys.path.insert(0, str(HGK_SRC))
from hg_kseos.util import canonical_json  # noqa: E402

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029")
EXEC_ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-NATIVE-EXEC")
B1_RUNNERS = pathlib.Path(r"C:\Projects\Agent_Workspace\var\B1-NATIVE-EXEC\runners")
REGISTRY = pathlib.Path(r"C:\ProgramData\HG-KSEOS\native-admission\registry.json")

# the work packages whose effect class is HOST_OP / REPO_WRITE / RELEASE (13 rows, measured R18)
GATED = ["WP-FHS-02", "WP-FHS-03", "WP-FHS-04", "WP-FHS-06", "WP-FHS-08", "WP-FHS-10", "WP-FHS-11",
         "WP-FHS-12", "WP-FHS-13", "WP-FHS-14", "WP-FHS-17", "WP-FHS-20", "WP-FHS-07"]
RUNNERS = ["native_e2e_lib.py", "native_issuer_runner.py", "native_receiver_runner.py",
           "host_lane_readback_runner.py", "loaded_identity_runner.py", "revoke_boundary_runner.py",
           "post_revoke_successor_runner.py"]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def root_identity(root: pathlib.Path) -> str:
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, w.LPVOID, w.DWORD, w.DWORD, w.HANDLE]
    kernel.CreateFileW.restype = w.HANDLE
    kernel.GetFileInformationByHandle.argtypes = [w.HANDLE, ctypes.c_void_p]
    h = kernel.CreateFileW(str(root), 0x80000000, 3, None, 3, 0x02200000, None)
    if h == w.HANDLE(-1).value:
        raise SystemExit("ERR_ROOT_HANDLE %s" % root)
    info = (ctypes.c_uint32 * 13)()
    try:
        if not kernel.GetFileInformationByHandle(w.HANDLE(h), ctypes.byref(info)):
            raise SystemExit("ERR_ROOT_HANDLE_ID")
    finally:
        kernel.CloseHandle(w.HANDLE(h))
    return f"{info[7]:08x}:{info[11]:08x}{info[12]:08x}"


def git(root: pathlib.Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise SystemExit(f"ERR_GIT {' '.join(args)}: {p.stderr.strip()[:300]}")
    return p.stdout.strip()


def build_root() -> dict:
    EXEC_ROOT.mkdir(parents=True, exist_ok=True)
    (EXEC_ROOT / "runners").mkdir(exist_ok=True)
    copied = []
    for name in RUNNERS:
        src = B1_RUNNERS / name
        if src.is_file():
            shutil.copy2(src, EXEC_ROOT / "runners" / name)
            copied.append(name)
    (EXEC_ROOT / "README.md").write_text(
        "# R19 native execution root\n\n"
        "Isolated root proposed for the R19 registry revision. It holds byte-identical copies of the\n"
        "approved runner set so an owner-elevated revision can pin them. Nothing here grants authority;\n"
        "the registry revision is the owner's step.\n", encoding="utf-8", newline="\n")
    if not (EXEC_ROOT / ".git").exists():
        git(EXEC_ROOT, "init", "-q")
        git(EXEC_ROOT, "config", "user.name", "r19-root")
        git(EXEC_ROOT, "config", "user.email", "r19-root@local")
    git(EXEC_ROOT, "add", "-A")
    p = subprocess.run(["git", "-C", str(EXEC_ROOT), "commit", "-q", "-m",
                        "R19 native exec root: approved runner copies for a proposed registry revision"],
                       capture_output=True, text=True)
    head = git(EXEC_ROOT, "rev-parse", "HEAD")
    approved = [{"path": f"runners/{n}", "sha256": sha(EXEC_ROOT / "runners" / n)} for n in copied]
    return {"root": str(EXEC_ROOT), "head": head, "root_identity": root_identity(EXEC_ROOT),
            "approved_files": approved, "commit_created": p.returncode == 0}


def requests(root: dict) -> list[dict]:
    out = []
    for wp in GATED:
        req = {
            "target_id": f"WO-R19-{wp.split('-')[-1]}-01",
            "taskspec_id": f"TS-R19-{wp.split('-')[-1]}-01",
            "writer": "HERMES-NATIVE-EXECUTOR",
            "root": root["root"],
            "base_head": root["head"],
            "permissions_json": '["read","write"]',
            "requirement_id": wp,
        }
        out.append({"wp": wp, "request": req,
                    "request_sha256": hashlib.sha256(canonical_json(req).encode("utf-8")).hexdigest()})
    return out


def main() -> int:
    out = ROUND / "owner_gate"
    out.mkdir(parents=True, exist_ok=True)
    root = build_root()
    reqs = requests(root)

    current = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
    policy = json.loads((pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\config\active-policy.json")
                         ).read_text(encoding="utf-8"))
    mission_source = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\SUBJECT_INTEGRITY.json")
    source_manifest_sha = hashlib.sha256(mission_source.read_bytes()).hexdigest() if mission_source.is_file() else None

    plan = {
        "schema": "HGK-OWNER-ENABLE-PLAN/1",
        "note": ("Proposed revision for owner review. The current registry was installed by an owner "
                 "elevated step (see registry.revision.installed_by); this plan reproduces that shape for "
                 "R19 and MUST be installed by the owner, not by an agent."),
        "mission_id": "FHS-MSC-R19-Skeleton-Spine-Implementation",
        "source_manifest_sha256": source_manifest_sha,
        "policy_sha256": policy["policy_digest"],
        "policy_epoch": int(current.get("policy_epoch", 0)) + 1,
        "max_ttl_seconds": 3600,
        "head": root["head"],
        "root": root["root"],
        "approved_files": root["approved_files"],
        "checker_os_sid": current.get("checker_os_sid"),
        "maker_os_sid": current.get("maker_os_sid"),
        "scope": {
            "database_path": str(pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db")),
            "head": root["head"],
            "root_identity": root["root_identity"],
            "task_kind": "B1_BOOTSTRAP_REPAIR",
            "lease_generation": 0,
            "request_sha256": [r["request_sha256"] for r in reqs],
        },
        "task_kinds": {"B1_BOOTSTRAP_REPAIR": {
            "state": "REGISTERED",
            "source_sha256": source_manifest_sha,
            "operations": ["create_taskspec", "create_workorder"],
            "registered_at": datetime.now(timezone.utc).date().isoformat(),
            "registered_by": "owner reviewed revision (plan sha pinned into the registry)",
        }},
        "approval_source": ("OWNER instruction 2026-10-29: pre-authorise the R19 gated work packages "
                            "(13 rows) so one bounded reference window can admit them natively"),
        "supersedes": {"registry_sha256": sha(REGISTRY) if REGISTRY.is_file() else None,
                       "policy_epoch": current.get("policy_epoch")},
    }
    (out / "REGISTRY_REVISION_PLAN.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "REQUEST_DIGESTS.json").write_text(json.dumps(reqs, ensure_ascii=False, indent=1), encoding="utf-8")

    plan_sha = sha(out / "REGISTRY_REVISION_PLAN.json")
    md = f"""# OWNER STEP — registry revision for R19 (NOT executed by the agent)

**Why you and not me**: `native_admission.authorize()` refuses with `REQUEST_SCOPE` unless the exact
request digest is already in the protected registry's `scope.request_sha256`. Writing that registry is
the act of granting native authority. An agent doing it would be issuing its own permit — refused by
design, so this round stops here and hands you a pinned plan instead.

**Measured facts (this round, this machine)**

| item | value |
|---|---|
| current registry | `{REGISTRY}` sha256 `{plan['supersedes']['registry_sha256']}` |
| current policy_epoch | `{current.get('policy_epoch')}` → proposed `{plan['policy_epoch']}` |
| dedicated exec root | `{root['root']}` |
| exec root HEAD | `{root['head']}` |
| root_identity | `{root['root_identity']}` |
| approved files | {len(root['approved_files'])} runner pins (sha256 in the plan) |
| gated work packages | {len(reqs)} request digests |

**The one command (elevated PowerShell, you run it)**

```powershell
# 1. review the bytes you are about to authorise
Get-FileHash -Algorithm SHA256 '{out / "REGISTRY_REVISION_PLAN.json"}'
# 2. install (same elevated-step shape as the current registry.revision 15)
#    the installer is the owner's; it must pin plan_sha256='{plan_sha}'
```

**What this does NOT do**: it does not sign the three reference kinds (`source_freeze`, `task_kind`,
`oracle_ratification`) — those are minted per operation from the owner key through
`owner_window.py` (one passphrase, one bounded window), and `authorize()` additionally requires the
canonical DB (`C:\\Projects\\Agent_Workspace\\HG-KSEOS\\var\\shared-spine\\hg-kseos.db`) and a lease
generation. After the revision is installed, the remaining chain is mechanical and the agent can run it.

**Claim ceiling**: a proposed plan. No permit has been issued, no reference signed, no native effect run.
"""
    (out / "OWNER_STEP.md").write_text(md, encoding="utf-8", newline="\n")
    print(json.dumps({"root": root["root"], "head": root["head"], "root_identity": root["root_identity"],
                      "approved_files": len(root["approved_files"]), "requests": len(reqs),
                      "plan_sha256": plan_sha, "policy_epoch": plan["policy_epoch"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
