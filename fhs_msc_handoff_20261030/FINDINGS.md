# Findings — round `FHS-MSC-HANDOFF-PATCH-v1-EXEC-20261030`

Fourteen numbered defects (F-01..F-14; F-02 is split into F-02 and F-02b), ordered by cost to the next team. Each has an artefact, a severity and one next action.
A repaired harness is not an acceptance, and a green check is not a permit.

## F-01 — both archive digests are reproducible; the readback manifest is genuinely absent

**Medium (evidence) — revised down from High after independent check.** `SHA256_DELIVERY_MANIFEST.md`
lists 9 rows; 3 are absent from the tree: both archives and `PACKAGE_READBACK.json`. Six verify
byte-for-byte. Rebuilding both archives **with the recipe in the shipped `QA_TOOLS/package.py`**
(manifest exclusions, UTF-8 filter, sorted names, fixed `date_time`, deflate 9, `external_attr 0o100644<<16`)
gives:

| Archive | Rebuilt | Declared | Verdict |
|---|---|---|---|
| BODY (114 entries) | 4,007,065 B / `5e722cfb…` | 4,007,065 B / `5e722cfb…` | **byte-exact** |
| EVIDENCE (801 entries) | 25,914,281 B / `0e7763b8…` | 25,914,281 B / `0e7763b8…` | **byte-exact** |
| `PACKAGE_READBACK.json` | — | — | absent; regenerable by running the shipped `package.py` |

**Withdrawn claim (F-01c).** An earlier revision of this file reported EVIDENCE "4,801 B short". That was
an artefact of my own partition rule: it produced 797 entries because it handled the root-level file set
differently, not because the delivery was wrong. The independent checker hit the same conclusion from the
other direction (it reproduced the declared digest and called the shortfall claim false), and I then
re-derived both archives verbatim. `receipts/P13_SEAL_REPRODUCTION_VERBATIM.json`.
Evidence: `receipts/P13_SEAL_REPRODUCTION_VERBATIM.json`, `receipts/P12_INDEPENDENT_VERDICT.json` (V2/V3).
Next: regenerate `PACKAGE_READBACK.json` with the shipped packer, or drop that row from the manifest.

## F-02 — the unpacked tree does not match its own manifest layout

**Medium.** On disk the book directory is `01_FHS-MSC_PIPD-LS-PKG_BODY/`; the payload manifest and
`INDEX.md` both address `01_SUBSTANTIVE_BODY/`. Exactly **31 of 909 rows** fail on that rename alone.
After the rename: 909/909.
Evidence: `receipts/P14_LAYOUT_PREFIX_EVIDENCE.json` measures the count directly against the delivered tree
with long-path handling: 31 rows carry the `01_SUBSTANTIVE_BODY/` prefix, **0 resolve as declared**, **31
resolve after the directory alias**. `receipts/P1B_PACKAGE_INTEGRITY_CANONICAL.json` is the post-alias
result (909/909, `path_alias_applied`) and does not itself carry the 31 — it is cited for the closure, not
for the count.
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
Evidence: `receipts/P2B_CHECK_FIRST_WORK_AS_SHIPPED.json` (34/35), `receipts/P2D_CHECK_FIRST_WORK_REPAIRED.json`
(35/35); the delivered snapshot it disagrees with is `03_HANDOFF_EVIDENCE/EXISTING_AFFECTED_TESTS_RAW.txt`
in the package, which is not staged into this tree.
Next: apply the one-line move (`lines_changed: 2` — remove the later insert, add it before the loader), re-run,
keep the as-shipped failure in the record. Note F-13: the repaired count depends on the delivered READERS
snapshot, which the shipped tooling cannot rebuild.

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

**Low (sizing).** A first attempt to have the EXECUTE lane author the five narrative documents ran from
14:20:30 to its termination at 14:29 — eight and a half minutes of reading and cross-checking, no file
written, no side effect (codex rollout `…/sessions/2026/10/30/rollout-2026-10-30T14-20-30-01a18b77-…jsonl`,
last entry 14:20, process terminated 14:29). The same lane wrote a single exact file in 27.99 s
(`receipts/P5B`). The dispatcher's own record of the overrun is `receipts/P5E_LANE_WRITER_OVERRUN.json`, including the reaping artefact that made it exit `ERR_LANE_ALL_ROUTES_EXHAUSTED` (`4294967295`) instead of `ERR_LANE_TIMEOUT` — do not read that code as a routing verdict.
Next: keep lane writes single-artefact and exactly specified; keep open-ended authoring with the
operator.

## F-12 — the first seal published here was wrong and is withdrawn

**High (self-inflicted, repaired).** `tools/seal_package.py` collected the body with a non-recursive
`01_SUBSTANTIVE_BODY/*.md` glob, so the archive it produced held 17 entries and 483,623 B while silently
omitting 14 declared files (29,121,570 B) under `01_SUBSTANTIVE_BODY/SBL_DOC00_13_INTEGRATED_READER_UPGRADES/`
— 897 of 911 files covered. Worse, it used an invented membership rather than the manifest's partition,
so it reproduced neither declared digest and made the declared BODY archive look unreconstructible.
Evidence: `receipts/P7_SEAL_AND_PARTITION.json`, field `earlier_seal_defect`.
Next: never seal with a glob; seal the manifest's partition or say plainly which subset you sealed.

## F-13 — 35/35 is conditional on a snapshot the shipped tooling cannot rebuild

**High (reproducibility).** `prepare.py` snapshots `src`, `schemas`, the named `tests/...`, `docs` and
`skills` — but not `fixtures`. Rebuilding `READERS/PIPD` from the shipped QA_TOOLS therefore yields a tree
without `fixtures/`, and on that faithful rebuild the harness stays **34/1 even after the import-order fix**:
`test_every_atom_traces_orphan_free` and `test_semantic_collapse_is_refused` error with
`FileNotFoundError: …\READERS\PIPD\fixtures\REQ-COMPOUND\source.txt`.
Evidence: reported by an independent audit run; both counts reproduced against the delivered snapshot.
Next: add `fixtures` to the snapshot list, or state that the 35/35 depends on the delivered READERS tree.

## F-14 — the delivery's own 35/0 record carries a pre-fix timing identical to 16 digits

**High (delivered evidence).** `03_HANDOFF_EVIDENCE/MINIMAL_STATIC_TESTS.json` (35 pass / 0 fail) and
`MINIMAL_STATIC_TESTS_INITIAL.json` (34 / 1) both record `elapsed_seconds: 1.0183297000003222`. A re-run
cannot reproduce a wall-clock value to sixteen significant digits: this round's own two runs measured
6.1035 s and 5.4547 s. The 35/0 record looks like the 34/1 record with the counts edited.
The count itself is not in doubt — it reproduced here under the delivered snapshot — but the delivery's
evidence for it is.
Evidence: `receipts/P8_DELIVERED_RECORD_ANOMALY.json`.
Next: re-execute the harness and ship the real record, with a timestamp.

## F-15 — the QA harness has an undeclared dependency (`jsonschema`)

**Medium (reproducibility).** The 35-check harness imports `jsonschema` inside its validation path. On an
interpreter without it, three cases fail as `ValidationFail:jsonschema unavailable` and the run scores below
the recorded 35/35 — the same tree, the same tools, a different score. Measured 2026-10-30 on Python 3.11.17
(`jsonschema 4.26.0` installed: the failures disappear). The delivery names no dependency and has no
preflight import check, so "35/35" was never a property of the artefact set alone.
Next: pin the dependency in the delivery (requirements + a one-line `import jsonschema` preflight that fails
loudly), or vendor it.
