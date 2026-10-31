# EVIDENCE_GAP — WP-FHS-17 bounded occupant chain

Reproduce: `cd C:/wg/queue/WP-FHS-17 && python tools/build_evidence.py`

This file states what the tree could not close. It is **not** a claim that the package passes. The officer's
verdict on this package is FAIL (`EVT-682dba95f5c16e25`) and this file does not change it.

Corrected 2026-10-31: an earlier handoff (`FAR-20261031-032`) cited this file as existing. It did not — the gap
was stated only in `wp17_receiver.py`'s docstring and in the `EXECUTED_BOUNDED_LOCAL` ceiling string. The file
exists now, which is the point of the correction: an absent object must be absent *and named*, not merely
unmentioned.

## What the chain actually measured (original tree, this round)

| Stage | Result | Artefact |
| --- | --- | --- |
| Grant issued by the original Issuer (`key_id 135455ca00280c39`) | `GRANT_VALID`, nonce unspent, TTL, WriteSet and candidate digest all matching | `evidence/grant.json`, `evidence/grant-status.json` |
| Receiver gate | 14/14 binding checks `ok` | `evidence/install.json` |
| Install | `PACKAGED → GRANT_OK → INSTALLED`, exact WriteSet, `O_CREAT|O_EXCL` | `evidence/install.json` |
| Fresh load | `LOADED_AND_INVOKED`, fresh process, `LoadedSHA` equals the pinned candidate bytes | `evidence/load.json` |
| Invoke + consumer | needed feature invoked with real input, original consumer `CONSUMER_ACK` | `evidence/load.json` |
| Negatives | 15/15 refused **for the reason under test** | `evidence/negatives/*` |
| Tamper | `LOADED_CHANGED_DURING_INVOKE`, consumer ack withheld | `evidence/tamper.json` |

## Gaps that remain OPEN

| Clause | State | What is missing |
| --- | --- | --- |
| `native_host_admission` | **OPEN** | The original Host Installer / Loader / Registry never ran. This tree is a bounded WP-local receiver; it applies a WriteSet and loads an occupant, it does not register one in the Host's capability registry. |
| `original_consumer_is_not_wp_local` | **OPEN** | The consumer that acked is the package's own consumer, not the Host's original Skill Reader. A self-ack is not an original ack. |
| `cap_boot_abi_resolution` | **OPEN** | The occupant is resolved by this receiver's own resolver, not through the CAP-BOOT ABI the Host declares. |
| `officer_could_execute_subject` | **OPEN** | The VERIFY sitting could not run this tree: its sandbox write root is the dispatched repository, and `--guard-subject` is a digest anchor, not a write grant. A checker that cannot run the subject has not judged it. |
| `stage_root_vs_install_root` | **OPEN** | The load reads `evidence/stage-root` with `--local-loader-control`, while the install wrote `evidence/install-root`. The bytes are identical (measured), but "the loaded bytes are the installed bytes" is currently an equality of contents, not of provenance. |
| `rollout_identity_binding` | **OPEN** | `--identity-source codex-rollout` resolves the newest rollout from a directory; it does not bind to the child's pid or turn id (see `REQ-SEC-ROLLOUT-BINDING`). |

## What would close each gap

| Gap | Closing object |
| --- | --- |
| `native_host_admission` | the original Host Installer/Registry, present and answering on this host (see `FAR-20261031-033` §2: it is not in any of the four repos) |
| `original_consumer_is_not_wp_local` | an original Host Reader that resolves the occupant and returns its own ack |
| `cap_boot_abi_resolution` | the CAP-BOOT ABI resolver, not the receiver's own |
| `officer_could_execute_subject` | the subject tree inside the dispatched repository, or a sandbox that grants the subject as a write root |
| `stage_root_vs_install_root` | load directly from `install-root`, or record the staging step as the provenance link |
| `rollout_identity_binding` | a rollout whose `turn_id`/`pid` matches the spawn (R-6) |

## Ceiling

`EXECUTED_BOUNDED_LOCAL`. Not native admission, not canonical acceptance, not promotion, not release.
