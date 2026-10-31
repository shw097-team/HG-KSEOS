# HLPE qualification report

Status: `QUALIFIED_AS_READ_ONLY_ENGINEERING_BASE_WITH_PATH_REBIND_REQUIRED`

The canonical integrated target is `C:\Projects\Agent_Workspace\HG-KSEOS\工程基座\sdlc-prw-hlpe-formal` at clean HEAD `ee30dc034a3d4fd0e24a6bfdf77ad8aae273b400`. It is the reusable implementation seed and exposes `PlanCompiler`, shared contracts, bootstrap/factory components, schemas, tests, and the `python -m hlpe` CLI.

The immutable control base is the distinct 305-file r3 tree at `C:\Projects\Agent_Workspace\HG-KSEOS\工程基座\SDLC_PRW_HLPE\_HLPE_BASE\HLPE_MAIN_PLATFORM_3DOMAINS_v2026.07.22-r3`. It must not be relabelled as the r1 integrated code seed.

Historical acceptance evidence at the unchanged target HEAD records 51/51 runtime tests, 90/90 requirements, 36/36 canonical tests, 4,083/4,083 assets, 13/13 assurance gates, and zero blocking TT. That evidence is useful provenance but not a fresh HG-KSEOS qualification because its manifests bind the old `C:\Projects\AGENT WORK SPACE\SDLC_PRW_HLPE` root.

The `sdlc-prw-formal` and `sru-orochi-formal` repositories contain substantial pre-existing user changes. They are preserved read-only; no reset, cleanup, or writer reuse is allowed. A fresh binding must target the clean integrated repository or a new isolated worktree only.

Required qualification continuation:

1. resolve the HG-KSEOS path binding without editing upstream manifests in place;
2. verify the r3 exact set and hashes under `_HLPE_BASE`;
3. run schema validation, round-trip, critical-field negative fixtures, fallback, and readback from a writable isolated receiver;
4. issue a new binding receipt with rollback and evidence.
