#!/usr/bin/env python3
"""selftest_fhs_entry_guard.py — run the FHS hard-entry cases end to end, standalone (stdlib only).

Every case is a REAL subprocess invocation whose stdout+stderr, exit status and decisive fields are
written under `--workdir`. Nothing is asserted about a run that was not executed: a case that cannot
be executed is reported UNRUN (which is a failure of the selftest, not a pass).

Cases
-----
  E01  fresh-process bypass      dispatcher with NO --fhs-binding -> FHS_ENTRY_ASSERT_REQUIRED, exit 20,
                                 zero codex spawns (child-sentinel absent), attempts == []
  POS  positive control          valid reader-minted binding + one-shot capability -> gets PAST the
                                 guard, spawns the child, fails only at the next evidence stage
  E02  token replay              the identical POS dispatch again -> FHS_ENTRY_TOKEN_CONSUMED, exit 29,
                                 zero codex spawns
  E03  epoch drift               binding minted against a scratch mirror, registry bytes replaced ->
                                 FHS_ENTRY_EPOCH_DRIFT, exit 22
  E04  retired arm               --arm opencode-go/mimo-v2.6-pro -> FHS_ENTRY_RETIRED_ARM, exit 24
  E05  no capability             valid binding, no token -> FHS_ENTRY_TOKEN_REQUIRED, exit 28,
                                 zero codex spawns

Usage
-----
  python scripts/selftest_fhs_entry_guard.py [--workdir DIR] [--hgk-root DIR] [--reader PATH]
                                             [--python EXE] [--keep]

Exit status: 0 only when every case ran and matched its expectation; 1 otherwise.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts" / "fhs_entry_guard.py"
DISPATCH = ROOT / "scripts" / "hgk-lane-dispatch.py"
STUB = ROOT / "tests" / "fixtures" / "stub_lane_child_echo_prompt.py"
DEFAULT_HGK = pathlib.Path(r"C:/Projects/Agent_Workspace/FHS/HG-KSEOS")
DEFAULT_READER = pathlib.Path(
    r"C:/Projects/Agent_Workspace/FHS_R26_WT/sbl-3lm/evidence/fhs-w0-r26-repair-20261109/tools/fhs_3lm.py")
LANE = "EXECUTE"
ARM = "opencode-go/deepseek-v4.1-flash"
RETIRED_ARM = "opencode-go/mimo-v2.6-pro"


class Case:
    ok: bool | None = None

    def __init__(self, name: str, expect_exit, expect_code, note: str):
        self.name = name
        self.expect_exit = expect_exit
        self.expect_code = expect_code
        self.note = note
        self.ok = None
        self.observed: dict = {}
        self.failures: list[str] = []

    def check(self, label: str, condition: bool, detail=None) -> None:
        self.observed[label] = detail if detail is not None else condition
        if not condition:
            self.failures.append(f"{label}: {detail!r}" if detail is not None else label)


def stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_case(case: Case, workdir: pathlib.Path, argv: list[str], env_extra=None) -> dict:
    """Execute one case, persist its log, and return {exit, stdout, receipt}."""
    cdir = workdir / case.name
    cdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(env_extra or {})
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL, timeout=900)
    log = cdir / "run.log"
    log.write_text(
        f"# case {case.name}\n# argv: {json.dumps(argv)}\n"
        f"# env: {json.dumps({k: v for k, v in (env_extra or {}).items()})}\n"
        f"# exit: {proc.returncode}\n# --- stdout ---\n{proc.stdout}\n# --- stderr ---\n{proc.stderr}\n",
        encoding="utf-8")
    receipt = None
    for candidate in (cdir / "receipt.json",):
        if candidate.is_file():
            try:
                receipt = json.loads(candidate.read_text(encoding="utf-8"))
            except ValueError:
                receipt = None
    meta = {"case": case.name, "argv": argv, "exit": proc.returncode,
            "log": str(log), "note": case.note}
    (cdir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"exit": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
            "receipt": receipt, "log": str(log), "dir": cdir}


def json_of(stdout: str):
    """The last JSON object printed to stdout (several entry points print a record and nothing else)."""
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except ValueError:
        pass
    start = text.find("{")
    while start != -1:
        try:
            return json.loads(text[start:])
        except ValueError:
            start = text.find("{", start + 1)
    return None


def mint_binding(py: str, reader: pathlib.Path, hgk_root: pathlib.Path, run_id: str,
                 session_id: str, cdir: pathlib.Path) -> tuple[dict | None, dict]:
    argv = [py, str(reader), "--hgk-root", str(hgk_root), "--bind", LANE, "primary",
            "--run-id", run_id, "--session-id", session_id, "--work-id", "L5-SELFTEST"]
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          stdin=subprocess.DEVNULL, timeout=300)
    (cdir / "bind.log").write_text(
        f"# argv: {json.dumps(argv)}\n# exit: {proc.returncode}\n{proc.stdout}\n---\n{proc.stderr}\n",
        encoding="utf-8")
    body = json_of(proc.stdout) or {}
    path = None
    if body.get("path"):
        # the reader prints the binding path relative to ITS round dir, which is the tool dir's parent
        candidate = pathlib.Path(reader).resolve().parent.parent / body["path"]
        path = candidate if candidate.is_file() else None
    return ({"path": str(path) if path else None, "record": body.get("record"),
             "binding_id": body.get("binding_id"), "exit": proc.returncode} if path else None), body


def mint_capability(py: str, binding: pathlib.Path, run_id: str, token: str, hgk_root, reader,
                    entry_dir: pathlib.Path, cdir: pathlib.Path) -> dict:
    argv = [py, str(GUARD), "assert-entry", "--binding", str(binding), "--lane", LANE,
            "--arm", ARM, "--require-bound", "--run-id", run_id, "--guard-token", token,
            "--entry-dir", str(entry_dir)]
    if hgk_root:
        argv += ["--hgk-root", str(hgk_root)]
    if reader:
        argv += ["--binding-reader", str(reader)]
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          stdin=subprocess.DEVNULL, timeout=300)
    (cdir / "mint.log").write_text(
        f"# argv: {json.dumps(argv)}\n# exit: {proc.returncode}\n{proc.stdout}\n---\n{proc.stderr}\n",
        encoding="utf-8")
    return {"exit": proc.returncode, "record": json_of(proc.stdout)}


def dispatcher_argv(binding, run_id, receipt: pathlib.Path, hgk_root, reader,
                    entry_dir=None) -> list[str]:
    argv = [sys.executable, str(DISPATCH), "--lane", LANE, "--prompt", "PROBE_FHS_ENTRY",
            "--nonce", "PROBE_NONCE", "--codex-executable", str(STUB), "--max-candidates", "1",
            "--json-out", str(receipt)]
    if binding:
        argv += ["--fhs-binding", str(binding)]
    if run_id:
        argv += ["--fhs-entry-token", str(run_id)]
    if hgk_root:
        argv += ["--fhs-hgk-root", str(hgk_root)]
    if reader:
        argv += ["--fhs-binding-reader", str(reader)]
    if entry_dir:
        argv += ["--fhs-entry-dir", str(entry_dir)]
    return argv


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="selftest_fhs_entry_guard.py")
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--hgk-root", default=str(DEFAULT_HGK))
    ap.add_argument("--reader", default=os.environ.get("FHS_3LM_PATH") or str(DEFAULT_READER))
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--keep", action="store_true", help="do not prune a previous workdir")
    a = ap.parse_args(argv)

    workdir = pathlib.Path(a.workdir or (ROOT / "var" / "selftest-fhs-entry" / stamp()))
    if workdir.exists() and not a.keep:
        shutil.rmtree(workdir, ignore_errors=True)
    workdir.mkdir(parents=True, exist_ok=True)

    hgk_root = pathlib.Path(a.hgk_root)
    reader = pathlib.Path(a.reader)
    py = a.python
    run_id = f"l5-selftest-{stamp().lower()}-{os.getpid()}"
    entry_dir = workdir / "entry-dir"
    entry_dir.mkdir(parents=True, exist_ok=True)
    print(f"selftest workdir: {workdir}")
    print(f"hgk_root: {hgk_root}  reader: {reader}")
    print(f"run_id:   {run_id}\n")

    cases: list[Case] = []

    # ---- E01: fresh process, no binding -----------------------------------------------------
    c = Case("E01_FRESH_PROCESS_BYPASS", 20, "FHS_ENTRY_ASSERT_REQUIRED",
             "a fresh process with no binding must be refused before any child exists")
    sentinel = workdir / c.name / "child_sentinel.txt"
    receipt = workdir / c.name / "receipt.json"
    out = run_case(c, workdir, dispatcher_argv(None, None, receipt, hgk_root, reader),
                   {"HGK_STUB_PROMPT_OUT": str(sentinel), "FHS_3LM_PATH": str(reader)})
    doc = out["receipt"] or json_of(out["stdout"]) or {}
    c.check("exit", out["exit"] == 20, out["exit"])
    c.check("code", doc.get("code") == "FHS_ENTRY_ASSERT_REQUIRED", doc.get("code"))
    c.check("child_spawned", not sentinel.exists(), sentinel.exists())
    c.check("attempts", doc.get("attempts") == [], doc.get("attempts"))
    c.check("zero_spawn_flag", doc.get("zero_spawn") is True, doc.get("zero_spawn"))
    c.check("stage_is_entry", "fhs_entry" in str(doc.get("stage") or ""), doc.get("stage"))
    cases.append(c)

    # ---- POS: valid binding + valid capability ----------------------------------------------
    c = Case("POS_E01B_BOUND_CONTROL", "not-20..29", "past-the-guard",
             "a bound run must get PAST the entry guard and fail only at the next stage")
    cdir = workdir / c.name
    cdir.mkdir(parents=True, exist_ok=True)
    binding, bind_body = mint_binding(py, reader, hgk_root, run_id, f"sess-{run_id}", cdir)
    if not binding:
        c.failures.append(f"the binding could not be minted by the reader: {json.dumps(bind_body)[:400]}")
        c.ok = False
        cases.append(c)
        print("POS: BLOCKED at binding mint (see above)")
    else:
        cap = mint_capability(py, pathlib.Path(binding["path"]), run_id, "PROBE_TOKEN_POS",
                              hgk_root, reader, entry_dir, cdir)
        c.check("mint_exit", cap["exit"] == 0, cap["exit"])
        sentinel = cdir / "child_sentinel.txt"
        receipt = cdir / "receipt.json"
        out = run_case(c, workdir, dispatcher_argv(binding["path"], run_id, receipt, hgk_root, reader,
                                                   entry_dir),
                       {"HGK_STUB_PROMPT_OUT": str(sentinel)})
        doc = out["receipt"] or json_of(out["stdout"]) or {}
        entry = doc.get("fhs_entry") or {}
        c.observed["exit"] = out["exit"]
        c.check("exit_outside_guard_codes", out["exit"] not in range(20, 30), out["exit"])
        c.check("entry_gate_passed", entry.get("code") is None, entry.get("code"))
        c.check("child_spawned", sentinel.exists(), sentinel.exists())
        c.check("attempts_recorded", len(doc.get("attempts") or []) >= 1,
                [x.get("exit") for x in (doc.get("attempts") or [])])
        c.check("post_guard_failure", doc.get("code") not in (None, ""), doc.get("code"))
        c.check("token_spent", ((entry.get("token") or {}).get("capability") or {}).get("spent") is True,
                ((entry.get("token") or {}).get("capability") or {}).get("spent"))
        c.check("binding_id_recorded", entry.get("arm") == ARM, entry.get("arm"))
        cases.append(c)

    # ---- E02: replay the same capability ----------------------------------------------------
    c = Case("E02_TOKEN_REPLAY", 29, "FHS_ENTRY_TOKEN_CONSUMED",
             "a spent capability must not authorize a second dispatch")
    if not binding:
        c.failures.append("POS could not mint a binding, so the replay has no capability to replay")
        c.ok = False
    else:
        sentinel2 = workdir / c.name / "child_sentinel.txt"
        receipt2 = workdir / c.name / "receipt.json"
        out = run_case(c, workdir, dispatcher_argv(binding["path"], run_id, receipt2, hgk_root, reader,
                                                   entry_dir),
                       {"HGK_STUB_PROMPT_OUT": str(sentinel2)})
        doc = out["receipt"] or json_of(out["stdout"]) or {}
        c.check("exit", out["exit"] == 29, out["exit"])
        c.check("code", doc.get("code") == "FHS_ENTRY_TOKEN_CONSUMED", doc.get("code"))
        c.check("child_spawned", not sentinel2.exists(), sentinel2.exists())
        c.check("attempts", doc.get("attempts") == [], doc.get("attempts"))
    cases.append(c)

    # ---- E03: epoch drift on a scratch mirror ----------------------------------------------
    c = Case("E03_EPOCH_DRIFT", 22, "FHS_ENTRY_EPOCH_DRIFT",
             "registry bytes replaced after the binding was minted must refuse")
    cdir = workdir / c.name
    cdir.mkdir(parents=True, exist_ok=True)
    mirror = cdir / "hgk-mirror"
    (mirror / "config").mkdir(parents=True, exist_ok=True)
    for name in ("lane-routing-registry.yaml", "lane-route-slots.candidate.json",
                 "model-lane-assignment.json", "lane-arm-aliases.json"):
        src = hgk_root / "config" / name
        if src.is_file():
            shutil.copy2(src, mirror / "config" / name)
    drift_run = f"l5-drift-{stamp().lower()}-{os.getpid()}"
    binding3, bind_body3 = mint_binding(py, reader, mirror, drift_run, f"sess-{drift_run}", cdir)
    if not binding3:
        c.failures.append(f"the mirror binding could not be minted: {json.dumps(bind_body3)[:400]}")
        c.ok = False
    else:
        reg = mirror / "config" / "lane-routing-registry.yaml"
        with reg.open("a", encoding="utf-8") as fh:
            fh.write("\n# drift injected by selftest_fhs_entry_guard.py (E03)\n")
        argv_g = [py, str(GUARD), "assert-entry", "--binding", binding3["path"], "--lane", LANE,
                  "--arm", ARM, "--require-bound", "--hgk-root", str(mirror),
                  "--binding-reader", str(reader)]
        out = run_case(c, workdir, argv_g, None)
        doc = json_of(out["stdout"]) or {}
        c.check("exit", out["exit"] == 22, out["exit"])
        c.check("code", doc.get("code") == "FHS_ENTRY_EPOCH_DRIFT", doc.get("code"))
        c.check("bound_sha_differs", ((doc.get("registry") or {}).get("sha256") or "") !=
                (binding3["record"] or {}).get("registry_sha256"), True)
    cases.append(c)

    # ---- E04: retired arm -------------------------------------------------------------------
    c = Case("E04_RETIRED_ARM", 24, "FHS_ENTRY_RETIRED_ARM",
             "the retired arm must be refused by name, with its replacement")
    if not binding:
        c.failures.append("no valid binding to assert the retired arm against")
        c.ok = False
    else:
        argv_g = [py, str(GUARD), "assert-entry", "--binding", binding["path"], "--lane", LANE,
                  "--arm", RETIRED_ARM, "--require-bound", "--hgk-root", str(hgk_root),
                  "--binding-reader", str(reader)]
        out = run_case(c, workdir, argv_g, None)
        doc = json_of(out["stdout"]) or {}
        c.check("exit", out["exit"] == 24, out["exit"])
        c.check("code", doc.get("code") == "FHS_ENTRY_RETIRED_ARM", doc.get("code"))
        c.check("replacement_named",
                (doc.get("retirement") or {}).get("replacement") == "opencode-go/mimo-v2.6-flash",
                (doc.get("retirement") or {}).get("replacement"))
        # independent second witness: the reader refuses the same arm on its own exit 9
        argv_r = [py, str(reader), "--hgk-root", str(hgk_root), "--assert-arm", RETIRED_ARM]
        proc = subprocess.run(argv_r, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", stdin=subprocess.DEVNULL, timeout=300)
        (cdir / "reader_assert_arm.log").write_text(
            f"# argv: {json.dumps(argv_r)}\n# exit: {proc.returncode}\n{proc.stdout}\n", encoding="utf-8")
        c.check("reader_refuses_same_arm", proc.returncode == 9, proc.returncode)
    cases.append(c)

    # ---- E05: valid binding, no capability --------------------------------------------------
    c = Case("E05_NO_CAPABILITY", 28, "FHS_ENTRY_TOKEN_REQUIRED",
             "a valid binding without a one-shot capability must not spawn")
    if not binding:
        c.failures.append("no valid binding")
        c.ok = False
    else:
        sentinel5 = workdir / c.name / "child_sentinel.txt"
        receipt5 = workdir / c.name / "receipt.json"
        out = run_case(c, workdir, dispatcher_argv(binding["path"], None, receipt5, hgk_root, reader,
                                                   entry_dir),
                       {"HGK_STUB_PROMPT_OUT": str(sentinel5)})
        doc = out["receipt"] or json_of(out["stdout"]) or {}
        c.check("exit", out["exit"] == 28, out["exit"])
        c.check("code", doc.get("code") == "FHS_ENTRY_TOKEN_REQUIRED", doc.get("code"))
        c.check("child_spawned", not sentinel5.exists(), sentinel5.exists())
        c.check("attempts", doc.get("attempts") == [], doc.get("attempts"))
    cases.append(c)

    # ---- verdict ----------------------------------------------------------------------------
    print(f"{'case':<26}{'expect':<18}{'observed':<18}{'verdict'}")
    failed = []
    for c in cases:
        if c.ok is None:
            obs_exit = c.observed.get("exit")
            obs_code = c.observed.get("code")
            c.ok = not c.failures
        else:
            obs_exit = c.observed.get("exit")
            obs_code = c.observed.get("code")
        if not c.ok:
            failed.append(c)
        print(f"{c.name:<26}{str(c.expect_exit):<18}{str(obs_exit):<18}"
              f"{'PASS' if c.ok else 'FAIL'}")
        for f in c.failures:
            print(f"    - {f}")
    summary = {"schema": "FHS-ENTRY-SELFTEST/1", "workdir": str(workdir), "run_id": run_id,
               "hgk_root": str(hgk_root), "binding_reader": str(reader),
               "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "cases": [{"case": c.name, "expect_exit": str(c.expect_exit),
                          "expect_code": c.expect_code, "ok": c.ok,
                          "observed": c.observed, "failures": c.failures,
                          "note": c.note, "log": str(workdir / c.name / "run.log")} for c in cases],
               "failed": [c.name for c in failed]}
    (workdir / "SELFTEST_RESULT.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n{'PASS' if not failed else 'FAIL'}: {len(cases) - len(failed)}/{len(cases)} cases "
          f"(result: {workdir / 'SELFTEST_RESULT.json'})")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
