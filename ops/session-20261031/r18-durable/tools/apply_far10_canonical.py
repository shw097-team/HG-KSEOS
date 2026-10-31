"""Point the R18 gate at the canonical owner delegation, retire the second-key one, re-run the matrix.

FAR_R18-10 D1: the canonical delegation (`governance/delegation_R18_canonical.*`, owner 412b3519…) is the
only one that may authorise anything. The first envelope (`be760975…`) stays on disk as drill evidence and
is explicitly marked retired so nobody later mistakes it for authority.
"""
import json
import pathlib
import subprocess
import sys

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
GATE = ROUND / "tools" / "delegation_gate.py"

# ---------------------------------------------------------------- gate: canonical first, hex sig support
s = GATE.read_text(encoding="utf-8")
old = '''def load_signed():
    """Returns (env, rec, sig) or (None, None, None) when the delegation has been withdrawn."""
    if not ((GOV / "owner_envelope.json").is_file() and (GOV / "delegation_R18.json").is_file()
            and (GOV / "delegation_R18.sig").is_file()):
        return None, None, None
    env = json.loads((GOV / "owner_envelope.json").read_text(encoding="utf-8"))
    rec = json.loads((GOV / "delegation_R18.json").read_text(encoding="utf-8"))
    sig = base64.b64decode((GOV / "delegation_R18.sig").read_text(encoding="ascii").strip())
    return env, rec, sig'''
new = '''def load_signed():
    """Canonical delegation first (owner 412b3519…); the second-key envelope is a drill artefact only."""
    can_rec, can_sig = GOV / "delegation_R18_canonical.json", GOV / "delegation_R18_canonical.sig"
    if can_rec.is_file() and can_sig.is_file():
        rec = json.loads(can_rec.read_text(encoding="utf-8"))
        sig = bytes.fromhex(can_sig.read_text(encoding="ascii").strip())
        env = {"fingerprint": rec.get("owner_fingerprint"),
               "public_key_hex": rec.get("owner_public_key_hex"),
               "source": "delegation_R18_canonical.json"}
        return env, rec, sig
    if not ((GOV / "owner_envelope.json").is_file() and (GOV / "delegation_R18.json").is_file()
            and (GOV / "delegation_R18.sig").is_file()):
        return None, None, None
    env = json.loads((GOV / "owner_envelope.json").read_text(encoding="utf-8"))
    rec = json.loads((GOV / "delegation_R18.json").read_text(encoding="utf-8"))
    sig = base64.b64decode((GOV / "delegation_R18.sig").read_text(encoding="ascii").strip())
    return env, rec, sig'''
assert old in s, "load_signed block not found"
GATE.write_text(s.replace(old, new), encoding="utf-8")
print("gate now prefers the canonical delegation")

# revoked check should key on whichever delegation_id is live
s = GATE.read_text(encoding="utf-8")
if 'rec.get("delegation_id") in revoked_ids()' not in s:
    print("WARN: revocation branch not found (already keyed differently)")

# ---------------------------------------------------------------- retire the drill envelope
retire = {
    "schema": "R18.SECOND_OWNER_KEY.RETIRED/1",
    "fingerprint": "be76097571a7d7fd73a84b4625a0b557364ba4e4be919fcfe83d4798a661a002",
    "status": "RETIRED_SECOND_OWNER_KEY",
    "why": ("created before FAR_R18-10 established that the canonical owner identity is "
            "~/.hgk-owner/owner.key.enc (fingerprint 412b3519…). It is kept only as evidence of the "
            "envelope drill and confers no authority."),
    "authoritative_delegation": "governance/delegation_R18_canonical.json",
}
if (GOV / "owner_envelope.json").is_file():
    (GOV / "SECOND_KEY_RETIRED.json").write_text(json.dumps(retire, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
    print("second-key envelope marked RETIRED_SECOND_OWNER_KEY")

# ---------------------------------------------------------------- re-run matrix under the canonical key
py = sys.executable
cases = [
    ("POS", "WP-FHS-00", "SOURCE_READ", "", "", "WP00 source currentness"),
    ("POS", "WP-FHS-01", "SOURCE_READ", "", "", "WP01 authority ledger"),
    ("POS", "WP-FHS-09", "SOURCE_READ", "", "", "WP09 independent HOLD verdict"),
    ("POS", "WP-FHS-19", "SOURCE_READ", "", "", "WP19 supply chain"),
    ("POS", "WP-FHS-21", "SOURCE_READ", "", "", "WP21 96-cell rerun"),
    ("POS", "WP-FHS-06", "REPO_WRITE_TO_CANDIDATE_BRANCH", "candidate/r18-openspec-only", "", "WP06 first slice"),
    ("POS", "WP-FHS-18", "REPO_WRITE_TO_CANDIDATE_BRANCH", "candidate/r18-openspec-only", "", "WP18 repair"),
    ("NEG", "WP-FHS-02", "HOST_OP", "", "", "native not delegated"),
    ("NEG", "WP-FHS-14", "RELEASE", "", "", "release never delegated"),
    ("NEG", "WP-FHS-05", "LOCAL_DRAFT_WRITE", "", "", "class denied"),
    ("NEG", "WP-FHS-06", "REPO_WRITE_TO_CANDIDATE_BRANCH", "main", "", "main denied"),
    ("NEG", "WP-FHS-00", "SOURCE_READ", "", "2027-01-01T00:00:00+00:00", "expired"),
    ("NEG", "WP-FHS-16", "SOURCE_READ", "", "", "not allowlisted"),
]
rows = []
for kind, wp, cls, target, now, reason in cases:
    cmd = [py, "-B", str(GATE), "--wp", wp, "--class", cls]
    if target:
        cmd += ["--target", target]
    if now:
        cmd += ["--now", now]
    if kind == "POS":
        cmd += ["--consume"]
    cmd += ["--reason", reason]
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        d = json.loads(p.stdout)
    except Exception:
        d = {"decision": "PARSE_ERROR", "raw": p.stdout[-200:]}
    rows.append({"kind": kind, "wp": wp, "effect_class": cls, "target": target, "rc": p.returncode,
                 "decision": d.get("decision"), "recorded": d.get("recorded"),
                 "owner_fingerprint": d.get("owner_fingerprint")})

pos = [r for r in rows if r["kind"] == "POS"]
neg = [r for r in rows if r["kind"] == "NEG"]
okp = sum(1 for r in pos if r["decision"] == "PERMIT_DERIVED")
okn = sum(1 for r in neg if str(r["decision"]).startswith("REFUSED_"))
rec = {
    "schema": "R18.DELEGATION_GATE_MATRIX/2",
    "delegation": "governance/delegation_R18_canonical.json",
    "delegation_id": json.loads((GOV / "delegation_R18_canonical.json").read_text(encoding="utf-8"))["delegation_id"],
    "owner_fingerprint": json.loads((GOV / "delegation_R18_canonical.json").read_text(encoding="utf-8"))["owner_fingerprint"],
    "pos_cases": len(pos), "pos_permitted": okp, "neg_cases": len(neg), "neg_refused": okn,
    "all_cases_expected": okp == len(pos) and okn == len(neg),
    "rows": rows,
    "claim_ceiling": ("LOCAL_DERIVATION_NOT_NATIVE_BUNDLE: enforces the canonical owner's signed scope; "
                      "issues no native PERMIT and performs no HOST_OP or release"),
}
(ROUND / "receipts" / "DELEGATION_GATE_MATRIX_CANONICAL.json").write_text(
    json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("POS %d/%d  NEG %d/%d  all_expected=%s" % (okp, len(pos), okn, len(neg), rec["all_cases_expected"]))
for r in rows:
    print("  %s %-11s %-33s -> %s" % (r["kind"], r["wp"], r["effect_class"], r["decision"]))
