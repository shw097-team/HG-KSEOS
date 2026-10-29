"""R14 H0 — compile a real PI-PKG from the TS14 guided spec and validate it against PIPD's own output schema.

H0 (PIPD source/PI) is the one level M1 was missing: eight skills existing is not a PI. This takes the atoms that
already validated against pipd-pi-compile's INPUT schema, compiles them into a PI-PKG, and validates the OUTPUT
against the skill's output schema. Deterministic: subject_id and content_hash are derived from the input bytes.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

WS = Path(r"C:/Projects/Agent_Workspace")
SPEC = WS / "_r14_packet/raw/ts14_guided_spec.json"
SCHEMA = WS / "PIPD/skills/pipd-pi-compile/schemas/output.schema.json"
OUT = WS / "_r14_packet/raw/ts14_pi_pkg.json"


def canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def main() -> int:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    pin = spec["pi_compile_input"]
    intent, atoms, goal, profile = pin["intent"], pin["atoms"], pin["goal"], pin["profile"]
    h = hashlib.sha256(canon({"intent": intent, "atoms": atoms, "goal": goal, "profile": profile})).hexdigest()
    # the output contract requires a subject_id per atom (the input contract does not): the compiler assigns it
    atoms_out = [{**a,
                  "subject_id": "ATOM-" + hashlib.sha256(canon(a)).hexdigest()[:16],
                  "content_hash": hashlib.sha256(canon(a)).hexdigest(),
                  "version": "1", "schema_version": "RequirementAtom@1"} for a in atoms]
    pkg = {
        "subject_id": "PI-" + h[:16],
        "content_hash": h,
        "version": "1",
        "schema_version": "PI-PKG@1",
        "stable_semantic_contract": {
            "contract": "stable",
            "profile_binding": {
                "profile": profile,
                "axes": ["intent", "knowledge", "verification", "release"],
                "vetoes": ["no_evidence_for_acceptance", "release_handoff_without_readback"],
                "artifact_depth": "L3_INTEGRATION_RUNTIME",
                "assurance": ["independent_checker_required", "raw_evidence_per_acceptance"]},
            "atoms": atoms_out,
            "goal": goal,
        },
        # the schema pins this to DOC-03 DOMAIN_ORACLES: an invented oracle string is refused, which is the point
        "acceptance": {"mode": "bound", "oracle_source": "DOC-03 DOMAIN_ORACLES"},
        # the schema fixes every trace row to PI-PKG -> RequirementAtom (no intent row); following the contract
        "trace": [
            {"from_type": "PI-PKG", "from_id": "PI-" + h[:16], "from_hash": h,
             "to_type": "RequirementAtom",
             "to_id": "ATOM-" + hashlib.sha256(canon(a)).hexdigest()[:16],
             "to_hash": hashlib.sha256(canon(a)).hexdigest(),
             "rationale": a.get("source_clause", "")[:120]}
            for a in atoms
        ],
    }
    import jsonschema
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = []
    try:
        jsonschema.validate(pkg, schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"{list(exc.absolute_path)}: {exc.message}")
    # independent negative control: a PI-PKG missing acceptance must be refused by the same schema
    broken = {k: v for k, v in pkg.items() if k != "acceptance"}
    try:
        jsonschema.validate(broken, schema)
        neg = "FAILED_TO_REJECT"
    except jsonschema.ValidationError:
        neg = "REJECTED"
    doc = {"schema": "SBL-TS14-PI-PKG-COMPILE/1", "ok": not errors, "errors": errors,
           "negative_control": neg, "pi_pkg": pkg,
           "input_digest": "sha256:" + h,
           "compiled_from": str(SPEC.relative_to(WS)),
           "claim_ceiling": "PI compiled and schema-valid; not admitted by PIPD, not executed"}
    doc["schema"] = "SBL-TS14-PI-PKG-COMPILE/1"
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ok": doc["ok"], "errors": errors, "negative_control": neg,
                      "subject_id": pkg["subject_id"], "atoms": len(atoms)}, ensure_ascii=False))
    return 0 if doc["ok"] and neg == "REJECTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
