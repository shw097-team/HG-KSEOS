"""WP-12 controlled reproduction: identical payload bytes, one variable (root length), one interpreter.

The PLAN lane's independent reading of FAR-054 was that "260 characters" is a strong lead and not a causal
proof, and it named the experiment: hold the interpreter, the package bytes and the launch conditions
constant, vary only the root, and import the reported module in a fresh process on both sides of the limit.

The first attempt at this script answered the question the wrong way round: it imported the payload from its
*installed* location, which fails earlier and for a different reason — that environment also ships CPython 3.14
extension modules (`pydantic_core.*.pyd` compiled for cp314) into a 3.11 runtime, so the turn dies on
`pydantic_core._pydantic_core` before it ever reaches the module under test. A negative that refuses for the
wrong reason discharges nothing.

So the comparison is built from copies of one source payload:

  B   short root (125-char module path)                        -> expected to import
  C1  same bytes, padded so the module path is 259 chars       -> expected to import
  C2  same bytes, padded so the module path is 260 chars       -> expected to fail on the module under test

and the installed location is measured separately, as its own finding: the environment carries a second,
independent defect (ABI mismatch), which is why "rebuild it at a short root with the matching interpreter"
is the repair rather than "move it".

Usage:
    python scripts/wp12_maxpath_controlled_repro.py --json <out.json>
"""
from __future__ import annotations

try:  # every child of this process must be consoleless
    import winproc as _winproc  # noqa: E402
    _winproc.install()
except Exception:
    pass

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes")
RUNTIME_PY = ROOT / "hermes-agent" / ".hermes-runtime" / "python" / "cpython-3.11.17-windows-x86_64-none" / "python.exe"
VENV_SP = ROOT / "hermes-agent" / "venv" / "Lib" / "site-packages"
INSTALLS = ROOT / "installs"
TARGET_MODULE = "openai.types.responses.response_computer_tool_call_output_screenshot_param"
TARGET_REL = "types/responses/response_computer_tool_call_output_screenshot_param.py"
SCRATCH = pathlib.Path(os.environ.get("TMPDIR", r"C:\Users\user\AppData\Local\Temp")) / "wp12-maxpath"
LIMIT = 259


def py_digest(pkg: pathlib.Path) -> tuple[str, int]:
    """Digest over the package's .py files only: the copies must be provably the same source payload."""
    h = hashlib.sha256()
    n = 0
    base = "\\\\?\\" + str(pkg)
    for root, _dirs, files in os.walk(base):
        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base).replace("\\", "/")
            try:
                with open(full, "rb") as fh:
                    d = hashlib.sha256(fh.read()).hexdigest()
            except OSError as exc:
                d = f"UNREADABLE:{exc.errno}"
            h.update(f"{rel}\0{d}\n".encode())
            n += 1
    return h.hexdigest(), n


def abi_defects(pkg: pathlib.Path) -> dict:
    """Extension modules in the environment that no 3.11 interpreter can load."""
    hits = []
    base = "\\\\?\\" + str(pkg.parent)
    for root, _dirs, files in os.walk(base):
        for f in files:
            if f.endswith((".pyd", ".so")) and ("cp3" in f) and ("cp311" not in f) and ("cp39" not in f):
                hits.append(f)
            if len(hits) > 8:
                break
    return {"foreign_extension_modules": sorted(hits)[:8], "count": len(hits)}


def try_import(pkg_root: pathlib.Path, label: str) -> dict:
    """Fresh 3.11 process; the payload under test first, the product venv behind it for third-party deps.

    The child gets a scrubbed environment: a PYTHONPATH inherited from the caller would put another `openai`
    ahead of the payload and the test would then answer a question nobody asked (measured once: both boundary
    cases "imported" and the module came from the product venv).
    """
    code = (
        "import sys, json, os\n"
        f"root = r'{pkg_root}'\n"
        "sys.path.insert(0, root)\n"
        f"sys.path.append(r'{VENV_SP}')\n"
        "out = {'label': %r, 'sys_path0': sys.path[0], 'root_exists': os.path.isdir(root),\n"
        "       'payload_init': os.path.isfile(os.path.join(root, 'openai', '__init__.py'))}\n"
        "try:\n"
        "    import openai\n"
        f"    from {TARGET_MODULE} import ResponseComputerToolCallOutputScreenshotParam  # noqa: F401\n"
        "    out['ok'] = True\n"
        "    out['openai_file'] = openai.__file__\n"
        "    out['version'] = openai.__version__\n"
        "    out['came_from_payload'] = os.path.normcase(openai.__file__).startswith(os.path.normcase(root))\n"
        "except Exception as exc:\n"
        "    out['ok'] = False\n"
        "    out['error'] = f'{type(exc).__name__}: {exc}'\n"
        "print('RESULT ' + json.dumps(out))\n"
    ) % label
    env = {k: v for k, v in os.environ.items() if k.upper() not in
           ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "HERMES_HOME", "HERMES_PROFILE")}
    started = time.time()
    r = subprocess.run([str(RUNTIME_PY), "-c", code], capture_output=True, text=True, env=env,
                       errors="replace", encoding="utf-8", timeout=300)
    line = next((l for l in r.stdout.splitlines() if l.startswith("RESULT ")), "")
    out = json.loads(line[7:]) if line else {"label": label, "ok": False,
                                             "error": (r.stderr.strip() or "no RESULT line")[-300:]}
    out["duration_s"] = round(time.time() - started, 2)
    out["exit"] = r.returncode
    return out


def root_for_target_len(base: pathlib.Path, target_len: int) -> pathlib.Path:
    """A root under *base* whose <root>/openai/<TARGET_REL> is exactly target_len characters."""
    tail = len("/openai/" + TARGET_REL)
    want = target_len - tail
    return base / ("p" * max(1, want - len(str(base)) - 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    args = ap.parse_args()

    pkgs = sorted(p for p in INSTALLS.glob("*/environments/*/venv/Lib/site-packages/openai") if p.is_dir())
    if not pkgs:
        raise SystemExit("NO_MANAGED_ENV: no installed openai package under installs/*/environments/*")
    installed = pkgs[0]
    installed_sp = installed.parent

    shutil.rmtree("\\?\\" + str(SCRATCH), ignore_errors=True)  # long paths need the prefix
    SCRATCH.mkdir(parents=True, exist_ok=True)

    src_digest, src_files = py_digest(installed)

    # B: short root.
    short_root = SCRATCH / "s"
    shutil.copytree("\\\\?\\" + str(installed), "\\\\?\\" + str(short_root / "openai"), dirs_exist_ok=True)
    b = try_import(short_root, "B_SHORT_ROOT")
    b["measured_target_len"] = len(str(short_root / "openai" / TARGET_REL))
    b_digest, b_files = py_digest(short_root / "openai")

    # C: the boundary, both sides, same bytes.
    boundary = []
    for want in (LIMIT, LIMIT + 1):
        root = root_for_target_len(SCRATCH / "pad", want)
        dst = root / "openai"
        root.mkdir(parents=True, exist_ok=True)
        # Always copy: a leftover from an earlier run made `if not dst.exists()` skip the copy, and the "test"
        # then imported the product venv's openai instead of the payload (measured: payload_init False).
        shutil.copytree("\\\\?\\" + str(installed), "\\\\?\\" + str(dst), dirs_exist_ok=True)
        r = try_import(root, f"C_TARGET_LEN_{want}")
        r["measured_target_len"] = len(str(dst / TARGET_REL))
        r["payload_matches_source"] = py_digest(dst)[0] == src_digest
        boundary.append(r)

    # The installed location measured on its own terms.
    as_installed = try_import(installed_sp, "A_AS_INSTALLED")
    as_installed["openai_root"] = str(installed_sp)
    as_installed["measured_target_len"] = len(str(installed / TARGET_REL))
    as_installed["foreign_abi"] = abi_defects(installed)

    under, over = boundary
    checks = {
        "copies_are_the_same_payload": b_digest == src_digest and b_files == src_files
                                       and under["payload_matches_source"] and over["payload_matches_source"],
        "short_root_imports": b["ok"] is True and b.get("came_from_payload") is True,
        "at_259_imports": under["ok"] is True and under["measured_target_len"] == LIMIT
                          and under.get("came_from_payload") is True,
        "at_260_fails_on_the_module_under_test": over["ok"] is False
                                                and over["measured_target_len"] == LIMIT + 1
                                                and TARGET_MODULE in over.get("error", ""),
    }
    doc = {
        "schema": "HGK-WP12-MAXPATH-REPRO/2",
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "interpreter": str(RUNTIME_PY),
        "hypothesis": "the module is unreachable because its full path is 260 characters, not because it is absent",
        "payload": {"source": str(installed), "py_files": src_files, "digest": src_digest,
                    "short_copy_digest": b_digest},
        "b_short_root": b,
        "c_boundary": boundary,
        "a_as_installed": as_installed,
        "separate_finding_not_part_of_the_test": (
            "the installed environment also ships extension modules built for another CPython, so it cannot be "
            "imported from this 3.11 runtime even at a short path; that is why the repair is a rebuild at a short "
            "root with the matching interpreter, not a move"),
        "max_path_limit": LIMIT,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "verdict_why": ("identical .py payload imports at 259 characters and fails at 260 with the production error, "
                        "so the path is the cause and the package is complete"),
        "falsifier": ("the same payload fails at 259, or imports at 260, or the 260 failure names something other "
                      "than the module under test"),
    }
    out = pathlib.Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree("\\?\\" + str(SCRATCH), ignore_errors=True)  # long paths need the prefix
    print(json.dumps({"verdict": doc["verdict"], "json": str(out),
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                      "checks": checks,
                      "boundary": [(x["measured_target_len"], x["ok"]) for x in boundary],
                      "installed_error": (as_installed.get("error") or "")[:120],
                      "installed_foreign_abi": as_installed["foreign_abi"]["count"]}, ensure_ascii=False))
    return 0 if doc["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
