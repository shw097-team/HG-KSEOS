"""console_window_gate — three-valued verdicts, no vacuous pass.

The gate exists because a hiding flag cannot be verified by reading code: it has to be observed. These tests
pin the three answers on a synthetic ledger so the gate never reports PASS for a window it did not measure.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GATE = ROOT / "scripts" / "console_window_gate.py"


def _ledger(tmp_path: Path, rows: list[dict]) -> Path:
    p = tmp_path / "events.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + ("\n" if rows else ""), encoding="utf-8")
    return p


def _run(*args: str) -> tuple[int, dict]:
    proc = subprocess.run([sys.executable, str(GATE), *args], capture_output=True, text=True)
    body = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, body


def test_window_with_events_fails(tmp_path):
    led = _ledger(tmp_path, [
        {"at": "2026-10-31T02:01:31", "pid": 11, "exe": "WindowsTerminal.exe", "title": "git.EXE", "class": "CASCADIA_HOSTING_WINDOW_CLASS"},
        {"at": "2026-10-31T02:01:33", "pid": 12, "exe": "python.exe", "title": "", "class": "PseudoConsoleWindow"},
    ])
    rc, body = _run("--events", str(led), "--since", "2026-10-31T02:01:00", "--until", "2026-10-31T02:02:00", "--assert-zero")
    assert body["verdict"] == "FAIL"
    assert body["observed"] == 2
    assert body["by_exe"]["WindowsTerminal.exe"] == 1
    assert rc == 1


def test_covered_window_without_events_passes(tmp_path):
    led = _ledger(tmp_path, [
        {"at": "2026-10-31T01:00:00", "pid": 1, "exe": "WindowsTerminal.exe", "title": "", "class": "x"},
        {"at": "2026-10-31T05:00:00", "pid": 2, "exe": "WindowsTerminal.exe", "title": "", "class": "x"},
    ])
    rc, body = _run("--events", str(led), "--since", "2026-10-31T03:00:00", "--until", "2026-10-31T04:00:00", "--assert-zero")
    assert body["verdict"] == "PASS"
    assert body["observed"] == 0
    assert rc == 0


def test_window_before_ledger_is_inconclusive_not_pass(tmp_path):
    led = _ledger(tmp_path, [{"at": "2026-10-31T02:00:00", "pid": 1, "exe": "python.exe", "title": "", "class": "x"}])
    rc, body = _run("--events", str(led), "--since", "2026-10-31T00:10:00", "--until", "2026-10-31T00:20:00", "--assert-zero")
    assert body["verdict"] == "INCONCLUSIVE"
    assert rc == 3


def test_missing_ledger_is_inconclusive(tmp_path):
    rc, body = _run("--events", str(tmp_path / "nope.jsonl"), "--since", "2026-10-31T00:00:00", "--until", "2026-10-31T01:00:00", "--assert-zero")
    assert body["verdict"] == "INCONCLUSIVE"
    assert rc == 3


def test_no_window_argument_is_a_usage_error(tmp_path):
    proc = subprocess.run([sys.executable, str(GATE)], capture_output=True, text=True)
    assert proc.returncode == 2
    assert "ERR_NO_WINDOW" in proc.stderr
