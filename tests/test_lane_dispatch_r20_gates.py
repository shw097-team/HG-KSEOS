"""R20: the two fail-closed gates added to scripts/hgk-lane-dispatch.py (D7 + sealed-home/OAuth).

Both gates refuse BEFORE any spawn, so these tests cost no model call. The control case proves the
gates do not over-refuse an assigned arm: it fails later, on a deliberately missing child binary.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DISPATCH = ROOT / "scripts" / "hgk-lane-dispatch.py"
SEALED = Path(os.environ.get("LOCALAPPDATA", "")) / "HG-KSEOS" / "codex-hermes"
HUMAN = Path.home() / ".codex"
OAUTH = "https://chatgpt.com/backend-api/codex"
LOCAL = "http://127.0.0.1:10101/v1"


def load_module():
    spec = importlib.util.spec_from_file_location("hgk_lane_dispatch_r20", DISPATCH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def run(args):
    r = subprocess.run([sys.executable, str(DISPATCH)] + args, cwd=str(ROOT),
                       capture_output=True, text=True, timeout=180)
    body = (r.stdout or "") + (r.stderr or "")
    try:
        return r.returncode, json.loads(body[body.find("{"):]), body
    except Exception:
        return r.returncode, {}, body


def test_assignment_is_read_and_contains_the_owner_arm():
    mod = load_module()
    asg = mod.lane_assigned_arms("VERIFY_SECURITY")
    assert asg["ok"] is True
    assert "openai-codex/gpt-6.1-sol" in asg["arms"]
    assert asg["revision"] is not None


def test_unknown_role_has_no_assignment():
    mod = load_module()
    asg = mod.lane_assigned_arms("NO_SUCH_ROLE")
    assert asg["ok"] is False
    assert asg["arms"] == []


def test_pool_entry_outside_assignment_is_refused():
    rc, rec, raw = run(["--lane", "VERIFY_SECURITY", "--prompt", "noop", "--nonce", "deadbeefdeadbeef",
                        "--require-arm", "opencode-go/glm-5.3-flash", "--identity-source", "codex-rollout",
                        "--codex-home", str(HUMAN), "--allow-human-home-transport",
                        "--relay-base", LOCAL, "--timeout", "15"])
    assert rc == 4, raw
    assert rec["code"] == "ERR_ARM_NOT_IN_ASSIGNMENT"
    assert rec["lane_assignment"]["arms"], "the refusal must show what IS assigned"


def test_sealed_home_with_oauth_relay_is_refused_before_spawn():
    rc, rec, raw = run(["--lane", "EXECUTE", "--prompt", "noop", "--nonce", "deadbeefdeadbeef",
                        "--codex-home", str(SEALED), "--relay-base", OAUTH, "--timeout", "15"])
    assert rc == 4, raw
    assert rec["code"] == "ERR_SEALED_HOME_OAUTH_TRANSPORT"
    assert "--allow-human-home-transport" in rec["next_command"]


def test_assigned_arm_passes_both_gates():
    """Control: the same dispatch with the assigned arm and a login home is not refused by either gate."""
    rc, rec, raw = run(["--lane", "VERIFY_SECURITY", "--prompt", "noop", "--nonce", "deadbeefdeadbeef",
                        "--require-arm", "openai-codex/gpt-6.1-sol", "--identity-source", "codex-rollout",
                        "--codex-home", str(HUMAN), "--allow-human-home-transport",
                        "--relay-base", OAUTH,
                        "--codex-executable", str(ROOT / "scripts" / "no-such-codex-binary.exe"),
                        "--timeout", "15"])
    assert rec.get("code") not in ("ERR_ARM_NOT_IN_ASSIGNMENT", "ERR_SEALED_HOME_OAUTH_TRANSPORT"), raw

# --------------------------------------------------------------------------------------------------
# R20b: the audit proved the first version was only a NAMING gate -- `--force-rank` still reached
# spawn with an arm outside the lane's assignment. These three cases pin the repaired behaviour.
# --------------------------------------------------------------------------------------------------

STUB = ROOT / "tests" / "fixtures" / "stub_lane_child.py"


def _stub_env(scratch: Path, nonce: str):
    env = dict(os.environ)
    env["HGK_STUB_EMIT_NONCE"] = nonce
    env["HGK_STUB_USAGE"] = str(scratch)
    env["HGK_STUB_USAGE_LINE"] = json.dumps({"provider": "stub", "model": "stub", "status": 200})
    return env


def _run_with_stub(extra_args, nonce="HGK_R20B_NONCE"):
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="r20b-"))
    ledger = tmp / "usage.jsonl"
    ledger.write_bytes(b"")
    r = subprocess.run([sys.executable, str(DISPATCH), "--prompt", "noop", "--nonce", nonce,
                        "--codex-executable", str(STUB), "--usage", str(ledger),
                        "--timeout", "60"] + extra_args,
                       cwd=str(ROOT), capture_output=True, text=True, timeout=180,
                       env=_stub_env(ledger, nonce))
    body = (r.stdout or "") + (r.stderr or "")
    try:
        rec = json.loads((r.stdout or "")[body.find("{"):body.rfind("}") + 1])
    except Exception:
        rec = {}
    return r.returncode, rec, body


def test_lane_group_shape_and_alternates_are_accepted():
    """A rev-33 shaped file (lane_group + non_default_alternates) must not read as 'no assignment'."""
    import tempfile
    mod = load_module()
    tmp = Path(tempfile.mkdtemp(prefix="r20b-asg-"))
    fixture = tmp / "assignment.json"
    fixture.write_text(json.dumps({"revision": 33, "assignment": [{
        "lane_group": "VERIFY_SECURITY", "assigned_provider": "opencode-go",
        "assigned_model": "deepseek-v4.1-flash",
        "non_default_alternates": [{"provider": "openai-codex", "model": "gpt-6.1-sol"}]}]},
        ensure_ascii=False), encoding="utf-8")
    original = mod.ASSIGNMENT_FILE
    try:
        mod.ASSIGNMENT_FILE = fixture
        asg = mod.lane_assigned_arms("VERIFY_SECURITY")
    finally:
        mod.ASSIGNMENT_FILE = original
    assert asg["ok"] is True, asg
    assert asg["shape"] == "lane_group"
    assert set(asg["arms"]) == {"opencode-go/deepseek-v4.1-flash", "openai-codex/gpt-6.1-sol"}
    assert asg["alternates_are_operator_selectable"] is True


def test_require_assigned_arms_filters_the_pool():
    """Strict mode: the serving arm must come from the assignment, and the filtered ones are recorded."""
    rc, rec, body = _run_with_stub(["--lane", "EXECUTE", "--require-assigned-arms"])
    assert rc == 0, body[-1500:]
    assert rec["ok"] is True, body[-1500:]
    posture = rec["assignment_posture"]
    assert posture["enforced"] is True
    assert posture["filtered_out"], "EXECUTE's pool does contain arms outside the assignment"
    assert rec["served_arm_assigned"] is True, rec.get("served_arm")


def test_unassigned_arm_serving_is_warned_not_silent():
    """Default mode keeps fallbacks, but an unassigned serving arm must be visible on receipt + stderr."""
    rc, rec, body = _run_with_stub(["--lane", "EXECUTE", "--force-rank", "2"])
    assert rc == 0, body[-1500:]
    if rec.get("served_arm_assigned") is False:
        assert "WARN_LANE_SERVED_UNASSIGNED_ARM" in body
        assert rec["assignment_posture"]["arms_outside_assignment"]
    else:
        # If the pool/assignment changed so rank 2 is assigned, the case is vacuous rather than green.
        pytest.skip(f"rank 2 resolved to an assigned arm ({rec.get('served_arm')}); case not exercised")


def test_missing_explicit_executable_is_a_typed_refusal_not_a_traceback():
    """TT-R20-7: --codex-executable bypasses the pin gate, so a typo used to surface as an uncaught
    FileNotFoundError from subprocess (no refusal body, no receipt). It must be a typed refusal that
    is only reachable AFTER the two gates above are cleared -- which is what makes it a real control."""
    rc, rec, body = run(["--lane", "VERIFY_SECURITY", "--prompt", "noop", "--nonce", "deadbeefdeadbeef",
                         "--require-arm", "openai-codex/gpt-6.1-sol", "--identity-source", "codex-rollout",
                         "--codex-home", str(HUMAN), "--allow-human-home-transport", "--relay-base", OAUTH,
                         "--codex-executable", str(ROOT / "scripts" / "no-such-codex-binary.exe"),
                         "--timeout", "30"])
    assert rc == 4, body[-1500:]
    assert rec.get("code") == "ERR_CODEX_EXECUTABLE_NOT_FOUND", body[-1500:]
    assert "Traceback" not in body
