---
name: method-tool-translation
description: "method-tool-translation: QuerySet、Top12、rubric、fit-gap、donor→first-party. Trigger when allowed when user/TaskSpec names the skill and required gates are met; user explicit for scout/translation. Do not trigger when high-risk effect without token; source/identity conflict; collision; runtime boundary breach."
---

# SK-18 — method-tool-translation

## Purpose
QuerySet、Top12、rubric、fit-gap、donor→first-party

## Trigger
allowed when user/TaskSpec names the skill and required gates are met; user explicit for scout/translation

## Do-not-trigger
high-risk effect without token; source/identity conflict; collision; runtime boundary breach

## Inputs
Authoritative source/TaskSpec inputs referenced by `WP-13／14`; exact paths/objects must be declared by the caller or current workspace contract.

## Preconditions
authority/source/scope/permission/inputs available; no blocking security finding

## Procedure
1. Resolve A0/A1 authority and the `WP-13／14` contract.
2. Validate source identity, scope, permissions and collision state.
3. Execute only the focused instruction: QuerySet、Top12、rubric、fit-gap、donor→first-party.
4. Run invocation/behavior/security fixtures before accepting the generated artifact.
5. Emit artifact hash, validator result, evidence reference and rollback reference; require receiver ACK/NACK.

## Outputs
Versioned skill result/projection and evidence receipt; never an implicit production or external-effect claim.

## Evidence
package manifest、schema/test/security reports、installation/removal receipt

## Errors
Deny on collision, source/identity conflict, permission expansion, security finding, missing evidence or receiver NACK. Preserve the prior accepted generation.

## Security
scripts run only in Harness sandbox; no secret echo; writable roots/egress declared Side effects require explicit approval token and Harness admission.

## Stop
Stop on authority conflict, injection/tool poisoning, undeclared effect/network/secret, failed functional oracle, retry exhaustion or Human veto.

## Escalation
F15-04 behavior verifier＋F16-05 security verifier

## Rollback
delete donor copy and restore first-party baseline

## Tests
Invocation: popular tool auto-adoption／donor command bypass rejected. Behavioral: positive/negative/boundary/adversarial plus collision and removal.

## Runtime status
`DESIGN/MATERIALIZED_LOCAL`; installation or invocation in the Windows/Codex runtime is `NOT_EXECUTED` unless returned external evidence says otherwise.
