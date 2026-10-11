# Control-plane admission receipt — credential broker standing install

This file records the ACTUAL governance route taken. `INSTALL_MANIFEST.json` labels its
`candidate_admission_script` as a *candidate*; the route actually used was the minimal one, and this
receipt exists so the installed directory does not reference a round path that was never created.

## Admission

| field | value |
|---|---|
| authority | HG-KSEOS, sole system governance / normative control plane |
| project | `HGK-CHU-20261009` (control-plane hardening unit) |
| requirement | `REQ-HGK-CREDBROKER-001` — FROZEN |
| taskspec / workorder | `TS-req-hgk-credbroker-001` / `WO-TS-req-hgk-credbroker-001` |
| API | typed `SharedSpine` / `ProjectLifecycleController.admit_requirement` — no raw SQL |
| project state | before `EXECUTING`, after `EXECUTING` (unchanged) |
| errors | 0 |
| route | A (minimal): admit into an existing admissible control-plane project rather than create a new lifecycle |
| why not a product round | `FAR-PIPD-R8-DISPATCH-004` §4: an edit to HG-KSEOS control-plane tooling needs its own admission and must not ride along inside a PIPD round |

## Install

| field | value |
|---|---|
| target | `HG-KSEOS/scripts/cred/` |
| mode | byte-preserving copy (`cp -p`), **not** reconstruction from rendered text |
| verification | every file `cmp`-identical to the candidate; all 6 entries pinned in `INSTALL_MANIFEST.json` re-hashed → **0 mismatches** |
| activation | **NONE.** A search of `config/` and `scripts/*.py` / `scripts/*.ps1` for `scripts/cred`, `cred_broker` and `cred_preflight` returns **0** references outside `scripts/cred/` itself. |

## Acceptance oracle status (from the admitted requirement)

| # | criterion | status |
|---|---|---|
| 1 | three modules present under `scripts/cred/` with the pinned sha256 | **PASS** — 6/6 pinned entries verified |
| 2 | `verify_offline.py` returns `PASS_OFFLINE_T5_UNPROVEN` or `PASS`; `selftest.py` 5/5 on DUMMY credentials | **PASS** — `verify_offline.py` → `PASS_OFFLINE_T5_UNPROVEN` (T5 needs network, reported SKIP not PASS); `selftest.py` → 5/5 on dummy credentials in R9 |
| 3 | no config references the installed path (non-activated) | **PASS** — 0 hits |
| 4 | no secret value in any artefact | **PASS** — only metadata was ever read; candidates carry no token value |

Criterion 2 is recorded honestly rather than rounded up: the offline verifier's own verdict names T5
as unproven, so it is **not** claimed as a full 5/5 here. The full 5/5 run happened in R9 on a
networked host, and is cited as such.

## What is NOT done

- The broker is **not wired into any lane**. Activating it (routing a write lane through it) is a
  separate, later, separately-admitted change.
- The GitHub App setup remains human: registering the App, downloading its private key, and installing
  it are **UI-only** — GitHub exposes no API for any of the three. Until then the PAT bridge is used.
- Nothing here rotates a credential. GitHub exposes no API to read a PAT's own expiry or to renew it.
