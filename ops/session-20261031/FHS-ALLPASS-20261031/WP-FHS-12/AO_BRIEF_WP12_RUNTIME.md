# VERIFY brief — WP-FHS-12, the Hermes runtime path (one work package)

> Third sitting. The first returned clause 2 VOID (the negative's error line was scraped from a shared log and
> predated the run) plus an arithmetic error. The second returned clause 2 FAIL and, more usefully, refused the
> equivalence between the recorded command and the entry `hermes` actually resolves to. Both were acted on: the
> experiment now runs three arms in one clean environment — the product runtime, the PATH shim, and the recovery
> entry `D:\Hermes-Recovery\live22in\hermes` — and reports which entry answers. The claim was narrowed to what
> those arms support. Judge the file as it is now, and say if the narrowing is still too wide.

You are the independent checker. The maker claims the blocker `RUNTIME_PATH_UNRESOLVED` is closed, and that the
cause of the PATH entry's failure is a 260-character module path rather than a missing package. Decide whether
the evidence supports that, clause by clause, from the artefacts only.

Subject (read-only, on this machine):
- `C:\Projects\Agent_Workspace\HG-KSEOS\ops\session-20261031\FHS-ALLPASS-20261031\WP-FHS-12\RUNTIME_PATH_LAB.json`
- `C:\Projects\Agent_Workspace\HG-KSEOS\ops\session-20261031\FHS-ALLPASS-20261031\WP-FHS-12\MAXPATH_CONTROLLED_REPRO.json`
- the scripts: `...\HG-KSEOS\scripts\wp12_runtime_path_lab.py`, `...\scripts\wp12_maxpath_controlled_repro.py`
- the installed package the repro copies from:
  `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\installs\*\environments\*\venv\Lib\site-packages\openai`
- the failing entry: `D:\Hermes-Recovery\live22\bin\hermes` (+ `hermes.cmd` beside it)

Decide each clause PASS or FAIL, naming the field or command output you relied on:

1. `RUNTIME_PATH_LAB.json` records a positive measurement that is a REAL model turn: the nonce it issued appears
   verbatim in the answer, the process exit is 0, and the served model/provider come from a usage file written by
   that same process.
2. The same receipt records a negative through the entry `hermes` resolves to on PATH, that entry did not answer,
   and the error it carries is the one under test (`response_computer_tool_call_output_screenshot_param`), not an
   unrelated failure.
3. `MAXPATH_CONTROLLED_REPRO.json` is a controlled comparison: the payloads at each root are the same .py bytes
   (same file count and same digest), the interpreter is the same, and the only variable is the root length.
4. In that repro, the 259-character case imports and the 260-character case fails with the production error —
   i.e. the failure moves with the length, not with the content.
5. The separate finding is stated honestly: the installed environment also carries extension modules built for
   another CPython, so a "move the directory" repair would not fix it. Say whether the receipt keeps that finding
   separate from the path test instead of using it to explain the path test's result.

If a clause cannot be judged from the artefacts, answer VOID for it and name what is missing; VOID is not PASS.
Write the verdict JSON as the LAST fenced ```json block:

{"requirement":"WP-FHS-12","clauses":[{"id":1,"verdict":"PASS|FAIL","evidence":"..."}, ...],"overall":"PASS|FAIL"}

Do not modify anything: read-only.
