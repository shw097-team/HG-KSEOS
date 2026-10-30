# Findings — round `FHS-MSC-HANDOFF-PATCH-v1-EXEC-20261030`

Ten defects, ordered by cost to the next team. Each has an artefact, a severity and one next action.
A repaired harness is not an acceptance, and a green check is not a permit.

## F-01 — the delivered archives and the readback manifest do not exist

**High (evidence).** `SHA256_DELIVERY_MANIFEST.md` lists 9 rows; 3 are absent:
`FHS-MSC_BODY_..._HANDOFF-PATCH-v1.zip`, `FHS-MSC_EVIDENCE_..._HANDOFF-PATCH-v1.zip`,
`PACKAGE_READBACK.json`. Six verify byte-for-byte.
Evidence: `receipts/P1B_PACKAGE_INTEGRITY_CANONICAL.json` (check C).
Consequence: the two archive SHAs have never been verifiable. Anyone quoting the manifest's "sealed
once, every entry read back" sentence is quoting prose.
Next: adopt `receipts/P1C_SEAL_AND_READBACK.json` as the sealing claim or re-deliver the bytes.

## F-02 — the unpacked tree does not match its own manifest layout

**Medium.** On disk the book directory is `01_FHS-MSC_PIPD-LS-PKG_BODY/`; the payload manifest and
`INDEX.md` both address `01_SUBSTANTIVE_BODY/`. Exactly **31 of 909 rows** fail on that rename alone.
After the rename: 909/909.
Evidence: recomputation from `SHA256_PAYLOAD_MANIFEST.json` against the delivered tree; canonical result
in `receipts/P1B_PACKAGE_INTEGRITY_CANONICAL.json`.
Consequence: a verifier resolves 96.6% and blames the payload for the rest.

## F-02b — most of the apparent loss is the Win32 path limit, not the package

**High (tooling).** A second 415 rows fail a naive `Path.exists()` because the absolute path runs past
260 characters; with the `\\?\` prefix all 415 resolve and verify. So 446 misses split 31 layout +
415 path-length. Consequences: a receiver on a deep checkout reports ~446 missing rows and looks like a
corrupted delivery; `os.walk` silently truncates whole subtrees; and any manifest check written without
the prefix is unusable on this package.
Evidence: measured this round — 446 plain misses, 31 with the prefix. The prior handoff already carried
the same lesson (`p0_denominator.py`, short root + `\\?\` walk).
Next: ship the tree at a short root or a `.tar`; every verifier must walk with the prefix.
Next: ship the canonical name; make the verifier raise a named alias error, not a missing-file count.

## F-03 — the shipped 35-check harness fails on the shipped tree

**High (it is the package's own acceptance harness).** `check_first_work.py` calls
`loadTestsFromNames(...)` at line 81 and inserts `03_HANDOFF_EVIDENCE/READERS/PIPD` into `sys.path` at
line 83, so the five affected tests are imported before the path exists. The check records
`AssertionError: expected True; actual False`; the recorded root cause is
`ModuleNotFoundError: No module named 'tests'`. Result **34 PASS / 1 FAIL**. The delivered `EXISTING_AFFECTED_TESTS_RAW.txt` shows 5/5 OK, so
that evidence was produced with the snapshot importable for another reason (author cwd), not by the
shipped code path.
Evidence: `receipts/P2B_...` (34/35) and `receipts/P2D_...` (35/35 after the ordering repair).
Next: apply the two-line repair, re-run, keep the as-shipped failure in the record.

## F-04 — first-work identity is a function of the absolute draft root

**Medium (portability).** The original PIPD compiler binds the absolute source path into subject
identity: a re-run on the same bytes in a different root yields a different `PI-PKG.subject_id`, all 24
`ATOM-*`, every `REQ-*`, and therefore different `TaskSpecSeed` and `ExecutionHandoff` hashes, plus
fixture directories that do not exist at the new root. `ProductSPEC`, `ArchitectureSPEC`,
`ProgramSPEC`, `SourceReadback` and the 22-WP DAG are unaffected and reproduce byte-identically.
Evidence: `receipts/P2C_IDENTITY_ROOT_SCOPE.json` — absolute-path control gives two different
`content_hash`; root-relative intake gives `PI-d0974c55d63bc021` at both roots.
Next: decide at the original writer whether identity is content-scoped or explicitly root-scoped.

## F-05 — the declared WP-FHS-15 closure is not derivable from the typed DAG

**Medium (contract coherence).** The DAG declares `dependency_closure = [WP-FHS-00, WP-FHS-01,
WP-FHS-15]`; typed edges give `ancestors(WP-FHS-15) = {WP-FHS-00}` because
`WP-FHS-01 depends_on [WP-FHS-00]`. Both inputs exist as artefacts so the first work is not blocked, but
a scheduler built from the edges would skip 01.
Evidence: `receipts/P3_STRUCTURAL_CHECKS.json` → `D2_wp15_closure: REVIEW`.
Next: owner either types the edge or amends the declaration and says why 01 is not a prerequisite.

## F-06 — the lane toolchain pin points at a codex binary that does not exist

**Medium (fail-closed).** The pin resolves to `…\OpenAI\Codex\bin\0ab0e7a8f3779036\codex.exe`, absent.
Installed: `…\bin\22cfb1d302613eae\codex.exe` (codex-cli 0.166.0-alpha.5.1), the pinned runtime
`…\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe`, and npm `codex-cli 0.164.0`.
Evidence: `ERR_LANE_PIN_IDENTITY_INVALID` in `logs/lane_probe.out`.
Consequence: every lane turn refuses before spawn unless `--codex-executable` is passed, which bypasses
existence+digest verification by design.
Next: refresh the pin by owner-approved config change, or record the supplied binary's digest.

## F-07 — the dispatcher's receipt builder crashed after every successful spawn

**High (silent evidence loss).** `scripts/hgk-lane-dispatch.py` referenced `_producer` in `main()`'s
receipt dict; the name is bound only inside the per-attempt function. Every turn that reached receipt
assembly died with `NameError` after the model had already answered: the turn happened, the evidence did
not. Repair: bind `_producer = producer_identity()` before the dict. Script SHA-256 `c2c7414b…` →
`85356200…`; backup kept as `logs/hgk-lane-dispatch.py.before-R-EXEC-02`.
Next: land upstream with a regression test asserting a receipt is written on exit 0.

## F-08 — `served_arm_assigned` is false even when the assigned arm served

**Low (receipt semantics), but it weakens the gate it looks like.** The rollout identity reports
provider `openai-codex` and model `opencode-go/deepseek-v4.1-flash`; the receipt derives
`f"{provider}/{model}"` and compares against the assignment set `{"opencode-go/deepseek-v4.1-flash"}`.
The comparison cannot match when the transport model carries its provider prefix, so the field reads
`false` while `ok` is `true` and the assigned arm did serve.
Evidence: `receipts/P5A_LANE_PROBE_EXECUTE.json`.
Next: normalise the served identity to the assignment's arm key, or emit both raw and normalised values.

## F-09 — the staging script deleted the documents it was meant to accompany

**Medium (process, self-inflicted, repaired).** `tools/stage_repo.py` began with `rmtree(out)`; running
it a second time after the narrative documents were authored removed them, and the first push therefore
carried the receipts without `README`/`EXECUTION_REPORT`/`FINDINGS`/`REPRODUCE`/`EVIDENCE_INDEX`. The
script now removes only the six copied subtrees. This finding exists because the missing-file readback
against the pushed commit caught it — which is the point of reading back.
Next: any staging step must own an explicit subtree list, never a whole directory.

## F-10 — the assigned VERIFY arm could not be served

**High (gate blocked, not passed).** Dispatching `VERIFY_SECURITY` (`openai-codex/gpt-6.1-sol`,
assignment revision 38) returned `ERR_LANE_ALL_ROUTES_EXHAUSTED` with a single attempt: `exit 1`,
upstream `401 Unauthorized` from `http://127.0.0.1:10102/v1/responses`, no usage row, no nonce. The
assignment declares no fallback arm for this lane, so the dispatcher failed closed rather than
substituting a model.
Evidence: `logs/lane_verify.out`, `receipts/P5C_LANE_VERIFY_BLOCKED.json`.
Consequence: **independent acceptance did not run**. Everything in this branch remains author-side. A
separate advisory audit is recorded in `ADVISORY_AUDIT.md` and is explicitly NOT a lane verdict.
Next: provision the OAuth credential for the PLAN/VERIFY arm, then dispatch the same brief
(`C:\wg\brief_verify.md` in the round workspace) against the merged head.

## F-11 — a bounded-writer lane turn overran without producing files

**Low (sizing).** A first attempt to have the EXECUTE lane author the five narrative documents spent
more than nine minutes reading and cross-checking and produced nothing; it was terminated with no side
effects. The same lane wrote a single exact file in 28 s.
Next: keep lane writes single-artefact and exactly specified; keep open-ended authoring with the
operator.
