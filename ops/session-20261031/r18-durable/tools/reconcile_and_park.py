"""branch_reconcile + parknative (the two items that were left "in_progress/pending").

branch_reconcile: two candidate branches now carry overlapping R18 content. This measures which tip
contains the other, and writes a SUPERSEDED_BY record for the one that is not the delivery tip. It does
NOT delete, tag, merge or force-push anything — deleting a branch to tidy up would destroy the other
session's history.

parknative: the 11 HOST_OP/RELEASE WPs cannot be executed on this authority. Rather than one blanket
sentence ("needs native bundle"), each gets a typed row with owner, next_legal_action and
resume_predicate derived from its own declared fields.
"""
import json
import pathlib
import subprocess

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
HGK = pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
DELIVERY = "candidate/r18-openspec-only"
OTHER = "candidate/r18-fhs-skeleton-spine-20261029"


def git(*args):
    p = subprocess.run(["git", "-C", str(HGK)] + list(args), capture_output=True, text=True, timeout=90)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def tip(ref):
    rc, out, err = git("rev-parse", "--verify", ref)
    return out if rc == 0 else None


t_del, t_oth = tip(DELIVERY), tip(OTHER)
rec = {"schema": "R18.BRANCH_RECONCILE/1", "delivery_tip": {"branch": DELIVERY, "sha": t_del},
       "other": {"branch": OTHER, "sha": t_oth}, "actions": []}

if t_del and t_oth:
    rc_a, _, _ = git("merge-base", "--is-ancestor", t_oth, t_del)
    rc_b, _, _ = git("merge-base", "--is-ancestor", t_del, t_oth)
    rec["other_is_ancestor_of_delivery"] = rc_a == 0
    rec["delivery_is_ancestor_of_other"] = rc_b == 0
    if rc_a == 0 and rc_b != 0:
        verdict = "DELIVERY_SUPERSEDES_OTHER"
        superseded, keeper = OTHER, DELIVERY
    elif rc_b == 0 and rc_a != 0:
        verdict = "OTHER_SUPERSEDES_DELIVERY"
        superseded, keeper = DELIVERY, OTHER
    elif rc_a == 0 and rc_b == 0:
        verdict = "IDENTICAL"
        superseded, keeper = None, DELIVERY
    else:
        verdict = "DIVERGED_NEEDS_OWNER_CHOICE"
        superseded, keeper = None, DELIVERY
    rec["verdict"] = verdict
    rec["keeper"] = keeper
    if superseded:
        rec["superseded"] = superseded
        rec["actions"].append("recorded SUPERSEDED_BY in the round dir; branch left intact (no delete, no tag, "
                              "no force-push)")
        (ROUND / "BRANCH_SUPERSEDED.json").write_text(json.dumps({
            "schema": "R18.BRANCH_SUPERSEDED/1",
            "branch": superseded,
            "superseded_by": keeper,
            "reason": ("same R18 OpenSpec/evidence content landed on both; the delivery tip is %s and carries "
                       "the signed canonical delegation and gate matrix" % DELIVERY),
            "retained_because": "deleting or rewriting it would destroy another session's history",
            "recorded_utc": None,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
else:
    rec["verdict"] = "BRANCH_ABSENT"
(ROUND / "receipts" / "BRANCH_RECONCILE.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1),
                                                          encoding="utf-8")
print("branch reconcile:", rec["verdict"], "| delivery", (t_del or "-")[:8], "| other", (t_oth or "-")[:8])

# ---------------------------------------------------------------- parknative
g = json.loads((ROUND / "subject" / "03_TESTS_AND_READBACK" / "wp_graph.json").read_text(encoding="utf-8"))
gated = [n for n in g["nodes"] if n.get("effect_class") in ("HOST_OP", "RELEASE")]
rows = []
for n in sorted(gated, key=lambda x: x["id"]):
    wp, ec = n["id"], n["effect_class"]
    rows.append({
        "wp": wp,
        "name": n.get("name"),
        "tier": n.get("tier"),
        "phase": n.get("phase"),
        "effect_class": ec,
        "first_fail": n.get("first_fail"),
        "output": n.get("output"),
        "owner": "ORIGINAL_OWNER_OF_BOUND_ARTIFACT (write_set BIND_EXACT_BY_ORIGINAL_OWNER) + HG-KSEOS Issuer",
        "next_legal_action": (
            "RELEASE class: dedicated authorisation only (owner_window dedicated scope sourcefreeze/release, "
            "TTL<=1h, max_ops<=4) plus the Issuer's release record; never delegated, never agent-signed"
            if ec == "RELEASE" else
            "assemble a per-WP native bundle (subject digest + WP id + typed expected effect + nonce), get it "
            "signed in an in-person owner window, then submit to the HGK Issuer for a PERMIT"),
        "resume_predicate": (
            "issuer_permit_present(wp=%s) AND owner_signed_bundle(subject=%s) AND nonce_unused" %
            (wp, "5a06d8dd…")),
        "status": "PARKED_TYPED",
        "not_run_reason": "no Issuer PERMIT; a candidate ECP or a signature over a payload does not substitute",
        "fabrication_guard": "this round must not claim PASS/NOT_REQUIRED for this WP",
    })
rec2 = {
    "schema": "R18.WP_NATIVE_PARK/1",
    "count": len(rows),
    "by_class": {"HOST_OP": sum(1 for r in rows if r["effect_class"] == "HOST_OP"),
                 "RELEASE": sum(1 for r in rows if r["effect_class"] == "RELEASE")},
    "rows": rows,
    "claim_ceiling": ("typed PARK: the gate refusal ERR_NATIVE_BUNDLE_REQUIRED was reproduced, so the WP is "
                      "blocked by authority, not by effort. Nothing here is a permit, a pass, or a waiver"),
}
(ROUND / "receipts" / "WP_NATIVE_PARK.json").write_text(json.dumps(rec2, ensure_ascii=False, indent=1),
                                                       encoding="utf-8")
print("parknative rows:", rec2["count"], rec2["by_class"])
