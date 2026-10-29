"""Regression tests for the durability gates.

Each test names the recurrence class it holds down, because `scripts/recurrence_gate.py` refuses to
let a twice-recurred class be worked again unless its ledger entry points at a test that mentions the
class id. A test that only asserts the happy path is not a regression test.

Class map:
  RC-POLICY-WITHOUT-TRANSACTION  -> test_dirty_policy_is_refused
  RC-DISPOSABLE-REPAIR           -> test_subject_without_repo_is_refused
  RC-POLICY-DRIFT                -> test_reconcile_detects_and_repairs_drift
  RC-ACCEPTANCE-NEVER-GRANTED    -> test_acceptance_requires_grant_or_named_refusal
  RC-VACUOUS-PASS                -> test_manifest_refuses_incomplete_walk
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, *args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(SCRIPTS / script), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)


def make_repo(tmp: Path) -> Path:
    tmp.mkdir(parents=True, exist_ok=True)
    git(tmp, "init", "-q")
    git(tmp, "config", "user.email", "t@example.invalid")
    git(tmp, "config", "user.name", "test")
    (tmp / "config").mkdir(exist_ok=True)
    (tmp / "config" / "model-lane-assignment.json").write_text('{"revision": 1}\n', encoding="utf-8")
    git(tmp, "add", "-A")
    git(tmp, "commit", "-qm", "base")
    return tmp


def test_dirty_policy_is_refused(tmp_path):
    """RC-POLICY-WITHOUT-TRANSACTION: an uncommitted policy must not be usable."""
    repo = make_repo(tmp_path / "repo")
    rc, _ = run("ir1_policy_gate.py", "--repo", str(repo), "--json")
    assert rc == 0, "a committed policy must pass"

    (repo / "config" / "model-lane-assignment.json").write_text('{"revision": 2}\n', encoding="utf-8")
    rc, out = run("ir1_policy_gate.py", "--repo", str(repo), "--json")
    assert rc == 2
    assert json.loads(out.strip().splitlines()[-1])["verdict"] == "POLICY_DIRTY"


def test_subject_without_repo_is_refused(tmp_path):
    """RC-DISPOSABLE-REPAIR: a directory outside version control is not a subject."""
    loose = tmp_path / "loose"
    loose.mkdir()
    (loose / "a.md").write_text("x", encoding="utf-8")
    rc, out = run("ir4_subject_gate.py", "--path", str(loose), "--json")
    assert rc == 3
    assert json.loads(out.strip().splitlines()[-1])["verdict"] == "NO_REPO"

    repo = make_repo(tmp_path / "repo")
    rc, out = run("ir4_subject_gate.py", "--path", str(repo / "config"), "--json")
    assert rc == 0
    assert json.loads(out.strip().splitlines()[-1])["verdict"] == "COMMITTED"


def test_reconcile_detects_and_repairs_drift(tmp_path):
    """RC-POLICY-DRIFT: one authority, and the copies are projections of it."""
    repo = make_repo(tmp_path / "repo")
    (repo / "config" / "lane-routing-registry.yaml").write_text(
        "epoch: 1\nstatus: IN_FORCE\nroutes:\n"
        "- lane: PLAN\n  provider: openai-codex\n  model: gpt-6.1-sol\n  reasoning_effort: medium\n"
        "  fallbacks:\n  - provider: opencode-go\n    model: deepseek-v4.1-flash\n"
        "- lane: EXECUTE\n  provider: opencode-go\n  model: deepseek-v4.1-flash\n  fallbacks: []\n"
        "- lane: VERIFY_SECURITY\n  provider: openai-codex\n  model: gpt-6.1-sol\n  fallbacks: []\n",
        encoding="utf-8")
    (repo / "config" / "model-lane-assignment.json").write_text(
        json.dumps({"revision": 1, "lane_chains": {"PLAN": [
            {"provider": "opencode-go", "model": "deepseek-v4.1-flash"}]}}), encoding="utf-8")
    (repo / "config" / "lane-route-slots.candidate.json").write_text(
        json.dumps({"revision": 1, "lanes": [
            {"lane": "PLAN", "ordered_pool": [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash"}]},
            {"lane": "EXECUTE", "ordered_pool": []},
            {"lane": "VERIFY_SECURITY", "ordered_pool": []}]}), encoding="utf-8")

    script = SCRIPTS / "lane_policy_reconcile.py"
    src = script.read_text(encoding="utf-8")
    patched = (src.replace('ROOT = Path(__file__).resolve().parents[1]', f'ROOT = Path(r"{repo}")'))
    (repo / "reconcile.py").write_text(patched, encoding="utf-8")

    # the repo-local copy is what runs
    p = subprocess.run([sys.executable, str(repo / "reconcile.py"), "--check"], capture_output=True, text=True)
    assert p.returncode == 2, p.stdout + p.stderr
    assert "DRIFT" in p.stdout

    p = subprocess.run([sys.executable, str(repo / "reconcile.py"), "--write"], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    p = subprocess.run([sys.executable, str(repo / "reconcile.py"), "--check"], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    chains = json.loads((repo / "config" / "model-lane-assignment.json").read_text(encoding="utf-8"))["lane_chains"]
    assert chains["PLAN"][0]["model"] == "gpt-6.1-sol"


def test_acceptance_requires_grant_or_named_refusal(tmp_path):
    """RC-ACCEPTANCE-NEVER-GRANTED: NOT_RUN is not a terminal state."""
    rc, out = run("acceptance_default.py", "--round", "R", "--requirement", "REQ")
    assert rc == 2 and "NOT_RUN" in out

    rc, out = run("acceptance_default.py", "--round", "R", "--requirement", "REQ",
                  "--refusal-owner", "OWNER-1", "--expires", "2026-11-30")
    assert rc == 0 and "REFUSED_NAMED" in out

    oracle = tmp_path / "oracle.json"
    verdict = tmp_path / "verdict.json"
    oracle.write_text('{"threshold":"x"}', encoding="utf-8")
    verdict.write_text('{"verdict":"PASS"}', encoding="utf-8")
    import os
    os.utime(oracle, (verdict.stat().st_atime + 10, verdict.stat().st_mtime + 10))
    rc, out = run("acceptance_default.py", "--round", "R", "--requirement", "REQ",
                  "--oracle", str(oracle), "--verdict", str(verdict))
    assert rc == 2 and "AFTER the verdict" in out

    os.utime(oracle, (verdict.stat().st_atime - 10, verdict.stat().st_mtime - 10))
    rc, out = run("acceptance_default.py", "--round", "R", "--requirement", "REQ",
                  "--oracle", str(oracle), "--verdict", str(verdict))
    assert rc == 0 and "GRANTED" in out


def test_manifest_refuses_incomplete_walk(tmp_path):
    """RC-VACUOUS-PASS: a comparator that reports success on missing input is the defect."""
    root = tmp_path / "payload"
    root.mkdir()
    for i in range(3):
        (root / f"f{i}.txt").write_text(str(i), encoding="utf-8")

    tool = SCRIPTS / "durable_import.py"
    if not tool.exists():
        pytest.skip("durable_import.py not present in this checkout")
    p = subprocess.run([sys.executable, str(tool), "--root", str(root), "--id", "t",
                        "--out", str(tmp_path / "out"), "--assert-files", "3"],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    p = subprocess.run([sys.executable, str(tool), "--root", str(root), "--id", "t",
                        "--out", str(tmp_path / "out"), "--assert-files", "9"],
                       capture_output=True, text=True)
    assert p.returncode == 6
    assert "FILE_COUNT_MISMATCH" in p.stdout

    empty = tmp_path / "empty"
    empty.mkdir()
    p = subprocess.run([sys.executable, str(tool), "--root", str(empty), "--id", "e",
                        "--out", str(tmp_path / "out")], capture_output=True, text=True)
    assert p.returncode == 7
    assert "EMPTY" in p.stdout
