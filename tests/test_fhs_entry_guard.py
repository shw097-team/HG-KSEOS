"""EC-R26-001 / R26-03 — the FHS mechanical pre-dispatch entry guard.

These tests exercise the two properties the r26 external challenge demanded, at both levels:

* **unit** — `scripts/fhs_entry_guard.py` refuses with the named code and its own exit status for every
  way a binding can stop being true (absent, unparsable, epoch drift, pool drift, retired arm, arm
  mismatch, expiry, unresolvable reader), and its one-shot capability cannot be spent twice.
* **process** — `scripts/hgk-lane-dispatch.py` REFUSES BEFORE IT SPAWNS. The dispatch invariant is
  measured with a child sentinel: the stub child writes `$HGK_STUB_PROMPT_OUT` when it runs, so
  "zero spawns" is the absence of a file the child would have written, not a claim in a receipt.

Nothing here is typed into a generator: every refusal code asserted below is the exit status and JSON
that a real subprocess produced. A case whose dependency is missing (the SBL binding reader, or an
epoch-41 control plane carrying the retirement ledger) is SKIPPED with the reason, never silently
passed.
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD_PATH = ROOT / "scripts" / "fhs_entry_guard.py"
DISPATCH = ROOT / "scripts" / "hgk-lane-dispatch.py"
STUB = ROOT / "tests" / "fixtures" / "stub_lane_child_echo_prompt.py"
DEFAULT_HGK = pathlib.Path("C:/Projects/Agent_Workspace/FHS/HG-KSEOS")
DEFAULT_READER = pathlib.Path(
    "C:/Projects/Agent_Workspace/FHS_R26_WT/sbl-3lm/evidence/fhs-w0-r26-repair-20261109/tools/fhs_3lm.py")
LANE = "EXECUTE"
ARM = "opencode-go/deepseek-v4.1-flash"
RETIRED_ARM = "opencode-go/mimo-v2.6-pro"


def _load_guard():
    spec = importlib.util.spec_from_file_location("fhs_entry_guard_under_test", GUARD_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load_guard()


def _hgk_root() -> pathlib.Path:
    override = os.environ.get("FHS_TEST_HGK_ROOT")
    root = pathlib.Path(override) if override else DEFAULT_HGK
    if not (root / "config" / "lane-routing-registry.yaml").is_file():
        pytest.skip(f"no HGK control plane at {root} (set FHS_TEST_HGK_ROOT)")
    return root


def _reader() -> pathlib.Path:
    override = os.environ.get("FHS_3LM_PATH")
    path = pathlib.Path(override) if override else DEFAULT_READER
    if not path.is_file():
        pytest.skip(f"the SBL binding reader is absent at {path} (set FHS_3LM_PATH)")
    return path


def _mirror(tmp_path: pathlib.Path, hgk_root: pathlib.Path) -> pathlib.Path:
    """A scratch copy of the control-plane config: negatives mutate the COPY, never the round."""
    mirror = tmp_path / "hgk-mirror"
    (mirror / "config").mkdir(parents=True, exist_ok=True)
    for name in ("lane-routing-registry.yaml", "lane-route-slots.candidate.json",
                 "model-lane-assignment.json", "lane-arm-aliases.json"):
        src = hgk_root / "config" / name
        if src.is_file():
            shutil.copy2(src, mirror / "config" / name)
    return mirror


def _run(argv, env_extra=None, timeout=300) -> tuple[subprocess.CompletedProcess, dict]:
    env = dict(os.environ)
    env.update(env_extra or {})
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL, timeout=timeout)
    body: dict = {}
    text = (proc.stdout or "").strip()
    if text:
        try:
            parsed = json.loads(text)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            body = parsed
    return proc, body


def _bind(reader, hgk_root, run_id, outdir, lane=LANE, slot="primary", ttl=None):
    """Mint a real binding with the sanctioned issuer. Returns (path, record)."""
    argv = [sys.executable, str(reader), "--hgk-root", str(hgk_root), "--bind", lane, slot,
            "--run-id", run_id, "--session-id", f"sess-{run_id}", "--work-id", "L5-TEST"]
    if ttl is not None:
        argv += ["--ttl", str(ttl)]
    proc, body = _run(argv)
    assert proc.returncode == 0, f"the reader could not mint a binding: {proc.stdout}{proc.stderr}"
    path = pathlib.Path(reader).resolve().parent.parent / body["path"]
    assert path.is_file(), f"the reader reported {body['path']} but it does not exist"
    (pathlib.Path(outdir) / "bind.json").write_text(json.dumps(body, indent=1), encoding="utf-8")
    return path, body["record"]


@pytest.fixture(scope="session")
def bound(tmp_path_factory):
    """One reader-minted binding for the session (the issuer writes under its own round dir)."""
    reader, root = _reader(), _hgk_root()
    outdir = tmp_path_factory.mktemp("binding")
    run_id = f"l5-pytest-{os.getpid()}-{datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')}"
    path, record = _bind(reader, root, run_id, outdir)
    return {"path": path, "record": record, "run_id": run_id, "reader": reader, "hgk_root": root}


# ---------------------------------------------------------------------------------------------
# unit: the gate's own refusals
# ---------------------------------------------------------------------------------------------
def test_no_binding_is_assert_required_exit_20():
    code, rec = guard.gate_entry(binding=None, lane=LANE, arm=ARM, hgk_root=_hgk_root(),
                                 reader=_reader())
    assert (code, rec["code"]) == (20, "FHS_ENTRY_ASSERT_REQUIRED")
    assert rec["ok"] is False


def test_absent_binding_file_is_assert_required_exit_20(tmp_path):
    code, rec = guard.gate_entry(binding=tmp_path / "nope.json", lane=LANE, arm=ARM,
                                 hgk_root=_hgk_root(), reader=_reader())
    assert (code, rec["code"]) == (20, "FHS_ENTRY_ASSERT_REQUIRED")


def test_unparsable_binding_is_binding_invalid_exit_21(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    code, rec = guard.gate_entry(binding=bad, lane=LANE, arm=ARM, hgk_root=_hgk_root(),
                                 reader=_reader())
    assert (code, rec["code"]) == (21, "FHS_ENTRY_BINDING_INVALID")


def test_binding_without_registry_digest_is_binding_invalid_exit_21(tmp_path):
    """A binding that cannot name its epoch is not evidence, whatever else it carries."""
    vague = tmp_path / "vague.json"
    vague.write_text(json.dumps({"schema": "FHS.3LM.Binding/2", "lane": LANE,
                                 "provider": "opencode-go", "model": "deepseek-v4.1-flash"}),
                     encoding="utf-8")
    code, rec = guard.gate_entry(binding=vague, lane=LANE, arm=ARM, hgk_root=_hgk_root(),
                                 reader=_reader())
    assert (code, rec["code"]) == (21, "FHS_ENTRY_BINDING_INVALID")


def test_arm_mismatch_is_refused_exit_25(bound):
    code, rec = guard.gate_entry(binding=bound["path"], lane=LANE, arm="opencode-go/glm-5.3-flash",
                                 hgk_root=bound["hgk_root"], reader=bound["reader"])
    assert (code, rec["code"]) == (25, "FHS_ENTRY_ARM_MISMATCH")


def test_registry_drift_is_epoch_drift_exit_22(bound, tmp_path):
    mirror = _mirror(tmp_path, bound["hgk_root"])
    path, _rec = _bind(bound["reader"], mirror, f"l5-drift-{os.getpid()}",
                       tmp_path)
    reg = mirror / "config" / "lane-routing-registry.yaml"
    reg.write_bytes(reg.read_bytes() + b"\n# drift\n")
    code, rec = guard.gate_entry(binding=path, lane=LANE, arm=ARM, hgk_root=mirror,
                                reader=bound["reader"])
    assert (code, rec["code"]) == (22, "FHS_ENTRY_EPOCH_DRIFT")


def test_pool_drift_is_pool_drift_exit_23(bound, tmp_path):
    mirror = _mirror(tmp_path, bound["hgk_root"])
    path, _rec = _bind(bound["reader"], mirror, f"l5-pdrift-{os.getpid()}", tmp_path)
    pool = mirror / "config" / "lane-route-slots.candidate.json"
    doc = json.loads(pool.read_text(encoding="utf-8"))
    doc["change_log"] = list(doc.get("change_log") or []) + ["drift injected by test"]
    pool.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    code, rec = guard.gate_entry(binding=path, lane=LANE, arm=ARM, hgk_root=mirror,
                                reader=bound["reader"])
    assert (code, rec["code"]) == (23, "FHS_ENTRY_POOL_DRIFT")


def test_retired_arm_is_refused_by_name_exit_24(bound):
    registry = guard.scan_registry(bound["hgk_root"] / "config" / "lane-routing-registry.yaml")
    pool = guard.scan_pool(bound["hgk_root"] / "config" / "lane-route-slots.candidate.json")
    if RETIRED_ARM not in (registry.get("retired") or {}) and RETIRED_ARM not in (pool.get("retired") or {}):
        pytest.skip(f"{RETIRED_ARM} is not in the control plane's retirement ledger")
    code, rec = guard.gate_entry(binding=bound["path"], lane=LANE, arm=RETIRED_ARM,
                                 hgk_root=bound["hgk_root"], reader=bound["reader"])
    assert (code, rec["code"]) == (24, "FHS_ENTRY_RETIRED_ARM")
    assert (rec.get("retirement") or {}).get("replacement", "").startswith("opencode-go/")


def test_expired_binding_is_refused_exit_26(bound, tmp_path):
    """A genuinely expired binding: minted by the reader with a 1 s ttl, then waited out."""
    path, _rec = _bind(bound["reader"], bound["hgk_root"], f"l5-exp-{os.getpid()}", tmp_path, ttl=1)
    import time
    time.sleep(2)
    code, rec = guard.gate_entry(binding=path, lane=LANE, arm=ARM, hgk_root=bound["hgk_root"],
                                 reader=bound["reader"])
    assert (code, rec["code"]) == (26, "FHS_ENTRY_BINDING_EXPIRED")


def test_unresolvable_reader_is_guard_unresolved_exit_27(bound, tmp_path, monkeypatch):
    monkeypatch.setenv("FHS_3LM_PATH", str(tmp_path / "absent-reader.py"))
    monkeypatch.delenv("HGK_ROOT", raising=False)
    code, rec = guard.gate_entry(binding=bound["path"], lane=LANE, arm=ARM,
                                 hgk_root=bound["hgk_root"], reader=None)
    assert (code, rec["code"]) == (27, "FHS_ENTRY_GUARD_UNRESOLVED")


def test_reader_that_cannot_decide_is_not_a_binding_verdict(bound, tmp_path):
    """A reader that crashes is a GATE-resolution failure (27), not 'your binding is invalid'."""
    broken = tmp_path / "broken_reader.py"
    broken.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
    code, rec = guard.gate_entry(binding=bound["path"], lane=LANE, arm=ARM,
                                 hgk_root=bound["hgk_root"], reader=broken)
    assert (code, rec["code"]) == (27, "FHS_ENTRY_GUARD_UNRESOLVED")


# ---------------------------------------------------------------------------------------------
# unit: the one-shot capability
# ---------------------------------------------------------------------------------------------
def test_capability_is_one_shot_and_replay_is_29(bound, tmp_path):
    entry_dir = tmp_path / "entry"
    code, mint = guard.mint_capability(bound["run_id"], "TOKEN-T", LANE, ARM,
                                       {"binding_path": str(bound["path"]),
                                        "binding_id": bound["record"].get("binding_id"),
                                        "binding_sha256": guard.sha256_file(bound["path"]),
                                        "registry": {"sha256": bound["record"].get("registry_sha256")},
                                        "pool": {"sha256": bound["record"].get("pool_sha256")}},
                                       entry_dir=entry_dir)
    assert (code, mint["ok"]) == (0, True)
    first, rec1 = guard.consume_capability(run_id=bound["run_id"], lane=LANE, arm=ARM,
                                          entry_dir=entry_dir, binding_path=bound["path"])
    assert (first, rec1["ok"]) == (0, True)
    second, rec2 = guard.consume_capability(run_id=bound["run_id"], lane=LANE, arm=ARM,
                                           entry_dir=entry_dir, binding_path=bound["path"])
    assert (second, rec2["code"]) == (29, "FHS_ENTRY_TOKEN_CONSUMED")


def test_second_mint_for_the_same_run_is_29(bound, tmp_path):
    entry_dir = tmp_path / "entry"
    gate = {"binding_path": str(bound["path"]), "binding_id": "x", "binding_sha256": None,
            "registry": {}, "pool": {}}
    code1, _ = guard.mint_capability("run-x", "TOK", LANE, ARM, gate, entry_dir=entry_dir)
    code2, rec2 = guard.mint_capability("run-x", "TOK", LANE, ARM, gate, entry_dir=entry_dir)
    assert code1 == 0
    assert (code2, rec2["code"]) == (29, "FHS_ENTRY_TOKEN_CONSUMED")


def test_absent_capability_is_28(tmp_path):
    code, rec = guard.consume_capability(run_id="no-such-run", lane=LANE, arm=ARM,
                                        entry_dir=tmp_path / "entry")
    assert (code, rec["code"]) == (28, "FHS_ENTRY_TOKEN_REQUIRED")


def test_expired_capability_is_28_with_reason(tmp_path):
    entry_dir = tmp_path / "entry"
    gate = {"binding_path": None, "binding_id": "x", "binding_sha256": None,
            "registry": {}, "pool": {}}
    past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
    code, _ = guard.mint_capability("run-old", "TOK", LANE, ARM, gate, entry_dir=entry_dir, now=past,
                                    ttl=1)
    assert code == 0
    code, rec = guard.consume_capability(run_id="run-old", lane=LANE, arm=ARM, entry_dir=entry_dir)
    assert (code, rec["code"]) == (28, "FHS_ENTRY_TOKEN_REQUIRED")
    assert rec.get("reason") == "token_expired"


def test_capability_arm_mismatch_is_25(bound, tmp_path):
    entry_dir = tmp_path / "entry"
    gate = {"binding_path": str(bound["path"]), "binding_id": "x", "binding_sha256": None,
            "registry": {}, "pool": {}}
    guard.mint_capability("run-arm", "TOK", LANE, ARM, gate, entry_dir=entry_dir)
    code, rec = guard.consume_capability(run_id="run-arm", lane=LANE, arm="opencode-go/glm-5.3-flash",
                                        entry_dir=entry_dir)
    assert (code, rec["code"]) == (25, "FHS_ENTRY_ARM_MISMATCH")


# ---------------------------------------------------------------------------------------------
# unit: record-shape tolerance (field LOCATION only, never the predicate)
# ---------------------------------------------------------------------------------------------
def test_legacy_nested_epoch_record_is_read_by_location(tmp_path):
    """/1 bindings nested `epoch: {registry_sha256: ...}`; the reader owns their meaning, but the
    gate must still FIND the digest instead of reporting it absent."""
    legacy = {"schema": "FHS.3LM.Binding/1", "lane": LANE, "provider": "opencode-go",
              "model": "deepseek-v4.1-flash", "pool_sha256": "a" * 64,
              "epoch": {"registry_sha256": "b" * 64}}
    assert guard.binding_field(legacy, "registry_sha256") == "b" * 64
    assert guard.binding_field(legacy, "pool_sha256") == "a" * 64
    assert guard.binding_arm(legacy) == "opencode-go/deepseek-v4.1-flash"


def test_reader_code_map_is_total_over_the_shipped_refusal_vocabulary():
    for reader_code in ("EPOCH_DRIFT", "POOL_DIGEST_DRIFT", "RETIRED_ARM", "ARM_LEFT_POOL",
                        "BINDING_EXPIRED", "BINDING_TAMPERED", "HOLD_REGISTRY_POOL_DRIFT",
                        "ERR_HGK_ROOT_UNRESOLVED", "ERR_EPOCH_UNRESOLVED", "NOT_IN_LANE_POOL"):
        assert guard.READER_CODE_MAP[reader_code] in guard.EXIT_CODES
    for exit_status in (6, 7, 9):
        assert guard.READER_EXIT_MAP[exit_status] in guard.EXIT_CODES


# ---------------------------------------------------------------------------------------------
# process: the dispatcher refuses BEFORE it spawns
# ---------------------------------------------------------------------------------------------
def _dispatch_argv(tmp_path, binding=None, run_id=None, entry_dir=None, receipt_name="receipt.json",
                   hgk_root=None, reader=None):
    receipt = tmp_path / receipt_name
    argv = [sys.executable, str(DISPATCH), "--lane", LANE, "--prompt", "PROBE", "--nonce",
            "PROBE_NONCE", "--codex-executable", str(STUB), "--max-candidates", "1",
            "--json-out", str(receipt)]
    if binding is not None:
        argv += ["--fhs-binding", str(binding)]
    if run_id is not None:
        argv += ["--fhs-entry-token", str(run_id)]
    if entry_dir is not None:
        argv += ["--fhs-entry-dir", str(entry_dir)]
    if hgk_root is not None:
        argv += ["--fhs-hgk-root", str(hgk_root)]
    if reader is not None:
        argv += ["--fhs-binding-reader", str(reader)]
    return argv, receipt


def test_dispatcher_without_binding_spawns_nothing(tmp_path):
    """E01: the finding's own falsifier, measured with a child sentinel."""
    sentinel = tmp_path / "child_would_have_written_here.txt"
    argv, receipt = _dispatch_argv(tmp_path)
    proc, _ = _run(argv, {"HGK_STUB_PROMPT_OUT": str(sentinel)})
    assert proc.returncode == 20
    assert not sentinel.exists(), "the dispatcher spawned a child without a session binding"
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["code"] == "FHS_ENTRY_ASSERT_REQUIRED"
    assert doc["attempts"] == []
    assert doc["zero_spawn"] is True


def test_dispatcher_with_binding_but_no_capability_spawns_nothing(bound, tmp_path):
    """The second half of the gate: a binding alone does not authorize a spawn."""
    sentinel = tmp_path / "child_would_have_written_here.txt"
    argv, receipt = _dispatch_argv(tmp_path, binding=bound["path"], entry_dir=tmp_path / "entry",
                                   hgk_root=bound["hgk_root"], reader=bound["reader"])
    proc, _ = _run(argv, {"HGK_STUB_PROMPT_OUT": str(sentinel)})
    assert proc.returncode == 28
    assert not sentinel.exists(), "the dispatcher spawned a child without a spent capability"
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["code"] == "FHS_ENTRY_TOKEN_REQUIRED"
    assert doc["attempts"] == []


def test_bound_dispatched_run_passes_the_guard_and_then_replays_are_29(bound, tmp_path):
    """POS + E02 in one process pair: the capability opens the gate once and never twice."""
    entry_dir = tmp_path / "entry"
    mint = [sys.executable, str(GUARD_PATH), "assert-entry", "--binding", str(bound["path"]),
            "--lane", LANE, "--arm", ARM, "--require-bound", "--run-id", bound["run_id"],
            "--guard-token", "TOKEN-POS", "--entry-dir", str(entry_dir),
            "--hgk-root", str(bound["hgk_root"]), "--binding-reader", str(bound["reader"])]
    proc, minted = _run(mint)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert minted["capability"]["ok"] is True

    sentinel = tmp_path / "child_ran.txt"
    argv, receipt = _dispatch_argv(tmp_path, binding=bound["path"], run_id=bound["run_id"],
                                   entry_dir=entry_dir, receipt_name="pos.json",
                                   hgk_root=bound["hgk_root"], reader=bound["reader"])
    proc, _ = _run(argv, {"HGK_STUB_PROMPT_OUT": str(sentinel)})
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert proc.returncode not in set(range(20, 30)), doc.get("code")
    assert sentinel.exists(), "the guarded run never reached the child"
    assert (doc.get("fhs_entry") or {}).get("code") is None
    assert (doc.get("fhs_entry") or {}).get("token", {}).get("capability", {}).get("spent") is True
    assert len(doc["attempts"]) == 1

    sentinel2 = tmp_path / "child_ran_twice.txt"
    argv2, receipt2 = _dispatch_argv(tmp_path, binding=bound["path"], run_id=bound["run_id"],
                                     entry_dir=entry_dir, receipt_name="replay.json",
                                     hgk_root=bound["hgk_root"], reader=bound["reader"])
    proc2, _ = _run(argv2, {"HGK_STUB_PROMPT_OUT": str(sentinel2)})
    doc2 = json.loads(receipt2.read_text(encoding="utf-8"))
    assert proc2.returncode == 29
    assert doc2["code"] == "FHS_ENTRY_TOKEN_CONSUMED"
    assert not sentinel2.exists(), "a spent capability authorized a second child"
