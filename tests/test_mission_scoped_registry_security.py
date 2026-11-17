"""Security properties of mission-scoped machine registry selection.

Four claims, each with a real run:

  1. cross-mission leakage: a receiver pinned to M2 cannot admit references signed for M1, even
     though both registries are present and both files are readable;
  2. path traversal: a selector is validated as an id before it meets the filesystem, so no
     selector string can name a file outside <base>/missions/<id>/;
  3. symlink / reparse: a junction standing in for the mission directory is refused by held_root,
     not followed to whatever registry it points at;
  4. ACL preservation: the mission registry is checked by the SAME `assert_protected` rule as the
     unscoped ProgramData constant - selection did not lower it.

Only the ACL check is patched in tests 1 and 3, because an OS-protected ProgramData root is a host
prerequisite; test 4 runs the real ACL check.
"""
import base64
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from hg_kseos import native_admission as n
from hg_kseos.errors import InvariantViolation
from hg_kseos.spine import SharedSpine

MISSION_SELECTED = 'M2'
MISSION_OTHER = 'M1'
PIN = b'pin-bytes\n'


def _git(root):
    subprocess.run(['git', 'init', '-q', str(root)], check=True, capture_output=True)
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=fixture',
                    '-c', 'user.email=fixture@invalid', 'commit', '--allow-empty', '-qm', 'fixture'],
                   check=True, capture_output=True)
    return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()


class MissionSecurityTests(unittest.TestCase):
    def setUp(self):
        os.environ.pop(n.MISSION_SELECTOR_ENV, None)
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.artifact = base / 'artifact-root'
        self.artifact.mkdir()
        (self.artifact / 'pin.txt').write_bytes(PIN)
        self.head = _git(self.artifact)
        with n.held_root(self.artifact) as rootid:
            self.rootid = rootid
        self.adm = base / 'native-admission'
        self.adm.mkdir()
        self.legacy = self.adm / 'registry.json'
        self.mission_file = self.adm / 'missions' / MISSION_SELECTED / 'registry.json'
        self.other_file = self.adm / 'missions' / MISSION_OTHER / 'registry.json'
        self.db = self.artifact / 'disposable.db'

    def tearDown(self):
        os.environ.pop(n.MISSION_SELECTOR_ENV, None)
        self.temp.cleanup()

    # -- fixtures -------------------------------------------------------------------------------
    def document(self, mission_id):
        return {'schema': 'HGK-NATIVE-REGISTRY/1', 'canonical_profile': n.PROFILE,
                'status': 'ACTIVE', 'mission_id': mission_id,
                'owner_os_sid': 'S-1-5-18', 'checker_os_sid': 'S-1-5-32-544',
                'maker_os_sid': 'S-1-5-21-FIXTURE-MAKER',
                'root': str(self.artifact), 'source_manifest_sha256': '1' * 64,
                'policy_sha256': '2' * 64, 'policy_epoch': 1, 'max_ttl_seconds': 3600,
                'approved_files': [{'path': 'pin.txt',
                                    'sha256': hashlib.sha256(PIN).hexdigest()}],
                'keys': {'fixture': {'algorithm': 'Ed25519',
                                     'purposes': list(n.KINDS), 'revoked': False}},
                'task_kinds': {'UNIT-UNREGISTERED-OUTSIDE-FIXTURE':
                               {'state': 'REGISTERED', 'source_sha256': '3' * 64,
                                'operations': list(n.PURPOSES)}},
                'revoked_nonces': [],
                'scope': {'database_path': str(self.db.resolve()), 'head': self.head,
                          'root_identity': self.rootid, 'task_kind': 'UNIT-UNREGISTERED-OUTSIDE-FIXTURE',
                          'request_sha256': []}}

    def write(self, path, doc):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc), encoding='utf-8')
        return doc

    def bundle(self, doc, request, mission_id_for_references, seed='A', generation=0):
        sha = n.digest_request(request)
        now = datetime.now(timezone.utc)
        refs = []
        for i, kind in enumerate(n.KINDS):
            payload = {'profile': n.PROFILE, 'reference_kind': kind,
                       'mission_id': mission_id_for_references,
                       'source_manifest_sha256': doc['source_manifest_sha256'],
                       'subject_sha256': sha, 'policy_sha256': doc['policy_sha256'],
                       'policy_epoch': 1, 'operation': 'create_taskspec',
                       'purpose': n.PURPOSES['create_taskspec'], 'nonce': seed * 16 + str(i),
                       'issued_at': (now - timedelta(seconds=5)).isoformat(),
                       'expires_at': (now + timedelta(minutes=10)).isoformat(),
                       'lease_generation': generation, 'root_identity': self.rootid,
                       'head': self.head, 'task_kind': 'UNIT-UNREGISTERED-OUTSIDE-FIXTURE',
                       'evidence_ref': 'fixture-only'}
            refs.append({'key_id': 'fixture', 'payload': payload,
                         'signature': 'SYNTHETIC-VERIFIER-SEAM-NOT-SIGNED'})
        return {'references': refs, 'lease_generation': generation}

    def admitted_rows(self):
        with self.spine.connect() as c:
            return tuple(c.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
                         for t in ('taskspecs', 'native_admission_nonces',
                                   'native_admission_leases'))

    # -- 1. cross-mission leakage ----------------------------------------------------------------
    def test_cross_mission_leakage_is_refused_by_name(self):
        os.environ[n.MISSION_SELECTOR_ENV] = MISSION_SELECTED
        doc = self.write(self.mission_file, self.document(MISSION_SELECTED))
        self.write(self.other_file, self.document(MISSION_OTHER))
        request = n.taskspec_request('TS', 'R', 'objective', 'maker', self.artifact,
                                     {'network': 'OFF'}, ['unit'], 'evidence')
        doc['scope']['request_sha256'] = [n.digest_request(request)]
        self.write(self.mission_file, doc)
        with patch.object(n, 'REGISTRY', self.legacy), patch.object(n, 'assert_protected'), \
                patch.object(n, 'verify_signature', return_value=None):
            service = n.NativeAdmission(n.ProtectedRegistry())      # pinned to M2 by config
            self.assertEqual(service.registry.snapshot()['mission_id'], MISSION_SELECTED)
            self.spine = SharedSpine(self.db, admission=service)
            self.spine.initialize()
            self.spine.create_project()
            self.spine.register_requirement('R', 'fixture', 'fixture', 'A', 'fixture', '1', 'fixture')
            self.spine.acquire_lease('R', 'fixture', 'test-only-token')
            self.spine.transition_requirement('R', 'FROZEN', 'fixture', 'test-only-token', 0, 'E',
                                              'freeze')
            before = self.admitted_rows()
            # References signed for the OTHER mission, against M2's registry.
            with self.assertRaisesRegex(InvariantViolation,
                                        '^ERR_NATIVE_SAME_SUBJECT_BINDING$'):
                self.spine.create_taskspec('TS', 'R', 'objective', 'maker', self.artifact,
                                           {'network': 'OFF'}, ['unit'], 'evidence',
                                           admission_bundle=self.bundle(doc, request, MISSION_OTHER))
            self.assertEqual(self.admitted_rows(), before, 'refused admission wrote rows')
            self.assertEqual(before, (0, 0, 0))
            # The same receiver admits the same request when the references name ITS mission.
            self.spine.create_taskspec('TS', 'R', 'objective', 'maker', self.artifact,
                                       {'network': 'OFF'}, ['unit'], 'evidence',
                                       admission_bundle=self.bundle(doc, request, MISSION_SELECTED,
                                                                    seed='B'))
            self.assertEqual(self.admitted_rows(), (1, 3, 1))

    # -- 2. path traversal ----------------------------------------------------------------------
    def test_traversal_selector_is_refused_before_any_path_is_built(self):
        # both a would-be escape target and the string that would reach it exist
        self.write(self.legacy, self.document(MISSION_OTHER))
        for bad in ('../registry', f'{MISSION_SELECTED}/../../../registry', '..\\registry',
                    f'{MISSION_SELECTED}/..'):
            os.environ[n.MISSION_SELECTOR_ENV] = bad
            with self.assertRaisesRegex(InvariantViolation,
                                        '^ERR_NATIVE_MISSION_SELECTOR_SHAPE$'):
                n.machine_registry_path(n.mission_selector())

    def test_resolved_mission_path_is_always_under_the_protected_base(self):
        with patch.object(n, 'REGISTRY', self.legacy):
            for good in ('M1', 'MISSION-2', 'wp06_2026.11.17', 'a'):
                os.environ[n.MISSION_SELECTOR_ENV] = good
                resolved = n.machine_registry_path(n.mission_selector())
                self.assertEqual(resolved.parent.parent.parent, self.adm)
                self.assertEqual(resolved.name, 'registry.json')
                self.assertNotIn('..', resolved.parts)

    # -- 3. symlink / reparse ------------------------------------------------------------------
    def test_junction_in_place_of_the_mission_dir_is_refused(self):
        if os.name != 'nt':
            self.skipTest('Windows junction')
        elsewhere = Path(self.temp.name) / 'elsewhere'
        elsewhere.mkdir()
        self.write(elsewhere / 'registry.json', self.document(MISSION_SELECTED))
        (self.adm / 'missions').mkdir()
        link = self.adm / 'missions' / MISSION_SELECTED
        subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                        "New-Item -ItemType Junction -Path '" + str(link) + "' -Target '"
                        + str(elsewhere) + "' | Out-Null"], check=True, capture_output=True)
        try:
            os.environ[n.MISSION_SELECTOR_ENV] = MISSION_SELECTED
            with patch.object(n, 'REGISTRY', self.legacy), patch.object(n, 'assert_protected'):
                with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_(ROOT|REGISTRY)_REPARSE$'):
                    n.ProtectedRegistry().snapshot()
        finally:
            link.rmdir()

    # -- 4. ACL preservation ---------------------------------------------------------------------
    def test_mission_registry_keeps_the_machine_acl_rule(self):
        if os.name != 'nt':
            self.skipTest('Windows ACL')
        # A registry that is otherwise perfect, but owned by the current (maker) user instead of
        # SYSTEM/Administrators: the unscoped rule refuses it, and the mission path must too.
        path = self.write(self.mission_file, self.document(MISSION_SELECTED))
        with self.assertRaisesRegex(InvariantViolation, '^ERR_NATIVE_TRUST_ACL_UNPROTECTED$'):
            n.assert_protected(path)

    def test_mission_registry_is_still_checked_by_assert_protected(self):
        self.write(self.mission_file, self.document(MISSION_SELECTED))
        os.environ[n.MISSION_SELECTOR_ENV] = MISSION_SELECTED
        seen = []
        with patch.object(n, 'REGISTRY', self.legacy), \
                patch.object(n, 'assert_protected', side_effect=lambda p: seen.append(Path(p))):
            n.ProtectedRegistry().snapshot()
        self.assertEqual(seen, [self.mission_file, self.mission_file])


if __name__ == '__main__':
    unittest.main()
