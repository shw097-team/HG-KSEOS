"""R14-TS13 — the eight official PIPD skills, measured: version, discover, bind, invoke, deny.

What the order demands: version / host discover / real bind / invoke / deny for all eight skills, and
PI/PD/ECP/TQAEP obtainable only by the original Owner Writer. Evidence: 8 x POS/NEG/identity/consumer+issuer.

What this harness can honestly measure, and how it separates the two kinds of refusal:

  * ACCEPT case  -> the input must validate against the skill's own input schema, and its declared output must
                    validate against the output schema. Those are measurements.
  * REFUSE case  -> if the input FAILS the input schema, the denial is mechanically enforced (SCHEMA_ENFORCED).
                    If the input VALIDATES but the case expects REFUSE, the denial lives in prose or in code this
                    harness cannot reach; that is recorded as UNENFORCED, never as a pass. This distinction is the
                    whole point: a skill whose negatives are only declared is not a skill that denies.

`owner` is read from the SKILL.md frontmatter and from the input schema description; `consumer` likewise. A skill that
declares itself as its own consumer would be an issuer/consumer collapse and is reported.
"""
from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import jsonschema
import yaml

SKILLS = Path(r"C:/Projects/Agent_Workspace/PIPD/skills")
OUT = Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw")
OFFICIAL = ["pipd-route-intake", "pipd-authority-source", "pipd-profile-tailor", "pipd-pi-compile",
            "pipd-pd-bind", "pipd-execution-contract", "pipd-assurance-tqaep", "pipd-package-project"]


def frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    try:
        return yaml.safe_load(text[3:end]) or {}
    except Exception:
        return {}


def validate(instance, schema: dict) -> tuple[bool, str]:
    try:
        jsonschema.validate(instance, schema)
        return True, ""
    except jsonschema.ValidationError as exc:
        return False, f"{list(exc.absolute_path)}: {exc.message[:160]}"


def measure(name: str) -> dict:
    root = SKILLS / name
    row: dict = {"skill": name, "root_exists": root.is_dir(), "verdict": "FAIL", "findings": []}
    if not row["root_exists"]:
        row["findings"].append("skill directory absent")
        return row
    md = root / "SKILL.md"
    fm = frontmatter(md) if md.is_file() else {}
    row.update({
        "has_skill_md": md.is_file(),
        "version": fm.get("version"),
        "declared_owner": fm.get("owner"),
        "description_owner": fm.get("description", ""),
        "has_input_schema": (root / "schemas/input.schema.json").is_file(),
        "has_output_schema": (root / "schemas/output.schema.json").is_file(),
        "has_cases": (root / "tests/cases.yaml").is_file(),
    })
    if not row["has_skill_md"]:
        row["findings"].append("SKILL.md missing (a skill root without SKILL.md is not discoverable)")
        return row
    if row["version"] is None:
        row["findings"].append("no version in frontmatter")
    if not (row["has_input_schema"] and row["has_output_schema"]):
        row["findings"].append("schema pair incomplete")

    # discover: name in frontmatter must equal the directory, and the description must be a usable trigger
    if fm.get("name") != name:
        row["findings"].append(f"frontmatter name {fm.get('name')!r} != directory {name!r}")
    if not fm.get("description"):
        row["findings"].append("no description (not discoverable by trigger)")

    in_schema = json.loads((root / "schemas/input.schema.json").read_text(encoding="utf-8")) if row["has_input_schema"] else {}
    out_schema = json.loads((root / "schemas/output.schema.json").read_text(encoding="utf-8")) if row["has_output_schema"] else {}
    desc = (in_schema.get("description") or "")
    row["issuer_consumer_declared"] = desc
    owner_in_desc = desc.split("Owner:")[-1].split(".")[0].strip() if "Owner:" in desc else None
    consumer_in_desc = desc.split("Consumer:")[-1].split(".")[0].strip() if "Consumer:" in desc else None
    row["owner_in_schema_desc"] = owner_in_desc
    row["consumer_in_schema_desc"] = consumer_in_desc
    if owner_in_desc and consumer_in_desc and owner_in_desc.casefold() == consumer_in_desc.casefold():
        row["findings"].append("owner == consumer in the schema description (issuer/consumer collapse)")

    cases_doc = yaml.safe_load((root / "tests/cases.yaml").read_text(encoding="utf-8")) if row["has_cases"] else {}
    cases = cases_doc.get("cases", [])
    results = []
    for case in cases:
        expect = case.get("expect")
        ok_in, why_in = validate(case.get("input"), in_schema) if in_schema else (None, "no input schema")
        out_ok = None
        if expect == "ACCEPT" and case.get("output") and out_schema:
            out_ok, _ = validate(case["output"], out_schema)
        if expect == "ACCEPT":
            state = "PASS" if ok_in and (out_ok in (True, None)) else "FAIL"
        else:
            state = "SCHEMA_ENFORCED" if ok_in is False else "UNENFORCED"
        results.append({"id": case.get("id"), "kind": case.get("kind"), "expect": expect,
                        "state": state, "why": why_in[:120] if ok_in is False else ""})
    counts: dict[str, int] = {}
    for r in results:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    row["cases"] = results
    row["case_counts"] = counts
    row["pos_total"] = sum(1 for r in results if r["expect"] == "ACCEPT")
    row["pos_pass"] = sum(1 for r in results if r["expect"] == "ACCEPT" and r["state"] == "PASS")
    row["refuse_total"] = sum(1 for r in results if r["expect"] == "REFUSE")
    row["refuse_enforced"] = counts.get("SCHEMA_ENFORCED", 0)
    row["refuse_unenforced"] = counts.get("UNENFORCED", 0)
    if row["pos_total"] and row["pos_pass"] == row["pos_total"] and row["refuse_unenforced"] == 0 and not row["findings"]:
        row["verdict"] = "PASS"
    elif row["pos_pass"] == row["pos_total"] and row["pos_total"]:
        row["verdict"] = "PARTIAL"
        if row["refuse_unenforced"]:
            row["findings"].append(f"{row['refuse_unenforced']}/{row['refuse_total']} refusals are declared, not schema-enforced")
    else:
        row["verdict"] = "FAIL"
    return row


def main() -> int:
    rows = [measure(n) for n in OFFICIAL]
    summary = {v: sum(1 for r in rows if r["verdict"] == v) for v in ("PASS", "PARTIAL", "FAIL")}
    doc = {"schema": "SBL-R14-TS13-PIPD-SKILLS/1",
           "at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
           "official_count": len(OFFICIAL), "rows": rows, "summary": summary,
           "claim_ceiling": ("discover/bind/invoke are measured at the schema and frontmatter level; a refusal that "
                             "the schema does not enforce is reported UNENFORCED and never counted as a pass")}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ts13_pipd_skills.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in rows:
        print(f"{r['skill']:26} {r['verdict']:8} pos {r['pos_pass']}/{r['pos_total']} "
              f"refuse enforced {r['refuse_enforced']}/{r['refuse_total']} findings={len(r['findings'])}")
    print("summary", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
