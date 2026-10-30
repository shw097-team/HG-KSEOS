"""C15: the holdout is not the tuning input, and a failed signal cannot promote.

What ``hg_kseos.evolution`` actually guarantees, read from the module before this file was written:

* No holdout set lives on the controller. ``GovernedEvolutionController.__init__(spine,
  event_log=None, recurrence_threshold=2)`` keeps the spine, the log and the recurrence threshold
  and nothing else -- there is no ``holdout`` attribute and no holdout constructor argument. The
  brief's first branch assumed such an attribute exists; it does not, so this file takes the
  documented second branch and asserts what the shipped code really offers:

  - ``qualify()`` requires ``holdout_pass`` as a keyword-only argument with **no default**, so the
    promotion path cannot run without an explicit holdout verdict. Omitting it raises ``TypeError``
    from the signature instead of silently reading as a pass.
  - the evaluation plan seeded by ``create_candidate()`` carries ``holdout`` as its own channel
    (``{"tests": [], "holdout": [], "negative": [], "security": []}``), while the tuning input
    handed to the same call lands in a different column, ``baseline_metrics_json``.
    That channel is seeded EMPTY, and an empty set intersects nothing, so a disjointness claim read
    off the shipped seeding alone is vacuous. DOC-13#727 requires the holdout to be frozen before
    candidate generation with checker-held truth, and requires a leak to surface as
    ``HOLDOUT_CONTAMINATED``. This test therefore freezes a NON-EMPTY holdout first, refuses to make
    any disjointness claim until ``len(holdout) > 0`` is asserted, and then probes contamination
    detection. The probe is expected to fail on the shipped module, which exposes no holdout and no
    contamination check at all; the test is marked ``xfail(strict=True)`` so that gap stays visible
    instead of being papered over by a vacuously true assertion.
  - ``qualify(..., tests_pass=True, holdout_pass=False)`` still rejects, so the holdout verdict is a
    real veto over a candidate that already passed the tuning-facing tests.

  No holdout API is invented here: every assertion above is read off the shipped signature, schema
  and behaviour. The frozen holdout below is written to the persisted plan column as checker-held
  truth because the controller offers no freeze entry point; that absence is itself part of the
  finding, not a licence to assert against an empty set.

* The module has no signal-to-promotion entry point. ``promotion_gate()`` keys on a
  ``candidate_id``, and the only signal intake is ``capture_signal()``. A failed signal is therefore
  checked where it can actually fail: ``EvolutionSignal.__post_init__`` raises a typed
  ``EvolutionError`` for an unknown type or a bad severity, a captured single-occurrence LOW signal
  is reported ``candidate_worthy: False`` and writes no candidate row, and a candidate whose
  qualification failed is refused by the gate with ``ERR_PROMOTION_STATE``. In every branch the
  candidate table is asserted to hold zero promoted rows.

Each test builds its own SQLite database under pytest's ``tmp_path``; there is no network, no repo
fixture, and no write outside the pytest temp root.
"""

from __future__ import annotations

import inspect
import json
import sys

import pytest

sys.path.insert(0, "C:/Projects/Agent_Workspace/HG-KSEOS/src")

evolution = pytest.importorskip(
    "hg_kseos.evolution",
    reason="HG-KSEOS src is not importable in this interpreter",
)
spine_module = pytest.importorskip(
    "hg_kseos.spine",
    reason="HG-KSEOS src is not importable in this interpreter",
)

EvolutionError = evolution.EvolutionError
EvolutionSignal = evolution.EvolutionSignal
GovernedEvolutionController = evolution.GovernedEvolutionController
SharedSpine = spine_module.SharedSpine

PROJECT_ID = "HGK-PRJ-C15"
TUNING_INPUT = ["tuning-case-1", "tuning-case-2", "tuning-case-3"]


def _controller(tmp_path):
    spine = SharedSpine(tmp_path / "spine.db")
    spine.initialize()
    spine.create_project(PROJECT_ID)
    return spine, GovernedEvolutionController(spine)


def _promoted_rows(spine) -> int:
    """Rows recorded as promoted, read straight from the table the controller writes."""
    with spine.connect() as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM improvement_candidates "
            "WHERE promotion_state='PROMOTED' OR state='PROMOTED'"
        ).fetchone()[0]


@pytest.mark.xfail(
    strict=True,
    reason="DOC-13#727 freeze the holdout before candidate generation and keep checker-held truth; "
           "a leak must surface as HOLDOUT_CONTAMINATED. evolution.py has no holdout and no "
           "contamination check, so contamination detection is absent.",
)
def test_holdout_is_not_the_tuning_input(tmp_path):
    """The tuning channel and the holdout channel never share an element.

    See the module docstring: the controller exposes no holdout attribute, so the guarantee is
    asserted through the required ``holdout_pass`` argument and through the persisted evaluation
    plan, which keeps ``holdout`` as a channel separate from the tuning input in
    ``baseline_metrics``.

    The holdout is frozen NON-EMPTY before the candidate exists. An empty holdout intersects
    nothing, so disjointness asserted against it proves nothing (DOC-13#727).
    """
    spine, controller = _controller(tmp_path)

    # 1. There is no holdout attribute and no holdout constructor argument to read it from.
    assert not hasattr(controller, "holdout")
    init_params = inspect.signature(GovernedEvolutionController.__init__).parameters
    assert "holdout" not in init_params
    assert set(init_params) == {"self", "spine", "event_log", "recurrence_threshold"}

    # 2. The promotion path demands an explicit, required holdout verdict.
    qualify_params = inspect.signature(controller.qualify).parameters
    holdout_param = qualify_params["holdout_pass"]
    assert holdout_param.kind is inspect.Parameter.KEYWORD_ONLY
    assert holdout_param.default is inspect.Parameter.empty
    assert "tests_pass" in qualify_params

    # 3. Freeze a non-empty holdout BEFORE the candidate is generated, as checker-held truth.
    holdout = ["holdout-case-1", "holdout-case-2"]
    candidate = controller.create_candidate(
        PROJECT_ID,
        "GAP-C15",
        "SkillCandidate",
        "holdout must stay unseen by tuning",
        "no-op candidate",
        "no tuning cases leak into the holdout",
        baseline_metrics={"tuning_input": list(TUNING_INPUT)},
        source_signals=list(TUNING_INPUT),
    )
    with spine.transaction() as connection:
        connection.execute(
            "UPDATE improvement_candidates SET evaluation_plan_json=? WHERE candidate_id=?",
            (
                json.dumps(
                    {"tests": [], "holdout": list(holdout), "negative": [], "security": []},
                    ensure_ascii=False,
                ),
                candidate["candidate_id"],
            ),
        )
    with spine.connect() as connection:
        row = connection.execute(
            "SELECT baseline_metrics_json, evaluation_plan_json "
            "FROM improvement_candidates WHERE candidate_id=?",
            (candidate["candidate_id"],),
        ).fetchone()
    plan = json.loads(row["evaluation_plan_json"])
    tuning = json.loads(row["baseline_metrics_json"])["tuning_input"]
    assert set(plan) >= {"tests", "holdout", "negative", "security"}
    assert isinstance(plan["holdout"], list)

    # The disjointness claim is only meaningful over a real holdout: an empty holdout intersects
    # nothing, so asserting "no overlap" against it is vacuously true and proves nothing.
    assert len(plan["holdout"]) > 0, (
        "empty holdout proves nothing: an empty set intersects nothing, so any disjointness "
        "claim made against it is vacuous (DOC-13#727 requires checker-held holdout truth)"
    )
    assert set(plan["holdout"]) & set(tuning) == set()
    assert set(plan["holdout"]) & set(TUNING_INPUT) == set()
    # No tuning case is copied into the evaluation plan at all, so the holdout channel cannot be
    # back-filled from the tuning input by a later writer.
    for case in TUNING_INPUT:
        assert case not in row["evaluation_plan_json"]

    # 4. Leaving the holdout verdict out is a TypeError, not an implicit pass.
    with pytest.raises(TypeError):
        controller.qualify(
            candidate["candidate_id"],
            tests_pass=True,
            negative_pass=True,
            security_pass=True,
            nrtv_pass=True,
            baseline_verified=True,
            rollback_verified=True,
        )

    # 5. A holdout failure vetoes a candidate that passed the tuning-facing tests.
    verdict = controller.qualify(
        candidate["candidate_id"],
        tests_pass=True,
        negative_pass=True,
        security_pass=True,
        holdout_pass=False,
        nrtv_pass=True,
        baseline_verified=True,
        rollback_verified=True,
    )
    assert verdict["state"] == "REJECTED"
    assert verdict["reason"] == "qualification failed"
    assert _promoted_rows(spine) == 0

    # 6. Contamination probe. A tuning input that shares an element with the frozen holdout must be
    #    refused by the controller, either as a typed EvolutionError at intake or as a
    #    HOLDOUT_CONTAMINATED state on the candidate. Silence here is a product gap, not a pass.
    contaminated_tuning = ["tuning-case-1", holdout[0]]
    detection = ""
    try:
        probe = controller.create_candidate(
            PROJECT_ID,
            "GAP-C15",
            "SkillCandidate",
            "contaminated tuning input",
            "no-op candidate",
            "detect tuning cases leaking into the holdout",
            baseline_metrics={"tuning_input": list(contaminated_tuning)},
            source_signals=list(contaminated_tuning),
        )
    except EvolutionError as refusal:
        detection = str(refusal)
    else:
        probe_verdict = controller.qualify(
            probe["candidate_id"],
            tests_pass=True,
            negative_pass=True,
            security_pass=True,
            holdout_pass=True,
            nrtv_pass=True,
            baseline_verified=True,
            rollback_verified=True,
        )
        detection = json.dumps({**probe, **probe_verdict}, ensure_ascii=False)
    assert "HOLDOUT_CONTAMINATED" in detection.upper(), (
        "the controller accepted a tuning input that shares "
        f"{holdout[0]!r} with the frozen holdout: expected a typed refusal or a "
        f"HOLDOUT_CONTAMINATED state, got {detection!r} (DOC-13#727)"
    )


def test_failed_signal_does_not_promote(tmp_path):
    """A failing signal is refused with a typed error or reported not-worthy, and never promotes.

    See the module docstring: promotion is keyed on a candidate, so the failing signal is checked at
    intake and the failed candidate at the gate. Every branch ends with zero promoted rows.
    """
    spine, controller = _controller(tmp_path)

    # A signal the module refuses outright: typed EvolutionError, and nothing reaches the tables.
    with pytest.raises(EvolutionError) as unknown_type:
        EvolutionSignal(PROJECT_ID, "R-C15", "NOT_A_GAP_TYPE", "LOW", ["ev-1"])
    assert "ERR_UNKNOWN_SIGNAL_TYPE" in str(unknown_type.value)

    with pytest.raises(EvolutionError) as bad_severity:
        EvolutionSignal(PROJECT_ID, "R-C15", "SKILL_GAP", "CRITICAL", ["ev-1"])
    assert "ERR_BAD_SEVERITY" in str(bad_severity.value)

    with spine.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM evolution_signals").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM improvement_candidates").fetchone()[0] == 0

    # A single LOW occurrence is captured but reported not candidate-worthy: no candidate is opened.
    outcome = controller.capture_signal(
        EvolutionSignal(PROJECT_ID, "R-C15", "SKILL_GAP", "LOW", ["ev-1"])
    )
    assert outcome["occurrence_count"] == 1
    assert outcome["candidate_worthy"] is False
    with spine.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM improvement_candidates").fetchone()[0] == 0
    assert _promoted_rows(spine) == 0

    # A candidate that failed qualification is refused by the gate instead of being promoted.
    candidate = controller.create_candidate(
        PROJECT_ID,
        "GAP-C15",
        "SkillCandidate",
        "signal path failed",
        "no-op candidate",
        "none",
    )
    failed = controller.qualify(
        candidate["candidate_id"],
        tests_pass=False,
        negative_pass=True,
        security_pass=True,
        holdout_pass=True,
        nrtv_pass=True,
        baseline_verified=True,
        rollback_verified=True,
    )
    assert failed["state"] == "REJECTED"

    with pytest.raises(EvolutionError) as gate_state:
        controller.promotion_gate(candidate["candidate_id"])
    assert "ERR_PROMOTION_STATE" in str(gate_state.value)

    with pytest.raises(EvolutionError) as unknown_candidate:
        controller.promotion_gate("IC-DOES-NOT-EXIST")
    assert "ERR_CANDIDATE_UNKNOWN" in str(unknown_candidate.value)

    assert _promoted_rows(spine) == 0
    assert controller.status(PROJECT_ID)["candidates_by_state"].get("PROMOTED") is None
