"""GSTACK named-method route contract (C10 narrow).

The GSTACK rule is that ``route()`` is a registry lookup, so every flow —
including an unknown one — must return a decision, and ``NATIVE`` is itself a
valid disposition rather than "no execution surface".

Implementation note (read from ``hg_kseos/named_methods.py``): the decision
dict carries the selected route under the key ``route`` (values
``NATIVE | GSTACK | OPENSPEC``), not ``selected_route``. The behaviour this
module asserts is therefore the field the router actually publishes; asserting
a ``selected_route`` key would describe a surface that does not exist.
"""

import sys
from pathlib import Path

import pytest

# The package is not installed; HG-KSEOS/src must be importable.
SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

nm = pytest.importorskip(
    "hg_kseos.named_methods",
    reason="HG-KSEOS src is not importable in this interpreter",
)

lane_policy = pytest.importorskip(
    "hg_kseos.lane_policy",
    reason="HG-KSEOS src is not importable in this interpreter",
)

ROUTE_VOCABULARY = {"NATIVE", "GSTACK", "OPENSPEC"}

CANONICAL_FLOWS = (
    "plan",
    "implementation done",
    "qa",
    "security",
    "brownfield migration",
    "release readiness",
    "retro",
    "checker adapter unknown flow",
)


def test_route_is_total_over_canonical_flows():
    """Every canonical flow yields a decision dict carrying a selected route.

    ``selected_route`` is spelled ``route`` in the implementation; asserting
    the real key keeps this total-route check meaningful instead of passing on
    an absent field. A flow with no named-method mapping still returns a
    decision (``NATIVE``), so totality holds for unmapped flows too.
    """
    snapshot = nm.registry_snapshot()

    for flow in CANONICAL_FLOWS:
        decision = nm.route(flow)
        assert isinstance(decision, dict), f"{flow!r} did not return a dict"
        assert "route" in decision, f"{flow!r} decision has no route key"
        assert decision["route"] in ROUTE_VOCABULARY, (
            f"{flow!r} routed to unknown disposition {decision['route']!r}"
        )
        # A non-native route must be a genuine registry hit, never an invention.
        if decision["route"] != "NATIVE":
            assert decision["provider"] in snapshot, (
                f"{flow!r} routed to {decision['provider']!r}, "
                "which is absent from registry_snapshot()"
            )


def test_route_is_deterministic_for_security():
    """Two consecutive security routes select the same route and provider.

    Routing is keyed off the registry with no randomness or time input, so a
    repeated call must be byte-for-byte equivalent on the decision fields.
    """
    first = nm.route("security")
    second = nm.route("security")

    assert first["route"] == second["route"]
    assert first["provider"] == second["provider"]
    assert first["state"] == second["state"]


def test_registry_is_non_empty_and_stable():
    """The active set is populated and fully backed by the registry snapshot.

    ``registry_snapshot()`` is a pure projection of ``NAMED_METHODS``, so two
    calls must agree; the active set is a subset of that projection, and the
    STANDBY entry (``spec_kit``) is deliberately excluded from it.
    """
    active = nm.ACTIVE_SELECTED
    assert isinstance(active, (set, frozenset))
    assert active, "ACTIVE_SELECTED must not be empty"

    first = nm.registry_snapshot()
    second = nm.registry_snapshot()
    assert first, "registry_snapshot() must not be empty"
    assert set(first) == set(second), "registry_snapshot() is not stable"

    missing = active - set(first)
    assert not missing, f"active named methods absent from registry: {sorted(missing)}"
    for name in active:
        assert first[name]["runtime_required_now"] is True
        assert first[name]["current_execution_scope"] != "STANDBY"

    assert "spec_kit" not in active, "STANDBY spec_kit must not be active"


def test_unknown_flow_does_not_fail_open():
    """An unmapped flow returns a decision instead of raising.

    ``state`` and ``provider`` are present but ``None`` for the native path,
    and ``final_authority`` stays ``True``: the decision is closed on the
    native HGK surface, not an open hole. Asserting presence of ``state``
    (rather than a non-null value) reflects the implementation, which only
    populates ``state`` for named-method routes.
    """
    decision = nm.route("checker adapter unknown flow")

    assert isinstance(decision, dict)
    assert decision["route"] == "NATIVE"
    assert decision["provider"] is None
    assert "state" in decision and "fallback" in decision
    assert decision["final_authority"] is True


@pytest.mark.xfail(
    strict=True,
    reason=(
        "R15_1#285 authority boundary absent from the routing surface: "
        "hg_kseos.lane_policy exposes no scope/permission resolver (see __all__), "
        "so a route decision cannot be shown to withhold an out-of-scope permission; "
        "the only typed scope refusal lives in role_binding.validate_binding"
    ),
)
def test_route_decision_is_not_authority():
    """A route decision must not, by itself, grant a permission.

    The challenge is that ``final_authority=True`` inside a decision dict is a
    value, not a permission boundary. The boundary would have to be a scope
    resolver that takes the role's declared scope plus a requested permission
    and returns a typed refusal for anything outside the declaration.

    ``lane_policy`` has no such surface. Rather than pass by asserting the flag
    it happens to carry, this test calls the resolver the boundary would need
    and fails loudly while it is absent; ``xfail(strict=True)`` keeps the gap
    visible and turns it into a failure the day the surface appears unproven.
    """
    resolver = getattr(lane_policy, "resolve_permission", None) or getattr(
        lane_policy, "resolve_scope", None
    )
    assert resolver is not None, (
        "lane_policy publishes no scope resolver: a route decision is not authority, "
        "but nothing here can refuse an out-of-scope permission"
    )

    declared = {"product-write"}
    requested = "release-promotion"
    assert requested not in declared

    try:
        outcome = resolver(declared_scope=declared, permission=requested)
    except Exception as exc:  # the refusal must be typed, so it must carry a code
        assert getattr(exc, "code", None), f"refusal without a typed code: {exc!r}"
    else:
        pytest.fail(f"an out-of-scope permission was admitted by routing: {outcome!r}")


def test_registry_route_is_deterministic_and_non_empty():
    """The active set is non-empty and every canonical flow routes identically twice.

    Determinism is asserted in bulk: both passes are collected into lists and
    compared once, so one call per flow, one assert. A per-flow test would
    report the same property eight times and hide the aggregate disagreement.
    """
    assert nm.ACTIVE_SELECTED, "ACTIVE_SELECTED must not be empty"

    first = [nm.route(flow) for flow in CANONICAL_FLOWS]
    second = [nm.route(flow) for flow in CANONICAL_FLOWS]

    assert first == second, [
        (flow, a, b) for flow, a, b in zip(CANONICAL_FLOWS, first, second) if a != b
    ]
