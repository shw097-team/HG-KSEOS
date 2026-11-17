"""Mission-scoped machine registry SELECTION (WP06 candidate) - one file, one mission.

These tests lock the three properties the candidate claims:

  * no selector  -> the ProgramData constant, i.e. byte-identical to main 7e5e8613;
  * a selector   -> that mission's registry under the same protected base dir;
  * a wrong file -> a NAMED refusal, never a silent choice between two present registries.

ACL checking is patched out in the selection tests only: an OS-protected ProgramData root is a host
prerequisite, and `test_mission_acl_original_domain` measures the real Windows path separately.

LABEL: every run in this module is STAND_IN_NOT_ORIGINAL_DOMAIN - the roots live under %TEMP% and are
owned by the invoking user, so the real DACL rule would refuse them all. A pass here says the
SELECTION logic is right and says nothing about Windows protection.
"""
import json
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from hg_kseos import native_admission as n
from hg_kseos.errors import InvariantViolation

PIN = b'pin-bytes\n'
PIN_SHA = __import__('hashlib').sha256(PIN).hexdigest()
STAND_IN_NOT_ORIGINAL_DOMAIN = 'patched ACL gate: stand-in roots, not original-domain evidence'


def registry_doc(mission_id, root):
    return {'schema': 'HGK-NATIVE-REGISTRY/1', 'canonical_profile': n.PROFILE, 'status': 'ACTIVE',
            'mission_id': mission_id, 'owner_os_sid': 'S-1-5-18', 'checker_os_sid': 'S-1-5-32-544',
            'maker_os_sid': 'S-1-5-21-FIXTURE-MAKER', 'root': str(root),
            'source_manifest_sha256': '1' * 64, 'policy_sha256': '2' * 64, 'policy_epoch': 1,
            'max_ttl_seconds': 3600, 'approved_files': [{'path': 'pin.txt', 'sha256': PIN_SHA}]}


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name) / 'native-admission'
        self.base.mkdir()
        self.root = Path(self.temp.name) / 'artifact-root'
        self.root.mkdir()
        (self.root / 'pin.txt').write_bytes(PIN)
        self.legacy = self.base / 'registry.json'
        self.missions = self.base / 'missions'
        os.environ.pop(n.MISSION_SELECTOR_ENV, None)

    def tearDown(self):
        os.environ.pop(n.MISSION_SELECTOR_ENV, None)
        self.temp.cleanup()

    # -- fixtures -------------------------------------------------------------------------------
    def write(self, path, doc):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc), encoding='utf-8')
        return path

    def select(self, mission):
        os.environ[n.MISSION_SELECTOR_ENV] = mission

    @contextmanager
    def patched(self):
        # STAND_IN_NOT_ORIGINAL_DOMAIN: both gates are patched, so a mission root under %TEMP% can be
        # exercised at all. The real gate is measured in test_mission_acl_original_domain.
        with patch.object(n, 'REGISTRY', self.legacy), patch.object(n, 'assert_protected'),                 patch.object(n, 'assert_mission_protected'):
            yield

    def snapshot(self):
        with self.patched():
            return n.ProtectedRegistry().snapshot()

    def refused(self, code):
        with self.patched():
            with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_' + code + '$'):
                n.ProtectedRegistry().snapshot()

    # -- (a) no selector is the untouched behaviour ---------------------------------------------
    def test_no_selector_resolves_the_unscoped_constant(self):
        with self.patched():
            self.assertIsNone(n.mission_selector())
            self.assertEqual(n.registry_path(), self.legacy)
            self.assertEqual(n.registry_path(n.MACHINE_PROFILE), self.legacy)

    def test_no_selector_reads_legacy_file_and_never_scans_the_missions_dir(self):
        # Two mission registries AND the legacy file exist. Without a selector the receiver must
        # read the constant - not pick the only mission, not pick the first one.
        self.write(self.legacy, registry_doc('LEGACY-MISSION', self.root))
        self.write(self.missions / 'M1' / 'registry.json', registry_doc('M1', self.root))
        self.write(self.missions / 'M2' / 'registry.json', registry_doc('M2', self.root))
        with self.patched():
            self.assertEqual(n.registry_path(), self.legacy)
        self.assertEqual(self.snapshot()['mission_id'], 'LEGACY-MISSION')

    def test_no_selector_keeps_the_bootstrap_refusal_code(self):
        self.refused('TRUST_BOOTSTRAP_REQUIRED')

    # -- (b) a valid selector picks that mission's registry ---------------------------------------
    def test_selector_resolves_that_missions_registry(self):
        self.write(self.missions / 'M1' / 'registry.json', registry_doc('M1', self.root))
        self.select('M1')
        with self.patched():
            self.assertEqual(n.registry_path(), self.base / 'missions' / 'M1' / 'registry.json')
        self.assertEqual(self.snapshot()['mission_id'], 'M1')

    def test_selector_is_pinned_at_construction_and_a_later_change_is_refused(self):
        # Pinning alone would make a mid-flight change harmless but invisible; the candidate refuses
        # it by name instead, so a worker cannot quietly re-point the receiver.
        self.write(self.missions / 'M1' / 'registry.json', registry_doc('M1', self.root))
        self.write(self.missions / 'M2' / 'registry.json', registry_doc('M2', self.root))
        self.select('M1')
        with self.patched():
            receiver = n.ProtectedRegistry()
            self.assertEqual(receiver.snapshot()['mission_id'], 'M1')
            os.environ[n.MISSION_SELECTOR_ENV] = 'M2'
            with self.assertRaisesRegex(InvariantViolation,
                                        '^ERR_NATIVE_MISSION_SELECTOR_WORKER_RESELECT$'):
                receiver.snapshot()

    def test_stand_in_runs_are_labelled(self):
        self.assertIn('not original-domain', STAND_IN_NOT_ORIGINAL_DOMAIN)

    # -- (c) a file whose mission_id differs is refused by name ----------------------------------
    def test_registry_declaring_another_mission_is_refused_by_name(self):
        self.write(self.missions / 'M1' / 'registry.json', registry_doc('M2', self.root))
        self.select('M1')
        self.refused('MISSION_REGISTRY_MISMATCH')

    def test_registry_without_a_scalar_mission_is_refused_by_name(self):
        doc = registry_doc('M1', self.root)
        doc['mission_id'] = ['M1', 'M2']          # one file still admits exactly one mission
        self.write(self.missions / 'M1' / 'registry.json', doc)
        self.select('M1')
        self.refused('MISSION_REGISTRY_MISMATCH')

    # -- (d)/(e) mis-selection is a refusal, never a choice --------------------------------------
    def test_absent_selected_registry_refuses_instead_of_downgrading(self):
        # The legacy file IS present and readable. A pinned mission that has no file must not fall
        # back to it: that would silently admit a different mission.
        self.write(self.legacy, registry_doc('LEGACY-MISSION', self.root))
        self.select('M1')
        self.refused('MISSION_REGISTRY_ABSENT')

    def test_wrong_one_of_two_present_returns_refusal_not_selection(self):
        self.write(self.missions / 'M1' / 'registry.json', registry_doc('M2', self.root))
        self.write(self.missions / 'M2' / 'registry.json', registry_doc('M2', self.root))
        self.select('M1')
        self.refused('MISSION_REGISTRY_MISMATCH')
        self.select('M2')
        self.assertEqual(self.snapshot()['mission_id'], 'M2')

    # -- selector shape: the selector is an id, never a path -------------------------------------
    def test_selector_cannot_be_a_path(self):
        # No NUL case: os.environ itself refuses an embedded NUL, so that shape can never arrive.
        for bad in ('../M1', 'M1/../../etc', '..', 'M1/M2', r'M1\M2', 'C:', 'C:\\temp',
                    'C:/temp', '', 'M' * 65, '.hidden', '-flag', 'a b', 'M1.', 'M1\nM2'):
            os.environ[n.MISSION_SELECTOR_ENV] = bad
            if bad == '':
                self.assertIsNone(n.mission_selector())      # empty == no selector, as before
                continue
            with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_MISSION_SELECTOR_SHAPE$'):
                n.mission_selector()

    def test_traversal_selector_never_reaches_the_filesystem(self):
        # A would-be escape target exists and is a perfectly valid registry: if shape validation
        # were missing, M1/../../escape would read it.
        escape = Path(self.temp.name) / 'escape' / 'registry.json'
        self.write(escape, registry_doc('ESCAPED', self.root))
        self.select('M1/../../../escape/registry')
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_MISSION_SELECTOR_SHAPE$'):
            self.snapshot()

    # -- the request cannot choose the root ------------------------------------------------------
    def test_request_keys_naming_a_root_are_refused_by_name(self):
        for key in n.REQUEST_ROOT_KEYS:
            request = n.taskspec_request('TS', 'R', 'objective', 'maker', self.root,
                                         {'network': 'OFF'}, ['unit'], 'evidence')
            request[key] = str(self.legacy)
            with self.subTest(key=key):
                # Refused before the connection or the registry is touched: connection is None.
                with self.assertRaisesRegex(InvariantViolation,
                                            '^ERR_NATIVE_REQUEST_SELECTED_ROOT$'):
                    self._authorize(request)

    def _authorize(self, request):
        service = n.NativeAdmission(registry=type('R', (), {'snapshot': staticmethod(lambda: {})})())
        with service.authorize(None, 'create_taskspec', request,
                               {'references': [], 'lease_generation': 0}):
            self.fail('request-selected root was accepted')

    def test_bundle_cannot_carry_a_root(self):
        service = n.NativeAdmission(registry=type('R', (), {'snapshot': staticmethod(lambda: {})})())
        request = n.taskspec_request('TS', 'R', 'objective', 'maker', self.root,
                                     {'network': 'OFF'}, ['unit'], 'evidence')
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_BUNDLE_REQUIRED$'):
            with service.authorize(None, 'create_taskspec', request,
                                   {'references': [], 'lease_generation': 0,
                                    'registry_path': str(self.legacy)}):
                self.fail('bundle-carried root was accepted')


if __name__ == '__main__':
    unittest.main()
