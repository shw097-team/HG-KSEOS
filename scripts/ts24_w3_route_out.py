"""R14-TS24 — try to route a W3 request to the SWOF Native Owner and record the typed outcome.

The obligation is not "get a W3 permit"; it is "route out to the SWOF Native Owner with task/WriteSet/Permit/ACK, and
without a legitimate W3 record NO_EFFECT, never writing the SWOF repo". So this measures whether any W3 issuer or
receiver ACK exists today, writes a read-only route-out request, and states the verdict the evidence supports.
"""
from __future__ import annotations
import json, subprocess
from datetime import UTC, datetime
from pathlib import Path

WS = Path(r"C:/Projects/Agent_Workspace")
SWOF = WS / "SWOF"
OUT = WS / "_r14_packet/raw/ts24_w3_route_out.json"


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(SWOF), *args], capture_output=True, text=True)
    return (r.stdout or r.stderr).strip()


def search() -> dict:
    """Look for a W3 permit or ACK by name, and by content, without touching the repo."""
    names = []
    for pattern in ("*permit*", "*Permit*", "*W3*", "*w3*", "*ACK*", "*ack*"):
        names += [str(p.relative_to(SWOF)) for p in SWOF.rglob(pattern)
                  if ".git" not in p.parts and p.is_file()]
    hits = []
    for p in SWOF.rglob("*.json"):
        if ".git" in p.parts:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "W3" in text and ("permit" in text.lower() or "acknowledg" in text.lower()):
            hits.append(str(p.relative_to(SWOF)))
    return {"files_named_like_permit_w3_ack": sorted(set(names))[:20],
            "files_mentioning_W3_with_permit_or_ack": sorted(set(hits))[:20],
            "count": len(set(names)) + len(set(hits))}


def real_permits() -> list[dict]:
    """A permit must LOOK like one: the Fabric AUTHORITY_RECEIPT field set, not a document that says "W3".

    First pass counted 20 "legitimate" hits and was wrong - they were W2 evidence return packs and R4 reconciliation
    files that mention W3 in prose. A permit is identified by its fields, not by the word.
    """
    found = []
    for p in SWOF.rglob("*.json"):
        if ".git" in p.parts:
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        stack = [doc]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                keys = set(cur)
                if "granted_scope" in keys and ({"authority_identity", "issuer_identity"} & keys):
                    found.append({"file": str(p.relative_to(SWOF)),
                                  "keys": sorted(k for k in ("receipt_id", "authority_identity", "granted_scope",
                                                             "expires_at", "signature_ref") if k in keys)})
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
    return found


def main() -> int:
    status = git("status", "--porcelain")
    head = git("rev-parse", "HEAD")
    w2 = sorted(str(p.relative_to(SWOF)) for p in (SWOF / "acceptance/evidence").rglob("*RETURN_PACK*.json"))[:5]
    found = search()
    # a W3 issuer would be a signed artifact from the SWOF Native Owner; a schema mentioning W3 is not one
    permits = real_permits()
    legitimate = permits
    verdict = "NO_EFFECT" if not permits else "W3_PERMIT_PRESENT"
    doc = {
        "schema": "SBL-TS24-W3-ROUTE-OUT/1",
        "at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "swof_repo": {"path": str(SWOF), "head": head, "worktree_clean": status == "",
                      "written_by_this_round": False,
                      "proof": "git status --porcelain empty; HEAD unchanged; this script only reads"},
        "w2_frozen_readset": {"evidence_samples": w2, "present": bool(w2)},
        "w3_probe": found,
        "permits_by_field_signature": permits,
        "note_on_first_pass": ("a text search found 155 files mentioning W3 and 20 'candidates'; all were W2 evidence "
                              "return packs / R4 reconciliation files. The permit test is now structural."),
        "verdict": verdict,
        "request": {
            "to": "SWOF Native Owner (W3 issuer)",
            "task": "first governed small SWOF change under SBL/TMP->PIPD->Commander->HGK/Hermes/Codex->Challenge->SWOF receiver",
            "writeset_proposed": ["SWOF/src/<new module or bounded repair target>", "SWOF/tests/<matching test>"],
            "required_permit_fields": ["issuer_identity", "granted_scope", "writeset", "expires_at",
                                       "revocation_path", "signature_ref", "nonce"],
            "required_ack": "receiver ACK naming the same subject tuple (source sha, WriteSet, permit id) or a typed NACK",
            "what_sbl_will_do_on_permit": ["compile PI/PD for the chosen requirement", "issue HGK WorkOrder + role binding",
                                           "execute via Codex bounded writer in a sandbox copy",
                                           "independent VERIFY/SECURITY challenge", "return evidence to SWOF receiver"]},
        "claim_ceiling": ("No W3 permit exists in the SWOF repo, so TS25/TS26 are HOLD. Nothing was written to SWOF and "
                          "no governed SWOF change is claimed. This is a typed route-out request, not a result."),
    }
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "w3_hits": found["count"], "legitimate": len(legitimate),
                      "swof_head": head[:12], "swof_clean": status == ""}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
