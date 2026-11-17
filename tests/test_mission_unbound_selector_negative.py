"""NEG/POS for the unbound-host selector (owner ruling 2026-11-17 §二).

The R4a adversarial shape, re-stated as a test:

    no supervisor record + no supervisor directory + a non-empty HGK_MISSION_ID
    + ANOTHER mission's registry already present under <base>/missions/

Pre-fix behaviour: `mission_selector()` returns the environment value and
`registry_path()` resolves to that other mission's registry, so a worker's own
environment chooses which protected registry it is admitted under.

Required behaviour: on such a host the selector is refused by name, because an
environment variable is not a supervisor decision. The unchanged B1 path is
"no selector at all -> the ProgramData constant", and that must keep working.

Label: the base is a temp dir and `assert_protected` is patched, so these runs are
STAND_IN_NOT_ORIGINAL_DOMAIN - they prove selection logic only.
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hg_kseos import native_admission as n
from hg_kseos.errors import InvariantViolation

STAND_IN_NOT_ORIGINAL_DOMAIN = True
MISSION, OTHER = 'MISSION-A', 'MISSION-B'


class UnboundSelectorTests(unittest.TestCase):
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
        # another mission's registry exists; NO supervisor directory is created
        other = self.base / 'missions' / OTHER
        other.mkdir(parents=True)
        (other / 'registry.json').write_text('{"schema":"HGK-NATIVE-REGISTRY/1"}', encoding='utf-8')

    def tearDown(self):
        n.REGISTRY, n.assert_protected = self._registry, self._protect
        for key in (n.MISSION_SELECTOR_ENV, n.TRUST_PROFILE_ENV):
            os.environ.pop(key, None)
        self.temp.cleanup()

    def refused(self, code, call):
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_' + code + '$'):
            call()

    # -- POS: the untouched B1 path -------------------------------------------------------------
    def test_b1_positive_no_selector_resolves_the_programdata_constant(self):
        self.assertIsNone(n.mission_selector())
        self.assertEqual(n.registry_path(), self.constant)
        self.assertEqual(n.trust_profile(), n.MACHINE_PROFILE)

    # -- NEG: the owner-named shape -------------------------------------------------------------
    def test_neg_unbound_host_with_existing_other_mission_registry_refuses_the_env_selector(self):
        os.environ[n.MISSION_SELECTOR_ENV] = OTHER
        self.refused('SUPERVISOR_BINDING_ABSENT', n.mission_selector)

    def test_neg_unbound_host_refuses_the_selector_before_any_registry_is_resolved(self):
        os.environ[n.MISSION_SELECTOR_ENV] = OTHER
        self.refused('SUPERVISOR_BINDING_ABSENT', n.registry_path)

    def test_neg_unbound_host_refuses_a_selector_naming_an_absent_mission(self):
        os.environ[n.MISSION_SELECTOR_ENV] = 'MISSION-DOES-NOT-EXIST'
        self.refused('SUPERVISOR_BINDING_ABSENT', n.mission_selector)

    def test_neg_unbound_host_refuses_the_selector_even_where_scoping_is_installed(self):
        # the same refusal must not depend on the supervisor directory happening to exist
        (self.base / n.SUPERVISOR_DIRNAME).mkdir()
        os.environ[n.MISSION_SELECTOR_ENV] = OTHER
        self.refused('SUPERVISOR_BINDING_ABSENT', n.mission_selector)

    # -- POS: a real binding still selects ------------------------------------------------------
    def test_pos_bound_host_still_selects_its_own_mission(self):
        n.bind_supervisor_scope(MISSION)
        os.environ.pop(n.MISSION_SELECTOR_ENV, None)
        self.assertEqual(n.mission_selector(), MISSION)
        self.assertEqual(n.registry_path(), self.base / 'missions' / MISSION / 'registry.json')

    def test_neg_bound_host_refuses_reselection_to_the_other_mission(self):
        n.bind_supervisor_scope(MISSION)
        os.environ[n.MISSION_SELECTOR_ENV] = OTHER
        self.refused('MISSION_SELECTOR_WORKER_RESELECT', n.mission_selector)


if __name__ == '__main__':
    unittest.main()
