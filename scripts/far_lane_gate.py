#!/usr/bin/env python3
"""Fail-closed evidence gate for a three-lane FAR research round.

The round lifecycle owns dispatch; this gate owns the meaning of ``PUBLISHABLE``. A typed lane
summary is useful only when it resolves to the in-run raw dispatcher receipt it names, that receipt
has not changed, and the raw receipt passes ``lane_evidence_gate.judge``. All three summaries must
bind the same run and question, and the synthesis must cite all three summaries.

Exit 0 = PUBLISHABLE; exit 3 = INVALID_RESEARCH.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

K = Path(__file__).resolve().parent.parent
if str(K / "scripts") not in sys.path:
    sys.path.insert(0, str(K / "scripts"))

import lane_evidence_gate  # noqa: E402

SUMMARY_SCHEMA = "HGK-FAR-LANE-SUMMARY/2"
STATE_SCHEMA = "HGK-FAR-STATE/2"
SUMMARIES = {
    "PLAN": ("PLAN_RECEIPT.json", "openai-codex/gpt-6.1-sol"),
    "EXECUTE": ("EXECUTE_RECEIPT.json", "opencode-go/deepseek-v4.1-flash"),
    "VERIFY_SECURITY": ("VERIFY_RECEIPT.json", "openai-codex/gpt-6.1-sol"),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _object(path: Path) -> tuple[dict | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{exc.__class__.__name__}: {exc}"
    if not isinstance(value, dict):
        return None, "JSON root is not an object"
    return value, None


def _arm_pair(value: object) -> tuple[str | None, str | None]:
    if not value:
        return None, None
    text = str(value).strip()
    if "/" in text:
        provider, _, model = text.partition("/")
        return provider.lower(), model.lower()
    return None, text.lower()


def _transport_matches(value: object, expected_arm: str, served_provider: object) -> bool:
    """Compare a transport id to a canonical arm under the provider's spelling rule."""
    if not isinstance(value, str) or not value.strip():
        return False
    expected = _arm_pair(expected_arm)
    actual = _arm_pair(value)
    if actual[0] is None:
        actual = (
            str(served_provider).strip().lower()
            if isinstance(served_provider, str) and served_provider.strip()
            else None,
            actual[1],
        )
    return actual == expected


def _raw_arm(receipt: dict) -> str | None:
    attempts = receipt.get("attempts") if isinstance(receipt.get("attempts"), list) else []
    attempt = attempts[-1] if attempts and isinstance(attempts[-1], dict) else {}
    model = attempt.get("model")
    provider = attempt.get("provider")
    if provider and model:
        return f"{provider}/{model}"
    return str(model) if model else None


def _resolve_inside(run: Path, relative: object) -> tuple[Path | None, str | None]:
    if not isinstance(relative, str) or not relative.strip():
        return None, "dispatch_receipt is missing"
    if Path(relative).is_absolute():
        return None, f"dispatch_receipt must be relative to the run: {relative!r}"
    candidate = (run / relative).resolve()
    try:
        candidate.relative_to(run.resolve())
    except ValueError:
        return None, f"dispatch_receipt escapes the run directory: {relative!r}"
    if not candidate.is_file():
        return None, f"raw dispatch receipt is absent: {relative}"
    return candidate, None


def _validate_lane(
    run: Path,
    run_id: str,
    lane: str,
    filename: str,
    expected_arm: str,
) -> tuple[dict | None, dict[str, str], list[dict]]:
    findings: list[dict] = []
    evidence: dict[str, str] = {}
    summary_path = run / filename
    if not summary_path.is_file():
        findings.append({"lane": lane, "problem": f"{filename} ABSENT; the lane has no summary"})
        return None, evidence, findings

    summary, problem = _object(summary_path)
    if problem:
        findings.append({"lane": lane, "problem": f"{filename} unreadable: {problem}"})
        return None, evidence, findings
    assert summary is not None
    required = {
        "schema": SUMMARY_SCHEMA,
        "run": run_id,
        "lane": lane,
        "required_arm": expected_arm,
    }
    for field, expected in required.items():
        if summary.get(field) != expected:
            findings.append({
                "lane": lane,
                "problem": f"{field} mismatch: expected {expected!r}, got {summary.get(field)!r}",
            })
    nonce = summary.get("nonce")
    if not isinstance(nonce, str) or not nonce.strip():
        findings.append({"lane": lane, "problem": "summary has no round nonce"})
    question_sha256 = summary.get("question_sha256")
    if not _is_sha256(question_sha256):
        findings.append({"lane": lane, "problem": "summary has no question_sha256"})

    raw_path, raw_problem = _resolve_inside(run, summary.get("dispatch_receipt"))
    if raw_problem:
        findings.append({"lane": lane, "problem": raw_problem})
        return summary, evidence, findings
    assert raw_path is not None
    evidence.update({
        "summary": summary_path.name,
        "raw": raw_path.relative_to(run.resolve()).as_posix(),
        "raw_sha256": _sha256(raw_path),
    })
    if summary.get("dispatch_receipt_sha256") != evidence["raw_sha256"]:
        findings.append({
            "lane": lane,
            "problem": "raw dispatch receipt no longer matches the summary digest",
            "recorded": summary.get("dispatch_receipt_sha256"),
            "actual": evidence["raw_sha256"],
        })

    receipt, problem = _object(raw_path)
    if problem:
        findings.append({"lane": lane, "problem": f"raw dispatch receipt unreadable: {problem}"})
        return summary, evidence, findings
    assert receipt is not None
    attempts = receipt.get("attempts")
    if (not isinstance(attempts, list) or not attempts
            or not isinstance(attempts[-1], dict)):
        findings.append({
            "lane": lane,
            "problem": "raw dispatcher receipt has no well-formed final attempt",
        })
        return summary, evidence, findings
    try:
        verdict = lane_evidence_gate.judge(
            receipt, lane, nonce if isinstance(nonce, str) else None, 1)
    except Exception as exc:
        findings.append({
            "lane": lane,
            "problem": "raw dispatcher receipt could not be judged",
            "detail": f"{exc.__class__.__name__}: {exc}",
        })
    else:
        if verdict.get("verdict") != "LANE_SERVED_AS_CLAIMED":
            findings.append({
                "lane": lane,
                "problem": "raw dispatcher receipt did not prove the lane claim",
                "gate": verdict,
            })
    used_transport = receipt.get("used_transport_model")
    if not isinstance(used_transport, str) or not used_transport.strip():
        findings.append({
            "lane": lane,
            "problem": "raw dispatcher receipt has no used_transport_model",
        })
    elif not _transport_matches(used_transport, expected_arm, attempts[-1].get("provider")):
        findings.append({
            "lane": lane,
            "problem": f"transport arm mismatch: expected {expected_arm!r}, "
                       f"got {used_transport!r}",
        })
    raw_arm = _raw_arm(receipt)
    if _arm_pair(raw_arm) != _arm_pair(expected_arm):
        findings.append({
            "lane": lane,
            "problem": f"served arm mismatch: expected {expected_arm!r}, got {raw_arm!r}",
        })
    if summary.get("served_arm") != raw_arm:
        findings.append({
            "lane": lane,
            "problem": f"summary served_arm does not match raw receipt: "
                       f"{summary.get('served_arm')!r} != {raw_arm!r}",
        })
    return summary, evidence, findings


def check(run: Path) -> dict:
    run = run.resolve()
    findings: list[dict] = []
    summaries: dict[str, dict] = {}
    receipt_evidence: dict[str, dict[str, str]] = {}

    state_path = run / "STATE.json"
    state, problem = _object(state_path)
    if problem:
        findings.append({"problem": f"STATE.json unreadable: {problem}"})
        state = {}
    elif state.get("schema") != STATE_SCHEMA:
        findings.append({"problem": f"STATE.json schema mismatch: {state.get('schema')!r}"})
    if state.get("run") != run.name:
        findings.append({"problem": f"STATE.json run mismatch: {state.get('run')!r} != {run.name!r}"})
    if state.get("publication_status") != "LANE_DISPATCH_COMPLETE":
        findings.append({
            "problem": "STATE.json is not LANE_DISPATCH_COMPLETE",
            "publication_status": state.get("publication_status"),
        })
    required_lanes = ["execute", "plan", "verify"]
    served_lanes = ["execute", "plan", "verify"]
    if state.get("lanes_required") != required_lanes:
        findings.append({
            "problem": "STATE.json lanes_required is not the exact required lane set",
            "lanes_required": state.get("lanes_required"),
        })
    if state.get("lanes_served") != served_lanes:
        findings.append({
            "problem": "STATE.json lanes_served is not the exact required lane set",
            "lanes_served": state.get("lanes_served"),
        })
    state_question = state.get("question_sha256")
    if not _is_sha256(state_question):
        findings.append({"problem": "STATE.json has no question_sha256"})

    for lane, (filename, expected_arm) in SUMMARIES.items():
        summary, evidence, lane_findings = _validate_lane(run, run.name, lane, filename, expected_arm)
        findings.extend(lane_findings)
        if summary is not None:
            summaries[lane] = summary
        if evidence:
            receipt_evidence[lane] = evidence

    question_digests = {
        lane: value.get("question_sha256")
        for lane, value in summaries.items()
        if isinstance(value.get("question_sha256"), str)
    }
    if len(question_digests) != len(SUMMARIES):
        findings.append({"problem": "not all three lane summaries bind the round question"})
    if len(set(question_digests.values())) != 1:
        findings.append({"problem": "lane summaries bind different questions",
                         "question_sha256": question_digests})
    if state_question and question_digests and state_question not in set(question_digests.values()):
        findings.append({
            "problem": "STATE.json question does not match the lane summaries",
            "state_question_sha256": state_question,
            "lane_question_sha256": question_digests,
        })

    synthesis_path = run / "ResearchSynthesis.md"
    synthesis: dict = {"file": synthesis_path.name, "present": synthesis_path.is_file()}
    if not synthesis_path.is_file():
        findings.append({"problem": "ResearchSynthesis.md is absent"})
    else:
        body = synthesis_path.read_text(encoding="utf-8", errors="replace")
        citations = {filename: filename in body for filename, _ in SUMMARIES.values()}
        synthesis["citations"] = citations
        for filename, cited in citations.items():
            if not cited:
                findings.append({
                    "file": synthesis_path.name,
                    "problem": f"synthesis does not cite required lane artefact {filename}",
                })

    same_question = (len(question_digests) == len(SUMMARIES)
                     and len(set(question_digests.values())) == 1)
    return {
        "schema": "HGK-FAR-GATE/2",
        "run": run.name,
        "verdict": "PUBLISHABLE" if not findings else "INVALID_RESEARCH",
        "question_sha256": next(iter(set(question_digests.values())))
        if same_question else None,
        "receipts": receipt_evidence,
        "synthesis": synthesis,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run_dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    run = Path(args.run_dir)
    if not run.is_dir():
        print(json.dumps({"run": run.name, "verdict": "INVALID_RESEARCH",
                          "findings": [{"problem": f"{run} is not a directory"}]}))
        return 3
    result = check(run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "PUBLISHABLE" else 3


if __name__ == "__main__":
    sys.exit(main())
