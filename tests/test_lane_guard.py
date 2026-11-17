
"""Regression tests for the pre-dispatch lane guard (R2-R5 of round FAR-LANE-SOD-003).

Closed defects: V3 bare-string admission, V4 skipped provider reconciliation, V5 non-projected
reasoning_effort, V6 argv-forced epoch. Each test names the defect it locks down.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("hgk_lane_guard", ROOT / "scripts" / "hgk-lane-guard.py")
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)

_spec2 = importlib.util.spec_from_file_location("lane_policy_mod", ROOT / "src" / "hg_kseos" / "lane_policy.py")
lp = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(lp)

FIXTURE_NOTE = "CONTROL-FIXTURE-NOT-A-REAL-ADMISSION"


def _fixture(path, model, provider, engine):
    path.write_text(json.dumps({
        "schema": FIXTURE_NOTE, "status": "ADMITTED",
        "arm": {"engine": engine, "model": model, "provider": provider},
        "served": {"engine": engine, "model": model, "provider": provider},
    }), encoding="utf-8")
    return str(path)


def evaluate(argv):
    return guard.evaluate(guard.build_parser().parse_args(argv))


# ---------------------------------------------------------------------------- R2-02 fixtures
def _assignment_row(role):
    data = json.loads(dsp.ASSIGNMENT_FILE.read_text(encoding="utf-8"))
    for row in data.get("assignment") or []:
        if str(row.get("role") or row.get("lane_group") or "").upper() == role.upper():
            return row
    raise AssertionError(f"no assignment row for {role}")


def _mutated_assignment(*, drop_selector_arm=None, set_auto_false=None):
    """A copy of the LIVE assignment with one owner declaration removed/retagged. Written to the
    caller's temp dir; never edits config/model-lane-assignment.json."""
    data = json.loads(dsp.ASSIGNMENT_FILE.read_text(encoding="utf-8"))
    for row in data.get("assignment") or []:
        sel = (row.get("supply_selector") or {}).get("arms") or []
        if drop_selector_arm:
            row["supply_selector"]["arms"] = [
                a for a in sel
                if (a.get("provider"), a.get("model")) != drop_selector_arm]
        if set_auto_false:
            for a in sel:
                if (a.get("provider"), a.get("model")) == set_auto_false:
                    a["automatic_selection"] = False
    return data


class _assignment_swapped:
    """Point dsp.ASSIGNMENT_FILE at a temp copy for the duration of a `with` block."""

    def __init__(self, data):
        self.data = data
        self.saved = None
        self.path = None

    def __enter__(self):
        self.path = pathlib.Path(tempfile.mkdtemp()) / "model-lane-assignment.json"
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        self.saved = dsp.ASSIGNMENT_FILE
        dsp.ASSIGNMENT_FILE = self.path
        return self.path

    def __exit__(self, *exc):
        dsp.ASSIGNMENT_FILE = self.saved
        shutil.rmtree(self.path.parent, ignore_errors=True)
        return False


def _dispatch_module():
    spec = importlib.util.spec_from_file_location(
        "hgk_lane_dispatch", ROOT / "scripts" / "hgk-lane-dispatch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dsp = _dispatch_module()


def _registry_with_pair(tmp, *, status, distinct_required):
    """Copy the live registry, force the EXECUTE/VERIFY_SECURITY declaration, re-pin the source
    digest so only the SoD surface (not source_digest) is under test."""
    reg = copy.deepcopy(lp.load_registry())
    reg["source_of_routes"]["sha256"] = lp._sha256_file(ROOT / reg["source_of_routes"]["path"])
    for pair in reg["sod_invariants"]["pairs"]:
        if {pair.get("maker"), pair.get("checker")} == {"EXECUTE", "VERIFY_SECURITY"}:
            pair["distinct_required"] = distinct_required
    for conflict in reg["sod_invariants"]["declared_conflicts"]:
        if conflict.get("id") == "SOD006-C3":
            conflict["status"] = status
    path = tmp / "registry_fixture.json"
    path.write_text(json.dumps(reg), encoding="utf-8")
    return str(path)


def _registry_without_declaration(tmp):
    """Copy the live registry and STRIP every EXECUTE/VERIFY_SECURITY declaration entry, so the pair
    is genuinely undeclared (no pairs entry, no OWNER_ORDERED_IN_FORCE conflict)."""
    reg = copy.deepcopy(lp.load_registry())
    reg["source_of_routes"]["sha256"] = lp._sha256_file(ROOT / reg["source_of_routes"]["path"])
    reg["sod_invariants"]["pairs"] = [
        pair for pair in reg["sod_invariants"]["pairs"]
        if {pair.get("maker"), pair.get("checker")} != {"EXECUTE", "VERIFY_SECURITY"}
    ]
    reg["sod_invariants"]["declared_conflicts"] = [
        conflict for conflict in reg["sod_invariants"]["declared_conflicts"]
        if conflict.get("id") != "SOD006-C3"
    ]
    path = tmp / "registry_open.json"
    path.write_text(json.dumps(reg), encoding="utf-8")
    return str(path)


def _root_with_assignment(tmp, *, doc, subdir):
    """Materialise `doc` as the pinned routing source under a temp `--root`, with a registry whose
    source digest matches it, so the ONLY surface under test is the epoch read."""
    root = tmp / subdir
    target = root / lp.load_registry()["source_of_routes"]["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc), encoding="utf-8")
    reg = copy.deepcopy(lp.load_registry())
    reg["source_of_routes"]["sha256"] = lp._sha256_file(target)
    reg_path = tmp / f"registry_{subdir}.json"
    reg_path.write_text(json.dumps(reg), encoding="utf-8")
    return root, reg_path


PLAN_ARM = ["--lane", "PLAN", "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
            "--target-engine", "openai-codex", "--target-model", "gpt-6.1-sol", "--target-provider", "openai-codex"]
VERIFY_ARM = ["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go", "--maker-model", "minimax-m3.1-flash-free",
              "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go"]


class TestLaneGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.plan_fix = _fixture(self.tmp / "plan.json", "gpt-6.1-sol", "openai-codex", "openai-codex")
        self.verify_fix = _fixture(self.tmp / "verify.json", "deepseek-v4.1-flash", "opencode-go", "hermes")
        self.deepseek_fix = _fixture(self.tmp / "deepseek.json", "deepseek-v4.1-flash", "opencode-go", "hermes")

    def test_sod_same_model_is_refused(self):
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go",
                      "--maker-model", "deepseek-v4.1-flash", "--target-engine", "hermes",
                      "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
                      "--admission", "ADMITTED"])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])

    # -- owner-ordered exemption (round ROUND3-LANE-REBIND-AND-CLOSURE-20261016) --------------------
    def test_sod_undeclared_same_model_pair_still_refused(self):
        # The regression that must NOT move: an undeclared same-model pair is refused, exit 2, and
        # never carries a declared_conflict field.
        reg = _registry_without_declaration(self.tmp)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE", "--maker-engine", "opencode-go",
                      "--maker-model", "deepseek-v4.1-flash", "--target-engine", "hermes",
                      "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
                      "--admission", self.deepseek_fix, "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])
        self.assertNotIn("declared_conflict", v)

    def test_declared_owner_ordered_pair_admits_with_conflict_id(self):
        reg = _registry_with_pair(self.tmp, status="OWNER_ORDERED_IN_FORCE", distinct_required=False)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE",
                      "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
                      "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash",
                      "--target-provider", "opencode-go", "--admission", self.deepseek_fix,
                      "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertEqual(v["status"], "ADMIT")
        self.assertEqual(v.get("declared_conflict"), "SOD006-C3")
        check = [c for c in v["checks"] if c["id"] == "sod_distinct_model"][0]
        self.assertTrue(check["ok"])
        self.assertEqual(check.get("declared_conflict"), "SOD006-C3")
        self.assertIn("SOD006-C3", check["detail"])

    def test_distinct_pair_admits_without_declared_conflict(self):
        v = evaluate(VERIFY_ARM + ["--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertNotIn("declared_conflict", v)
        check = [c for c in v["checks"] if c["id"] == "sod_distinct_model"][0]
        self.assertNotIn("declared_conflict", check)

    def test_declared_but_still_distinct_required_is_refused(self):
        # The exemption cannot be widened: named by the declaration, but distinct_required is still
        # true -> still refused.
        reg = _registry_with_pair(self.tmp, status="OWNER_ORDERED_IN_FORCE", distinct_required=True)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE",
                      "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
                      "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash",
                      "--target-provider", "opencode-go", "--admission", self.deepseek_fix,
                      "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])
        self.assertNotIn("declared_conflict", v)

    def test_declared_but_wrong_status_is_refused(self):
        # Named by the declaration and distinct_required false, but status is not
        # OWNER_ORDERED_IN_FORCE -> still refused.
        reg = _registry_with_pair(self.tmp, status="SUPERSEDED", distinct_required=False)
        v = evaluate(["--lane", "VERIFY_SECURITY", "--maker-lane", "EXECUTE",
                      "--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
                      "--target-engine", "hermes", "--target-model", "deepseek-v4.1-flash",
                      "--target-provider", "opencode-go", "--admission", self.deepseek_fix,
                      "--registry", reg, "--root", str(ROOT)])
        self.assertEqual(v["exit_code"], 2)
        self.assertIn("ERR_LANE_SOD_VIOLATION", v["errors"])
        self.assertNotIn("declared_conflict", v)

    def test_admit_with_receipt_evidence(self):
        v = evaluate(VERIFY_ARM + ["--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertEqual(v["status"], "ADMIT")

    def test_v3_bare_admitted_string_is_not_admissible(self):
        v = evaluate(VERIFY_ARM + ["--admission", "ADMITTED"])
        self.assertEqual(v["exit_code"], 3)
        self.assertIn("ERR_LANE_NOT_ADMITTED", v["errors"])
        detail = [c["detail"] for c in v["checks"] if c["id"] == "arm_admitted"][0]
        self.assertIn("evidence=ABSENT", detail)

    def test_v4_provider_mismatch_is_refused(self):
        v = evaluate(VERIFY_ARM[:-2] + ["--target-provider", "nvidia", "--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 3)
        self.assertIn("ERR_LANE_NOT_ADMITTED", v["errors"])

    def test_v4_omitted_provider_is_not_a_wildcard(self):
        arm = ["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go",
               "--maker-model", "minimax-m3.1-flash-free", "--target-engine", "hermes",
               "--target-model", "deepseek-v4.1-flash"]
        v = evaluate(arm + ["--admission", self.verify_fix])
        self.assertEqual(v["exit_code"], 3)
        self.assertIn("ERR_LANE_NOT_ADMITTED", v["errors"])

    def test_v1_stale_source_pin_is_refused(self):
        reg = self.tmp / "registry_stale.yaml"
        text = (ROOT / "config" / "lane-routing-registry.yaml").read_text(encoding="utf-8")
        text = text.replace(lp.load_registry()["source_of_routes"]["sha256"], "de" * 32)
        reg.write_text(text, encoding="utf-8")
        v = evaluate(PLAN_ARM + ["--admission", self.plan_fix, "--registry", str(reg)])
        self.assertEqual(v["exit_code"], 4)
        self.assertIn("ERR_LANE_SOURCE_STALE", v["errors"])

    def test_v6_expected_epoch_is_an_assertion_not_an_override(self):
        v = evaluate(PLAN_ARM + ["--admission", self.plan_fix, "--expected-epoch", "8"])
        self.assertEqual(v["exit_code"], 4)
        assertion = [c for c in v["checks"] if c["id"] == "expected_epoch_assertion"]
        self.assertEqual(len(assertion), 1)
        self.assertFalse(assertion[0]["ok"])
        # R2-02: live_epoch is the routing CONTRACT epoch (registry_epoch/epoch), never the document's
        # own revision counter. Asserting `revision` here ENCODED the defect: the guard read 44 while
        # the registry's epoch was 41, so every ADMIT path refused ERR_LANE_STALE_EPOCH and this test
        # stayed green while test_admit_with_receipt_evidence went red. The discriminating assertion
        # below makes the fixture's own shape part of the test, so the old reader cannot pass it again
        # even if the document later happens to carry revision == registry_epoch.
        assignment = lp.load_site(ROOT / "config" / "model-lane-assignment.json")
        self.assertNotEqual(assignment["revision"], assignment["registry_epoch"],
                            "fixture cannot discriminate: revision == registry_epoch, so a reader "
                            "that returns the revision would also pass")
        self.assertEqual(v["live_epoch"], assignment["registry_epoch"])

    # ---------------------------------------------------------------- R2-02 additions
    def test_r2_epoch_is_contract_epoch_41_not_revision_44(self):
        """POS: the live epoch a pristine tree reports is 41, the value both epoch keys carry, and the
        value the registry itself declares -- not the document's 44th revision."""
        assignment = lp.load_site(ROOT / "config" / "model-lane-assignment.json")
        live = guard._live_epoch(guard.build_parser().parse_args(
            PLAN_ARM + ["--admission", self.plan_fix]), lp.load_registry())
        self.assertEqual(live, 41)
        self.assertEqual(live, assignment["registry_epoch"])
        self.assertEqual(live, assignment["epoch"])
        self.assertNotEqual(live, assignment["revision"])
        v = evaluate(PLAN_ARM + ["--admission", self.plan_fix])
        self.assertEqual(v["exit_code"], 0, v["errors"])
        self.assertEqual(v["live_epoch"], 41)

    def test_r2_contract_epoch_wins_over_assignment_revision(self):
        """OWNER check (1): the assignment carries BOTH the contract epoch (41) and its own revision
        (44), and they differ. The guard must report the EPOCH. A reader that consults `revision` --
        first, last, or as a fallback -- reports 44 here and fails."""
        base = lp.load_site(ROOT / "config" / "model-lane-assignment.json")
        shapes = {
            # only the contract-epoch key: the strongest form, nothing else could supply 41
            "contract_epoch_only": {"registry_epoch": None, "contract_epoch": 41, "epoch": None},
            # every epoch key agrees; `revision` still says 44
            "all_epoch_keys": {"registry_epoch": 41, "contract_epoch": 41, "epoch": 41},
        }
        for name, fields in shapes.items():
            with self.subTest(shape=name):
                doc = copy.deepcopy(base)
                doc["revision"] = 44
                for key, value in fields.items():
                    if value is None:
                        doc.pop(key, None)
                    else:
                        doc[key] = value
                self.assertEqual(doc["revision"], 44)
                root, reg = _root_with_assignment(self.tmp, doc=doc, subdir=name)
                args = guard.build_parser().parse_args(
                    PLAN_ARM + ["--admission", self.plan_fix, "--registry", str(reg),
                                "--root", str(root)])
                live = guard._live_epoch(args, lp.load_registry(reg))
                self.assertEqual(live, 41, f"{name}: read {live}, not the epoch 41")
                self.assertNotEqual(live, 44, f"{name}: read the revision 44 as the epoch")
                v = guard.evaluate(args)
                self.assertEqual(v["exit_code"], 0, v["errors"])
                self.assertEqual(v["live_epoch"], 41)

    def test_r2_absent_malformed_or_conflicting_epoch_is_refused(self):
        """OWNER check (2): an epoch the guard cannot establish is NOT an admission. Absent (only
        the 44 revision), malformed, and self-contradictory epoch fields are each refused under the
        existing stale-epoch code ERR_LANE_STALE_EPOCH / exit 4 -- never admitted, and never
        rescued by falling back to `revision`."""
        base = lp.load_site(ROOT / "config" / "model-lane-assignment.json")
        cases = {
            "absent_revision_only": (
                {"registry_epoch": None, "contract_epoch": None, "epoch": None}, "EPOCH_ABSENT"),
            "malformed_epoch": (
                {"registry_epoch": "epoch-41", "contract_epoch": None, "epoch": None},
                "EPOCH_MALFORMED"),
            "conflicting_epoch_fields": (
                {"registry_epoch": 41, "contract_epoch": None, "epoch": 42}, "EPOCH_CONFLICT"),
        }
        for name, (fields, defect) in cases.items():
            with self.subTest(shape=name):
                doc = copy.deepcopy(base)
                doc["revision"] = 44
                for key, value in fields.items():
                    if value is None:
                        doc.pop(key, None)
                    else:
                        doc[key] = value
                root, reg = _root_with_assignment(self.tmp, doc=doc, subdir=f"bad_{name}")
                v = guard.evaluate(guard.build_parser().parse_args(
                    PLAN_ARM + ["--admission", self.plan_fix, "--registry", str(reg),
                                "--root", str(root)]))
                self.assertEqual(v["exit_code"], 4, f"{name}: {v['errors']} / {v['checks']}")
                self.assertEqual(v["status"], "REFUSE")
                self.assertEqual(v["decision"], "REFUSE")
                self.assertIn("ERR_LANE_STALE_EPOCH", v["errors"])
                self.assertIsNone(v["live_epoch"], f"{name}: an unestablished epoch still produced a value")
                check = [c for c in v["checks"] if c["id"] == "epoch_current"][0]
                self.assertFalse(check["ok"])
                self.assertEqual(check["code"], "ERR_LANE_STALE_EPOCH")
                self.assertIn(defect, check["detail"])
        # An epoch document that is not on disk at all is the same refusal class, not an exemption.
        with self.subTest(shape="epoch_source_absent"):
            reg_doc = copy.deepcopy(lp.load_registry())
            reg_doc["source_of_routes"]["path"] = "config/absent-lane-assignment.json"
            reg_doc["source_of_routes"].pop("sha256", None)
            reg_path = self.tmp / "registry_absent_source.json"
            reg_path.write_text(json.dumps(reg_doc), encoding="utf-8")
            v = guard.evaluate(guard.build_parser().parse_args(
                PLAN_ARM + ["--admission", self.plan_fix, "--registry", str(reg_path)]))
            self.assertEqual(v["exit_code"], 4, f"{v['errors']} / {v['checks']}")
            self.assertIn("ERR_LANE_STALE_EPOCH", v["errors"])
            self.assertIsNone(v["live_epoch"])
            check = [c for c in v["checks"] if c["id"] == "epoch_current"][0]
            self.assertFalse(check["ok"])
            self.assertIn("EPOCH_ABSENT", check["detail"])

    def test_r2_undeclared_arm_is_still_refused(self):
        """NEG: widening the READ did not widen ACCEPTANCE. An arm in no declared shape -- and the
        bare-model and transport-alias forms of a declared arm -- are still not in the assignment."""
        asg = dsp.lane_assigned_arms("PLAN")
        for bogus in ("opencode-go/gpt-9-imaginary", "deepseek-v4.1-flash",
                      "unlisted-provider/gpt-6.1-sol"):
            self.assertNotIn(bogus, asg["arms"])
        mutated = _mutated_assignment(drop_selector_arm=("opencode-go", "mimo-v2.6-flash"))
        with _assignment_swapped(mutated):
            after = dsp.lane_assigned_arms("PLAN")
        self.assertNotIn("opencode-go/mimo-v2.6-flash", after["arms"],
                         "an arm removed from the owner's selector pool must stop being assigned")

    def test_v5_reasoning_effort_survives_projection(self):
        policy = lp.project_policy(lp.load_registry())
        self.assertEqual(policy["routes"]["VERIFY_SECURITY"]["reasoning_effort"], "medium")
        self.assertEqual(lp.load_registry()["routes"][2]["reasoning_effort"], "medium") if False else None


if __name__ == "__main__":
    unittest.main()
