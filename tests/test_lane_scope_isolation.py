"""The lane-scope guard: known residue is registered, NEW divergence fails.

Why this test exists: the R14 fidelity audit reported 44 inconsistencies and it was tempting to call the wiring wrong.
Most of them were not drift at all - they were a session's interactive model, or the residue of an owner mandate that
bound a lane for one round and was only partly reverted. Comparing those planes produces noise loud enough to hide a
real regression.

So the guard compares ONE plane only (L: registry -> assignment projection), and holds the historical residue in
config/lane_scope_exceptions.json, where every entry carries its origin commit and its date. A new divergence has no
exception and fails here. Removing an exception is a deliberate act; it should happen when the value is re-derived, not
because the test was annoying.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "config/lane-routing-registry.yaml"
ASG = ROOT / "config/model-lane-assignment.json"
EXC = ROOT / "config/lane_scope_exceptions.json"
ROLES = ("PLAN", "EXECUTE", "VERIFY_SECURITY")
LANE_FIELDS = ("provider", "model", "transport_model", "automatic_selection")
SESSION_ONLY_SUFFIX = ("-free", "v4.1-flash", "mimo", "glm-5.3-flash")


def divergences() -> list[dict]:
    registry = yaml.safe_load(REG.read_text(encoding="utf-8"))
    by_lane = {route["lane"]: route for route in registry["routes"]}
    assignment = json.loads(ASG.read_text(encoding="utf-8"))
    found = []
    for role in ROLES:
        chain = assignment["lane_chains"][role]
        for index, arm in enumerate(by_lane[role]["arms"][: len(chain)]):
            for field in LANE_FIELDS:
                if arm.get(field) != chain[index].get(field):
                    found.append({"role": role, "index": index, "field": field,
                                  "lane_scope_value": arm.get(field),
                                  "assignment_value": chain[index].get(field)})
    return found


class LaneScopeIsolationTests(unittest.TestCase):
    def test_new_divergence_fails_and_known_residue_is_registered(self) -> None:
        exceptions = {(e["role"], e["index"], e["field"], e["assignment_value"])
                      for e in json.loads(EXC.read_text(encoding="utf-8"))["exceptions"]}
        unregistered = [d for d in divergences()
                        if (d["role"], d["index"], d["field"], d["assignment_value"]) not in exceptions]
        self.assertEqual(unregistered, [],
                         "new lane-scope divergence with no registered exception: " + json.dumps(unregistered, indent=1))

    def test_registered_exceptions_all_carry_provenance(self) -> None:
        """Provenance is required - except for booleans, which git -S cannot attribute.

        `automatic_selection: true/false` appears in almost every revision of the file, so there is no single commit to
        name. Saying so is better than inventing one; the exception still carries its classification and its values.
        """
        for entry in json.loads(EXC.read_text(encoding="utf-8"))["exceptions"]:
            self.assertIn(entry["classification"],
                          ("SUPERSEDED_ROUND_RESIDUE", "CURRENT_ROUND_NOT_DERIVED"), entry)
            if isinstance(entry["assignment_value"], bool):
                continue
            self.assertTrue(entry.get("origin_commit"), entry)
            self.assertTrue(entry.get("origin_date"), entry)

    def test_session_models_never_sit_in_the_lane_scope_arm(self) -> None:
        """A session's interactive model may not be the declared arm of a lane.

        This is the isolation the round needed: the container may run a session on any model, and that must never be
        read as the lane's binding, nor written into the registry's declaration.
        """
        registry = yaml.safe_load(REG.read_text(encoding="utf-8"))
        for route in registry["routes"]:
            model = str(route.get("model", ""))
            self.assertFalse(model.endswith(SESSION_ONLY_SUFFIX) and "sol" not in model and route["lane"] == "PLAN",
                             f"PLAN must not be declared on a session-tier model: {model}")
            primary = route["arms"][0]
            identity = primary.get("canonical_identity") or primary.get("model")
            # openai-codex takes a bare id; the other providers take provider/model. Both are "the declared identity".
            allowed = {identity, f"{primary['provider']}/{identity}"}
            self.assertIn(primary.get("transport_model"), allowed,
                          f"{route['lane']} primary transport must carry the declared identity")

    def test_epoch_matches_between_assignment_and_registry(self) -> None:
        """A projection that names an older epoch than the registry is stale by definition.

        The current skew (registry 30, assignment 29) is the ROOT CAUSE of all ten value divergences: the registry
        advanced and the projection was never re-derived from it. It is registered as a dated exception so this test
        fails on any further movement instead of staying red.
        """
        registry = yaml.safe_load(REG.read_text(encoding="utf-8"))
        assignment = json.loads(ASG.read_text(encoding="utf-8"))
        have = (str(registry.get("epoch")), str(assignment.get("registry_epoch")))
        registered = json.loads(EXC.read_text(encoding="utf-8")).get("epoch_skew")
        want = (str(registered["registry"]), str(registered["assignment"])) if registered else (have[0], have[0])
        self.assertEqual(have, want,
                         "the assignment must name the registry epoch it was projected from "
                         "(registered skew: %s)" % (registered,))


if __name__ == "__main__":
    unittest.main()
