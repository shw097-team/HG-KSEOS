## 1. Admit and freeze the change

- [x] 1.1 Register the requirement and admit TaskSpecs/WorkOrders through the HG-KSEOS lifecycle API (project FAR-LANE-SOD-010-CONVERGE, writer=codex)
- [x] 1.2 Capture the task definition preimage (registered task file and `schtasks /query /tn ... /xml`) with sha256 before any change
- [x] 1.3 Record the rollback command for every step in the apply checklist

## 2. Windowless launcher host

- [x] 2.1 Add the windowless launcher (wscript + VBS) that invokes the same pwsh and the same supervisor script with the same `-Action Run -MaxRestarts 3 -WindowSeconds 300` arguments
- [x] 2.2 Rewrite the task definition so its action command is the windowless host, preserving triggers, logon type, execution time limit, multiple-instance policy and start-when-available
- [x] 2.3 Re-register the task and read the definition back
- [x] 2.4 Measure one full trigger cycle with the host-measured window instrument and confirm zero visible console or terminal windows while the supervisor receipt is still refreshed

## 3. Recoverability and auditability

- [x] 3.1 Append one JSON line per run to `relay-supervisor.receipts.jsonl` with run sequence, epoch, status, restart count and health, without changing the existing single-receipt contract
- [x] 3.2 Add a cooldown so a restart is attempted at most once per epoch
- [ ] 3.3 Separate the recovery budget from the trigger interval so a recovery attempt cannot drop the next trigger
      (DEFERRED by PLAN ruling D2 — CONV-2, not bundled into this repair)
      (DEFERRED by PLAN ruling D2 — CONV-2, not bundled into this repair)

## 4. Independent verification and close-out

- [x] 4.1 Obtain an independent check from a lane on a different model (checker brief as a contract file; checker writes only under the round's verify directory)
- [x] 4.2 Re-run the window instrument after the change and record the pass/fail evidence with timestamps
- [x] 4.3 Freeze the round evidence manifest, disclose every side effect, and state the claim ceiling
