# OWNER STEP — registry revision for R19 (NOT executed by the agent)

**Why you and not me**: `native_admission.authorize()` refuses with `REQUEST_SCOPE` unless the exact
request digest is already in the protected registry's `scope.request_sha256`. Writing that registry is
the act of granting native authority. An agent doing it would be issuing its own permit — refused by
design, so this round stops here and hands you a pinned plan instead.

**Measured facts (this round, this machine)**

| item | value |
|---|---|
| current registry | `C:\ProgramData\HG-KSEOS\native-admission\registry.json` sha256 `73b4dec3225ffa81cbf4f30af631d73d73d482cef02a2b338c82ebf2119a8a87` |
| current policy_epoch | `34` → proposed `35` |
| dedicated exec root | `C:\Projects\Agent_Workspace\var\R19-NATIVE-EXEC` |
| exec root HEAD | `1f56991d9737c399a0f302b4c29b7498b264b2eb` |
| root_identity | `32165637:002d0000000a80e0` |
| approved files | 7 runner pins (sha256 in the plan) |
| gated work packages | 13 request digests |

**The one command (elevated PowerShell, you run it)**

```powershell
# 1. review the bytes you are about to authorise
Get-FileHash -Algorithm SHA256 'C:\Projects\Agent_Workspace\var\R19-FHS-20261029\owner_gate\REGISTRY_REVISION_PLAN.json'
# 2. install (same elevated-step shape as the current registry.revision 15)
#    the installer is the owner's; it must pin plan_sha256='0807eba282724591ae5963a59529843d12b2f026f618fe28caf02f1404720202'
```

**What this does NOT do**: it does not sign the three reference kinds (`source_freeze`, `task_kind`,
`oracle_ratification`) — those are minted per operation from the owner key through
`owner_window.py` (one passphrase, one bounded window), and `authorize()` additionally requires the
canonical DB (`C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db`) and a lease
generation. After the revision is installed, the remaining chain is mechanical and the agent can run it.

**Claim ceiling**: a proposed plan. No permit has been issued, no reference signed, no native effect run.
