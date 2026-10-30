# Evidence index

"Decisive" = a reviewer should read it. "Informative" = supports a detail; nothing depends on it alone.

## Receipts

| File | Verdict | Decisive | Establishes |
|---|---|---|---|
| `P1_PACKAGE_INTEGRITY.json` | A/D/E PASS, C FAIL | informative | the first run, which tolerated the renamed book directory via an alias. Its `B_undeclared_files` writes `extra: 33` where the set has 2 members — a counting bug, superseded by P1B and by P1_VERIFIED (both report the two manifests). Do not cite its arithmetic. |
| `P1B_PACKAGE_INTEGRITY_CANONICAL.json` | A/D/E PASS, C FAIL | **decisive** | 909/909 payload rows match bytes+SHA-256 on the canonical layout; 30/30 links; three delivery rows absent (F-01). |
| `P1C_SEAL_AND_READBACK.json` | PASS | **decisive** | the new seal: two archives, per-entry readback, second seal byte-identical. |
| `P2_FIRST_WORK_RUN.json` | PASS | **decisive** | 24 clauses → 24 atoms, PI PASS, 3 SPECs, KnownAnswer 0, `NATIVE_NOT_RUN`, per-file identical/differing table. |
| `P2B_CHECK_FIRST_WORK_AS_SHIPPED.json` | 34/35 | **decisive** | the harness fails as shipped; failing check and cause named (F-03). |
| `P2D_CHECK_FIRST_WORK_REPAIRED.json` | 35/35 | **decisive** | same harness after the ordering repair only. |
| `P2C_IDENTITY_ROOT_SCOPE.json` | PASS | **decisive** | identity is absolute-root scoped; root-relative intake is stable (F-04). |
| `P3_STRUCTURAL_CHECKS.json` | 6 PASS + 1 REVIEW | **decisive** | DAG shape, closure mismatch (F-05), 24 complete atoms, FUO ten fields, SPEC acceptance, 2,221 unique readers. |
| `P5A_LANE_PROBE_EXECUTE.json` | ok=true | **decisive** | EXECUTE lane served `opencode-go/deepseek-v4.1-flash` with nonce echo; also the F-08 artefact. |
| `P5B_LANE_EXECUTE_WRITER.json` | ok=true | **decisive** | a bounded single-file write through the same lane, 28 s, own nonce. |
| `P9_OWNER_WINDOW.json` | CLOSED, ops 0 | **decisive** | the owner signing window: opened 13:54:16, closed 14:54:01, `ops_used 0`, `refusals 0`, broker gone; the passphrase never entered this repository or the agent context. |
| `P5E_LANE_WRITER_OVERRUN.json` | OVERRUN_TERMINATED | **decisive** | the terminated authoring turn: 8.5 min, 0 files, and the `4294967295` reaping artefact (F-11). |
| `P5C_LANE_VERIFY_BLOCKED.json` | ok=false | **decisive** | the VERIFY arm returned upstream 401 / all routes exhausted: independent acceptance did not run (F-10). |
| `P7_SEAL_AND_PARTITION.json` | BODY PASS / EVIDENCE FAIL | **decisive** | the declared archives rebuilt from the manifest's own partition: BODY byte-exact (114 entries, 4,007,065 B, `5e722cfb…`), EVIDENCE 4,801 B short; also records the withdrawn first seal (F-01, F-12). |
| `P8_DELIVERED_RECORD_ANOMALY.json` | ANOMALY | **decisive** | the delivery's 35/0 record and its 34/1 predecessor share `elapsed_seconds` to sixteen digits (F-14). |
| `P1_PACKAGE_INTEGRITY_VERIFIED.json` | **FAIL** (A/B/D PASS; C/E/F/G/H FAIL, I SKIPPED) | **decisive** | an independent worker run on the same tree. Its `F_reseal_deterministic` rebuilds the BODY archive to the declared digest byte-exactly while the EVIDENCE archive falls short — the first evidence that the BODY claim was checkable. It is a FAILing receipt: do not read it as corroboration of a PASS. |

## Logs

| File | What it is |
|---|---|
| `first_work.out` | stdout of the first-work run. |
| `check_first_work.out` | harness as shipped: 34/35, failing check named. |
| `check_first_work_patched.out` | after the ordering repair: 35/35. |
| `PIPD_5_AFFECTED_TESTS_RAW.txt` | raw `unittest -v` of the five named tests. The file records no commit, path or command; the `995c7ad` attribution comes from `REPRODUCE.md` step 7, run in this round. |
| `lane_probe.out`, `lane_verify.out`, `lane_writer.out` | the three lane turns as the dispatcher printed them, including the 401 and the `ERR_LANE_ALL_ROUTES_EXHAUSTED` (F-06, F-08, F-10). |
| `hgk-lane-dispatch.py.before-R-EXEC-02` | the dispatcher before the `NameError` repair, so the before/after digest pair in F-07 has an artefact. |

## Tools

| File | Does | Read before trusting |
|---|---|---|
| `verify_package.py` | payload/delivery manifest + links + claim keywords | any integrity number |
| `seal_package.py` | deterministic seal, per-entry readback, idempotence | any archive SHA |
| `exec_checks.py` | structural invariants over the reproduced first work | any DAG/atom/FUO number |
| `identity_probe.py` | absolute-root vs root-relative identity | F-04 |
| `stage_repo.py` | deterministic staging of this tree's receipts/tools/artefacts | what is in this tree |

## Not evidence

`STAGED_MANIFEST.json` is an inventory: it lists what was copied and with which SHA-256 so later tampering
is detectable. It does not establish that the copy was correct — that is what `receipts/` is for.

## Advisory audit

`ADVISORY_AUDIT.md` records three independent read-only processes that attacked the claims above, which of
their findings were confirmed by re-measurement, and which one was rejected. It is explicitly not a lane
verdict.

## Claim ceiling

`PIPD_CONSTRUCTION_HANDOFF_READY`, author side, static. No native admission, native verification,
independent acceptance or release is claimed in any artefact here. The first-work output is a set of
design candidates for the original PIPD intake — not a permit, not a WorkOrder.
