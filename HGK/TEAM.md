# HGK Team — RP-002 Stage-2 Projection

schema: RP002-PROJECT-TEAM-STAGE2-PROJECTION/1
parent_schema_ref: RP002-PROJECT-TEAM/2
project_id: HGK-REFERENCE-PROJECT-002
canonical_board_id: RP002-FABRIC-BOOTSTRAP

## Persistent P0 profiles (5)
- hgk-orchestrator — compile/route admitted WorkOrder; Kanban topology; task-class admission
- hgk-coding-factory — bounded implementation; Codex writer route; worktree
- hgk-engineering-reviewer — L1 review, design/conformance finding
- hgk-qa — L1 tests/QA/reproduction
- hgk-security — L1 security/permission/supply-chain checks

## Governance profiles (2, materialized at O1)
- construction-commander — classify/compile bounded engineering request; issue WorkOrder
- acceptance-officer — VERIFY_ONLY; candidate write / WorkOrder create / repair / promotion all denied

## On-demand workers
hgk-knowledge-distiller, hgk-documentation-worker, hgk-performance-worker, hgk-design-worker,
hgk-devex-worker, specialist-research-worker

## Invariants
ROLE != PROFILE != WORKER. No permanent profile per gstack role.
SQS stack state: PENDING_STAGE3_NOT_YET_MATERIALIZED.
escalation_policy_ref: C:\Projects\Agent_Workspace\Fabric\control\SOD_POLICY.yaml
no_live_write: true
