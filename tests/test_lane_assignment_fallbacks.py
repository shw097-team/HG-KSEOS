"""A4 / TT-R20-6: a declared fallback chain must be representable, and must not be reachable by accident.

The measured problem: the assignment file (rev 35/36) lists assigned_model + transport_model and no
fallbacks at all, while the pool holds 14 arms. Under strict selection there is then no lawful way to
degrade -- an operator either edits the pool (which silently rewrites the assignment) or turns strictness
off (which is what the naming-only gate effectively did). This locks the SHAPE: fallbacks are read from
the assignment file, are never inferred from the pool, and are reported separately from the primary pair.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISPATCH = ROOT / "scripts" / "hgk-lane-dispatch.py"


def load_module(tmp_assignment: Path):
    spec = importlib.util.spec_from_file_location("hgk_lane_dispatch_a4", DISPATCH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    mod.ASSIGNMENT_FILE = tmp_assignment
    return mod


BASE = {"schema": "HGK-MODEL-LANE-ASSIGNMENT/1", "revision": 99, "registry_epoch": 99}
BASE_ASSIGNMENT = Path(__file__).resolve().parent / "fixtures" / "assignment_primary_gpt61.json"


def write(tmp_path: Path, row: dict) -> Path:
    p = tmp_path / "assignment.json"
    p.write_text(json.dumps({**BASE, "assignment": [row]}, ensure_ascii=False), encoding="utf-8")
    return p


def test_primary_pair_is_reported_separately_from_fallbacks(tmp_path):
    p = write(tmp_path, {"role": "VERIFY_SECURITY", "assigned_provider": "openai-codex",
                         "assigned_model": "gpt-6.1-sol", "transport_model": "gpt-6.1-sol"})
    got = load_module(p).lane_assigned_arms("VERIFY_SECURITY")
    assert got["ok"] is True
    # The assigned pair AND the declared transport model are both primary; rev 36 lists the bare alias
    # `gpt-6.1-sol` next to the qualified form, so both appear and neither is treated as a fallback.
    assert "openai-codex/gpt-6.1-sol" in got["primary_arms"]
    assert "gpt-6.1-sol" in got["primary_arms"]
    assert got["declared_fallbacks"] == []
    assert got["fallbacks_declared"] is False


def test_declared_fallback_strings_are_selectable_and_reported(tmp_path):
    p = write(tmp_path, {"role": "VERIFY_SECURITY", "assigned_provider": "openai-codex",
                         "assigned_model": "gpt-6.1-sol",
                         "fallbacks": ["opencode-go/deepseek-v4.1-flash"]})
    got = load_module(p).lane_assigned_arms("VERIFY_SECURITY")
    assert got["declared_fallbacks"] == ["opencode-go/deepseek-v4.1-flash"]
    assert got["fallbacks_declared"] is True
    assert "opencode-go/deepseek-v4.1-flash" in got["arms"]
    assert "openai-codex/gpt-6.1-sol" in got["primary_arms"]
    assert got["alternates_are_operator_selectable"] is True


def test_declared_fallback_objects_are_selectable(tmp_path):
    p = write(tmp_path, {"role": "PLAN", "assigned_provider": "openai-codex",
                         "assigned_model": "gpt-6.1-sol",
                         "fallbacks": [{"provider": "opencode-go", "model": "deepseek-v4.1-flash"}]})
    got = load_module(p).lane_assigned_arms("PLAN")
    assert got["declared_fallbacks"] == ["opencode-go/deepseek-v4.1-flash"]
    assert "opencode-go/deepseek-v4.1-flash" in got["arms"]


def test_pool_membership_never_creates_a_fallback(tmp_path):
    """A pool arm that the assignment does not name must stay outside `arms`: the pool is not a decision."""
    p = write(tmp_path, {"role": "EXECUTE", "assigned_provider": "opencode-go",
                         "assigned_model": "deepseek-v4.1-flash"})
    got = load_module(p).lane_assigned_arms("EXECUTE")
    assert "openai-codex/gpt-6.1-sol" not in got["arms"]
    assert got["fallback_arms"] == []


def test_declared_fallback_is_never_in_primary_arms(tmp_path):
    """C4 / TT-R20-18: the independent VERIFY lane held this claim because no test excluded a declared
    fallback from primary_arms -- ordering alone was doing the work. Now it is an assertion."""
    d = {"schema": "HGK-MODEL-LANE-ASSIGNMENT/1", "revision": 99, "assignment": [{
        "role": "VERIFY", "assigned_provider": "openai-codex", "assigned_model": "gpt-6.1-sol",
        "transport_model": "gpt-6.1-sol", "authority": "test",
        "fallbacks": [{"provider": "opencode-go", "model": "deepseek-v4.1-flash"}],
    }]}
    p = tmp_path / "assignment.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    got = load_module(p).lane_assigned_arms("VERIFY")
    assert "opencode-go/deepseek-v4.1-flash" not in got["primary_arms"]
    assert "opencode-go/deepseek-v4.1-flash" in got["fallback_arms"]
    assert got["primary_arms"] == ["gpt-6.1-sol", "openai-codex/gpt-6.1-sol"]
    assert "assigned_provider/assigned_model" in got["primary_source"]


def test_served_equivalence_does_not_inherit_the_bare_model_rule():
    """C11: a BARE --require-arm must not accept a serve from an undeclared provider."""
    mod = load_module(BASE_ASSIGNMENT)
    assert mod.arm_equivalent("unlisted-provider/gpt-6.1-sol", "gpt-6.1-sol") is True      # selection
    assert mod.arm_served_equivalent("unlisted-provider/gpt-6.1-sol", "gpt-6.1-sol") is False  # verdict
    assert mod.arm_served_equivalent("desktop_router/gpt-6.1-sol", "openai-codex/gpt-6.1-sol") is True
    assert mod.arm_served_equivalent("opencode-go/gpt-6.1-sol", "openai-codex/gpt-6.1-sol") is False


def test_a_row_declaring_the_same_arm_as_primary_and_fallback_is_refused(tmp_path):
    """C4 / TT-R20-19: the only shape in which the two lists can collide, and the shape that makes the
    separation falsifiable. A contaminating implementation ('primary = list(arms)' AFTER the fallbacks are
    appended) collapses this case into a duplicate -- which is exactly why it must be a refusal, not a union."""
    row = {"role": "VERIFY", "assigned_provider": "openai-codex", "assigned_model": "gpt-6.1-sol",
           "transport_model": "gpt-6.1-sol", "authority": "test",
           "fallbacks": ["openai-codex/gpt-6.1-sol"]}
    got = load_module(write(tmp_path, row)).lane_assigned_arms("VERIFY")
    assert got["ok"] is False
    assert got["code"] == "ERR_ASSIGNMENT_PRIMARY_FALLBACK_OVERLAP"
    assert got["overlap"] == ["openai-codex/gpt-6.1-sol"]


def test_disjoint_primary_and_fallback_still_resolve(tmp_path):
    row = {"role": "VERIFY", "assigned_provider": "openai-codex", "assigned_model": "gpt-6.1-sol",
           "transport_model": "gpt-6.1-sol", "authority": "test",
           "fallbacks": [{"provider": "opencode-go", "model": "deepseek-v4.1-flash"}]}
    got = load_module(write(tmp_path, row)).lane_assigned_arms("VERIFY")
    assert got["ok"] is True
    assert not (set(got["primary_arms"]) & set(got["fallback_arms"]))


def test_alias_equivalent_overlap_is_refused_even_when_the_strings_differ(tmp_path):
    """C4 / TT-R20-20: exact-string overlap detection missed case variants and declared aliases. The arm
    desktop_router/gpt-6.1-sol IS openai-codex/gpt-6.1-sol, so a row that lists one as primary and the other
    as fallback declares the same arm twice."""
    row = {"role": "VERIFY", "assigned_provider": "openai-codex", "assigned_model": "gpt-6.1-sol",
           "transport_model": "gpt-6.1-sol", "authority": "test",
           "fallbacks": ["desktop_router/gpt-6.1-sol"]}
    got = load_module(write(tmp_path, row)).lane_assigned_arms("VERIFY")
    assert got["ok"] is False
    assert got["code"] == "ERR_ASSIGNMENT_PRIMARY_FALLBACK_OVERLAP"


def test_case_variant_overlap_is_refused(tmp_path):
    row = {"role": "VERIFY", "assigned_provider": "OpenAI-Codex", "assigned_model": "GPT-6.1-SOL",
           "transport_model": "gpt-6.1-sol", "authority": "test",
           "fallbacks": ["openai-codex/gpt-6.1-sol"]}
    got = load_module(write(tmp_path, row)).lane_assigned_arms("VERIFY")
    assert got["ok"] is False
    assert got["code"] == "ERR_ASSIGNMENT_PRIMARY_FALLBACK_OVERLAP"
