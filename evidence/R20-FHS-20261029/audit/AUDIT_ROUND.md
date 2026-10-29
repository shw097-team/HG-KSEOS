# R20 parallel audit — three independent sub-agents (SWARM round)

Dispatched as three parallel children on the same frozen inputs, read-only, each with its own scratch
root. Their job was to falsify the author's own claims, not to confirm them. Full transcripts are local
(`hermes/cache/delegation/live/deleg_0ea7fbba/task-*.log`); the measurements below are what they returned.

## A1 — shipped package audit (zip → `C:\r20audit1`)

| Claim under test | Measured | Verdict |
|---|---|---|
| validator green on shipped bytes | `passed 2789 / failed 0`, `failures: []`, exit 0 | confirmed |
| file count 89 | 89 regular files (`os.walk`) | confirmed |
| no self-embedded archive | 0 `*.zip`, 0 `.7z/.tar/.gz/.rar/.xz/.bz2`; zip has 0 directory entries | confirmed |
| `PACKAGE_DENOMINATOR.json` reconciles | 89 files / 132,416,007 B / max_rel_path_len 64 / 89 entries — all equal | confirmed |
| checksum list covers the tree | 88 rows, 88 well-formed, 0 duplicates; 88 listed vs 89 present (only itself unlisted) | **defect found** |

**Defect A1-1**: `artifact_checksums.sha256` pinned `MANIFEST.md = 6f22bc10…` while the shipped file is
`8ece6d7e…` (87/88 correct). `validate.py` never reads the list, so the 2789 PASS did not cover it.
Root cause: the list was written *before* `MANIFEST.md` was rewritten (packaging order).

**Second measurement worth keeping**: running `validate.py` rewrites 4 shipped files
(`source_recheck.json`, `static_validation_result.json/.md`, `test_matrix.md`) — tree bytes
132,416,007 → 132,417,185 — so checksum verification must be done on a fresh extract, never in place.

## A2 — independent re-verification from the shipped bytes

| Check | Measured |
|---|---|
| validator, copy of the tree | 2789 / 0, no failing ids |
| validator, fresh zip extract | 2789 / 0 |
| 29 relocated locator rows | **29/29** current file digest == pinned digest, 0 mismatch, 0 IO errors |
| shipped `source_manifest.json` digest | `beff2590…` == `manifest_sha256_after` in `P1B_LOCATOR_REPAIR.json` |
| r2-revision2 immutability | **85 compared / 85 matched / 0 mismatched**, sizes equal, sum 145,944,348 B |
| long paths | 37 files >260 chars (max 289), `\\?\` handled all, no error |

Same defect A1-1 independently re-found (identical bytes in tree, copy and zip → not a copy artifact).
Observed but not a defect: the `…_r2-revision3` **directory** is gone; the shipped artifact is the
archive (+ `.sha256`), which is what the receipts' `target` path referred to at build time.

## A3 — dispatcher gate audit (read the diff, ran both suites)

| Question | Answer |
|---|---|
| assignment gate after the pool check? | yes — pool refusal at `:2076-2085`, assignment gate at `:2103-2120`; empirically `--require-arm nowhere` still returns `ERR_LANE_REQUIRED_ARM_ABSENT` |
| both assignment schema shapes read? | yes (`:1069` `role or lane_group`, `:1081-1083` alternates) — but no test covered the `lane_group` shape |
| human home resolved lazily? | yes (`human_oauth_home()` `:1039`, `Path.home()` `:1047`, `try/except`) |
| tests | `test_lane_dispatch_r20_gates.py` 5 passed; `test_lane_dispatch_ao_guard.py` 136 passed |
| can an unassigned arm still be dispatched? | **YES — real bypass** |

**Defect A3-1 (the important one)**: the gate body was `if args.require_arm:`, i.e. a **naming** gate.
`--lane VERIFY_SECURITY --force-rank 3` (arm `opencode-go/glm-5.3-flash`, outside that lane's assignment)
reached spawn with no refusal. 9 of 14 pool arms sit outside their lane's assignment.

Also reported: wrong code for "file reads fine but no row for this role" (`ERR_ARM_ASSIGNMENT_UNREADABLE`),
and a pre-existing uncaught `FileNotFoundError` for a non-resolving `--codex-executable` (not touched by
this round; carried forward).

## Repairs applied from this audit (R20b)

| Finding | Repair | Evidence |
|---|---|---|
| A1-1 checksum list stale | packaging writes `MANIFEST.md` **before** the list, then verifies every row and aborts on any miss; the shipped archive was rebuilt from its own bytes with the single row corrected | `receipts/P1D_R20B_CHECKSUM_REPAIR.json` (88 rows verified, 0 missing, 0 stale) |
| A3-1 naming-only gate | `--require-assigned-arms` (strict selection, `ERR_NO_ASSIGNED_ARM`) + always-on detection: an unassigned serving arm is recorded (`served_arm_assigned`) and emits `WARN_LANE_SERVED_UNASSIGNED_ARM` | `tests/test_lane_dispatch_r20_gates.py` C4a/C4b/C5 |
| A3 "no row" code | `ERR_LANE_ASSIGNMENT_NO_ROW` for that case, `ERR_ARM_ASSIGNMENT_UNREADABLE` only for read errors | same test file |
| A3 no `lane_group` coverage | unit case builds a rev-33 shaped fixture and asserts the parsed arm set | same test file |

Suite after repairs: **144 passed** (136 pre-existing lane-guard + 8 gate cases); 0 regressions.
