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
