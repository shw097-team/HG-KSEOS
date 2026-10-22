## Why

The HGK sealed-relay supervisor scheduled task `\Root\HGK-OpenCodex-Sealed-10101` was
registered on 2026-10-07 by round FAR-LANE-SOD-004 (step S4, "previously absent") to health
check and, if needed, restart the sealed EXECUTE-lane relay on `http://127.0.0.1:10101`.
Its action launches `pwsh.exe` directly with no window-hiding directive, under an interactive
logon token, on a five-minute repetition trigger. Two independent FAR rounds (FAR-LANE-SOD-008
and FAR-LANE-SOD-009) measured the consequence on this host: a visible console window appears
on the operator's desktop for roughly 1.3-2.5 seconds at every trigger (measured at
21:33:05-21:33:07 and 21:38:05-21:38:08 on 2026-10-08, each aligned with the supervisor receipt
being rewritten), and it does so whether or not any governed task is executing. A controlled
probe matrix over six task variants proved that neither the task's `<Hidden>true</Hidden>`
setting nor a `-WindowStyle Hidden` command-line directive suppresses the window on a host where
Windows Terminal is the default terminal host; only a windowless launcher host did. The same
rounds also measured two further gaps: the supervisor overwrites a single receipt file each run
(no run history, so "has it ever actually restarted the relay" is not answerable after the fact),
and its recovery window (`WindowSeconds=300`) equals its trigger interval (`PT5M`), so under an
unhealthy relay one recovery attempt can consume the whole window and the next trigger is dropped
by `IgnoreNew`.

The task itself is not removable: it is the only automatic bootstrap and recovery path for the
relay that the sealed EXECUTE lane depends on, and it started that relay at the most recent logon
(process evidence: a detached `bun.exe` relay owner with no other parent).

## What Changes

- Replace the scheduled task's action host with a windowless launcher (wscript.exe running a VBS
  that invokes the same PowerShell and the same supervisor script with identical governance
  arguments), and add `<Hidden>true</Hidden>` as belt-and-braces. The governance semantics
  (`-Action Run -MaxRestarts 3 -WindowSeconds 300`, `PT5M` repetition, interactive logon) are
  preserved unchanged.
- Give the supervisor an append-only run history (`relay-supervisor.receipts.jsonl`, one JSON line
  per run carrying a run sequence, epoch, status, restart count and health) while keeping the
  existing single receipt file contract intact for existing readers.
- Add a cooldown so that a restart is attempted at most once per epoch instead of re-entering the
  restart loop within the same recovery window.
- Separate the recovery budget from the trigger interval so a recovery attempt cannot silently
  swallow the following trigger.
- Keep the documented rollback valid: the lane-enforcement kit already defines removal/restore of
  this task as its rollback, and the convergence keeps that rollback meaningful by not changing the
  supervisor's governance arguments.

## Impact

Affected: the definition of the scheduled task `\Root\HGK-OpenCodex-Sealed-10101`; the supervisor
script `scripts/supervise-hgk-opencodex.ps1` (additive change only); the supervisor's evidence
directory (`var/far-lane-sod-003/evidence/`); the operator-visible desktop behaviour of the host.
Not affected: the sealed relay code or port, the provider/model binding of the EXECUTE lane, the
EXECUTE front door, the Shared Spine schema, provider credentials, SQS financial truth, and any
production or live-broker path. No claim of external acceptance is made by this change.
