"""The served arm must be provable on the lane that actually pays.

Measured 2026-10-23: an OAuth-direct turn (base https://chatgpt.com/backend-api/codex) consumed the owner's tokens -
turn.completed recorded 243,886 input / 1,182 output - and still produced `ok=false, model=null`, because the wrapper
only trusted the relay's usage ledger and the ChatGPT backend writes no such ledger. The honest lane looked like the
broken one, while the relay lane looked green and paid for nothing.

`resolve_rollout_identity` closes that by reading what the codex client itself recorded for this run and this cwd:
`$CODEX_HOME/sessions/**/rollout-*.jsonl` carries `model_provider` in `session_meta` and the model name in the turn
context. These tests pin the two properties that make it evidence rather than a guess: it must resolve BOTH fields,
and it must not answer for a different cwd.
"""
import importlib.util
import json
import os
import time
from pathlib import Path

DISPATCH = Path(__file__).resolve().parents[1] / "scripts" / "hgk-lane-dispatch.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("hgk_lane_dispatch_identity", DISPATCH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_rollout(home: Path, cwd: str, provider: str, model: str, stamp: float | None = None) -> Path:
    day = home / "sessions" / "2026" / "10" / "23"
    day.mkdir(parents=True, exist_ok=True)
    path = day / ("rollout-2026-10-23T00-00-00-%s.jsonl" % uuidish())
    meta = {"timestamp": "2026-10-23T00:00:00.000Z", "ordinal": 0, "type": "session_meta",
            "payload": {"session_id": "s", "id": "s", "cwd": cwd, "model_provider": provider,
                        "cli_version": "0.163.0-alpha.11"}}
    turn = {"timestamp": "2026-10-23T00:00:01.000Z", "ordinal": 1, "type": "turn_context",
            "payload": {"model": model}}
    path.write_text(json.dumps(meta) + "\n" + json.dumps(turn) + "\n", encoding="utf-8")
    when = stamp if stamp is not None else time.time()
    os.utime(path, (when, when))
    return path


_COUNTER = {"n": 0}


def uuidish() -> str:
    _COUNTER["n"] += 1
    return "test%04d" % _COUNTER["n"]


def test_identity_resolves_from_the_clients_own_rollout(tmp_path):
    mod = _load_module()
    cwd = str(tmp_path / "work")
    Path(cwd).mkdir()
    _write_rollout(tmp_path / "home", cwd, "openai", "gpt-6.1-sol")
    got = mod.resolve_rollout_identity(tmp_path / "home", time.time() - 60, cwd, timeout_s=2)
    assert got is not None
    assert got["provider"] == "openai-codex"      # rollout says "openai"; the declaration names the arm "openai-codex"
    assert got["model"] == "gpt-6.1-sol"
    assert got["source"] == "codex-rollout"


def test_identity_refuses_a_rollout_for_another_cwd(tmp_path):
    mod = _load_module()
    mine = str(tmp_path / "mine")
    other = str(tmp_path / "other")
    Path(mine).mkdir()
    Path(other).mkdir()
    _write_rollout(tmp_path / "home", other, "openai", "gpt-6.1-sol")
    assert mod.resolve_rollout_identity(tmp_path / "home", time.time() - 60, mine, timeout_s=2) is None


def test_identity_refuses_a_rollout_from_before_the_run(tmp_path):
    mod = _load_module()
    cwd = str(tmp_path / "work")
    Path(cwd).mkdir()
    _write_rollout(tmp_path / "home", cwd, "openai", "gpt-6.1-sol", stamp=time.time() - 3600)
    assert mod.resolve_rollout_identity(tmp_path / "home", time.time() - 30, cwd, timeout_s=1) is None


def test_identity_needs_the_model_not_only_the_provider(tmp_path):
    """A rollout with session_meta but no turn context must not yield a half-identity."""
    mod = _load_module()
    cwd = str(tmp_path / "work")
    Path(cwd).mkdir()
    home = tmp_path / "home"
    day = home / "sessions" / "2026" / "10" / "23"
    day.mkdir(parents=True)
    meta = {"type": "session_meta", "payload": {"cwd": cwd, "model_provider": "openai"}}
    (day / "rollout-only-meta.jsonl").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    assert mod.resolve_rollout_identity(home, time.time() - 60, cwd, timeout_s=1) is None
