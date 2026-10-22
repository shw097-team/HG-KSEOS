"""R14-TS22 — assemble the M1 gate packet and refuse to sign it.

The order defines M1 as: only after TS02-09 reach H0/H1/H2/H3 (H0 PIPD source/PI, H1 CAPC C0-C9, H2 HGK
identity/repo/permit, H3 actual-world readback), with real SP calls and checker dynamic readback, may
`M1_NATIVE_CHAIN_READY` be signed - with the same-WorkOrder true case, multiple denies, and an **Owner Gate**.

Two things an agent must not do here: sign the gate (that is the Owner's act, and self-signing is exactly the
self-promotion this workspace forbids), and call a level met because something adjacent exists. So this script
measures each level from the artefacts on disk, prints the gap when a level is not met, and emits the packet with
`signed: false`.

Level evidence this script looks for (all paths relative to the workspace):
  H0  a compiled PI package for a real subject (PIPD PI-PKG output validating against its schema) + the source it
      binds to; a skills catalogue alone is NOT H0.
  H1  CAPC C0-C9 compile result for the round contract.
  H2  HGK identity / repo / permit: the TS03 native probe (10 properties) + workorder/lease/rebinding denies.
  H3  an actual-world readback by a different principal: the F0 E6 observer receipt and the dynamic checker receipt.
"""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

WS = Path(r"C:/Projects/Agent_Workspace")
RAW = WS / "_r14_packet/raw"
OUT = RAW / "ts22_m1_gate_packet.json"


def sha(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def load(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def h0() -> dict:
    # A PI-PKG for a real subject: the PIPD pi-compile output schema plus a produced instance.
    schema = WS / "PIPD/skills/pipd-pi-compile/schemas/output.schema.json"
    instances = [p for p in (WS / "_r14_packet/raw").glob("*pi*.json") if "pi_compile" in p.name.lower()
                 or p.name.startswith("ts14")]
    compiled = [p for p in instances if load(p)]
    return {"level": "H0", "name": "PIPD source/PI", "schema_present": schema.is_file(),
            "schema_sha256": sha(schema), "pi_instances_found": [p.name for p in compiled],
            "met": bool(compiled),
            "gap": None if compiled else ("no compiled PI-PKG for a real subject exists; the eight skills' "
                                          "existence is not H0, and no PI has been compiled against a frozen source")}


def h1() -> dict:
    ev = WS / "_r14_ev/_governance/round-20261022-r14/raw"
    cand = [p for p in [RAW / "ts01_compile.txt", RAW / "ts01_capc.txt",
                        ev / "compile_r14/compiler-receipt.json", ev / "compile_r14/compiler-report.json"]
            if p.is_file()]
    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in cand)
    ok = "PROMPT_COMPILE_PASS" in text
    return {"level": "H1", "name": "CAPC C0-C9", "evidence": [p.name for p in cand],
            "pass_markers": text.count("PROMPT_COMPILE_PASS"), "met": ok,
            "gap": None if ok else "no CAPC C0-C9 compile receipt on disk"}


def h2() -> dict:
    probe = load(RAW / "ts03_probe_after_gapfix.json") or {}
    satisfied = probe.get("satisfied")
    gaps = probe.get("gaps")
    denies = [p["property"] for p in probe.get("rows", []) if p.get("verdict") == "SATISFIED"
              and any(k in p["property"] for k in ("scope", "expiry", "replay", "separation", "lease", "revocation"))]
    met = satisfied == 10 and gaps == 0 and len(denies) >= 4
    return {"level": "H2", "name": "HGK identity/repo/permit", "probe_satisfied": satisfied,
            "probe_gaps": gaps, "deny_properties": denies, "met": met,
            "gap": None if met else "native probe incomplete or fewer than four deny properties measured"}


def h3() -> dict:
    e6 = load(RAW / "e6_observer.json") or {}
    chk = load(RAW / "checker_final7.json") or {}
    chk_ok = bool(chk.get("ok")) and (chk.get("served_arm") == "openai-codex/gpt-6.1-sol")
    met = bool(e6.get("observer_matches_local")) and chk_ok
    return {"level": "H3", "name": "actual-world readback",
            "e6_observer": {"served_arm": e6.get("served_arm"),
                            "matches_local": e6.get("observer_matches_local"),
                            "artifact_sha256": (e6.get("artifact_sha256") or "")[:16]},
            "checker": {"ok": chk.get("ok"), "served_arm": chk.get("served_arm")},
            "met": met,
            "gap": None if met else "no independent readback pairing a lane observer with a checker receipt"}


def main() -> int:
    levels = [h0(), h1(), h2(), h3()]
    open_gaps = [l for l in levels if not l["met"]]
    doc = {
        "schema": "SBL-R14-TS22-M1-GATE/1",
        "at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "gate": "M1_NATIVE_CHAIN_READY",
        "levels": levels,
        "levels_met": sum(1 for l in levels if l["met"]),
        "levels_total": len(levels),
        "verdict": "M1_GATE_PACKET_READY_FOR_OWNER" if not open_gaps else "M1_NOT_READY",
        "open_gaps": [{"level": l["level"], "gap": l["gap"]} for l in open_gaps],
        "signed": False,
        "signer": None,
        "why_unsigned": ("M1 is an Owner Gate. An agent may assemble and measure the packet; it may not supply the "
                         "other principal's signature, and this round forbids self-promotion."),
        "claim_ceiling": "packet + measurements only; M1 is NOT signed and no milestone is claimed",
    }
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    for l in levels:
        print(f"{l['level']} {l['name']:26} met={l['met']}" + (f"  GAP: {l['gap']}" if l["gap"] else ""))
    print("verdict:", doc["verdict"], f"({doc['levels_met']}/{doc['levels_total']} levels)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
