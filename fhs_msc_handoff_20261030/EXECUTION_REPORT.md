# Execution report — `FHS-MSC-HANDOFF-PATCH-v1-EXEC-20261030`

Objective: take delivery of `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1` (goal
`PIPD_CONSTRUCTION_HANDOFF_READY`) and execute it — verify, run the first work, verify the structure,
exercise the bounded lanes, publish for external development.

Governing split: Fabric = governance contract (read-only); SBL = product-engineering command entry;
HG-KSEOS = native authorization/state/acceptance control plane. HG-KSEOS is the only repository written
to, and only additively.

## Phase 1 — package integrity (`receipts/P1*.json`)

911 files on disk; `SHA256_PAYLOAD_MANIFEST.json` declares 909 rows (it excludes itself and
`SHA256_DELIVERY_MANIFEST.md` by construction).

- A naive `Path.exists()` on the manifest paths fails for 446 of 909 rows, and the two causes are
  different. **31 rows** name `01_SUBSTANTIVE_BODY/` while the unpacked directory is
  `01_FHS-MSC_PIPD-LS-PKG_BODY/` — a real layout mismatch, every file present, only the name differs.
  The other **415 rows** exist and are unreadable only because the absolute path exceeds the
  260-character Win32 limit: with the `\\?\` prefix all 415 resolve. Measured on the original tree;
  a verifier that does not walk with a long-path prefix will report roughly half the payload missing.
- After restoring the canonical name: **909/909 rows match on bytes and SHA-256**, 0 mismatch,
  0 missing; the only undeclared files are the two manifests; **30/30** relative links resolve.
- `SHA256_DELIVERY_MANIFEST.md`: 6 of 9 rows verify, **3 absent** (both archives and
  `PACKAGE_READBACK.json`). Not a mismatch — an absence.

Verdict: payload **PASS** after the rename; sealing **FAIL** as delivered.

## Phase 2 — sealing: what reproduces and what does not (`receipts/P7_SEAL_AND_PARTITION.json`)

The delivery names two archives and a `PACKAGE_READBACK.json`; none of the three is in the tree. Whether
their digests were ever verifiable depends on whether the membership can be recovered, so this phase used
the delivery's **own partition** — BODY = rows under `01_SUBSTANTIVE_BODY/` or `02_FIRST_WORK/` or at the
root, EVIDENCE = rows under `02_EVIDENCE_AUDIT_APPENDICES/` or `03_HANDOFF_EVIDENCE/` — with the pinned
recipe (sorted names, fixed timestamp, deflate 9, no directory entries).

| Archive | Entries | Built | Declared | Verdict |
|---|---:|---|---|---|
| `…_BODY_…zip` | 114 | 4,007,065 B / `5e722cfb…` | 4,007,065 B / `5e722cfb…` | **PASS — byte-exact** |
| `…_EVIDENCE_…zip` | 801 | 25,914,281 B / `0e7763b8…` | 25,914,281 B / `0e7763b8…` | **PASS — byte-exact** |
| `PACKAGE_READBACK.json` | — | — | — | **absent**, regenerable by the shipped `package.py` |

**Corrected after independent check.** An earlier revision of this phase reported the EVIDENCE rebuild at
797 entries and 25,909,480 B ("4,801 B short"). That was my partition rule dropping four root-level files,
not a defect in the delivery: rebuilt with the recipe in the shipped `QA_TOOLS/package.py`, both archives
match their declared size and digest exactly (`P13`, and the checker's V2/V3 in `P12`). The only real
absence is `PACKAGE_READBACK.json`.

**Two corrections to this round's own earlier work.** The first seal published here was built on a
non-recursive `01_SUBSTANTIVE_BODY/*.md` glob with an invented membership: 17 entries, 483,623 B, which
silently excluded 14 files (29,121,570 B) under `01_SUBSTANTIVE_BODY/SBL_DOC00_13_INTEGRATED_READER_UPGRADES/`
and reproduced neither declared digest. It is superseded by P7. And the inference drawn from it — that the
declared BODY archive's composition could not be reconstructed from the tree — was wrong and is retracted:
it reconstructed exactly on the first try once the manifest's partition was used instead of a guess.

## Phase 3 — first work `WP-FHS-15` (`receipts/P2*.json`)

Re-executed in an isolated root: 24 functional clauses → 24 atoms, PI reader PASS, strict handoff reader
PASS, three SPECs, KnownAnswer re-asked 0, `NATIVE_NOT_RUN`, no native WorkOrder.

- As shipped the 35-check harness returns **34/35**. `EXISTING_5_AFFECTED_TESTS` records
  `AssertionError: expected True; actual False`; the recorded root cause is
  `ModuleNotFoundError: No module named 'tests'` — `loadTestsFromNames()` imports the test modules
  before the `sys.path.insert` on the next line (F-03).
- With the two-line ordering change only: **35/35**.
- Determinism: `ProductSPEC`, `ArchitectureSPEC`, `ProgramSPEC`, `SourceReadback` and the 22-WP DAG are
  **byte-identical** to the delivery. `PI-PKG`, `TaskSpecSeed`, `RUN/FUO` and `ExecutionHandoff` differ, and the cause
  is proved: absolute-root identity. Two absolute roots → two `content_hash`; root-relative intake →
  identical `PI-d0974c55d63bc021` at both (`receipts/P2C_...`). No writer code was modified.

## Phase 4 — structural verification (`receipts/P3_STRUCTURAL_CHECKS.json`)

| Check | Verdict | Measured |
|---|---|---|
| D1 22-WP DAG | PASS | 22 nodes, 36 edges, acyclic, topological order complete |
| D2 declared vs edge closure | **REVIEW** | declared `{00,01,15}`; edges give `{00,15}` |
| D3 no future-receipt predecessor | PASS | depends only on WP-FHS-00 |
| D4 PI atoms | PASS | 24 atoms with source_ref, owner, oracle, negative fixture, failure condition |
| D5 FUO ten fields | PASS | all ten |
| D6 three SPECs | PASS | acceptance present, no orphan negative |
| D7 current readers | PASS | 2,221 locators, 2,221 unique |

D2: `WP-FHS-01 depends_on [WP-FHS-00]`, so 01 is a sibling-after-00 and never an ancestor of 15. Both
inputs exist, so the first work holds; the declaration and the graph still disagree, and only the owner
may re-type the edge.

## Phase 5 — lanes (`receipts/P5*.json`)

| Turn | Lane | Arm served | Seconds | ok |
|---|---|---|---:|---|
| probe | EXECUTE | `opencode-go/deepseek-v4.1-flash` | 7.2 | true |
| bounded single-file write | EXECUTE | `opencode-go/deepseek-v4.1-flash` | 27.99 | true |
| independent acceptance | VERIFY_SECURITY | **none** — `ERR_LANE_ALL_ROUTES_EXHAUSTED`, upstream 401 | 0 | **false** |

The writer never checks its own work. The VERIFY lane failed closed (F-10): the assigned arm
`openai-codex/gpt-6.1-sol` returns 401 through the local relay, the assignment declares no fallback, and
the dispatcher refused rather than substituting a model. **Independent acceptance therefore did not
run**; an advisory audit performed by a separate process is recorded in `ADVISORY_AUDIT.md` and is not a
lane verdict.

Three control-plane defects were repaired or recorded: the toolchain pin (F-06), the receipt-builder
`NameError` (F-07, script SHA-256 `c2c7414b…` → `85356200…`, backup kept), and the `served_arm_assigned`
comparison (F-08).

## Phase 6 — owner envelope

One owner-key signing window was opened before any work (`TTL 8 h`, `max_ops 40`, ceiling
`REPOSITORY_WRITE`, scope `registry_row_sign,merkle_root_sign`, `ui_impl=tkinter`), so no later step could
block on a prompt. The passphrase never entered the agent context or any file. The window refuses
release/sourcefreeze/policy-authority/trust-anchor/owner-enrollment payloads by construction. This
round's ceiling required no signature: `ops_used = 0`, closed at the end.

## Phase 7 — delivery

A fresh clone of `shw097-team/HG-KSEOS`, branch `fhs-msc-handoff-patch-v1-exec-20261030`, PR #7. Additive
only: this directory plus an OpenSpec change. No existing file modified, no policy touched, nothing
force-pushed, no merge, no tag, no release. The pushed tree was read back through the GitHub API
(65 delivery blobs: 11 receipts, 17 books, 5 verifiers, the first-work artefacts) and compared by
SHA-256 against the local tree.

## Next round

1. Provision the VERIFY arm's credential and dispatch the existing brief against the merged head (F-10).
2. Owner decision on the WP-FHS-15 closure edge (F-05) and on identity scoping (F-04).
3. Adopt the new seal as the only sealing claim (F-01); ship the canonical layout (F-02).
4. Treat the shipped harness as broken until repaired (F-03); refresh the toolchain pin (F-06).
