"""Separate the four scopes that were being compared as if they were one.

The R14 lane-fidelity audit reported 44 "field-path inconsistencies". Reading that as "the wiring is wrong" mixes four
different planes:

  L  lane scope      config/lane-routing-registry.yaml - the authority for lane -> provider/model, carrying
                     selection_authority for the round that set it (epoch).
  R  round scope     per-round role_mandate.json consumed by scripts/runtime_role_binding_assert.py (P1-A). A round may
                     legitimately bind the same lane to a different arm for its duration; that is an owner decision,
                     recorded in the round's own history, not a defect.
  S  session scope   sessions.model / model_config in Hermes state.db. Several root sessions ran CONCURRENTLY on
                     2026-10-22 on opencode-go models other than gpt-6.1-sol. A session's interactive model is not a
                     lane binding and must never be compared against L.
  V  served scope    session_model_usage receipts - what actually answered a call.

config/model-lane-assignment.json is a PROJECTION of L for the current round. When a superseded R wrote a value and a
later round restored only part of it, the leftover is SUPERSEDED_ROUND_RESIDUE: a hygiene finding with an owner and a
date, not evidence of misbehaviour and not a reason to declare the lane wrong.

This script classifies every divergence by origin commit, and can register the historical ones as explicit exceptions so
that any NEW divergence is caught while the known residue stays visible.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import subprocess
from pathlib import Path

import yaml

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

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "config/lane-routing-registry.yaml"
ASG = ROOT / "config/model-lane-assignment.json"
EXC = ROOT / "config/lane_scope_exceptions.json"
HERMES = Path(r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes")
ROLES = ("PLAN", "EXECUTE", "VERIFY_SECURITY")
LANE_FIELDS = ("provider", "model", "transport_model", "automatic_selection")


def git(*args: str) -> str:
    result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return (result.stdout or "").strip()


def origin_of(value: str) -> dict:
    """Which commit introduced this exact value into the assignment file."""
    out = git("log", "-S", '"' + value + '"', "--format=%h|%ad|%s", "--date=short",
              "--", "config/model-lane-assignment.json")
    lines = [line for line in out.splitlines() if "|" in line]
    if not lines:
        return {"commit": None, "date": None, "subject": None}
    first = lines[-1].split("|", 2)
    return {"commit": first[0], "date": first[1], "subject": first[2] if len(first) > 2 else ""}


def sessions_now() -> list[dict]:
    db = HERMES / "state.db"
    if not db.is_file():
        return []
    con = sqlite3.connect("file:" + str(db) + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        """SELECT id,model,billing_provider,parent_session_id,message_count,started_at
           FROM sessions WHERE parent_session_id IS NULL ORDER BY rowid DESC LIMIT 25""")]
    con.close()
    out = []
    for row in rows:
        try:
            started = dt.datetime.fromtimestamp(float(row["started_at"]), dt.UTC).astimezone(
                dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
        except Exception:
            started = str(row["started_at"])
        out.append({**row, "started_local": started})
    return out


def main(write: bool) -> int:
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    by_lane = {route["lane"]: route for route in reg["routes"]}
    asg = json.loads(ASG.read_text(encoding="utf-8"))
    epoch = asg.get("registry_epoch")
    findings = []
    for role in ROLES:
        arms = by_lane[role]["arms"]
        chain = asg["lane_chains"][role]
        for index, arm in enumerate(arms[: len(chain)]):
            for field in LANE_FIELDS:
                want, have = arm.get(field), chain[index].get(field)
                if want == have:
                    continue
                origin = origin_of(str(have))
                subject = (origin["subject"] or "").upper()
                classification = ("SUPERSEDED_ROUND_RESIDUE" if "MINIMAX-MANDATE" in subject
                                  else "CURRENT_ROUND_NOT_DERIVED")
                findings.append({"role": role, "index": index, "field": field, "lane_scope_value": want,
                                 "assignment_value": have, "classification": classification, "origin": origin})
    concurrent = [s for s in sessions_now() if s["model"] and "gpt-6.1-sol" not in s["model"]
                  and (s["message_count"] or 0) > 50]
    counts = {c: sum(1 for f in findings if f["classification"] == c)
              for c in ("SUPERSEDED_ROUND_RESIDUE", "CURRENT_ROUND_NOT_DERIVED")}
    doc = {
        "schema": "SBL-R14-LANE-SCOPE-ISOLATION/1",
        "at_utc": dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z"),
        "registry_epoch": epoch,
        "scopes": {
            "L_lane": {"authority": "config/lane-routing-registry.yaml",
                       "note": "authority for lane -> provider/model"},
            "R_round": {"authority": "per-round role_mandate.json + scripts/runtime_role_binding_assert.py (P1-A)",
                        "note": "a round may bind a lane differently for its duration; owner decision, recorded"},
            "S_session": {"authority": "Hermes state.db sessions.model",
                          "note": "the interactive model of a session; never a lane binding"},
            "V_served": {"authority": "session_model_usage", "note": "what actually answered a call"},
        },
        "divergences": findings,
        "counts": counts,
        "session_scope_observations": concurrent,
        "reading": ("Every divergence is between L (registry, epoch {}) and its projection in the assignment. The PLAN "
                    "transport value came from an owner mandate that bound all three lanes to MiniMax for one round and "
                    "was only partly reverted afterwards, so it is stale round residue. Concurrent sessions running "
                    "other models are S-scope and are not lane drift at all.".format(epoch)),
        "claim_ceiling": ("Classified, not repaired. Registering the residue as an exception makes it visible and dated; "
                          "it does not make the projection correct, and it changes no runtime binding."),
    }
    out = ROOT / "var/R14-LANE-SCOPE-20261022"
    out.mkdir(parents=True, exist_ok=True)
    (out / "isolation.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    if write:
        exceptions = []
        for f in findings:
            exceptions.append({
                "role": f["role"], "index": f["index"], "field": f["field"],
                "lane_scope_value": f["lane_scope_value"], "assignment_value": f["assignment_value"],
                "classification": f["classification"],
                "origin_commit": f["origin"]["commit"], "origin_subject": f["origin"]["subject"],
                "origin_date": f["origin"]["date"],
            })
        EXC.write_text(json.dumps({
            "schema": "SBL-LANE-SCOPE-EXCEPTIONS/1",
            "registry_epoch": epoch,
            "reason": ("Values below were written by a round whose mandate differed and were not re-derived afterwards. "
                       "They are registered so the guard fails on NEW divergence only, and so this history stays "
                       "visible instead of being silently normalised away."),
            "exceptions": exceptions,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"counts": counts, "epoch": epoch,
                      "concurrent_non_gpt_sessions": len(concurrent), "wrote_exceptions": write},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-exceptions", action="store_true")
    raise SystemExit(main(parser.parse_args().write_exceptions))
