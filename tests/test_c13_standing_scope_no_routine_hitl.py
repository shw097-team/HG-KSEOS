"""C13: FAR standing scope needs no routine HITL and cannot widen itself.

What the product actually guarantees, read from the code before writing these tests:

* ``lane_policy`` resolves a lane to a *route* (provider/model/engine/auth/arms), not to an ACL. There is
  no permission-set type anywhere in the package, so "permission set" below means the exact set of
  route facts a role resolves to, plus the declared write scope carried by a ``role_binding`` document.
  Both are pure data returns: neither module prompts, reads a terminal, or carries an
  ``AWAITING_APPROVAL``-style state. That absence is the "no routine HITL" property, and it is asserted
  by making every interactive channel raise if touched rather than by grepping for keywords.
* ``lane_policy`` has no scope-refusal surface at all. The typed refusal for "outside the declared
  scope" lives in ``role_binding.validate_binding`` and is ``ERR_ROLE_BINDING_SCOPE_MISMATCH``. It fires
  only when a lane is bound -- i.e. on the governed dispatch path -- because the scope list is a
  per-role fact, not a global ACL. These tests exercise the governed path, which is the one C13 is
  about; they do not pretend lane-less validation performs a scope check it does not perform.
* ``project_policy`` publishes exactly thirteen fields per lane and deliberately drops the registry's
  descriptive ``lanes``/``role_group`` keys. The finite-scope test pins the published field set so a
  new field cannot appear in the projection without this test moving with it.
"""

from __future__ import annotations

import copy
import inspect
import importlib
import pkgutil
import sys
import types
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

lane_policy = pytest.importorskip(
    "hg_kseos.lane_policy",
    reason="HG-KSEOS src is not importable in this interpreter",
)
role_binding = pytest.importorskip(
    "hg_kseos.role_binding",
    reason="HG-KSEOS src is not importable in this interpreter",
)

LANES = ("PLAN", "EXECUTE", "VERIFY_SECURITY")

# The exact fields _compact_route publishes. A projection that grows or loses a field changes what a
# role is allowed to resolve to, so the set is pinned rather than merely sampled.
PUBLISHED_ROUTE_FIELDS = frozenset({
    "lane",
    "engine",
    "provider",
    "model",
    "canonical_identity",
    "auth",
    "oauth",
    "fallbacks",
    "admission_status",
    "reasoning_effort",
    "arms",
    "selection_authority",
    "selected_arm",
})

# States that would mean a routine resolution had been parked for a human. None of them may appear.
BLOCKING_STATES = frozenset({
    "AWAITING_APPROVAL",
    "AWAITING_HUMAN",
    "PENDING_APPROVAL",
    "PENDING_HUMAN",
    "BLOCKED_HITL",
    "REQUIRES_APPROVAL",
})


def _forbid_interactive(monkeypatch) -> None:
    """Make every interactive channel raise, so "resolved without asking" is proven, not assumed."""

    def _refuse(*args, **kwargs):
        raise AssertionError("resolution attempted to prompt for human input")

    monkeypatch.setattr("builtins.input", _refuse)
    monkeypatch.setattr(
        "sys.stdin",
        types.SimpleNamespace(read=lambda *a, **k: _refuse(), readline=lambda *a, **k: _refuse()),
    )
    getpass = pytest.importorskip("getpass")
    monkeypatch.setattr(getpass, "getpass", _refuse)


def _binding(scope: list[str]) -> dict:
    """A well-formed HGK-ROLE-BINDING/1 document whose three roles are all declared."""
    return {
        "schema": role_binding.ROLE_BINDING_SCHEMA,
        "round": "round-20261022-r15_2",
        "session": "session-c13",
        "workorder": "WO-C13",
        "base_head": "0" * 40,
        "subject": "C13",
        "expiry": "2099-01-01T00:00:00+00:00",
        "mandate_digest": "sha256:" + "a" * 64,
        "scope": list(scope),
        "roles": {
            lane: {
                "provider": "opencode-go",
                "model": "deepseek-v4.1-flash",
                "surface": "codex-cli",
                "rank": 0,
            }
            for lane in LANES
        },
    }


def _arm_tokens(route: dict) -> frozenset:
    """Order-insensitive identity of a route's arms."""
    return frozenset((arm.get("provider"), arm.get("model")) for arm in route.get("arms", []))


def _fallback_tokens(route: dict) -> frozenset:
    """Order-insensitive identity of a route's fallbacks."""
    return frozenset((fb.get("provider"), fb.get("model")) for fb in route.get("fallbacks", []))


def _permission_facts(route: dict) -> dict:
    """The permission-relevant facts of one projected route, copied into plain hashables.

    Every value is rebuilt from the caller-visible container, so comparing two of these compares
    *values* only. That matters: the point of the aliasing test below is to catch two projections
    that share mutable state, and a snapshot that held a live reference would mutate alongside the
    object it is supposed to police.
    """
    return {
        "provider": route.get("provider"),
        "model": route.get("model"),
        "canonical_identity": route.get("canonical_identity"),
        "arms": _arm_tokens(route),
        "fallbacks": _fallback_tokens(route),
        "arm_count": len(route.get("arms", [])),
        "fallback_count": len(route.get("fallbacks", [])),
    }


PER_EFFECT_CHECK_CITATION = (
    "SBL_HGK_FABRIC_PIPD_LS_PKG_R15_1_FULL_SUBSTANTIVE_INTEGRATED_REPAIR_REPLACEMENT_2026-10-22.md#1400"
)

# The nine facts a per-effect Native admission check has to bind at the moment of the effect. A
# check that omits any one of them admits an effect it cannot actually justify: an unbound subject,
# an unbound repository/path, an unbound action class or risk, a stale ticket, a replayed nonce, a
# missing lease, or a policy epoch the caller has since superseded.
PER_EFFECT_ADMISSION_FACTS = frozenset({
    "subject_hash",
    "repository",
    "path",
    "action_class",
    "risk",
    "expiry",
    "token_nonce",
    "lease",
    "current_policy",
})


def _package_modules():
    """Yield every importable ``hg_kseos`` submodule, tolerating optional-dependency failures."""
    package = pytest.importorskip(
        "hg_kseos", reason="HG-KSEOS src is not importable in this interpreter"
    )
    for module_info in pkgutil.iter_modules(package.__path__):
        if module_info.name.startswith("__"):
            continue
        try:
            yield importlib.import_module(f"hg_kseos.{module_info.name}")
        except Exception:  # a module that needs an absent optional dependency
            continue


def _per_effect_checkers() -> list[str]:
    """Names of callables that bind all nine per-effect admission facts in one signature."""
    found: list[str] = []
    for module in _package_modules():
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if getattr(func, "__module__", None) != module.__name__:
                continue  # re-exported, not defined here
            try:
                params = set(inspect.signature(func).parameters)
            except (TypeError, ValueError):
                continue
            if PER_EFFECT_ADMISSION_FACTS <= params:
                found.append(f"{module.__name__}.{name}")
    return found


@pytest.mark.xfail(
    strict=True,
    reason=(
        f"{PER_EFFECT_CHECK_CITATION} requires a per-effect Native admission check binding subject "
        "hash, repository, path, action class, risk, expiry, token nonce, lease and current policy; "
        "HG-KSEOS exposes no such callable today, so this gap stays visible"
    ),
)
def test_per_effect_native_admission_check_binds_every_fact():
    """A per-effect admission check must bind all nine facts and refuse any that disagree.

    Measured on the current source, this test fails as expected: lane admission
    (``lane_admission.decide_status``) is a per-ARM probe that decides whether a model lane answered,
    and ``role_binding.validate_binding`` is per-ROLE (lane, scope, digest, expiry). Neither is
    per-EFFECT: nothing today takes the concrete action being performed -- repository, path, action
    class, risk, token nonce and a live lease -- and refuses it. The nine-fact binding is therefore
    absent, and ``_compact_route``'s aliased fallbacks (see the aliasing test above) are a second,
    independent reason a caller's effect is not tightly bound to the policy it was admitted under.

    Written ``xfail(strict=True)`` on purpose. If the product grows the check, this test starts
    passing, strict xfail turns that into a failure, and whoever adds the surface is told to
    convert this into a real assertion instead of leaving a silent xpass behind.
    """
    checkers = _per_effect_checkers()
    assert checkers, (
        "no callable binds all nine per-effect admission facts "
        f"({sorted(PER_EFFECT_ADMISSION_FACTS)}); citation {PER_EFFECT_CHECK_CITATION}"
    )

    # Only reached once such a check exists: prove it refuses facts that do not line up.
    module_name, _, func_name = checkers[0].partition(".")
    module = importlib.import_module(module_name)
    check = getattr(module, func_name)
    signature = inspect.signature(check)
    aligned = {
        "subject_hash": "sha256:" + "b" * 64,
        "repository": "HG-KSEOS",
        "path": "src/hg_kseos/lane_policy.py",
        "action_class": "write",
        "risk": "LOW",
        "expiry": "2099-01-01T00:00:00+00:00",
        "token_nonce": "nonce-c13-per-effect",
        "lease": "lease-c13-per-effect",
        "current_policy": "epoch:33",
    }
    kwargs = {key: value for key, value in aligned.items() if key in signature.parameters}

    refusal = pytest.raises(Exception)
    for drift in (
        {"action_class": "delete"},
        {"path": "src/hg_kseos/spine.py"},
        {"risk": "CONSTITUTIONAL"},
        {"expiry": "2000-01-01T00:00:00+00:00"},
        {"token_nonce": "nonce-already-spent"},
        {"lease": ""},
        {"current_policy": "epoch:00"},
        {"subject_hash": "sha256:" + "0" * 64},
        {"repository": "other-repo"},
    ):
        moved = dict(kwargs, **drift)
        with refusal:
            check(**moved)


def test_declared_roles_resolve_without_routine_hitl(monkeypatch):
    """PLAN, EXECUTE and VERIFY_SECURITY each resolve to a full route without asking anyone.

    Two surfaces are resolved, both on the routine path: the policy route for each lane and the bound
    arm for each declared role. Every interactive channel is trapped, so a resolver that reached for
    stdin, or a credential helper that prompted, would fail here instead of quietly succeeding.
    VERIFY_SECURITY resolves with ``admission_status`` of ``UNPROVEN`` in the live registry. That is a
    measured-admission fact, not an approval gate: the route still resolves, and no blocking state is
    raised anywhere in the result.
    """
    _forbid_interactive(monkeypatch)

    registry = lane_policy.load_registry()
    policy = lane_policy.project_policy(registry)
    binding = _binding(["src/hg_kseos/lane_policy.py"])

    for lane in LANES:
        route = policy["routes"][lane]
        assert route["lane"] == lane
        assert route["provider"], f"{lane} resolved without a provider"
        assert route["model"], f"{lane} resolved without a model"
        assert route["arms"], f"{lane} resolved without any declared arm"
        assert route["admission_status"] not in BLOCKING_STATES

        arm = role_binding.resolve_arm(binding, lane)
        assert arm["provider"] == "opencode-go"
        assert arm["model"] == "deepseek-v4.1-flash"
        assert arm["surface"] == "codex-cli"
        assert arm["arm"] == "opencode-go/deepseek-v4.1-flash"
        for value in arm.values():
            assert value not in BLOCKING_STATES, f"{lane} arm carries blocking state {value!r}"

        # The governed validation path also returns, rather than deferring to a human.
        result = role_binding.validate_binding(binding, lane=lane)
        assert result["binding_digest"], f"{lane} validation produced no digest"


def test_scope_cannot_be_widened_by_the_caller():
    """A permission outside the declared scope is refused with a typed error, never granted.

    The refusal is ``BindingError`` (a subclass of ``InvariantViolation``) carrying
    ``ERR_ROLE_BINDING_SCOPE_MISMATCH``. It is checked on the governed path -- a lane must be bound --
    because the declared scope belongs to the role being resolved. An undeclared role name is likewise
    refused rather than defaulting to the union of every role's scope.
    """
    declared = ["src/hg_kseos/lane_policy.py"]
    binding = _binding(declared)

    for widening in (
        ["src/hg_kseos/lane_policy.py", "src/hg_kseos/spine.py"],
        ["src/hg_kseos/lane_policy.py", "/etc/passwd"],
        ["src/scripts/hgk-lane-dispatch.py"],
    ):
        with pytest.raises(role_binding.BindingError) as caught:
            role_binding.validate_binding(binding, lane="EXECUTE", scope=widening)
        assert isinstance(caught.value, role_binding.InvariantViolation)
        assert caught.value.code == "ERR_ROLE_BINDING_SCOPE_MISMATCH"
        assert "outside declared scope" in str(caught.value.detail)

    # A bare string is treated as a one-element request, so it cannot smuggle a wider grant either.
    with pytest.raises(role_binding.BindingError) as caught:
        role_binding.validate_binding(binding, lane="PLAN", scope="src/hg_kseos/spine.py")
    assert caught.value.code == "ERR_ROLE_BINDING_SCOPE_MISMATCH"

    # An undeclared role is refused; there is no implicit catch-all scope to widen into.
    with pytest.raises(role_binding.BindingError) as caught:
        role_binding.resolve_arm(binding, "ADMIN")
    assert caught.value.code == "ERR_ROLE_BINDING_LANE_UNDECLARED"

    # The same request that stays inside the declaration resolves.
    inside = role_binding.validate_binding(binding, lane="EXECUTE", scope=declared)
    assert inside["binding_digest"]


def test_declared_scope_is_finite_and_equals_the_policy_file():
    """Each role's projected scope equals what the registry declares, and nothing more.

    The projection republishes exactly the arms and fallbacks the policy file declares, publishes
    exactly ``PUBLISHED_ROUTE_FIELDS`` per lane, and answers ``None`` for a lane the file does not
    declare while the invariants keep ``unknown_lane: DENY`` and ``global_overrides_permitted: False``.
    The registry's descriptive ``lanes``/``role_group`` keys are intentionally not projected; that is
    a narrowing, so it cannot be read as extra authority.
    """
    registry = lane_policy.load_registry()
    policy = lane_policy.project_policy(registry)
    declared = {route["lane"]: route for route in registry["routes"]}

    assert set(policy["routes"]) == set(LANES)
    for lane in LANES:
        projected = policy["routes"][lane]
        source = declared[lane]

        assert set(projected) == PUBLISHED_ROUTE_FIELDS, (
            f"{lane} projection publishes {sorted(set(projected) ^ PUBLISHED_ROUTE_FIELDS)} "
            "outside the pinned field set"
        )
        assert _arm_tokens(projected) == _arm_tokens(source), (
            f"{lane} projected arms differ from the policy file"
        )
        assert projected["fallbacks"] == source["fallbacks"]
        assert projected["provider"] == source["provider"]
        assert projected["model"] == source["model"]

        # Descriptive-only registry keys are dropped, never reinterpreted as permissions.
        assert "lanes" not in projected
        assert "role_group" not in projected

    assert policy["invariants"]["unknown_lane"] == "DENY"
    assert policy["invariants"]["global_overrides_permitted"] is False
    assert lane_policy.route_for_lane(registry, "ADMIN") is None
    assert "ADMIN" not in policy["routes"]


def test_standing_scope_is_stable_across_repeated_resolution():
    """Mutating one projection must not touch a second one or the next resolve.

    This test deliberately takes two INDEPENDENT projections, ``a`` and ``b``, with no ``deepcopy``
    anywhere, then mutates ``a`` in place. The earlier version of this test deep-copied the
    projection before mutating it, which meant an implementation that returned aliases into its own
    registry still passed -- the copy absorbed the mutation. That was not a test of the
    defensive-copy boundary at all.

    FINDING (recorded here rather than reverted, per the repair brief): ``_compact_route`` deep-copies
    ``arms`` but builds ``fallbacks`` with ``list(route.get("fallbacks", []))``. A list copy is
    shallow, so every projected route's fallback entries ARE the registry's own dict objects. Editing
    one fallback dict through a projection therefore rewrites the in-memory registry, and every later
    ``project_policy`` call republishes the attacker's fallback. ``arms`` are safe; ``fallbacks`` are
    not. This test fails on the current source for exactly that reason, and must stay failing until
    the projection deep-copies its fallback entries.
    """
    registry = lane_policy.load_registry()

    # Two independent resolutions of the same role. `b` is the expected value; nothing is copied
    # from it into the mutation target, and nothing about `a` is pre-frozen.
    a = lane_policy.project_policy(registry)
    b = lane_policy.project_policy(registry)
    snapshot = {lane: _permission_facts(b["routes"][lane]) for lane in LANES}
    assert {lane: _permission_facts(a["routes"][lane]) for lane in LANES} == snapshot

    # Mutate `a` destructively: rewrite the route's own facts, rewrite every element dict it hands
    # out, then clear and re-seed both permission containers.
    for lane in LANES:
        route = a["routes"][lane]
        route["provider"] = "attacker-provider"
        route["model"] = "attacker-model"
        route["canonical_identity"] = "attacker-model"
        for arm in route["arms"]:
            arm["provider"] = "attacker-provider"
            arm["model"] = "attacker-model"
        for fallback in route["fallbacks"]:
            fallback["provider"] = "attacker-provider"
            fallback["model"] = "attacker-model"
        route["arms"].clear()
        route["arms"].append({"provider": "attacker-provider", "model": "attacker-model"})
        route["fallbacks"].clear()
        route["fallbacks"].append({"provider": "attacker-provider", "model": "attacker-model"})

    # `b` was resolved before the mutation and must be untouched by it.
    for lane in LANES:
        assert _permission_facts(b["routes"][lane]) == snapshot[lane], (
            f"{lane}: mutating one projection rewrote an independently resolved projection, so the "
            "projection hands out aliases instead of copies"
        )

    # A third, freshly resolved projection must also still match the snapshot.
    fresh = lane_policy.project_policy(registry)
    for lane in LANES:
        assert _permission_facts(fresh["routes"][lane]) == snapshot[lane], (
            f"{lane}: a caller's edit to a returned projection changed what a later resolve "
            f"publishes (got {_permission_facts(fresh['routes'][lane])!r}); the projection is not a copy"
        )

    # Repeated governed resolution of the same role is stable too.
    binding = _binding(["src/hg_kseos/lane_policy.py"])
    for lane in LANES:
        one = role_binding.resolve_arm(binding, lane)
        two = role_binding.resolve_arm(binding, lane)
        assert one == two, f"{lane} arm resolution is not stable"

    # A caller who edits the resolved document holds a projection, not authority: the widened copy no
    # longer matches the persisted binding's digest and is refused as a foreign projection.
    grew = copy.deepcopy(binding)
    grew["scope"].append("src/hg_kseos/spine.py")
    with pytest.raises(role_binding.BindingError) as caught:
        role_binding.require_projection_matches(binding, grew)
    assert caught.value.code == "ERR_ROLE_BINDING_PROJECTION_MISMATCH"

    # The unmodified document is the projection and passes.
    assert role_binding.require_projection_matches(binding, copy.deepcopy(binding))

    # Repeated governed resolution of the same role is stable too.
    binding = _binding(["src/hg_kseos/lane_policy.py"])
    for lane in LANES:
        one = role_binding.resolve_arm(binding, lane)
        two = role_binding.resolve_arm(binding, lane)
        assert one == two, f"{lane} arm resolution is not stable"

    # A caller who edits the resolved document holds a projection, not authority: the widened copy no
    # longer matches the persisted binding's digest and is refused as a foreign projection.
    grew = copy.deepcopy(binding)
    grew["scope"].append("src/hg_kseos/spine.py")
    with pytest.raises(role_binding.BindingError) as caught:
        role_binding.require_projection_matches(binding, grew)
    assert caught.value.code == "ERR_ROLE_BINDING_PROJECTION_MISMATCH"

    # The unmodified document is the projection and passes.
    assert role_binding.require_projection_matches(binding, copy.deepcopy(binding))
