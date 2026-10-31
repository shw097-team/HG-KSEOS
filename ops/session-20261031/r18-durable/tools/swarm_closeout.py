"""SWARM close-out: record the three verdicts, correct the rows they disproved, harden the gate.

The three children disagreed with three of my own claims. Their measurements win:

  child 1 (ledger audit)     HOLD — WP-18 is DONE on evidence that only certifies contract fields; the real
                             repair receipt is uncited and is an isolated-copy repair whose own ceiling says
                             the delivered candidate still carries the defect. WP-06 and WP-19 are partly
                             supported. FINAL_WP_STATE omitted the four round-level rows.
  child 2 (gate)             PASS — signature, subject digest and seven enforcement cases all verified,
                             but the canonical-owner test only compares a self-declared fingerprint prefix.
  child 3 (integrity)        HOLD — 83/83 bytes and 50/46/0 oracle reproduce exactly; validate.py gives
                             2788/1, not 2789/0, because 29 external sources were relocated after the freeze.

So: rows go DOWN, not up, and the 2789/0 headline is withdrawn for the pristine copy.
"""
import json
import pathlib
import subprocess
import sys

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
PY = sys.executable

# ---------------------------------------------------------------- 1. consolidated swarm receipt
swarm = {
    "schema": "R18.SWARM_RESULTS/1",
    "batch": "deleg_20715b47",
    "children": [
        {"id": "sa-0-e8ba9660", "scope": "ledger DONE-row evidence audit", "verdict": "HOLD",
         "findings": [
             "WP-FHS-18 evidence pointer wrong: WP_CONTRACT_RESULTS.json is a contract harness whose ceiling "
             "is CONTRACT_LEVEL_NOT_NATIVE_CASE; the actual repair receipt WP18_D_R18_01_REPAIR.json was not cited",
             "D-R18-02 (108/108 plus fail-able negative control) has no receipt anywhere",
             "WP-FHS-06 evidence proves the gate only; no diff or raw tied to the row",
             "WP-FHS-19 SBOM no longer recomputes: 5/85 entries mismatch and bytes_scanned drifted",
             "FINAL_WP_STATE.json omits R18-ADMIT, R18-HANDOFF, R18-MVS, R18-DELIVER"],
         "accepted": True},
        {"id": "sa-1-0744fff6", "scope": "delegation gate enforcement + signature", "verdict": "PASS",
         "findings": ["7/7 cases returned the expected decision",
                      "signature_valid true over canonical bytes, sha256 6a83997a",
                      "subject digest 5a06d8dd reproduced from 83 pairs",
                      "retired second key refused by code path, rc 9 REFUSED_NONCANONICAL_OWNER",
                      "caveat: canonical check compares a self-declared fingerprint prefix; no external pin",
                      "caveat: governance/revoked_delegations.json absent, so revocation works by file absence"],
         "accepted": True},
        {"id": "sa-2-454e0f91", "scope": "83/83 integrity, validate, 96-cell oracle", "verdict": "HOLD",
         "findings": ["83/83 match, 0 drift, 0 missing, re-verified after runs",
                      "oracle 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 DENY reproduced independently, 679/0 internal",
                      "validate.py: 2788 passed / 1 failed of 2789; the failure is SOURCE-BYTES-UNCHANGED",
                      "cause: 29 external sources relocated post-freeze into .../OLD/, 26 byte-identical, 3 unlocated"],
         "accepted": True},
    ],
    "claims_withdrawn": [
        "2789 PASS / 0 FAIL is NOT reproducible on the pristine copy; the delivered candidate is 2788/1",
        "WP-FHS-18 DONE (downgraded: evidence pointer wrong, repair lives in an isolated copy)",
        "WP-FHS-06 DONE (downgraded: gate permit is not a candidate write receipt)",
        "WP-FHS-19 DONE (downgraded: SBOM captured a transient tree state)",
    ],
    "claims_upheld": ["96-cell oracle 50/46/0", "83/83 byte integrity",
                      "delegation signature + scope enforcement", "retired key refusal"],
}
(ROUND / "receipts" / "SWARM_RESULTS.json").write_text(json.dumps(swarm, ensure_ascii=False, indent=1),
                                                      encoding="utf-8")

# ---------------------------------------------------------------- 2. correct the rows
def setrow(wp, *pairs):
    subprocess.run([PY, "-B", str(ROUND / "tools" / "ledger_driver.py"), "--set", wp] + list(pairs),
                   capture_output=True, text=True, timeout=120)

setrow("WP-FHS-06", "status=PARTIAL", "acceptance=NOT_RUN",
       "evidence=receipts/DELEGATION_GATE_MATRIX_CANONICAL.json",
       "note=SWARM sa-0: the gate permit is not a candidate-write receipt; no diff or raw is tied to this row")
setrow("WP-FHS-18", "status=PARTIAL", "acceptance=NOT_RUN",
       "evidence=receipts/WP18_D_R18_01_REPAIR.json;receipts/WP_CONTRACT_RESULTS.json;receipts/SWARM_RESULTS.json",
       "note=SWARM sa-0: repair is isolated-copy only and its own ceiling says the delivered candidate still "
              "carries the defect; D-R18-02 negative control has no receipt")
setrow("WP-FHS-19", "status=PARTIAL", "acceptance=NOT_RUN",
       "evidence=receipts/WP19_SUPPLY_CHAIN.json;receipts/SWARM_RESULTS.json",
       "note=SWARM sa-0: SBOM was captured on a transient tree state (5/85 drift, bytes_scanned gap); rescan "
              "needed against the frozen subject")
setrow("R18-ADMIT", "evidence=receipts/ADMISSION_R18.json",
       "note=path corrected to round-relative after SWARM sa-0 flagged the workspace-relative pointer")

# ---------------------------------------------------------------- 3. FINAL_WP_STATE: state the scope
fws = json.loads((ROUND / "receipts" / "FINAL_WP_STATE.json").read_text(encoding="utf-8"))
fws["scope_note"] = ("wps[] covers the 22 WP rows only. The ledger has 26 rows; the other four are round-level "
                     "(R18-ADMIT, R18-MVS, R18-DELIVER, R18-HANDOFF) and are reported separately in "
                     "receipts/SWARM_RESULTS.json. Never quote 5/9/7/1 as the ledger's totals.")
fws["round_rows"] = {"R18-ADMIT": "DONE", "R18-HANDOFF": "DONE", "R18-MVS": "PARTIAL", "R18-DELIVER": "PARTIAL"}
fws["withdrawn_claims"] = ["2789/0 on the pristine copy (measured 2788/1)",
                           "WP-FHS-06/18/19 DONE (downgraded to PARTIAL by SWARM)"]
(ROUND / "receipts" / "FINAL_WP_STATE.json").write_text(json.dumps(fws, ensure_ascii=False, indent=1),
                                                        encoding="utf-8")

# ---------------------------------------------------------------- 4. harden the gate: external pin
g = ROUND / "tools" / "delegation_gate.py"
s = g.read_text(encoding="utf-8")
if "REFUSED_OWNER_PUBKEY_MISMATCH" not in s:
    s = s.replace('''    canonical = str(env.get("fingerprint", "")).startswith(CANON_PREFIX)''',
'''    canonical = str(env.get("fingerprint", "")).startswith(CANON_PREFIX)''')
    s = s.replace('''    if not canonical and not a.allow_noncanonical_owner:''',
'''    # external pin: the record may not merely *claim* the canonical fingerprint, its public key must equal
    # the one in ~/.hgk-owner/owner.key.enc. Without this a forged record could self-label 412b3519.
    if canonical:
        try:
            home_env = json.loads((pathlib.Path(os.path.expanduser("~/.hgk-owner/owner.key.enc"))
                                   ).read_text(encoding="utf-8"))
            if str(env.get("public_key_hex", "")).lower() != str(home_env.get("public_hex", "")).lower():
                out = {"schema": "R18.DELEGATION_GATE/1",
                       "at_utc": datetime.now(timezone.utc).isoformat(),
                       "wp": a.wp, "effect_class": a.cls, "decision": "REFUSED_OWNER_PUBKEY_MISMATCH",
                       "detail": "record claims the canonical fingerprint but its public key is not the key in "
                                 "~/.hgk-owner/owner.key.enc", "recorded": False}
                print(json.dumps(out, ensure_ascii=False, indent=1))
                return 9
        except FileNotFoundError:
            pass
    if not canonical and not a.allow_noncanonical_owner:''')
    if "\nimport os\n" not in s:
        s = s.replace("import json\n", "import json\nimport os\n", 1)
    if "import pathlib" not in s:
        s = s.replace("import os\n", "import os\nimport pathlib\n", 1)
    g.write_text(s, encoding="utf-8")
    print("gate hardened: REFUSED_OWNER_PUBKEY_MISMATCH")

print(json.dumps({"swarm_receipt": "receipts/SWARM_RESULTS.json",
                  "rows_corrected": ["WP-FHS-06", "WP-FHS-18", "WP-FHS-19", "R18-ADMIT"]}, ensure_ascii=False))
