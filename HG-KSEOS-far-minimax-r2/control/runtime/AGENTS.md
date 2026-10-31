# AGENTS.md — Windows/Codex Runtime Projection Scope
Version: v2026.08.07-FINAL-r2
Applies to: Windows bootstrap, Codex worktree, Harness/Loop runtime-projection paths.

Windows Native PowerShell is the P0 profile. Non-admin and sandboxed operation is default. External effects require TaskSpec + unexpired approval token. Allowed roots, network, secrets, timeout and cleanup are explicit. Never push/merge/deploy/release by implication. Checkpoint before effectful transitions; on NACK revoke leases/tokens, restore pre-state and return evidence.
