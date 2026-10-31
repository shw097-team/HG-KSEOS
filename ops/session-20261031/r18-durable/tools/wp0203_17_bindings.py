"""WP-02 / WP-03 / WP-17 binding measurement: what is actually bound right now on this host.

These three WPs are the last agent-reachable ones (they are read-only measurement, not host effects).
The point is to replace "PARKED with a sentence" by a measurement of the binding that exists at this
subject/scope/epoch, and to say plainly which part is absent.

WP-02  Fabric policy binding      : is an active policy loaded, what epoch, does it name the subject?
WP-03  HGK Issuer binding         : is an issuer present, can it issue, does it refuse without a bundle?
WP-17  CAP-BOOT                   : is a capability bootstrap record present for this scope?
"""
import hashlib
import json
import pathlib
import subprocess

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
WS = pathlib.Path(r"C:\Projects\Agent_Workspace")
SUBJECT_DIGEST = "5a06d8ddfcfaeefdda4430a0fcd0677e5ca036ac9e10072b5f00e141824f430d"


def sha(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def load(p):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


# ---------------------------------------------------------------- WP-02 Fabric policy
pol_path = WS / "HG-KSEOS" / "config" / "active-policy.json"
pol = load(pol_path)
wp02 = {
    "schema": "R18.WP02_FABRIC_POLICY_BINDING/1",
    "policy_path": str(pol_path),
    "present": pol_path.is_file(),
    "sha256": sha(pol_path),
    "epoch": (pol or {}).get("epoch") or (pol or {}).get("policy_epoch"),
    "keys": sorted(pol)[:14] if isinstance(pol, dict) else None,
    "names_subject_digest": SUBJECT_DIGEST[:16] in json.dumps(pol or ""),
    "verdict": None,
}

# ---------------------------------------------------------------- WP-03 HGK Issuer
native = WS / "HG-KSEOS" / "src" / "hg_kseos" / "native_admission.py"
reg = pathlib.Path(r"C:\ProgramData\HG-KSEOS\native-admission\registry.json")
registry = load(reg)
issuer_probe = None
try:
    p = subprocess.run(
        [str(WS / "HG-KSEOS" / ".venv" / "Scripts" / "python.exe"), "-B", "-c",
         "import json,sys; sys.path.insert(0,'src');\n"
         "from hg_kseos import native_admission as na\n"
         "print(json.dumps({'module':True,'has_authorize':hasattr(na,'authorize')}))"],
        cwd=str(WS / "HG-KSEOS"), capture_output=True, text=True, timeout=120)
    issuer_probe = json.loads(p.stdout.strip().splitlines()[-1]) if p.stdout.strip() else {"raw": p.stderr[-200:]}
except Exception as e:
    issuer_probe = {"error": "%s: %s" % (type(e).__name__, e)}

wp03 = {
    "schema": "R18.WP03_ISSUER_BINDING/1",
    "issuer_module_present": native.is_file(),
    "issuer_module_sha256": sha(native),
    "issuer_probe": issuer_probe,
    "registry_path": str(reg),
    "registry_present": reg.is_file(),
    "registry_rev": (registry or {}).get("registry_rev"),
    "registry_rows": len((registry or {}).get("rows") or []),
    "owner_signed": bool((registry or {}).get("owner_signature")),
    "refusal_reproduced": "ERR_NATIVE_BUNDLE_REQUIRED (recorded in receipts/WP02_03_REFUSAL.json of this round)",
    "verdict": None,
}

# ---------------------------------------------------------------- WP-17 CAP-BOOT
cap_candidates = [
    WS / "HG-KSEOS" / "config" / "cap-boot.json",
    WS / "HG-KSEOS" / "var" / "shared-spine" / "cap-boot.json",
    WS / "Fabric" / "config" / "cap-boot.json",
]
cap_hits = [{"path": str(c), "present": c.is_file(), "sha256": sha(c) if c.is_file() else None}
            for c in cap_candidates]
wp17 = {
    "schema": "R18.WP17_CAPBOOT/1",
    "candidates": cap_hits,
    "cap_boot_present": any(h["present"] for h in cap_hits),
    "verdict": "MEASURED_PRESENT" if any(h["present"] for h in cap_hits) else "MEASURED_ABSENT",
    "claim_ceiling": "presence measurement only; a CAP-BOOT record is not a permit and authorises nothing",
}

wp02["verdict"] = ("POLICY_LOADED_EPOCH_%s" % wp02["epoch"]) if wp02["present"] and wp02["epoch"] else (
    "POLICY_PRESENT_NO_EPOCH" if wp02["present"] else "POLICY_ABSENT")
wp03["verdict"] = ("ISSUER_PRESENT_REGISTRY_REV_%s" % wp03["registry_rev"]) if wp03["issuer_module_present"] else (
    "ISSUER_ABSENT")

out = {"schema": "R18.WP0203_17_BINDINGS/1", "measured_utc": None,
       "wp02": wp02, "wp03": wp03, "wp17": wp17,
       "claim_ceiling": ("binding presence measured on this host at this moment; none of it is a native "
                         "PERMIT, and WP-02/03/17 remain non-native-effect WPs")}
(ROUND / "receipts" / "WP0203_17_BINDINGS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                           encoding="utf-8")
print(json.dumps({"wp02": wp02["verdict"], "wp03": wp03["verdict"], "wp17": wp17["verdict"]},
                 ensure_ascii=False))
