---
name: hgk-governed-runtime
description: Route bounded plan/execute/verify work through the pinned HG-KSEOS native control plane; never mint Permits or claim native effect
---

# HGK governed runtime (adapter)

This skill is an *adapter*, not a control plane. It tells an agent harness how to reach the pinned
HG-KSEOS root, what ABI it can speak, and where the boundary of its authority is.

## What it does

1. **Resolve the root.** Read `adapter.json` next to this skill and use its `hgk_root`; never guess a
   different root and never invent a spine database.
2. **Probe before use.** Call the adapter's `doctor` first. A failed probe means the native plane is
   not reachable — report `HOST_PENDING`, do not substitute a local simulation for it.
3. **Stay inside the ABI.** `plan`, `execute`, `verify` are readable entry points. `WorkOrder`,
   `ExecutionBinding` and `Permit` are *required from the native plane*; this adapter cannot issue,
   sign or admit any of them.

## What it must never do

- Mint a Permit, admit a WorkOrder, or self-sign an acknowledgement.
- Describe a local Python check as a native effect.
- Modify the HGK root: upgrades there belong to the HGK owner under a separate WorkOrder.
