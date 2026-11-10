"""test_lane_epoch_validate.py — the epoch-41 arm-retirement plane must refuse, not just describe.

Four executed cases, three of them refusals. Each refusal fixture is built by mutating ONE site of the
tree's own ported config and asserting that the validator's own exit code and named code change —
the unmutated copy is run first and must pass, so a test cannot go green because the tool refuses
everything.

    POS-H4   the ported epoch-41 config                     -> exit 0, epoch 41 numeric, every slot admitted,
                                                               the retired arm absent from every pool
    NEG-H1   a pool that still lists the retired arm        -> RETIREMENT_DRIFT
    NEG-H2   `epoch: forty-one`                             -> EPOCH_UNPARSEABLE
    NEG-H3   PLAN rank 4 still holds the retired arm        -> RETIRED_ARM_IN_POOL

Run: C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m pytest tests/test_lane_epoch_validate.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "scripts" / "lane_epoch_validate.py"
REGISTRY = Path("config") / "lane-routing-registry.yaml"
POOL = Path("config") / "lane-route-slots.candidate.json"
ASSIGNMENT = Path("config") / "model-lane-assignment.json"
RETIRED = "opencode-go/mimo-v2.6-pro"
REPLACEMENT = "opencode-go/mimo-v2.6-flash"


def _run(root: Path) -> tuple[int, dict, str]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        capture_output=True, text=True, encoding="utf-8",
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:  # a crash must not read as a refusal
        payload = {"verdict": "UNPARSEABLE_OUTPUT", "codes": [], "primary_code": None}
    return proc.returncode, payload, proc.stdout + proc.stderr


@pytest.fixture()
def tree(tmp_path: Path) -> Path:
    """A private copy of the three live control-plane files, so a mutation can never touch the repo."""
    for rel in (REGISTRY, POOL, ASSIGNMENT):
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / rel, dst)
    return tmp_path


def _pool(tree: Path) -> dict:
    return json.loads((tree / POOL).read_text(encoding="utf-8"))


def _write_pool(tree: Path, doc: dict) -> None:
    (tree / POOL).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _set_pool_arm(tree: Path, lane: str, rank: int, model: str, provider: str = "opencode-go") -> None:
    doc = _pool(tree)
    for node in doc["lanes"]:
        if node["lane"] != lane:
            continue
        for entry in node["ordered_pool"]:
            if entry["rank"] == rank:
                entry["provider"] = provider
                entry["model"] = model
                entry["transport_model"] = model if provider == "openai-codex" else f"{provider}/{model}"
                break
        else:
            raise AssertionError(f"{lane} has no rank {rank}")
    _write_pool(tree, doc)


def test_pos_h4_ported_epoch41_config_passes(tmp_path: Path) -> None:
    code, out, log = _run(REPO)
    assert code == 0, log
    assert out["verdict"] == "PASS" and out["codes"] == [], log
    assert out["epoch"] == 41 and isinstance(out["epoch"], int)
    assert out["contract_epoch"] == 34
    assert out["status"] == "IN_FORCE"
    assert out["retired_arms"] == [RETIRED]
    slots = out["slots"]
    assert slots["admitted"] == slots["total"] and slots["total"] > 0
    assert slots["by_lane"] == {"PLAN": 6, "EXECUTE": 4, "VERIFY_SECURITY": 5}
    # the owner-ordered admission: PLAN rank 4 is the replacement, not the retired arm
    doc = json.loads((REPO / POOL).read_text(encoding="utf-8"))
    plan = next(n for n in doc["lanes"] if n["lane"] == "PLAN")
    rank4 = next(e for e in plan["ordered_pool"] if e["rank"] == 4)
    assert f"{rank4['provider']}/{rank4['model']}" == REPLACEMENT
    # and the retired arm is absent from every pool of the ported tree
    for node in doc["lanes"]:
        for entry in node["ordered_pool"]:
            assert f"{entry['provider']}/{entry['model']}" != RETIRED, node["lane"]


def test_neg_h1_pool_still_listing_the_retired_arm_is_retirement_drift(tree: Path) -> None:
    # control: the copy is clean before the fault is injected
    code, out, log = _run(tree)
    assert code == 0 and out["verdict"] == "PASS", log

    # fault: the epoch advanced and the registry retires the arm, but the EXECUTE pool was never updated
    _set_pool_arm(tree, "EXECUTE", 2, "mimo-v2.6-pro")

    code, out, log = _run(tree)
    assert code == 2, log
    assert out["verdict"] == "REFUSED"
    assert out["primary_code"] == "RETIREMENT_DRIFT", log
    assert RETIRED in json.dumps(out["findings"], ensure_ascii=False)


def test_neg_h2_non_numeric_epoch_is_epoch_unparseable(tree: Path) -> None:
    code, out, log = _run(tree)
    assert code == 0 and out["verdict"] == "PASS", log

    path = tree / REGISTRY
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = 0
    for i, line in enumerate(lines):
        if line.rstrip() == "epoch: 41":
            lines[i] = "epoch: forty-one"
            hits += 1
    assert hits == 1, f"expected exactly one `epoch: 41` line, found {hits}"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    code, out, log = _run(tree)
    assert code == 2, log
    assert out["primary_code"] == "EPOCH_UNPARSEABLE", log
    assert "forty-one" in json.dumps(out["findings"], ensure_ascii=False)


def test_neg_h3_plan_rank4_retired_arm_is_retired_arm_in_pool(tree: Path) -> None:
    code, out, log = _run(tree)
    assert code == 0 and out["verdict"] == "PASS", log

    # fault: the owner-ordered admission slot itself holds the arm the registry retired
    _set_pool_arm(tree, "PLAN", 4, "mimo-v2.6-pro")

    code, out, log = _run(tree)
    assert code == 2, log
    assert out["primary_code"] == "RETIRED_ARM_IN_POOL", log
    assert "PLAN" in json.dumps(out["findings"], ensure_ascii=False)
    assert out["slots"]["admitted"] < out["slots"]["total"]
