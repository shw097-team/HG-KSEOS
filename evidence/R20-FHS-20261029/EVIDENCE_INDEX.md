# R20 — FHS-MSC PIPD-LS PKG SKELETON SPINE, revision3 (2026-10-29)

Round: `R20-FHS-20261029` · Subject: `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`
Delivered sibling: `…_r2-revision3` · Claim ceiling: **AUTHOR_SIDE / LOCAL / CANDIDATE**

This bundle exists so an outside engineer can re-run every claim below without access to this host's
`var/` tree. Each claim names the receipt that carries its raw measurement.

---

## 1. What was asked, what was found

| Item | Measurement | Receipt |
|---|---|---|
| r2 file denominator | **85 files / 145,944,348 B** (R19's own tools had measured 44 — `pathlib.rglob` hit MAX_PATH) | `receipts/DENOMINATOR.json` |
| r2 validator, shipped bytes, fresh run | **2788 passed / 1 failed** | `receipts/validate_r2_pristine.out` |
| r2's own shipped report | claimed **2789 passed / 0 failed** | **VOID** — see `notes/VOID_R2_REPORT.md` |
| broken locators carried in from R19 | **29 rows**, each pinned to a 64-hex digest | `receipts/P1B_LOCATOR_REPAIR.json` |
| ZIP self-embedding in r2 | the archive shipped **inside itself** | `notes/VOID_R2_REPORT.md` §3 |

The r2 report is not "slightly off": the same bytes, run again, produce a different verdict than the
report shipped with them. It is voided rather than corrected in place, because a corrected number in
the same file would inherit the same untrustworthiness.

## 2. What revision3 does differently

1. **Hash-gated relocation, not name matching.** A row moves only when the candidate file hashes to the
   pinned 64-hex value; otherwise the row stays HOLD. 29/29 moved.
2. **Line endings normalised to LF** in the added documents — the validator's `markdown_issues()` check
   (`F-23-POS`) reads CRLF as a document-parse issue. Measured: it fired on the first rebuild.
3. **No self-embedded archive.** Derived lists are rebuilt excluding the archive, and the two generated
   TSVs are excluded from their own checksum corpus.
4. **Package counts have one home.** `03_TESTS_AND_READBACK/PACKAGE_DENOMINATOR.json` is written after
   all content exists and before the derived lists, so prose points at it instead of restating numbers
   that can drift. (The independent checker found exactly that drift in pass 1 — see §4.)

## 3. Result

| Metric | Value |
|---|---|
| Files in the shipped tree | **89** |
| Validator (shipped bytes) | **2789 passed / 0 failed** (`AUTHOR_STATIC_FIXTURES_ONLY`) |
| Same-input re-run | semantically identical; the validator writes `elapsed_ms`, so raw byte equality is impossible and is **not** claimed (`receipts/P1C_IDEMPOTENCE.json`) |
| ZIP entries / bytes | 89 / 13,578,116 |
| ZIP sha256 | `0432b9b4e572369d8856803f35b88b85b2d976b3f8d80e9f2f14c30eece1b06c` |
| Rebuild determinism | rebuilt archive equals shipped archive (`receipts/P1E_SHIPPED_VERIFICATION.json`) |
| Disposition tables | `HOLD_DISPOSITION.tsv` **46 rows**, `STAGE18_TRACE.tsv` **18 rows** |

Oracle cell verdicts behind the HOLD table: `PASS_LOCAL_ORACLE 50 / HOLD 46 / DENY 0` (96 cells).

## 4. Independent VERIFY lane (advisory, not acceptance)

Dispatched through `scripts/hgk-lane-dispatch.py`, `--lane VERIFY_SECURITY`, arm pinned by
`--require-arm` + `--force-rank`.

| Pass | Lane result | Verdict |
|---|---|---|
| 1 | `code=ERR_NO_ARM_EMITTED_NONCE` — the brief never told the child to echo the nonce, so the run could not be receipted | `PASS_WITH_FINDINGS`: one real finding — `REVISION3_NOTES.md` still quoted pre-table counts (84 files / 132,391,661 B) |
| 2 | `ok=true`, `required_arm == served_arm == openai-codex/gpt-6.1-sol`, 150.9 s, usage receipt OK, subject mutation CLEAN | **PASS**, 7/7 claims (C1–C7), zero disagreements |

Pass 1 is reported, not hidden: a check that cannot be receipted is not a pass. The finding it raised was
repaired by removing the volatile numbers (single home: `PACKAGE_DENOMINATOR.json`), and pass 2 ran
against the repaired bytes.

**Ceiling:** the lane verdict is advisory. It is not an `OracleReceipt`, not a canonical acceptance
status, and not owner acceptance. Independence is **process-only** (checker and maker share the same
model family); model diversity is **not** claimed.

## 5. Dispatcher gates added in this round

Two pre-spawn refusals in `scripts/hgk-lane-dispatch.py`, both fail-closed with typed codes:

| Code | Trigger | Why it exists |
|---|---|---|
| `ERR_ARM_NOT_IN_ASSIGNMENT` | `--require-arm <arm>` where the arm is absent from `config/model-lane-assignment.json` for that lane | the pool is a routing table, not the decision; otherwise a pool edit silently rewrites the owner's assignment |
| `ERR_SEALED_HOME_OAUTH_TRANSPORT` | OAuth relay (`backend-api/codex`) + a lane home with no `auth.json` | this pair returns 401 **after** a full model call; measured as a slow, expensive false failure |

Ordering matters and was measured: an arm that is absent from the pool keeps
`ERR_LANE_REQUIRED_ARM_ABSENT`, so the assignment gate is placed **after** the pool-membership check.

Tests: `tests/test_lane_dispatch_r20_gates.py` (5 cases: 2 negative, 2 unit, 1 control that proves the
gates do not over-refuse an assigned arm). Suite with the change: **141 passed**; suite without it:
**136 passed** → no regressions.

> An earlier draft resolved `Path.home()` at import time. With a minimal child environment (tests pass a
> bare `env`), that killed the module and turned 13 unrelated lane-guard tests into no-JSON crashes. The
> fix resolves the home lazily inside the refusal path. Recorded because "the gate broke the tests" is a
> real failure mode, not noise.

## 6. Findings that stay open (not hidden)

1. **All 18 stage rows are `ABSENT`** (`tables/STAGE18_TRACE.tsv`): no machine artifact in the package
   carries an instance of any stage's output contract. The trace states the measurement; it does not
   claim the stages were executed.
2. **46 HOLD cells stay HOLD** (`tables/HOLD_DISPOSITION.tsv`), each with its reader class
   (CALIBRATION 11 / HUMAN_DECISION 11 / HUMAN_JUDGE 11 / TWO_VERSION 8 / PERFORMANCE 5), the required
   reader, the next legal action, and the source line + clause digest. They are not converted to PASS.
3. **The repo copy of `config/model-lane-assignment.json` was stale (rev 33)** relative to the machine
   (rev 35: PLAN/VERIFY = `openai-codex/gpt-6.1-sol`, EXECUTE = `opencode-go/deepseek-v4.1-flash`).
   The delivered branch carries rev 35, which is the routing the owner declared for this round; the
   discrepancy is recorded rather than silently reconciled.
4. **Long paths.** 37 of 85 subject paths exceed 260 chars with Win32 long-path support disabled on this
   host. All validation/packaging ran from short roots (`C:\r20pkg*`); the bundled ZIP is the exact
   shipped archive.

## 7. Reproduction

```bash
# 1. subject is frozen: r2-revision2 is never written. r3 is a sibling.
# 2. expand the bundled archive into a SHORT root (long paths are off on this host)
unzip evidence/R20-FHS-20261029/package/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip -d C:/r20check
cd C:/r20check && python -B tools/validate.py
#   expected: passed 2789 / failed 0

# 3. determinism: rebuild the archive from the tree and compare digests
python - <<'PY'
import hashlib, pathlib, zipfile
z = pathlib.Path("C:/r20check/../r3.zip")
# rebuild with the same ordered-entry rule the packaging step used, then:
#   sha256(expected) == 0432b9b4e572369d8856803f35b88b85b2d976b3f8d80e9f2f14c30eece1b06c
PY

# 4. gates
cd <repo> && PYTHONPATH=src python -m pytest tests/test_lane_dispatch_r20_gates.py -q
#   expected: 5 passed
python scripts/hgk-lane-dispatch.py --lane EXECUTE --prompt noop --nonce deadbeefdeadbeef \
  --codex-home "$LOCALAPPDATA/HG-KSEOS/codex-hermes" --relay-base https://chatgpt.com/backend-api/codex
#   expected: exit 4 / ERR_SEALED_HOME_OAUTH_TRANSPORT + the corrected command
```

## 8. Claim ceiling (read before quoting anything here)

```text
revision3 package          = AUTHOR_SIDE_LOCAL, validator green on shipped bytes
independent VERIFY verdict = ADVISORY (process-only independence)
owner acceptance           = NOT_RUN
external acceptance        = NOT_RUN
repo main merge            = NOT_DONE (candidate branch only)
production / live / remote = NOT_CLAIMED
r2-revision2 bytes         = UNMODIFIED (rollback point preserved)
```

Nothing in this bundle may be read as "the package is accepted". It says: the package validates, the
repairs are digest-gated, one independent lane read it and agreed, and the remaining HOLDs are enumerated
with the reader each one needs.
