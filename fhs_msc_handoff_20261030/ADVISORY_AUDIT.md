# Advisory audit — three independent read-only processes

**What this is not.** It is not the VERIFY lane. That lane was dispatched
(`VERIFY_SECURITY`, assigned arm `openai-codex/gpt-6.1-sol`) and returned `ERR_LANE_ALL_ROUTES_EXHAUSTED`
with an upstream `401` before any model ran (`receipts/P5C_LANE_VERIFY_BLOCKED.json`). No verdict exists
and no box in `tasks.md` is closed by this file.

**What it is.** Because the gate was blocked, three separate processes were started with no context from
the writing session and told to attack specific claims. Each had its own scratch directory and was told
not to modify anything. Their reports are adversarial input, not evidence: every claim below was
re-measured against the receipts before it changed a document, and one of their findings was wrong.

## Audit A — payload integrity and seal

**Reported.** 909 rows declared, 909 checked, 909 match, 0 mismatch; exactly two undeclared files (the two
manifests); body archive `483,623 B` / `07d62b49fa35dabfdae0d7bc481fcd19155c9248aeb2727a1e814d68bc50b225`;
evidence archive `25,987,085 B` / `9497133b150c260dec26a2855e66a1a70f91def96e2241d5693208d55…`; two seal
runs byte-identical.

**Verified.** Identical to `receipts/P1C_SEAL_AND_READBACK.json` and `receipts/P1B_…`. No document changed.

## Audit B — first-work reproducibility

**Reported.** Byte-identical: `ProductSPEC`, `ArchitectureSPEC`, `ProgramSPEC`, `SourceReadback`,
`ORIGINAL_22_WP_DAG`. Differing: `PI-PKG`, `TaskSpecSeed`, `RUN/FUO`, `ExecutionHandoff`. Harness 34/1 as
shipped → 35/0 after the import-order repair. Identity probe: control differs, repair matches.

**Verified** against `receipts/P2_FIRST_WORK_RUN.json`, `P2B`, `P2D`, `P2C`. `EXECUTION_REPORT.md` Phase 3
listed only three differing files and was **corrected to four** (`RUN/FUO.json` was missing). The quoted
failure text was also tightened: the check records `AssertionError: expected True; actual False`, and the
recorded root cause is `ModuleNotFoundError: No module named 'tests'` — the earlier wording presented the
cause as if it were the observed failure.

## Audit C — document review against receipts

**Reported, and acted on:**

| Finding | My re-measurement | Change |
|---|---|---|
| "429 rows unresolved" appears in no receipt | Confirmed: no receipt contains 429. Re-measured from `SHA256_PAYLOAD_MANIFEST.json` against the delivered tree: 446 plain misses, of which **31** are the directory rename and **415** resolve with the `\\?\` prefix — i.e. the 260-character Win32 limit, not layout | Every "429" replaced with the measured split; new finding **F-02b** |
| `P1`'s `B_undeclared_files` writes `extra: 33` where the set has 2 members | Confirmed; P1B and P1_VERIFIED both say 2 | `EVIDENCE_INDEX` now warns not to cite P1's arithmetic |
| `P1_PACKAGE_INTEGRITY_VERIFIED.json` described as "PASS … independent re-derivation" | Confirmed misleading: its C check records the declared BODY archive **absent** | Row rewritten: A/B/D/E PASS, C FAIL, corroborates F-01 |
| `tasks.md` asserted a VERIFY verdict "is published with the PR" when none was produced | Confirmed; the box can never close itself | Rewritten as attempted-and-blocked with the receipt named |
| Six `### Requirement:` blocks, nine `#### Scenario:` blocks, no credential material, no over-claim of native admission or release | Confirmed by my own count and grep | No change; recorded as the one place the corpus is disciplined |

**Reported, and rejected:** the auditor read the Phase 2 argument ("the declared BODY archive cannot hold
4,808,325 raw bytes that deflate to 0.48 MB") as a contradiction. It is not: the 4,808,325 figure is the
raw byte total of the files the manifest assigns to that archive, and the point being made is that a
4,007,065-byte archive cannot contain them uncompressed — which compresses to the size we observe. The
sentence stands.

## Score

Three blocks of claims attacked. One was materially wrong (429), two were imprecise (differing-file count,
failure-text framing), one document contained an assertion that could never be true (`tasks.md`), and one
receipt was being oversold (`P1_VERIFIED`). All five are corrected in this commit. Nothing in the audit
raised a native-admission, release or acceptance claim, and nothing raised a credential leak.

That is the honest return on an advisory audit: it is worth roughly what it caught, and it is not a
substitute for the lane that failed closed.
