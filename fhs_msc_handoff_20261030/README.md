# FHS-MSC PIPD-LS-PKG — HANDOFF-PATCH-v1 execution evidence

Execution record of round **`FHS-MSC-HANDOFF-PATCH-v1-EXEC-20261030`**: the receiving side took the
delivered package, verified it, re-executed its first work, sealed it reproducibly, ran the bounded
lanes, and wrote down every defect it hit. Addressed to the external engineering team that continues
the build.

**Claim ceiling: `PIPD_CONSTRUCTION_HANDOFF_READY`** — author-side, static, reproducible.

| Claim | State |
|---|---|
| `PIPD_CONSTRUCTION_HANDOFF_READY` | asserted (static, author side) |
| `NATIVE_ADMITTED` / `NATIVE_VERIFIED` | NOT_RUN |
| `INDEPENDENT_ACCEPTED` | NOT_RUN — the assigned VERIFY arm could not be served (F-10) |
| `RELEASE` | NOT_RUN |

Nothing here is production ready, accepted, certified or released; nothing here grants a permit.

## Five-minute verification

```bash
python fhs_msc_handoff_20261030/tools/verify_package.py <unpacked-package>
python fhs_msc_handoff_20261030/tools/exec_checks.py    <reproduced-first-work>
python fhs_msc_handoff_20261030/tools/seal_package.py   <unpacked-package> <out-dir>
```

Expect `A_payload_manifest PASS, rows 909, match 909`; `D1..D7` with exactly one `REVIEW`
(`D2_wp15_closure`); `verdict PASS` plus `idempotence.body_identical: true`.

## Tree

| Path | What it is |
|---|---|
| `receipts/` | one JSON per check: command, measured numbers, verdict |
| `tools/` | the verifiers actually used; read them before trusting a number |
| `first_work/` | the WP-FHS-15 output reproduced this round: 3 SPECs, PI-PKG, TaskSpecSeed, FUO, DAG, planner artefacts |
| `docs/` | the 17 current books, byte-identical to the delivery |
| `package/` | the delivery's own manifests, byte-exact, so an outsider can re-verify 909/909 |
| `logs/` | raw stdout: first-work run, the 35-check harness before and after repair, the five affected tests |
| `STAGED_MANIFEST.json` | per-file SHA-256 of the staged tree (inventory, not proof) |

## Not here

No native permit, WorkOrder, lease, Checker receipt, publication, tag or release. The first work stops
at `SOURCE_READ` / `LOCAL_DRAFT`; the SPECs and PI are design candidates for the original PIPD intake,
and the original HGK issuer still has to admit anything that becomes an effect.

## Reading order

`EXECUTION_REPORT.md` → `FINDINGS.md` → `REPRODUCE.md` → `EVIDENCE_INDEX.md`.
