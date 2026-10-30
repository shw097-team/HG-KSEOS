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

- As delivered, 429 rows did not resolve: the unpacked directory was `01_FHS-MSC_PIPD-LS-PKG_BODY/`
  while the manifest and `INDEX.md` address `01_SUBSTANTIVE_BODY/`. Every file existed; only the path
  differed.
- After restoring the canonical name: **909/909 rows match on bytes and SHA-256**, 0 mismatch,
  0 missing; the only undeclared files are the two manifests; **30/30** relative links resolve.
- `SHA256_DELIVERY_MANIFEST.md`: 6 of 9 rows verify, **3 absent** (both archives and
  `PACKAGE_READBACK.json`). Not a mismatch — an absence.

Verdict: payload **PASS** after the rename; sealing **FAIL** as delivered.

## Phase 2 — reproducible seal (`receipts/P1C_SEAL_AND_READBACK.json`)

`tools/seal_package.py` seals with a pinned recipe (sorted entries, zip-epoch timestamps, deflate 9, no
directory entries) and reads every entry back for CRC32, bytes, SHA-256 and UTF-8:

| Archive | Bytes | SHA-256 | Entries |
|---|---:|---|---:|
| `FHS-MSC_BODY_...-EXEC.zip` | 483,623 | `07d62b49…` | 17 |
| `FHS-MSC_EVIDENCE_...-EXEC.zip` | 25,987,085 | `9497133b…` | 880 |

17/17 and 880/880 clean; a second seal from the same input is byte-identical. This is a **new** seal, not
a reproduction: the declared evidence size (25,914,281 B) is within 0.28%, but the declared BODY size
(4,007,065 B) cannot hold 4,808,325 raw bytes that deflate to 0.48 MB, so the declared BODY archive's
composition is not reconstructible from the tree.

## Phase 3 — first work `WP-FHS-15` (`receipts/P2*.json`)

Re-executed in an isolated root: 24 functional clauses → 24 atoms, PI reader PASS, strict handoff reader
PASS, three SPECs, KnownAnswer re-asked 0, `NATIVE_NOT_RUN`, no native WorkOrder.

- As shipped the 35-check harness returns **34/35**; `EXISTING_5_AFFECTED_TESTS` fails with
  `ModuleNotFoundError: No module named 'tests'` (import order, F-03).
- With the two-line ordering change only: **35/35**.
- Determinism: `ProductSPEC`, `ArchitectureSPEC`, `ProgramSPEC`, `SourceReadback` and the 22-WP DAG are
  **byte-identical** to the delivery. `PI-PKG`, `TaskSpecSeed`, `ExecutionHandoff` differ, and the cause
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
| probe | EXECUTE | `opencode-go/deepseek-v4.1-flash` | 2.31 | true |
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
