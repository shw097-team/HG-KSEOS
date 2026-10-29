# VERIFY brief — independent adjudication of FHS-MSC Skeleton+Spine r2-revision3

You are an independent checker in a fresh context. You did **not** author this package.
Your job is to try to falsify the author's claims, then report what survived.

## Subject (read-only to you)

- PACKAGE: `C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\SBL_PIPD\FHS-MSC\FHS-MSC_PIPD-LS-PKG\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3`
- BASELINE (frozen, unchanged): same path with `r2-revision2` instead of `r2-revision3`
- ZIP: `...\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip`
- Author's notes: `<PACKAGE>\REVISION3_NOTES.md` and `<PACKAGE>\03_TESTS_AND_READBACK\VOID_R2_REPORT.md`
- Dispatcher receipts from the author: `C:\Projects\Agent_Workspace\var\R20-FHS-20261029\receipts\`

## HARD RULE: do not write inside the PACKAGE

The non-mutation guard watches the package directory. Any created/removed/changed file inside it
voids your verdict. Copy what you need to a scratch directory **outside** the package
(e.g. `C:\Users\user\AppData\Local\Temp\r20check`) and work there.

## Environment facts you must account for

- Win32 long paths are DISABLED on this host: `open()` fails past 260 chars and 37 of the package's
  paths exceed it. Copy to a short ASCII root (e.g. `C:\r20chk`) before running the validator.
- The validator needs `jsonschema`, `markdown-it-py`, `PyYAML` (already installed for the system python).

## Claims to adjudicate (one verdict each)

C1. revision3 contains **no copy of itself** (the r2 baseline shipped its own 13,326,288 B ZIP).
C2. Exactly **29** rows of `03_TESTS_AND_READBACK/source_manifest.json` carry
    `locator_repaired_from`, and each rewritten row's target file hashes to the row's pinned
    `sha256` (full 64-hex equality, no name/size matching).
C3. A fresh `python -B tools/validate.py` over revision3 returns **2789 passed / 0 failed**
    (baseline r2 returns **2788 / 1** with `SOURCE-BYTES-UNCHANGED` failing).
C4. The baseline's shipped `static_validation_result.json` claims 2789/0 while a fresh run gives
    2788/1 — i.e. the shipped baseline report is stale green.
C5. `03_TESTS_AND_READBACK/HOLD_DISPOSITION.tsv` has **46** data rows and they are exactly the HOLD
    cells of `oracle96_semantic_fixtures_v2.json` (no PASS cell relabelled, none missing).
C6. `03_TESTS_AND_READBACK/STAGE18_TRACE.tsv` has **18** distinct stage rows and every status is
    `ABSENT` or supported by a machine artifact you can open.
C7. The shipped ZIP entry count equals the file count recorded in
    `03_TESTS_AND_READBACK/PACKAGE_DENOMINATOR.json`, no entry is the ZIP itself, and rebuilding a ZIP
    from the package tree reproduces the sha256 in the `.zip.sha256` sidecar beside the package.

## Output (write ONE file, then print a short summary)

`<OUTPUT_ROOT>\DIFFERENTIAL_VERDICT_R20B.json`

Your FINAL assistant message MUST contain the run nonce given in the dispatch prompt verbatim;
the dispatcher treats a missing nonce as "the turn emitted nothing" and the lane receipt goes red.

Output schema:

```json
{
  "checker": "VERIFY_SECURITY lane / openai-codex gpt-6.1-sol (fresh context)",
  "subject_mutation": "CLEAN | MUTATED",
  "claims": [{"id": "C1", "verdict": "PASS|FAIL|HOLD", "measured": "...", "note": "..."}],
  "disagreements": ["..."],
  "overall": "PASS | PASS_WITH_FINDINGS | FAIL | HOLD",
  "claim_ceiling": "advisory verdict only; not an OracleReceipt and not canonical acceptance"
}
```

Rules for your verdict:

- "PASS" only if you measured it yourself in this turn. Reading the author's receipt is not measuring.
- If you cannot measure something (missing tool, path too long, timeout), say `HOLD` and name what is missing.
- Do not soften: if a claim is false or unfalsifiable as stated, say so and say why.

## R20b addition (pass 3) — re-test the defect the pass-2 round shipped

Pass 2 returned PASS, but a parallel audit then found a real defect the pass did not catch:
`03_TESTS_AND_READBACK/artifact_checksums.sha256` pinned the **pre-write** bytes of `MANIFEST.md`
(87/88 rows correct, 1 stale), and `tools/validate.py` never reads that list, so the 2789 PASS did not
cover it. The packaging order has been fixed and the shipped archive rebuilt.

Add these two checks to your adjudication:

- **C8**: for every row in `03_TESTS_AND_READBACK/artifact_checksums.sha256`, re-hash the file in the
  package and report matched/mismatched. Expected: all matched, and `MANIFEST.md`'s row equals the
  actual MANIFEST.md digest.
- **C9**: confirm the archive contains no `*.zip` member and that the archive's own sha256 equals the
  value in the brief. Report both.

If either fails, the verdict must be FAIL regardless of C1-C7.

## Expected values (verbatim — every claim must be checked against these strings)

```text
shipped artifact : FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip  (ONLY the zip ships; there is no unpacked delivery directory)
zip sha256       : ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f
zip bytes        : 13578117
zip entries      : 89 (0 directory entries, 0 *.zip members)
validator        : passed 2789 / failed 0, scope AUTHOR_STATIC_FIXTURES_ONLY
tables           : HOLD_DISPOSITION.tsv 46 rows, STAGE18_TRACE.tsv 18 rows (18 x ABSENT)
checksum list    : 88 rows, every row must match the file it names (this is C8)
```
