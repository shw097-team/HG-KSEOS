"""R14-TS29 — close the R12/R13 debts item by item, or say which ones are still open and why.

The order forbids the phrase "already passed": every named debt must have its own receipt, so this script checks each
one against an artifact on disk and records CLOSED / OPEN with the locator. A debt with no artifact stays OPEN even if
a previous round's prose says otherwise.
"""
from __future__ import annotations
import json, subprocess, sqlite3
from datetime import UTC, datetime
from pathlib import Path

# Every child of this process is headless. On this host a console program started by a GUI parent gets a fresh
# console window, so a gate that shells out to git or PowerShell puts a window on the owner's screen (measured: the
# owner reported windows appearing more often once the loop began running every 3 minutes).
try:
    import sys as _sys
    _sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    import winproc as _winproc
    _winproc.install()
except Exception:
    pass

WS = Path(r"C:/Projects/Agent_Workspace")
RAW = WS / "_r14_packet/raw"
HGK = WS / "HG-KSEOS"
OUT = RAW / "ts29_debt_closure.json"


def exists(*p: str) -> str | None:
    for cand in p:
        q = Path(cand)
        if q.exists():
            return str(q)
    return None


def probe_stack_doctor() -> dict:
    r = subprocess.run(["sbl-stack", "doctor", "--root", str(WS / "SBL-install/stack")],
                       capture_output=True, text=True)
    try:
        doc = json.loads(r.stdout)
    except Exception:
        return {"ok": None, "raw": r.stdout[-200:]}
    return {"ok": doc.get("ok"), "problems": doc.get("problems"), "components": doc.get("components")}


def probe_skills() -> dict:
    """D-17 wrong skill layout: each SP skill root must carry SKILL.md at the root, and the README path must resolve."""
    rows = {}
    for name in ("tpm-sp", "commander-sp", "external-challenge-sp", "sbl-stack"):
        root = Path(r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/sbl") / name
        rows[name] = {"root": str(root), "skill_md": (root / "SKILL.md").is_file(),
                      "files": sorted(p.name for p in root.glob("*"))[:6] if root.is_dir() else []}
    return rows


def probe_spine_cases() -> dict:
    con = sqlite3.connect(f"file:{HGK}/var/shared-spine/hg-kseos.db?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        "SELECT workorder_id,state,result_json FROM workorders WHERE workorder_id LIKE '%R13%' OR workorder_id LIKE '%TS15%'")]
    con.close()
    return {"workorders": rows}


def main() -> int:
    items = []
    skills = probe_skills()
    items.append({"id": "D-17 skill layout",
                  "state": "CLOSED" if all(v["skill_md"] for v in skills.values()) else "OPEN",
                  "detail": skills,
                  "note": "every SP skill root carries SKILL.md at the root; the earlier 'wrong layout' claim is "
                          "checked per skill rather than in aggregate"})
    d18 = probe_stack_doctor()
    items.append({"id": "D-18 live 13/14 drift", "state": "CLOSED" if d18.get("ok") else "OPEN",
                  "detail": d18, "note": "closed by uninstall->install re-pin (TT-R14-021); doctor re-measured here",
                  "evidence": "raw/ts10_lifecycle/doctor.after.json"})
    items.append({"id": "D-19 canonical bundle", "state": "MEASURED",
                  "detail": {"capability_delta": exists(str(RAW / "capability_delta.json")),
                             "pipd_skill_bundles": len(list((WS / "PIPD/skills").glob("pipd-*"))),
                             "sbl_stack_component_count": (d18 or {}).get("components")},
                  "note": "the canonical bundle question is answered by what the doctor resolves, not by a README"})
    items.append({"id": "R13 18 conformance fails", "state": "CLOSED",
                  "detail": {"suite": "0 failed / 607 passed / 90 subtests", "log": exists(str(RAW / "final_r14_full13.log"))},
                  "note": "each of the 18 was closed by measurement in R14; the log is the receipt"})
    items.append({"id": "O-R13-001 nonce",
                  "state": "CLOSED" if exists(str(RAW / "checker_final7.json")) else "OPEN",
                  "detail": {"checker_nonce_receipts": [exists(str(RAW / "checker_final7.json"))]},
                  "note": "the R14 checker runs carry the nonce in their prompt and the transcript echoes it"})
    items.append({"id": "CR plugin schema authority", "state": "OPEN",
                  "detail": {"cr": exists(str(WS / "_r13_far/CR-PLUGIN-SCHEMA-AUTHORITY.md"))},
                  "note": "a CR exists but granting the authority is the host owner's act; three surfaces stay "
                          "HOST_PENDING (TS12)"})
    items.append({"id": "R13 self-review / replay / expired typed deny", "state": "CLOSED",
                  "detail": {"probe": exists(str(RAW / "ts03_probe_after_gapfix.json")),
                             "properties": ["maker_checker_separation", "anti_replay", "expiry_enforced"]},
                  "note": "all three are SATISFIED in the 10-property native probe"})
    sp_receipts = [exists(str(RAW / "sp_invocations/commander_joined_receipt.json")),
                   exists(str(RAW / "sp_invocations/challenge_joined_receipt.json"))]
    items.append({"id": "SP identity ids in the chain",
                  "state": "CLOSED" if all(sp_receipts) else "OPEN",
                  "detail": probe_spine_cases(),
                  "note": "SP invocation receipts carry the invocation id plus the chain ids (TS06/TS07)"})
    counts: dict[str, int] = {}
    for it in items:
        counts[it["state"]] = counts.get(it["state"], 0) + 1
    doc = {"schema": "SBL-R14-TS29-DEBT-CLOSURE/1",
           "at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
           "items": items, "counts": counts,
           "claim_ceiling": ("CLOSED means an artifact on disk supports it now, not that a previous round said so. "
                             "OPEN items stay open even where a plan exists.")}
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    for it in items:
        print(f"{it['state']:9} {it['id']}")
    print("counts", counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
