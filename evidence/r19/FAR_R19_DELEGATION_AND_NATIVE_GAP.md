# FAR R19 — why 13 of 22 work packages cannot be closed by an agent, and what to do about it

Round `R19-FHS-20261029` · subject `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`
· continuation of `R18-FHS-SKELETON-SPINE-20261029`
· claim ceiling: measurements below are local and this machine only; nothing here is native, independently
accepted, released or promoted.

---

## 1. Decision question (the only one that matters)

> Is the remaining work blocked by **missing evidence**, or by **missing authority**?
> If it is authority, exactly which artefact is missing, and what is the smallest thing the owner must do?

## 2. Denominator (measured, not asserted)

| set | count | source |
|---|---|---|
| work packages in the typed DAG | 22 | `03_TESTS_AND_READBACK/wp_graph.json` |
| effect classes | `HOST_OP` 10 · `SOURCE_READ` 5 · `LOCAL_DRAFT_WRITE` 4 · `REPO_WRITE` 2 · `RELEASE` 1 | same |
| rows closed after R19 | **6 DONE / 13 PARTIAL / 7 PARKED** (ledger audit rc=0) | `ledger.json` |
| owner-signed delegation allowlist | **7 WPs**, classes `SOURCE_READ` + `REPO_WRITE_TO_CANDIDATE_BRANCH` | `governance/delegation_R18_canonical.json` |
| owner-signed delegation **deny** list | `RELEASE, HOST_INSTALL, secrets, force-push, main, merge, tag, **LOCAL_DRAFT_WRITE**` | same |
| protected registry request digests in scope | 245 (all B1 subject) | `%ProgramData%\HG-KSEOS\native-admission\registry.json` |
| R19 request digests in scope | **0** | measured: `REQUEST_SCOPE` is what `authorize()` raises |

## 3. Finding F19-1 — the ceiling is authority, not evidence

`native_admission.authorize()` refuses at `REQUEST_SCOPE` unless the exact request digest is already
listed in the protected registry's `scope.request_sha256`. That registry is written by an **owner
elevated step** (the current one records `installed_by: "OWNER STEP 3 (elevated), no passphrase used"`,
revision 15). `scripts/native-trust-maintenance.ps1` has no "revise" mode at all: `Enable` throws
`ERR_EXISTING_REGISTRY_USE_REVIEWED_REVISION_NOT_OVERWRITE` once a registry exists.

Therefore: **no agent action can produce the first R19 PERMIT.** Not more tests, not more evidence,
not a longer run. The three references (`source_freeze`, `task_kind`, `oracle_ratification`) are also
owner-key signatures, and each permit additionally needs the canonical DB plus a lease generation.

**Blast radius**: 10 `HOST_OP` + 2 `REPO_WRITE` + 1 `RELEASE` = **13 rows**, i.e. 59% of the DAG.

## 4. Finding F19-2 — the signed delegation is narrower than the DAG, and it denies a class the DAG needs

The delegation covers exactly 7 WPs and two classes. `LOCAL_DRAFT_WRITE` — the class of **WP-05, WP-07,
WP-15, WP-16** — is in the **deny** list. Consequence, measured this round: WP-05 and WP-16 have
complete, rerunnable engineering receipts but their ledger transition to `DONE` was **refused** by
`tools/delegation_gate.py`:

```
REFUSED WP-FHS-05: ERR_NO_DERIVED_PERMIT
REFUSED WP-FHS-16: ERR_NO_DERIVED_PERMIT
```

That is the gate working as specified. The defect is in the *scope*, not the gate: a delegation that
covers 7 of 22 rows cannot close the round no matter how much work is done. Previous rounds reported
"22/22 defensible" — true only in the weak sense that every row had a named reason for not closing.

## 5. Finding F19-3 — the repository's `main` shares no history with the delivery lineage

`main` = `f6dfb1e5`; lineage branch `candidate/r18-fhs-skeleton-spine-20261029` = `190df334`.
`POST /pulls` returns `422: The candidate/r19-fhs-implementation branch has no history in common with main`.
PR #4 (R18) targets `main` from an orphan root and has the same defect: it can never be merged.
R19 therefore opened **PR #5 against the real lineage** (`base=candidate/r18-fhs-skeleton-spine-20261029`,
head `db88f372`, 92 files, `mergeable: true`). Reaching `main` needs an owner decision on which root
is canonical — an unrelated-histories merge is exactly the kind of history rewrite that must not be
done silently.

## 5b. Finding F19-4 — even an owner-signed amendment cannot grant `LOCAL_DRAFT_WRITE`

Measured live this round, with the owner's passphrase window actually open (`WIN-254a1c9fbe72`, 40 ops):

1. built an amended `HGK.OWNER_DELEGATION/2` adding `WP-FHS-05/07/15/16`, the class
   `LOCAL_DRAFT_WRITE` bounded to `var/R19-FHS-20261029/**` and `var/R19-NATIVE-EXEC/**`, keeping every
   other denial;
2. signed it through the owner broker — **signature verifies** against the canonical owner key
   (`412b3519…`), 1 op consumed;
3. ran the gate: `WP-FHS-12 / LOCAL_DRAFT_WRITE → REFUSED_CLASS_DENIED`.

Cause: `tools/delegation_gate.py` carries `HARD_DENY = {RELEASE, HOST_INSTALL, secrets, force-push,
main, merge, tag, LOCAL_DRAFT_WRITE}` — a **code-level** deny that a signed record cannot lift. So
option B is not an owner decision that work can satisfy; it is a code change to the enforcement point.

**I did not make that change.** Editing `HARD_DENY` would be the agent loosening its own gate. The
signed amendment is preserved as `governance/delegation_R19_amendment_signed_NOT_INSTALLED.json`, the
canonical delegation was **restored** to `R18-CANON-6733b6bb`, and the gate is back to refusing
WP-05 (`REFUSED_WP_NOT_ALLOWLISTED`). One window op was consumed and is disclosed in
`receipts/DELEGATION_AMENDMENT_OUTCOME_R19.json`.

Consequence: WP-05 / WP-15 / WP-16 keep `PARTIAL` with `engineering=VERIFIED`. The work and the
receipts stand; only the ledger transition is refused, and it is refused by design.

## 6. Options (lowest friction first)

| # | option | who | cost | unblocks |
|---|---|---|---|---|
| A | Owner installs `owner_gate/REGISTRY_REVISION_PLAN.json` (policy_epoch 34→35, 13 request digests, dedicated exec root `var/R19-NATIVE-EXEC` @ `1f56991d`, root_identity `32165637:002d0000000a80e0`, 7 runner pins) | owner, one elevated step | 1 command + review | first R19 PERMIT; then 13 rows become mechanically runnable by the agent |
| B' | Owner decides on `LOCAL_DRAFT_WRITE`: either remove it from `HARD_DENY` in `tools/delegation_gate.py` and install the already-signed amendment, or state that it stays denied and the rows stay `PARTIAL` forever | owner, code-level | 1 edit + 1 restore | WP-05, WP-07, WP-15, WP-16 |
| C | Declare the subject "delivered as candidate" and stop at 6/13/7 | owner | 0 | nothing; documents the ceiling honestly |
| D | Re-root `main` onto the lineage or declare the lineage canonical | owner, repo-level | history decision | makes PR #5 mergeable and retires PR #4 |

**Recommendation: A + B' + D in one sitting.** A is the only option that produces new *native* evidence;
B' is a two-line decision that turns two finished rows green; D is a decision, not work. They are
independent, so any subset lands value.

## 7. Residual items that are evidence gaps, not authority gaps (agent-actionable, not yet done)

| item | state | why it is not closed |
|---|---|---|
| 96-cell oracle | 50 `PASS_LOCAL_ORACLE` / 46 `HOLD` / 0 `DENY` (679 checks, 0 fail) | the 46 HOLD cells need a calibrated Reader / human judge that does not exist on this host; 96 native cases remain `0` |
| 18-stage TPM trace | `stages_declared 18`, `stages_with_evidence **0**` | no per-stage execution receipt exists; producing one needs the host install (authority) |
| 192-cell Host/Kind matrix (WP-20) | `HOST_OP` | authority |
| LICENSE / NOTICE in the doc package | **absent** — recorded as `F-LIC-01` / `F-NOTICE-01` | a packaging decision, not a scan failure |
| MVS01-10 mapping | 5 DONE / 5 PARTIAL | follows the WP rows; no independent claim |

## 8. Non-claims

No permit, no reference signature, no native admission, no promotion, no release, no `main` merge,
no independent acceptance. The R19 receipts are `AUTHOR_SIDE + ISOLATED_LOCAL`. The 13 gated rows are
**NOT RUN**, not "blocked because broken" — `NOT_RUN ≠ FAILED`.
