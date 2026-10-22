# Design — R9-0 FAR residual closure

## D1. Why one new flat capability

The round's deltas are one acceptance shape (R9-A), one guarded-apply contract (R9-B), a set of record
corrections (R9-C) and a research receipt (R9-D). They share a single source of truth — the FAR run — and a
single ceiling, so splitting them would multiply texts without separating authority. Items already proposed
elsewhere are cited rather than restated, so no second text competes for the same act.

## D2. Why the fix is two hunks and not a relaxation

The failing legal TraceLink is a *caller-shape* defect: the check that refuses an unbound link is exactly the
control the R7-0 hardening added, so making the test pass by weakening that check would reopen the hole. The
adaptation instead (a) derives the endpoint/oracle binding from the bundle's own atoms when — and only when —
no frozen context is supplied, and (b) guards the mapping access. The negative control is therefore part of
the acceptance: the M04/M06/M16 probes must still REJECT after the change.

## D3. Why the corrections are part of the deliverable

Two published R8 claims did not survive re-measurement (the drift claim and the cap framing) and one was
resolved by the package's own words (10/6). A round that only adds findings and never withdraws them inflates
its own ledger; the corrections are carried in the same change so the next reader sees one state.

## D4. Why the rebind is handed over, not executed

A canonical lane-chain rebind is a control-plane governance mutation: the registry's own text places it
outside a product/evidence round's authorisation, and the governing-document research requires owner-approved
scope plus an admitted WorkOrder plus a separate DOC05 admission. A second live owner order (the same day)
re-pointed PLAN to GLM because the OAuth arm was exhausted; this round measures that the arm serves again,
which removes the *reason* for the deviation but not the *authority* the owner holds over the row.
