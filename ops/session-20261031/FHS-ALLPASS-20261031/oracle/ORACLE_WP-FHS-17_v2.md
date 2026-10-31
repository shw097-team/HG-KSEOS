# ORACLE — WP-FHS-17, sitting G

**Verdict: PASS** (bounded chain)

- nonce `NONCE-VERIFY-LANEACC-20261031-G`
- ceiling: bounded WP-local receiver chain — NOT native admission, NOT canonical acceptance, NOT promotion

| measured | value |
| --- | --- |
| install | INSTALLED |
| load | LOADED_AND_INVOKED |
| consumer | CONSUMER_ACK |
| negatives_all_refused | True |
| install_receipt_is_from_this_run | True |
| run_started | 2026-10-31T14:25:20Z |
| install_receipt | 2026-10-31T14:25:29.101966Z |

| clause | state |
| --- | --- |
| native_host_admission | OPEN |
| original_consumer_is_not_wp_local | OPEN |
| cap_boot_abi_resolution | OPEN |
| officer_could_execute_subject | CLOSED |
| stage_root_vs_install_root | OPEN |
| rollout_identity_binding | OPEN |

It does not mean the package is native-admitted. Five of six clauses stay OPEN and EVIDENCE_GAP.md still lists them. It means the bounded chain installs, loads, invokes, acks and refuses all 15 negatives for the reasons under test, and that an independent checker ran it in a verified copy without touching the record.
