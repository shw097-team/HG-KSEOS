"""R9-06 regression: `_repo_head()` must resolve the PROJECT target, not the process CWD.

Both tests drive the real lifecycle admission path (no mocks, no fabricated hashes) against real
temporary git repositories. They are RED on the pre-patch code and GREEN after the bounded repair.
"""
from __future__ import annotations

import subprocess

import pytest

from hg_kseos.errors import InvariantViolation
from hg_kseos.lifecycle import ProjectLifecycleController, ProjectRequest
from hg_kseos.spine import SharedSpine


def _mkrepo(path, seed: str = "seed") -> str:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    (path / "seed.txt").write_text(seed, encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "seed.txt"], check=True)
    subprocess.run(
        ["git", "-C", str(path), "-c", "user.email=t@example.invalid", "-c", "user.name=t",
         "commit", "-q", "-m", f"seed {seed}"],
        check=True,
    )
    return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()


def _admit(tmp_path, target) -> tuple[ProjectLifecycleController, str, SharedSpine]:
    spine = SharedSpine(tmp_path / "spine.db")
    spine.initialize()
    controller = ProjectLifecycleController(spine)
    request = ProjectRequest(goal="resolve the project repo head", target_root=str(target))
    pid = "P-R13"
    controller.start(request, project_id=pid)
    controller.intake(pid, request)
    order = ["SOURCE_DISCOVERY", "SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY", "DESIGN_READY"]
    current = controller.status(pid)["state"]
    for state in order[order.index(current) + 1:]:
        controller.transition(pid, state, trigger="r13-test")
    controller.plan(pid)
    return controller, pid, spine


def test_admission_uses_target_head_not_process_cwd(tmp_path, monkeypatch):
    target = tmp_path / "target_repo"
    elsewhere = tmp_path / "cwd_repo"
    target_head = _mkrepo(target, "target")
    cwd_head = _mkrepo(elsewhere, "cwd")
    assert target_head != cwd_head, "the two repos must have different HEADs for this test to mean anything"

    controller, pid, spine = _admit(tmp_path, target)
    monkeypatch.chdir(elsewhere)          # the defect: pre-patch this is what HEAD would come from
    assert cwd_head == subprocess.run(["git", "-C", str(elsewhere), "rev-parse", "HEAD"],
                                      capture_output=True, text=True, check=True).stdout.strip()

    controller.admit_workorders(pid)
    with spine.connect() as conn:
        heads = {row["base_head"] for row in conn.execute("SELECT base_head FROM workorders")}
    assert heads == {target_head}, f"base_head must be the target repo HEAD, got {heads}"


def test_admission_fails_closed_when_target_is_not_a_repo(tmp_path, monkeypatch):
    not_a_repo = tmp_path / "plain_dir"
    not_a_repo.mkdir()
    elsewhere = tmp_path / "cwd_repo"
    _mkrepo(elsewhere)

    controller, pid, _ = _admit(tmp_path, not_a_repo)
    monkeypatch.chdir(elsewhere)          # a valid repo in the CWD must NOT be used as a fallback

    with pytest.raises(InvariantViolation) as excinfo:
        controller.admit_workorders(pid)
    assert "ERR_REPO_HEAD" in str(excinfo.value), f"expected a typed repo-head refusal, got {excinfo.value!r}"
