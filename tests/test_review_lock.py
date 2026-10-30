"""The maker must not be able to commit into a subject a checker is reading.

Regression for the class that lost three checker verdicts on 2026-10-30: two AO sittings ended with
ERR_CHECKER_MUTATED_SUBJECT because the maker committed into the guarded tree mid-turn.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "review_lock.py"
LOCKS = ROOT / "var" / "review-locks"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


def test_lock_covers_the_subject_and_nothing_else(tmp_path):
    nonce = "TEST-LOCK-COVERAGE"
    try:
        acquired = run("acquire", "--subject", str(ROOT / "scripts"), "--nonce", nonce, "--ttl-min", "5")
        assert acquired.returncode == 0, acquired.stderr

        inside = run("check", "--path", str(ROOT / "scripts" / "review_lock.py"))
        assert inside.returncode == 1, "a path inside the locked subject must be refused"
        assert json.loads(inside.stdout)["code"] == "SUBJECT_UNDER_REVIEW"

        outside = run("check", "--path", str(tmp_path / "elsewhere.txt"))
        assert outside.returncode == 0, "a path outside the subject must not be refused"
    finally:
        run("release", "--nonce", nonce)


def test_a_released_lock_does_not_block():
    nonce = "TEST-LOCK-RELEASE"
    try:
        assert run("acquire", "--subject", str(ROOT / "scripts"), "--nonce", nonce).returncode == 0
    finally:
        assert run("release", "--nonce", nonce).returncode == 0
    assert run("check", "--path", str(ROOT / "scripts" / "review_lock.py")).returncode == 0


def test_an_expired_lock_does_not_block(monkeypatch):
    nonce = "TEST-LOCK-EXPIRED"
    LOCKS.mkdir(parents=True, exist_ok=True)
    lock = LOCKS / f"{nonce}.json"
    lock.write_text(json.dumps({
        "nonce": nonce, "subject": str((ROOT / "scripts").resolve()),
        "created_at": "2000-01-01T00:00:00+00:00", "expires_at": "2000-01-01T00:01:00+00:00",
    }), encoding="utf-8")
    try:
        assert run("check", "--path", str(ROOT / "scripts" / "review_lock.py")).returncode == 0, \
            "an expired lock must not wedge the repository"
    finally:
        lock.unlink(missing_ok=True)
