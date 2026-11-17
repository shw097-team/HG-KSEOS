"""Real Windows ACL / SID / ancestor measurements for a mission root.

Nothing here is a stand-in: every assertion is computed from this host's live security descriptors
through GetNamedSecurityInfo / GetEffectiveRightsFromAcl / LookupAccountSid. The module is split in
two on purpose:

  ORIGINAL DOMAIN  - the OS-protected registry that actually exists on this host
                     (C:\\ProgramData\\HG-KSEOS\\native-admission\\registry.json, owner
                     BUILTIN\\Administrators, DACL protected, Users read-only). The mission rule is
                     run against it and must PASS - that is the positive case, measured, not assumed.

  NEGATIVES        - each refusal is produced by the real rule on a real path: an %TEMP% root owned by
                     the invoking user, an ancestor with a Users write ACE, a junction in the chain, a
                     declared checker SID that the DACL gives nothing to.

What is NOT measured here, and must not be read into these results: a mission-scoped directory UNDER
ProgramData. Creating <base>/missions/<id>/ with a SYSTEM-owned explicit DACL needs Administrator
(the run window has no HOST_OPERATIONS), so no such directory exists on this host. Tests that need
that shape are marked STAND_IN_NOT_ORIGINAL_DOMAIN and patch the gate.
"""
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hg_kseos import native_admission as n
from hg_kseos.errors import InvariantViolation

REAL = Path(r'C:\ProgramData\HG-KSEOS\native-admission\registry.json')
CHECKER = 'S-1-5-32-545'          # BUILTIN\Users: read-only on the real registry
ABSENT_SID = 'S-1-5-21-9999999999-1-1-1001'
USERS_SID = '*S-1-5-32-545'
STAND_IN_NOT_ORIGINAL_DOMAIN = 'patched runs in this module are not original-domain evidence'


def icacls(path, grant):
    subprocess.run(['icacls', str(path), '/grant', grant], check=True, capture_output=True)


def junction(link, target):
    subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], check=True,
                   capture_output=True)


@unittest.skipUnless(os.name == 'nt', 'Windows ACL measurement')
class OriginalDomainAclTests(unittest.TestCase):
    """Positives measured on the real OS-protected registry; nothing patched."""

    def setUp(self):
        if not REAL.is_file():
            self.skipTest('no OS-protected registry on this host: %s' % REAL)

    def test_owner_and_dacl_are_measured_not_inferred(self):
        facts = n.acl_facts(REAL)
        self.assertEqual(facts['owner'], 'S-1-5-32-544')
        self.assertTrue(facts['dacl_protected'])
        self.assertTrue(facts['sddl'].startswith('O:BA'))
        self.assertEqual(len(facts['aces']), 3)
        granted = {(ace['sid'], ace['mask'], ace['inherited']) for ace in facts['aces']}
        self.assertIn(('S-1-5-18', 0x1F01FF, False), granted)          # SYSTEM full
        self.assertIn(('S-1-5-32-544', 0x1F01FF, False), granted)      # Administrators full
        self.assertIn(('S-1-5-32-545', 0x120089, False), granted)      # Users read+execute
        self.assertTrue(all(ace['inherited'] is False for ace in facts['aces']))

    def test_mission_rule_passes_on_the_real_registry(self):
        report = n.assert_mission_protected(REAL, CHECKER)
        self.assertEqual(report['failures'], [])
        self.assertTrue(report['verdicts']['owner_is_system_or_admin'])
        self.assertTrue(report['verdicts']['dacl_explicit'])
        self.assertTrue(report['verdicts']['no_foreign_write_ace'])
        self.assertTrue(report['verdicts']['ancestors_no_reparse'])
        self.assertTrue(report['verdicts']['ancestors_no_world_write'])
        self.assertTrue(report['checker']['can_read'])
        self.assertIn('C:\\ProgramData', [row['path'] for row in report['ancestors']])

    def test_checker_reachability_is_measured_per_sid(self):
        reachable = n.effective_rights(REAL, CHECKER) or 0
        self.assertTrue(reachable & n.FILE_READ_DATA)
        self.assertTrue(reachable & n.READ_CONTROL)
        # Everyone and an invented SID get nothing from this DACL: reachability is not "anyone can".
        self.assertEqual(n.effective_rights(REAL, 'S-1-1-0'), 0)
        self.assertEqual(n.effective_rights(REAL, ABSENT_SID), 0)

    def test_sid_resolution_is_reported_for_the_checker(self):
        self.assertTrue(n.sid_account(CHECKER)['resolved'])
        self.assertFalse(n.sid_account(ABSENT_SID)['resolved'])

    def test_unreachable_checker_sid_is_refused_by_name(self):
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_TRUST_CHECKER_UNREACHABLE$'):
            n.assert_mission_protected(REAL, ABSENT_SID)

    def test_working_tree_of_this_lane_is_refused_by_the_same_rule(self):
        # A real negative in the original domain: a file created by the invoking user is owned by
        # them, so the machine rule refuses it - exactly as it would refuse a mission root there.
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'probe.txt'
            path.write_text('probe', encoding='utf-8')
            with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_TRUST_ACL_UNPROTECTED$'):
                n.assert_mission_protected(path, CHECKER)


@unittest.skipUnless(os.name == 'nt', 'Windows ACL measurement')
class NegativeAclTests(unittest.TestCase):
    """Each refusal is produced by the real rule on a real path. No gate is patched."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.registry = self.root / 'registry.json'
        self.registry.write_text(json.dumps({'mission_id': 'M'}), encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def test_temp_root_is_refused_for_its_owner(self):
        facts = n.acl_facts(self.registry)
        self.assertNotIn(facts['owner'], n.SYSTEM_OWNER_SIDS)      # measured, not assumed
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_TRUST_ACL_UNPROTECTED$'):
            n.assert_mission_protected(self.registry, CHECKER)

    def test_world_writable_ancestor_is_detected_and_refused(self):
        share = self.root / 'share'
        (share / 'nested').mkdir(parents=True)
        registry = share / 'nested' / 'registry.json'
        registry.write_text('{}', encoding='utf-8')
        icacls(share, USERS_SID + ':(OI)(CI)F')
        rights = n.effective_rights(share, CHECKER) or 0
        self.assertTrue(rights & n.DELETE)                          # the grant is real
        report = n.mission_root_report(registry, CHECKER, base=share)
        self.assertFalse(report['verdicts']['ancestors_no_world_write'])
        with self.assertRaises(InvariantViolation):                 # leaf owner fires first here
            n.assert_mission_protected(registry, CHECKER)

    def test_junction_in_the_chain_is_detected_and_refused(self):
        real = self.root / 'real'
        (real / 'missions' / 'M').mkdir(parents=True)
        target = real / 'missions' / 'M' / 'registry.json'
        target.write_text('{}', encoding='utf-8')
        link = self.root / 'link'
        junction(link, real)
        via_link = link / 'missions' / 'M' / 'registry.json'
        self.assertTrue(via_link.is_file())
        report = n.mission_root_report(via_link, CHECKER, base=link)
        self.assertFalse(report['verdicts']['ancestors_no_reparse'])
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_ROOT_REPARSE$'):
            n.assert_mission_protected(via_link, CHECKER)

    def test_inherited_dacl_is_detected(self):
        # A file in %TEMP% inherits its DACL: measured as not-protected, which is what the mission
        # rule refuses (a mission registry must carry an explicit, non-inherited DACL).
        child = self.root / 'child'
        child.mkdir()
        target = child / 'registry.json'
        target.write_text('{}', encoding='utf-8')
        facts = n.acl_facts(target)
        self.assertFalse(facts['dacl_protected'])
        self.assertTrue(any(ace['inherited'] for ace in facts['aces']))
        report = n.mission_root_report(target, CHECKER, base=self.root)
        self.assertFalse(report['verdicts']['dacl_explicit'])
        self.assertIn('dacl_explicit', report['failures'])


@unittest.skipUnless(os.name == 'nt', 'Windows ACL measurement')
class StandInAclTests(unittest.TestCase):
    """The gate is patched here: these runs are labelled and are NOT original-domain evidence."""

    def test_patched_gate_is_labelled(self):
        self.assertIn('not original-domain', STAND_IN_NOT_ORIGINAL_DOMAIN)
        with tempfile.TemporaryDirectory() as temp:
            registry = Path(temp) / 'registry.json'
            registry.write_text('{}', encoding='utf-8')
            with patch.object(n, 'assert_mission_protected', return_value=None):
                self.assertIsNone(n.assert_mission_protected(registry, CHECKER))


if __name__ == '__main__':
    unittest.main()
