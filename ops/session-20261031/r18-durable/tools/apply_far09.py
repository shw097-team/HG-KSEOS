"""Apply FAR_R18-09 rulings D2/D3/D4 and emit the D5 evidence indexes.

D2  remove the C4 false positive (write_set is a constant across all 22 nodes, not a class signal)
D3  revocation must be a typed refusal, and a denylist must actually exist
D4  the gate must be structural: a ledger DONE transition for a WP needs a consumed permit
D5  the three repos that already have an evidence/ convention get their round index
"""
import json
import pathlib
import re

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
WS = pathlib.Path(r"C:\Projects\Agent_Workspace")

# ---------------------------------------------------------------- D2: harness
h = ROUND / "tools" / "wp_contract_harness.py"
s = h.read_text(encoding="utf-8")
old = '''    ws = n.get("write_set") or []
    ec = n.get("effect_class")
    if ec == "SOURCE_READ":
        checks["C4_write_set_coherent"] = ws == []
    elif ec == "LOCAL_DRAFT_WRITE":
        checks["C4_write_set_coherent"] = "BIND_EXACT_BY_ORIGINAL_OWNER" not in ws
    else:
        checks["C4_write_set_coherent"] = True'''
new = '''    ws = n.get("write_set") or []
    ec = n.get("effect_class")
    # write_set is a CONSTANT in this DAG: 17 nodes carry ["BIND_EXACT_BY_ORIGINAL_OWNER"] (a constraint on
    # the eventual owner binding), 5 carry []. Treating that constant as a per-class anomaly invented a
    # failure for LOCAL_DRAFT_WRITE only. The only real constraint is: reads write nothing.
    if ec == "SOURCE_READ":
        checks["C4_write_set_coherent"] = ws == []
    else:
        checks["C4_write_set_coherent"] = ws in ([], ["BIND_EXACT_BY_ORIGINAL_OWNER"])'''
assert old in s, "C4 block not found"
h.write_text(s.replace(old, new), encoding="utf-8")

# ---------------------------------------------------------------- D3: gate revocation
g = ROUND / "tools" / "delegation_gate.py"
s = g.read_text(encoding="utf-8")
s = s.replace('''EFFECTS = GOV / "delegation_effects.jsonl"''',
              '''EFFECTS = GOV / "delegation_effects.jsonl"
DENYLIST = GOV / "revoked_delegations.json"''')
s = s.replace('''def load_signed():
    env = json.loads((GOV / "owner_envelope.json").read_text(encoding="utf-8"))
    rec = json.loads((GOV / "delegation_R18.json").read_text(encoding="utf-8"))
    sig = base64.b64decode((GOV / "delegation_R18.sig").read_text(encoding="ascii").strip())
    return env, rec, sig''',
'''def load_signed():
    """Returns (env, rec, sig) or (None, None, None) when the delegation has been withdrawn."""
    if not ((GOV / "owner_envelope.json").is_file() and (GOV / "delegation_R18.json").is_file()
            and (GOV / "delegation_R18.sig").is_file()):
        return None, None, None
    env = json.loads((GOV / "owner_envelope.json").read_text(encoding="utf-8"))
    rec = json.loads((GOV / "delegation_R18.json").read_text(encoding="utf-8"))
    sig = base64.b64decode((GOV / "delegation_R18.sig").read_text(encoding="ascii").strip())
    return env, rec, sig


def revoked_ids():
    if not DENYLIST.is_file():
        return set()
    try:
        return set(json.loads(DENYLIST.read_text(encoding="utf-8")).get("revoked", []))
    except Exception:
        return set()''')

s = s.replace('''    env, rec, sig = load_signed()
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["public_key_hex"]))''',
'''    env, rec, sig = load_signed()
    if env is None:
        out = {"schema": "R18.DELEGATION_GATE/1",
               "at_utc": datetime.now(timezone.utc).isoformat(),
               "wp": a.wp, "effect_class": a.cls, "target": a.target,
               "decision": "REFUSED_REVOKED",
               "detail": "no delegation on disk: withdrawal is effective immediately",
               "recorded": False}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 8
    if rec.get("delegation_id") in revoked_ids():
        out = {"schema": "R18.DELEGATION_GATE/1",
               "at_utc": datetime.now(timezone.utc).isoformat(),
               "wp": a.wp, "effect_class": a.cls, "target": a.target,
               "delegation_id": rec.get("delegation_id"),
               "decision": "REFUSED_REVOKED",
               "detail": "delegation_id is in governance/revoked_delegations.json",
               "recorded": False}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 8
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["public_key_hex"]))''')
g.write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- D4: ledger hook
ld = ROUND / "tools" / "ledger_driver.py"
s = ld.read_text(encoding="utf-8")
hook = '''

def _permit_for(wp):
    """A WP may only reach DONE if the owner delegation actually authorised an effect on it."""
    import json as _j
    eff = ROUND / "governance" / "delegation_effects.jsonl"
    if not eff.is_file():
        return None, "ERR_NO_DELEGATION_EFFECTS"
    hits = []
    for line in eff.read_text(encoding="utf-8").splitlines():
        try:
            ev = _j.loads(line)
        except Exception:
            continue
        if ev.get("wp") == wp and ev.get("decision") == "PERMIT_DERIVED" and ev.get("recorded"):
            hits.append(ev)
    if not hits:
        return None, "ERR_NO_DERIVED_PERMIT"
    return hits[-1], None
'''
if "_permit_for" not in s:
    s = s.replace("\ndef main(", hook + "\n\ndef main(", 1)
    s = s.replace('''    if args.set:''', '''    if args.set:
        _wpid, _kv = args.set[0], args.set[1:]
        _status = None
        for item in _kv:
            if item.startswith("status="):
                _status = item.split("=", 1)[1].upper()
        if _status == "DONE":
            _permit, _err = _permit_for(_wpid)
            if _err:
                print("REFUSED %s: %s  (a DONE row needs a consumed owner-delegation permit; "
                      "run tools/delegation_gate.py --wp %s --class <class> --consume first)" % (_wpid, _err, _wpid))
                return 9
            print("PERMIT %s consumed_at=%s delegation=%s" % (_wpid, _permit.get("at_utc"), _permit.get("delegation_id")))''', 1)
    ld.write_text(s, encoding="utf-8")

print("patched: harness C4, gate revocation, ledger permit hook")

# ---------------------------------------------------------------- D5: evidence indexes
idx = ROUND / "EVIDENCE_INDEX_R18.md"
body = idx.read_text(encoding="utf-8") if idx.is_file() else None
if body is None:
    rows = []
    for r in sorted((ROUND / "receipts").glob("*.json")):
        rows.append("- `receipts/%s`" % r.name)
    body = ("# R18 evidence index — FHS-MSC Skeleton+Spine\n\n"
            "Round: `R18-FHS-SKELETON-SPINE-20261029`  Subject digest: `5a06d8dd…` (83 declared entries)\n\n"
            "Claim ceiling: locally measured, candidate-only. No native PERMIT, no release, no acceptance.\n\n"
            "## Receipts\n\n" + "\n".join(rows) + "\n")
    idx.write_text(body, encoding="utf-8")

targets = [
    (WS / "Fabric" / "evidence" / "EVIDENCE_R18_FHS_MSC_SKELETON_SPINE.md", "Fabric"),
    (WS / "SBL" / "evidence" / "EVIDENCE_R18_FHS_MSC_SKELETON_SPINE.md", "SBL"),
    (WS / "HG-KSEOS" / "evidence" / "EVIDENCE_R18_FHS_MSC_SKELETON_SPINE.md", "HG-KSEOS"),
]
for path, repo in targets:
    if path.parent.is_dir():
        path.write_text(
            "# R18 evidence index (%s)\n\n"
            "Round `R18-FHS-SKELETON-SPINE-20261029` against "
            "`FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`.\n\n"
            "Authoritative copies live outside this repo, in the round directory\n"
            "`var/R18-FHS-SKELETON-SPINE-20261029/` (not published: no raw, DB, keys or credentials).\n\n"
            "## What was measured\n\n"
            "- source/manifest/ZIP/DAG currentness: 82 manifest rows, 83 checksum entries, 84 ZIP members\n"
            "  22 nodes, 36 typed edges (`DATA_OR_ADMISSION` 34, `CAPABILITY` 2 — no acceptance edges)\n"
            "- candidate validator re-run: 2789 PASS / 0 FAIL after a data-side pin repair (was 2788/1)\n"
            "- 96-cell oracle re-run: 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL; 192 negative fixtures refused\n"
            "- independent challenge lane (`gpt-6.1-sol`, rank 2, nonce-bound): verdict **HOLD**\n"
            "- WP contract harness: 6 mechanical checks per WP over the DAG's own declared fields\n"
            "- owner delegation signed and enforced: 7 WPs permitted, 6 negative controls refused\n\n"
            "## What is NOT claimed\n\n"
            "No native bundle, no Issuer PERMIT for HOST_OP/RELEASE, no acceptance signature, no release.\n"
            "The independent verdict is HOLD because fixture consistency is not execution provenance.\n\n"
            "Reading order: `FAR_R18_07_STOP_REVIEW_AND_OWNER_ENVELOPE.md`, `FAR_R18_09_CLAIM_RECHECK.md`,\n"
            "`STATUS_HANDOFF.md`, `RESUME_HERE.md` in the round directory.\n",
            encoding="utf-8")
        print("evidence index ->", path)
    else:
        print("SKIP (no evidence dir):", path.parent)
