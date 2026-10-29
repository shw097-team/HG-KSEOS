# R20 — FHS-MSC PIPD-LS PKG SKELETON SPINE, revision3 (2026-10-29, round R20 + repair R20b)

Round: `R20-FHS-20261029` · Subject: `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`
Delivered artifact: `…_r2-revision3.zip` · Claim ceiling: **AUTHOR_SIDE / LOCAL / CANDIDATE**

Everything below is a measurement with a receipt. Where a measurement contradicted the author, the
contradiction is kept and the artifact was rebuilt — not the number.

---

## 1. What was asked, what was found

| Item | Measurement | Receipt |
|---|---|---|
| r2 file denominator | **85 files / 145,944,348 B** (R19 measured 44 — `pathlib.rglob` hit MAX_PATH) | `receipts/DENOMINATOR.json` |
| r2 validator, shipped bytes, fresh run | **2788 passed / 1 failed** | `receipts/validate_r2_pristine.out` |
| r2's shipped report | claimed **2789 / 0** | **VOID** — `notes/VOID_R2_REPORT.md` |
| locators carried in from R19 | **29 rows**, each pinned to a 64-hex digest | `receipts/P1B_LOCATOR_REPAIR.json` |
| r2 archive | shipped **inside itself** | void notice §3 |

The r2 report is not "slightly off": the same bytes produce a different verdict than the report shipped
with them. It is voided rather than corrected in place — a corrected number in the same file inherits the
same untrustworthiness.

## 2. What revision3 does differently

1. **Hash-gated relocation** — a row moves only when the candidate file hashes to the pinned 64-hex value.
   29/29 moved; name/prefix similarity is never evidence.
2. **LF normalisation** of added documents — the validator's document-parse check (`F-23-POS`) reads CRLF
   as a defect (measured on the first rebuild).
3. **No self-embedded archive**; derived lists exclude the archive, and the two generated TSVs exclude
   themselves from their own checksum corpus.
4. **One home for package counts** — `03_TESTS_AND_READBACK/PACKAGE_DENOMINATOR.json`, written after all
   content exists and before the derived lists (independent pass 1 caught prose drift here).
5. **Checksum list written last and verified at build time** (R20b, §4).

## 3. Result (final bytes)

| Metric | Value |
|---|---|
| Files in the archive | **89** (0 directory entries) |
| Tree bytes | 132,416,007 |
| Validator, fresh extract of the shipped archive | **2789 passed / 0 failed** (`AUTHOR_STATIC_FIXTURES_ONLY`) |
| Same-input re-run | semantically identical; the validator writes `elapsed_ms`, so raw byte equality is **not** claimed (`receipts/P1C_IDEMPOTENCE.json`) |
| Archive sha256 | **`ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f`** |
| Archive bytes | 13,578,117 |
| Rebuild from the tree | byte-identical archive (deterministic) |
| Superseded first build | `0432b9b4…` kept as `build/SUPERSEDED_r20_first_build.zip` |
| Disposition tables | `HOLD_DISPOSITION.tsv` **46 rows**, `STAGE18_TRACE.tsv` **18 rows** |

Oracle cell verdicts behind the HOLD table: `PASS_LOCAL_ORACLE 50 / HOLD 46 / DENY 0` (96 cells).

Two receipts need reading together, and saying so is cheaper than letting someone misread them:

- `receipts/P1D_PACKAGE.json` records the **13:13 build** (`0432b9b4…`, the one whose checksum list was
  stale). `receipts/P1D_R20B_CHECKSUM_REPAIR.json` is the authoritative record of the shipped archive:
  source `0432b9b4…` → rebuilt `ee009117…`, 88/88 rows verified.
- `receipts/P1C_VALIDATE.json` reports `idempotent: false` / `reproducible: false` — that is **raw byte**
  equality, which cannot hold because the validator writes `elapsed_ms`. The claim actually made is the
  **verdict projection**, and `receipts/P1C_IDEMPOTENCE.json` measures exactly that: identical semantic
  digest `534fa4c1…` across runs, 2789 passed / 0 failed.

## 4. R20b — the two defects the parallel audit found, and what changed

The audit (three read-only sub-agents, `audit/AUDIT_ROUND.md`) was asked to falsify the author's claims.
It found two real defects:

**D1 — the checksum list pinned a stale `MANIFEST.md`.** 87/88 rows correct; the `MANIFEST.md` row held
the **pre-write** digest (`6f22bc10…` vs actual `8ece6d7e…`). `tools/validate.py` never reads that list,
so the 2789 PASS did not cover it. Root cause: the list was generated *before* `MANIFEST.md` was rewritten.
Repair: packaging order inverted, and the list is now **verified row-by-row at build time** (any miss aborts
with `CHECKSUM_LIST_INVALID`). The shipped archive was rebuilt from its own bytes with that one row
corrected: **88/88 rows verified, 0 missing, 0 stale** (`receipts/P1D_R20B_CHECKSUM_REPAIR.json`).

**D2 — the assignment gate was a naming gate, not a dispatch gate.** The gate body was
`if args.require_arm:`, so `--force-rank 3` still reached spawn with an arm outside the lane's assignment
(9 of 14 pool arms are in that position). Repair: `--require-assigned-arms` (strict selection, typed
`ERR_NO_ASSIGNED_ARM`), plus always-on detection — the receipt records `served_arm_assigned` and an
unassigned serving arm emits `WARN_LANE_SERVED_UNASSIGNED_ARM`. Strict is **not** the default because the
assignment file lists no fallbacks; making it default would void the documented PLAN/VERIFY fallback chain
(TT-R20-6, owner decision).

## 5. Dispatcher gates added this round

| Code | Trigger | Rationale |
|---|---|---|
| `ERR_ARM_NOT_IN_ASSIGNMENT` | `--require-arm` names an arm absent from the lane's assignment | a pool entry is not the owner's routing decision |
| `ERR_SEALED_HOME_OAUTH_TRANSPORT` | OAuth relay + a lane home with no `auth.json` | this pair 401s **after** a full model call |
| `ERR_LANE_ASSIGNMENT_NO_ROW` | assignment file reads fine but has no row for the role | distinct from a read failure |
| `ERR_NO_ASSIGNED_ARM` | `--require-assigned-arms` and no assigned arm is in the pool | strict selection emptied the pool |
| `ERR_CODEX_EXECUTABLE_NOT_FOUND` | `--codex-executable` names a path that does not resolve | that flag **bypasses** the pin gate, so a typo used to surface as an uncaught `FileNotFoundError` from `subprocess` — no refusal body, no receipt (TT-R20-7, now repaired) |

Ordering is deliberate and measured: an arm absent from the *pool* keeps `ERR_LANE_REQUIRED_ARM_ABSENT`,
so the assignment gate sits after the pool-membership check. Tests: **9 new**;
suite **145 passed** with the change, **136 without** → 0 regressions.

> The negative-test receipt was itself wrong once, and that is recorded rather than tidied away: the
> first version scored the control case as "pass" whenever the run *did not* return one of the two new
> codes — so an uncaught traceback counted as success. A control that accepts a crash cannot distinguish
> "gates cleared" from "gates never ran". The control now requires `ERR_CODEX_EXECUTABLE_NOT_FOUND`,
> a code only reachable **after** both gates, and the assertion is equality, not `not in`.

> Two self-inflicted defects were found and fixed en route, both recorded because they are the exact
> failure modes that make "tests are green" meaningless: (a) the first gate ordering masked the more
> specific pool refusal; (b) an import-time `Path.home()` killed the module under a minimal child env and
> took 13 unrelated lane-guard tests with it.

## 6. Independent VERIFY lane (advisory, not acceptance)

| Pass | Lane receipt | Verdict | Notes |
|---|---|---|---|
| 1 | `ERR_NO_ARM_EMITTED_NONCE` (brief never asked for the nonce) | `PASS_WITH_FINDINGS` | found real drift in the package notes → repaired by centralising counts |
| 2 | **`ok=true`**, `required == served == openai-codex/gpt-6.1-sol`, 150.9 s, usage OK | **PASS**, C1–C7 | against the **first** build (`0432b9b4…`) |
| 3 | `ERR_NO_ARM_EMITTED_NONCE` | **HOLD** | C9 untestable: the brief never stated the expected archive digest. Correct behaviour — an untestable claim is not a pass |
| 4 | `ERR_NO_ARM_EMITTED_NONCE` | **PASS_WITH_FINDINGS**, C1–C9 all PASS, mutation CLEAN | against the repaired archive `ee009117…`; findings are the known baseline defect + brief wording |
| 5 | `ERR_NO_ARM_EMITTED_NONCE` | focused re-check **C8 PASS** (88/88 rows), **C9 PASS** (sha/bytes/entries equal) | `lane/FOCUSED_RECHECK_R20.json`, nonce `7143390aec96508f` |

Passes 3–5 produced verdicts but **no receipt-able lane identity/nonce** (`served_arm: null`), which
appeared only after `--guard-subject` was pointed at the 13.5 MB archive. Recorded as TT-R20-7 rather than
smoothed over: the verdicts are attributable by the nonce they quote, but the lane did not certify them.
The single receipted turn is pass 2, and it covers the first build.

**Ceiling:** the lane verdict is advisory. It is not an `OracleReceipt`, not a canonical acceptance
status, and not owner acceptance. Independence is **process-only** (same model family as the maker);
model diversity is **not** claimed.

## 6b. Configuration snapshot this evidence pins — and when the host moved

The committed `config/model-lane-assignment.json` is **revision 35 / registry_epoch 34**. The **host** file
is now **revision 36 / registry_epoch 36**, with exactly two field changes:

```text
PLAN            transport_model: opencode-go/deepseek-v4.1-flash -> gpt-6.1-sol
VERIFY_SECURITY transport_model: opencode-go/deepseek-v4.1-flash -> gpt-6.1-sol
(assigned_provider / assigned_model / authority unchanged in both rows)
```

**The change happened mid-round, not after it.** The lane receipts date it: the P3 gate tests at
`13:22:34Z` recorded `revision: 35` (arms without the bare `gpt-6.1-sol` alias), while passes 3–5 at
`13:49:52Z` / `13:54:52Z` / `13:57:00Z` all quote `revision: 36` with arms
`["gpt-6.1-sol", "openai-codex/gpt-6.1-sol"]`. Pass 2 (`13:16:42Z`) predates the `assignment_posture`
field, so it carries no revision at all — its lane identity (`required == served == openai-codex/gpt-6.1-sol`)
is unaffected by the change, since both revisions assign that model to VERIFY_SECURITY.

Two honest readings, both of which belong here:

1. **Rev 35 was internally inconsistent with the owner's role order.** For PLAN and VERIFY_SECURITY the row
   said `assigned_model: gpt-6.1-sol` while its `transport_model` pointed at deepseek. Rev 36 removes that
   contradiction. This round's lanes were dispatched with `--require-arm openai-codex/gpt-6.1-sol` over the
   OAuth relay — matching the owner order — and the gate compares against `assigned_model`, so lane
   behaviour was right even while the committed row contradicted itself.
2. **This branch pins rev 35, not rev 36.** A later reader must not assume the shipped routing snapshot
   equals the live host, and must not assume the round ran entirely under one revision — passes 3–5 ran
   after the host had already moved. Recorded as TT-R20-10 rather than absorbed, because silently
   re-baselining evidence onto a config the earlier phases never ran against is exactly the move that makes
   receipts decorative.


### 6c. The lane receipts' nonce fields contradict their own preserved bytes

Measured on the three unreceipted passes:

```text
pass   stdout_bytes (recorded)   file bytes   nonce bytes in that file   recorded nonce_present_raw_stdout
3      184,826                  184,826      True                       False
4      145,105                  145,105      True                       False
5      21,443                   21,443       True                       False
```

The attempt log is written **byte-exact from the captured buffer** (`write_bytes(raw)`), so a plain byte
search over exactly that buffer cannot be false while the nonce is in the file. A control run of the
current source against the deterministic stub child (`HGK_STUB_EMIT_NONCE=<the dispatched nonce>`) records
`nonce_present: true` **and** `nonce_present_raw_stdout: true`, so the source in this branch does not
reproduce the false negative.

Conclusion, stated at the ceiling the evidence supports: **those three receipts were not produced by this
source revision's capture path** (an older binary or a different composition path — the front door — is
the remaining candidate; the producer is *not* identified). Consequence for readers: their `ok: false` and
their `nonce_*` fields are **not citable evidence either way**; only the verdict documents they wrote
(`VERDICT_R20D_HOLD.json`, `VERDICT_R20E_PASS_WITH_FINDINGS.json`, `FOCUSED_RECHECK_R20.json`) are, and
those are advisory by construction. TT-R20-9.

## 7. Findings that stay open

1. **18/18 stage rows are `ABSENT`** — no machine artifact carries an instance of any stage's output
   contract.
2. **46 HOLD cells stay HOLD**, each annotated with the reader class it needs (CALIBRATION 11 /
   HUMAN_DECISION 11 / HUMAN_JUDGE 11 / TWO_VERSION 8 / PERFORMANCE 5) and the next legal action.
3. **Assignment file lists no fallbacks** (TT-R20-6) — a policy decision, not an agent one.
4. **Long paths**: 37 of 85 subject paths exceed 260 chars on this host (max absolute path 289 chars);
   all work ran from short roots.
5. `validate.py` rewrites 4 files in the tree it runs in → checksum verification must use a fresh extract.

## 8. Reproduction

```bash
# 1. r2-revision2 stays frozen; the delivered artifact is the archive.
unzip evidence/R20-FHS-20261029/package/*_r2-revision3.zip -d C:/r20check     # short root: long paths are off here
cd C:/r20check && python -B tools/validate.py                                # expected: 2789 passed / 0 failed

# 2. checksum list (R20b): every row must match
python - <<'PY'
import hashlib, pathlib
root = pathlib.Path("C:/r20check")
bad = []
for ln in (root/"03_TESTS_AND_READBACK/artifact_checksums.sha256").read_text(encoding="utf-8").splitlines():
    h, name = ln.split("  ", 1)
    if hashlib.sha256((root/name).read_bytes()).hexdigest() != h:
        bad.append(name)
print("mismatched:", bad)          # expected: []
PY

# 3. archive identity
sha256sum evidence/R20-FHS-20261029/package/*_r2-revision3.zip
#   expected: ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f

# 4. gates
PYTHONPATH=src python -m pytest tests/test_lane_dispatch_r20_gates.py -q      # expected: 8 passed
```

## 9. Claim ceiling (read before quoting anything here)

```text
revision3 archive           = AUTHOR_SIDE_LOCAL; validator green on shipped bytes; checksum list verified
independent VERIFY verdict  = ADVISORY (process-only independence; one receipted turn, on the first build)
owner acceptance            = NOT_RUN
external acceptance         = NOT_RUN
repo main merge             = NOT_DONE (candidate branch only)
production / live / remote  = NOT_CLAIMED
r2-revision2 bytes          = UNMODIFIED (85/85 hashes re-measured by an independent sub-agent)
```

Nothing here says "the package is accepted". It says: the archive validates, its own integrity lists are
now verified rather than decorative, the repairs are digest-gated, an independent lane read it and found
no disagreement it could substantiate, and everything still open is enumerated with the reader it needs.

---

## §9 Closure round (owner-authorized, 2026-10-29) — `CLOSURE_ROUND.md`

The FAR closure plan (`analysis/FAR_CLOSURE_AND_PROMOTION_20261029.md`, `analysis/CLOSURE_PLAN.json`) was
executed under an owner authorization anchored to exact bytes, not to a sentence in a chat log.

| claim | where it is checkable |
|---|---|
| A1..A8 machine items executed and re-measured | `CLOSURE_ROUND.md` §1; `tools/evidence_reconcile.py`, `tools/config_drift.py`, `tools/compare_lane_receipts.py`, `tools/render_owner_requests.py`; tests `test_lane_assignment_fallbacks.py` (10), `test_lane_dispatch_r20_gates.py` (11) |
| 8 owner packets cover all 75 residues exactly once | `owner_requests/OR-1..OR-8` (json+md); verify with `render_owner_requests.py --check` |
| owner authorization is a real, third-party-verifiable act | `owner_receipts/OWNER_AUTHORIZATION_R20.summary.json` — carries `body_json` + `owner_public_hex`; sha256 + Ed25519 verify with no key file |
| six falsification rounds, final 6 PASS / 4 HOLD / 0 FAIL | `lane/CLOSURE_VERIFY_R20_R6.json`, `lane/BRIEF_VERIFY_CLOSURE.md`, `var/R20-FHS-20261029/lane/receipts_attempt1_FAIL3.json` |
| suite carries no failure introduced by this round | `DEFECTS_R20B.json` TT-R20-16; baseline id set `var/R20-FHS-20261029/receipts/BASELINE_FAILED_IDS_6086908.txt`; 0 new ids |
| subset replay for main review | PR #6, `publish/r20-subset`, `SUBSET_MANIFEST.json` (file_count == measured diff, working-tree blobs) |

Ceilings unchanged and explicit: owner acceptance and external acceptance are **NOT_RUN**; the 75 residues
stay HOLD until the owner signs; release/tag/merge are the owner's acts and were not performed.
