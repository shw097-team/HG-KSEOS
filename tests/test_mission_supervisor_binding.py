"""Supervisor-bound mission/profile selection (WP06 r2).

What is being locked here is the difference between CONFIG and a WORKER'S ENVIRONMENT:

  * an unbound host keeps B1 exactly as it was - no selector means the ProgramData constant;
  * a bound host obeys the record, so an absent variable is not a fallback to B1;
  * a worker may not reselect, blank, re-scope or downgrade what the supervisor fixed.

Label: the tests that need a writable base run under %TEMP% and therefore patch the OS ACL gate.
Those runs are STAND_IN_NOT_ORIGINAL_DOMAIN - they prove the SELECTION logic and say nothing about
whether Windows protection holds. The two tests that exercise the real gate are named with
`original_domain` and do not patch anything.
"""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hg_kseos import native_admission as n
from hg_kseos.errors import InvariantViolation

STAND_IN_NOT_ORIGINAL_DOMAIN = True   # this module's patched runs are not original-domain evidence
MISSION, OTHER = 'MISSION-A', 'MISSION-B'


class SupervisorBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name) / 'native-admission'
        self.base.mkdir()
        self.constant = self.base / 'registry.json'
        self._registry, self._protect = n.REGISTRY, n.assert_protected
        n.REGISTRY = self.constant
        n.assert_protected = lambda path: None          # STAND_IN_NOT_ORIGINAL_DOMAIN
        for key in (n.MISSION_SELECTOR_ENV, n.TRUST_PROFILE_ENV):
            os.environ.pop(key, None)

    def tearDown(self):
        n.REGISTRY, n.assert_protected = self._registry, self._protect
        for key in (n.MISSION_SELECTOR_ENV, n.TRUST_PROFILE_ENV):
            os.environ.pop(key, None)
        self.temp.cleanup()

    def bind(self, mission: str | None = MISSION, profile=n.MACHINE_PROFILE):
        return n.bind_supervisor_scope(mission, profile)

    def refused(self, code, call):
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_' + code + '$'):
            call()

    # -- B1 legacy is untouched -----------------------------------------------------------------
    def test_unbound_host_resolves_the_constant_and_no_selector(self):
        self.assertIsNone(n.mission_selector())
        self.assertEqual(n.registry_path(), self.constant)
        self.assertEqual(n.trust_profile(), n.MACHINE_PROFILE)

    def test_unbound_host_still_honours_an_explicit_env_selector(self):
        # The pre-binding behaviour is kept on purpose: a host that never installed a supervisor
        # record is exactly today's B1/deployment behaviour, env selection included.
        os.environ[n.MISSION_SELECTOR_ENV] = MISSION
        self.assertEqual(n.mission_selector(), MISSION)
        self.assertEqual(n.registry_path(), self.base / 'missions' / MISSION / 'registry.json')

    def test_unbound_host_still_accepts_the_user_profile(self):
        os.environ[n.TRUST_PROFILE_ENV] = n.USER_PROFILE
        self.assertEqual(n.trust_profile(), n.USER_PROFILE)

    def test_unbound_host_still_refuses_an_unknown_profile(self):
        os.environ[n.TRUST_PROFILE_ENV] = 'administrator'
        self.refused('TRUST_PROFILE', n.trust_profile)

    # -- the record is the authority -------------------------------------------------------------
    def test_binding_pins_the_mission_when_the_environment_is_silent(self):
        self.bind(MISSION)
        os.environ.pop(n.MISSION_SELECTOR_ENV, None)
        self.assertEqual(n.mission_selector(), MISSION)   # not None, though nothing is exported
        self.assertEqual(n.registry_path(), self.base / 'missions' / MISSION / 'registry.json')

    def test_binding_may_pin_the_unscoped_constant_explicitly(self):
        self.bind(None)
        self.assertIsNone(n.mission_selector())
        self.assertEqual(n.registry_path(), self.constant)

    def test_binding_is_immutable(self):
        self.bind(MISSION)
        self.refused('SUPERVISOR_BINDING_IMMUTABLE', lambda: self.bind(OTHER))
        self.assertEqual(self.bind(MISSION)['mission_id'], MISSION)   # same value is idempotent

    def test_binding_refuses_a_path_shaped_mission(self):
        self.refused('MISSION_SELECTOR_SHAPE', lambda: self.bind('../escape'))

    # -- refusal 1: worker reselection ------------------------------------------------------------
    def test_worker_reselection_before_construction_is_refused(self):
        self.bind(MISSION)
        os.environ[n.MISSION_SELECTOR_ENV] = OTHER
        self.refused('MISSION_SELECTOR_WORKER_RESELECT', n.mission_selector)

    def test_worker_reselection_after_construction_is_refused(self):
        self.bind(MISSION)
        os.environ[n.MISSION_SELECTOR_ENV] = MISSION
        receiver = n.ProtectedRegistry()
        self.assertEqual(receiver.mission, MISSION)
        os.environ[n.MISSION_SELECTOR_ENV] = OTHER        # the pin makes this harmless...
        with self.assertRaisesRegex(InvariantViolation,
                                    '^ERR_NATIVE_MISSION_SELECTOR_WORKER_RESELECT$'):
            receiver._registry_path()                     # ...and this makes it visible

    def test_rewriting_the_binding_record_after_construction_is_refused(self):
        self.bind(MISSION)
        receiver = n.ProtectedRegistry()
        binding = n._binding_path()
        document = json.loads(binding.read_text(encoding='utf-8'))
        document['mission_id'] = OTHER
        binding.write_text(json.dumps(document), encoding='utf-8')
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_SUPERVISOR_BINDING_CHANGED$'):
            receiver._registry_path()

    # -- refusal 2: blank is not a fallback to B1 ------------------------------------------------
    def test_blank_selector_on_a_bound_host_is_refused_not_defaulted(self):
        self.bind(MISSION)
        os.environ[n.MISSION_SELECTOR_ENV] = ''           # e.g. cmd "set HGK_MISSION_ID="
        self.refused('MISSION_SELECTOR_BLANK', n.mission_selector)

    def test_blank_selector_does_not_fall_back_to_the_unscoped_file(self):
        # The constant holds a perfectly valid registry for ANOTHER mission: reading it would be a
        # silent downgrade, so the blank value has to be a refusal rather than a path.
        self.constant.write_text(json.dumps({'mission_id': OTHER}), encoding='utf-8')
        self.bind(MISSION)
        os.environ[n.MISSION_SELECTOR_ENV] = '   '
        self.refused('MISSION_SELECTOR_BLANK', n.registry_path)

    # -- refusal 3: profile downgrade ------------------------------------------------------------
    def test_profile_downgrade_is_refused_by_name(self):
        self.bind(MISSION, n.MACHINE_PROFILE)
        os.environ[n.TRUST_PROFILE_ENV] = n.USER_PROFILE
        self.refused('TRUST_PROFILE_DOWNGRADE', n.trust_profile)

    def test_profile_escalation_and_garbage_are_refused_by_name(self):
        self.bind(MISSION, n.USER_PROFILE)
        for value, code in ((n.MACHINE_PROFILE, 'TRUST_PROFILE_CONFLICT'),
                            ('administrator', 'TRUST_PROFILE_CONFLICT'),
                            ('', 'TRUST_PROFILE_BLANK')):
            os.environ[n.TRUST_PROFILE_ENV] = value
            with self.subTest(value=value):
                self.refused(code, n.trust_profile)

    def test_bound_profile_is_used_when_the_environment_is_silent(self):
        self.bind(MISSION, n.USER_PROFILE)
        os.environ.pop(n.TRUST_PROFILE_ENV, None)
        self.assertEqual(n.trust_profile(), n.USER_PROFILE)

    # -- refusal 4: unprotected environment override ----------------------------------------------
    def test_env_selection_without_a_record_is_refused_when_scoping_is_installed(self):
        n._binding_dir().mkdir(parents=True, exist_ok=True)   # installed, but never bound
        os.environ[n.MISSION_SELECTOR_ENV] = MISSION
        self.refused('SUPERVISOR_BINDING_ABSENT', n.mission_selector)

    def test_binding_shape_is_refused(self):
        binding = n._binding_path()
        binding.parent.mkdir(parents=True, exist_ok=True)
        for document in ({'schema': 'HGK-SUPERVISOR-SCOPE/1', 'trust_profile': 'root'},
                         {'schema': 'HGK-SUPERVISOR-SCOPE/1', 'trust_profile': 'machine',
                          'mission_id': '../escape'},
                         {'schema': 'other/1', 'trust_profile': 'machine'}):
            binding.write_text(json.dumps(document), encoding='utf-8')
            with self.subTest(document=document):
                self.refused('SUPERVISOR_BINDING_SHAPE', n.mission_selector)

    # -- original domain: a record the worker can write is not a decision -------------------------
    def test_original_domain_unprotected_binding_record_is_refused(self):
        # NO patch of assert_protected here: this is the real Windows rule reading a real DACL on a
        # %TEMP%-owned file. The refusal is the point - a record owned by the invoking user could be
        # rewritten by the very worker it is supposed to constrain.
        n.assert_protected = self._protect
        self.bind(MISSION)
        self.refused('SUPERVISOR_BINDING_UNPROTECTED', n.mission_selector)
        self.assertTrue(STAND_IN_NOT_ORIGINAL_DOMAIN)


if __name__ == '__main__':
    unittest.main()
