"""Deterministic tests for the mandatory three-lane FAR round lifecycle.

These fixtures spawn no provider. They exercise the gate and publication lifecycle through raw
dispatcher-shaped receipts on disk, so every negative case is otherwise a round that should pass.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUN_ID = "FAR-20261101-LIFECYCLE-TEST"
QUESTION = "Which mechanism makes three lane receipts mandatory before closure?"
LANES = {
    "PLAN": ("PLAN_RECEIPT.json", "_plan_dispatch.json", "openai-codex/gpt-6.1-sol"),
    "EXECUTE": ("EXECUTE_RECEIPT.json", "_execute_dispatch.json",
                "opencode-go/deepseek-v4.1-flash"),
    "VERIFY_SECURITY": ("VERIFY_RECEIPT.json", "_verify_dispatch.json",
                        "openai-codex/gpt-6.1-sol"),
}


def _load(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"test_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


far_gate = _load("far_lane_gate")
far_publish = _load("far_publish")
far_round = _load("far_round")


def _write_json(path: pathlib.Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1), encoding="utf-8",
                    newline="")


def _question_digest() -> str:
    return hashlib.sha256(QUESTION.encode("utf-8")).hexdigest()


def _raw_receipt(lane: str, arm: str, nonce: str) -> dict:
    provider, model = arm.split("/", 1)
    return {
        "lane": lane,
        "ok": True,
        "usage_receipt_ok": True,
        "used_transport_model": arm,
        "attempts": [{
            "rank": 1,
            "provider": provider,
            "model": model,
            "exit": 0,
            "nonce_present": True,
            "nonce": nonce,
        }],
    }


def _make_run(
    root: pathlib.Path,
    *,
    omit: str | None = None,
    question_digest: str | None = None,
    cite_all: bool = True,
) -> pathlib.Path:
    run = root / RUN_ID
    run.mkdir()
    digest = question_digest or _question_digest()
    citations = []
    receipts = {}
    for lane, (summary_name, raw_name, arm) in LANES.items():
        if lane == omit:
            continue
        nonce = f"FAR-{lane}-TEST"
        raw_path = run / raw_name
        _write_json(raw_path, _raw_receipt(lane, arm, nonce))
        summary = {
            "schema": "HGK-FAR-LANE-SUMMARY/2",
            "run": RUN_ID,
            "lane": lane,
            "nonce": nonce,
            "required_arm": arm,
            "served_arm": arm,
            "question_sha256": digest,
            "dispatch_receipt": raw_path.name,
            "dispatch_receipt_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            "ok": True,
            "usage_receipt_ok": True,
            "rank": 1,
            "exit": 0,
        }
        _write_json(run / summary_name, summary)
        receipts[lane] = summary
        if cite_all or lane != "EXECUTE":
            citations.append(summary_name)

    _write_json(run / "STATE.json", {
        "schema": "HGK-FAR-STATE/2",
        "run": RUN_ID,
        "question_sha256": digest,
        "publication_status": "LANE_DISPATCH_COMPLETE",
        "lanes_required": ["execute", "plan", "verify"],
        "lanes_served": sorted(
            "verify" if lane == "VERIFY_SECURITY" else lane.lower()
            for lane in LANES if lane != omit
        ),
        "receipts": receipts,
    })
    (run / "ResearchSynthesis.md").write_text(
        "# Synthesis\n\n" + "\n".join(f"Lane evidence: `{name}`" for name in citations) + "\n",
        encoding="utf-8",
        newline="",
    )
    return run


def test_valid_three_receipt_round_is_publishable_and_promotable(tmp_path, monkeypatch):
    run = _make_run(tmp_path)
    result = far_gate.check(run)
    assert result["verdict"] == "PUBLISHABLE", result["findings"]
    assert set(result["receipts"]) == set(LANES)

    monkeypatch.setattr(far_publish, "RUNS", tmp_path)
    rc = far_publish.main(["--promote", RUN_ID, "--by", "test-owner", "--note", "fixture"])
    assert rc == 0
    published = far_publish.state_of(run)
    assert published["state"] == "PUBLISHED", published
    assert published["question_sha256"] == _question_digest()


@pytest.mark.parametrize("missing_lane", LANES)
def test_omission_of_any_required_lane_prevents_closure(tmp_path, missing_lane):
    run = _make_run(tmp_path, omit=missing_lane)
    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any(f.get("lane") == missing_lane for f in result["findings"])


def test_foreign_raw_receipt_cannot_resolve_outside_the_run(tmp_path):
    run = _make_run(tmp_path)
    foreign = tmp_path / "_foreign_plan_dispatch.json"
    _write_json(foreign, _raw_receipt("PLAN", "openai-codex/gpt-6.1-sol",
                                      "FAR-PLAN-TEST"))
    summary_path = run / "PLAN_RECEIPT.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["dispatch_receipt"] = "../_foreign_plan_dispatch.json"
    summary["dispatch_receipt_sha256"] = hashlib.sha256(foreign.read_bytes()).hexdigest()
    _write_json(summary_path, summary)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("escapes the run directory" in f["problem"] for f in result["findings"])


def test_raw_receipt_changed_after_summary_is_refused(tmp_path):
    run = _make_run(tmp_path)
    raw = run / "_execute_dispatch.json"
    receipt = json.loads(raw.read_text(encoding="utf-8"))
    receipt["attempts"][0]["model"] = "glm-5.3-flash"
    _write_json(raw, receipt)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("no longer matches" in f["problem"] for f in result["findings"])


def test_existing_raw_receipt_with_matching_digest_still_must_pass_lane_gate(tmp_path):
    """A digest proves immutability; it does not prove the lane succeeded."""
    run = _make_run(tmp_path)
    raw = run / "_plan_dispatch.json"
    receipt = json.loads(raw.read_text(encoding="utf-8"))
    receipt["usage_receipt_ok"] = False
    _write_json(raw, receipt)
    summary_path = run / "PLAN_RECEIPT.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["dispatch_receipt_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    summary["usage_receipt_ok"] = False
    _write_json(summary_path, summary)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any(
        finding.get("lane") == "PLAN"
        and finding.get("problem") == "raw dispatcher receipt did not prove the lane claim"
        and "usage_receipt_not_ok" in finding["gate"]["problems"]
        for finding in result["findings"]
    )


def test_all_lanes_must_bind_the_same_question(tmp_path):
    run = _make_run(tmp_path)
    summary_path = run / "VERIFY_RECEIPT.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["question_sha256"] = "f" * 64
    _write_json(summary_path, summary)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("different questions" in f["problem"] for f in result["findings"])


def test_synthesis_must_cite_all_three_typed_summaries(tmp_path):
    run = _make_run(tmp_path, cite_all=False)
    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("EXECUTE_RECEIPT.json" in f["problem"] for f in result["findings"])


def test_publication_marker_alone_does_not_establish_published(tmp_path, monkeypatch):
    run = tmp_path / RUN_ID
    run.mkdir()
    (run / "ResearchSynthesis.md").write_text("A hand-authored marker fixture.\n",
                                              encoding="utf-8")
    _write_json(run / "PUBLICATION.json", {
        "schema": "HGK-FAR-PUBLICATION/2",
        "run": RUN_ID,
        "state": "PUBLISHED",
        "gate_verdict_at_promotion": "PUBLISHABLE",
        "question_sha256": _question_digest(),
        "receipts": {},
    })
    monkeypatch.setattr(far_publish, "RUNS", tmp_path)

    result = far_publish.state_of(run)
    assert result["state"] == "EVIDENCE_INVALID", result
    assert far_publish.main(["--status", RUN_ID]) == 0


def test_post_promotion_evidence_change_invalidates_publication(tmp_path, monkeypatch):
    run = _make_run(tmp_path)
    monkeypatch.setattr(far_publish, "RUNS", tmp_path)
    assert far_publish.main(["--promote", RUN_ID, "--by", "test-owner"]) == 0
    assert far_publish.state_of(run)["state"] == "PUBLISHED"

    raw = run / "_verify_dispatch.json"
    receipt = json.loads(raw.read_text(encoding="utf-8"))
    receipt["ok"] = False
    _write_json(raw, receipt)

    result = far_publish.state_of(run)
    assert result["state"] == "EVIDENCE_INVALID", result
    assert result["gate"] == "INVALID_RESEARCH"


@pytest.mark.parametrize("lanes", ["plan", "plan,execute", "plan,verify",
                                    "plan,execute,verify,extra"])
def test_authoritative_round_refuses_incomplete_lane_sets_before_dispatch(lanes, monkeypatch):
    monkeypatch.setattr(far_round, "RUNS", pathlib.Path("unused-test-runs"))
    with pytest.raises(SystemExit) as exc:
        far_round.main(["--run", RUN_ID, "--question", QUESTION, "--lanes", lanes])
    assert exc.value.code == 2


def test_authoritative_round_refuses_an_empty_question_before_dispatch(monkeypatch):
    monkeypatch.setattr(far_round, "RUNS", pathlib.Path("unused-test-runs"))
    with pytest.raises(SystemExit) as exc:
        far_round.main(["--run", RUN_ID, "--question", "   "])
    assert exc.value.code == 2


@pytest.mark.parametrize("run_id", ["../escape", "FAR-safe/child", r"FAR-safe\child", "other"])
def test_authoritative_round_refuses_unsafe_run_names(run_id, monkeypatch):
    monkeypatch.setattr(far_round, "RUNS", pathlib.Path("unused-test-runs"))
    with pytest.raises(SystemExit) as exc:
        far_round.main(["--run", run_id, "--question", QUESTION])
    assert exc.value.code == 2


def test_malformed_raw_receipt_is_refused_without_an_exception(tmp_path):
    run = _make_run(tmp_path)
    raw = run / "_plan_dispatch.json"
    raw.write_text("{not-json", encoding="utf-8")
    summary_path = run / "PLAN_RECEIPT.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["dispatch_receipt_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    _write_json(summary_path, summary)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("raw dispatch receipt unreadable" in f["problem"] for f in result["findings"])


def test_raw_receipt_without_transport_model_is_refused(tmp_path):
    run = _make_run(tmp_path)
    raw = run / "_plan_dispatch.json"
    receipt = json.loads(raw.read_text(encoding="utf-8"))
    del receipt["used_transport_model"]
    _write_json(raw, receipt)
    summary_path = run / "PLAN_RECEIPT.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["dispatch_receipt_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    _write_json(summary_path, summary)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("no used_transport_model" in f["problem"] for f in result["findings"])


def test_raw_receipt_with_wrong_transport_arm_is_refused(tmp_path):
    run = _make_run(tmp_path)
    raw = run / "_execute_dispatch.json"
    receipt = json.loads(raw.read_text(encoding="utf-8"))
    receipt["used_transport_model"] = "opencode-go/glm-5.3-flash"
    _write_json(raw, receipt)
    summary_path = run / "EXECUTE_RECEIPT.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["dispatch_receipt_sha256"] = hashlib.sha256(raw.read_bytes()).hexdigest()
    _write_json(summary_path, summary)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("transport arm mismatch" in f["problem"] for f in result["findings"])


def test_state_must_record_the_exact_successful_lane_set(tmp_path):
    run = _make_run(tmp_path)
    state_path = run / "STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["lanes_served"] = ["execute", "plan"]
    _write_json(state_path, state)

    result = far_gate.check(run)
    assert result["verdict"] == "INVALID_RESEARCH"
    assert any("lanes_served" in f["problem"] for f in result["findings"])


def test_unreadable_existing_dispatch_is_summarized_without_raising(tmp_path):
    run = tmp_path / RUN_ID
    (run / "lane_output").mkdir(parents=True)
    raw = run / "_plan_dispatch.json"
    raw.write_text("{not-json", encoding="utf-8")

    summary = far_round.summarize_dispatch(
        RUN_ID,
        "PLAN",
        "openai-codex/gpt-6.1-sol",
        "FAR-PLAN-TEST",
        _question_digest(),
        raw,
        run,
    )

    assert summary["ok"] is False
    assert summary["code"] == "UNREADABLE_DISPATCH_RECEIPT"


def test_publish_cli_refuses_path_expressions(tmp_path, monkeypatch):
    monkeypatch.setattr(far_publish, "RUNS", tmp_path)
    with pytest.raises(SystemExit) as exc:
        far_publish.main(["--status", "../escape"])
    assert exc.value.code == 2
