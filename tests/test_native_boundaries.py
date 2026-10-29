"""Boundary regressions: disposable fixtures only; no native acceptance claims."""
import copy
import sqlite3
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock, patch

from hg_kseos import native_admission as n
from hg_kseos.errors import InvariantViolation
from hg_kseos.lifecycle import ProjectLifecycleController
from hg_kseos.spine import SharedSpine
import test_native_admission as fixture


class RequestBoundaryTests(unittest.TestCase):
    def test_late_requirement_does_not_turn_invariant_failure_into_success(self):
        spine = Mock()
        spine.create_taskspec.side_effect = InvariantViolation('ERR_TASKSPEC_CRITICAL_FIELD_MISSING')
        controller = ProjectLifecycleController(spine)
        with patch.object(controller, '_project_state', return_value='EXECUTING'), \
             patch.object(controller, 'plan', return_value={'target_root': str(Path.cwd())}), \
             patch.object(controller, '_repo_head', return_value='a' * 40):
            with self.assertRaisesRegex(InvariantViolation, 'ERR_TASKSPEC_CRITICAL_FIELD_MISSING'):
                controller.admit_requirement('P', 'R', 'goal')
        spine.create_workorder.assert_not_called()

    def test_relative_or_missing_roots_are_not_promoted_to_cwd(self):
        for root in (None, '', '.', 'worktrees', Path('relative')):
            with self.subTest(root=root), self.assertRaisesRegex(InvariantViolation, 'ROOT_ABSOLUTE'):
                n.taskspec_request('T', 'R', 'goal', 'owner', root, {}, ['unit'], 'raw')

    def test_lifecycle_missing_or_relative_target_fails_before_registration(self):
        for root in (None, '', 'worktrees'):
            spine = Mock()
            controller = ProjectLifecycleController(spine)
            with patch.object(controller, '_project_state', return_value='PLAN_READY'), \
                 patch.object(controller, 'plan', return_value={'target_root': root, 'plan': []}):
                with self.subTest(root=root), self.assertRaisesRegex(InvariantViolation, 'ROOT_ABSOLUTE'):
                    controller.admit_workorders('P')
            spine.register_requirement.assert_not_called()


class TransactionBoundaryTests(unittest.TestCase):
    def test_baseexception_rolls_back_before_guard_release(self):
        events = []
        conn = Mock()
        conn.execute.side_effect = lambda *a: events.append('begin')
        conn.rollback.side_effect = lambda: events.append('rollback')
        conn.close.side_effect = lambda: events.append('close')
        spine = SharedSpine(Path('unused.db'))
        with patch.object(spine, '_open', return_value=conn):
            with self.assertRaises(KeyboardInterrupt):
                with spine.transaction() as transaction:
                    transaction.native_guards.callback(lambda: events.append('guard-release'))
                    raise KeyboardInterrupt()
        self.assertEqual(events, ['begin', 'rollback', 'guard-release', 'close'])

    def test_guard_cleanup_failure_still_closes_connection(self):
        conn = Mock()
        spine = SharedSpine(Path('unused.db'))
        def cleanup():
            raise RuntimeError('cleanup-fault')
        with patch.object(spine, '_open', return_value=conn):
            with self.assertRaisesRegex(RuntimeError, 'cleanup-fault'):
                with spine.transaction() as transaction:
                    transaction.native_guards.callback(cleanup)
        conn.commit.assert_called_once()
        conn.close.assert_called_once()


class PinnedReaderTests(unittest.TestCase):
    def test_exact_bytes_and_replacement_denied_until_release(self):
        import os
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'public.json'
            original = b'{"x":1}\r\n'
            path.write_bytes(original)
            with n.held_root(path.parent), n.pinned_file(path) as stream:
                self.assertEqual(stream.read(), original)
                if os.name == 'nt':
                    with self.assertRaises(OSError):
                        path.write_bytes(b'changed')
                    with self.assertRaises(OSError):
                        path.rename(path.with_suffix('.moved'))
            path.write_bytes(b'after-release')
            self.assertEqual(n.pinned_file_bytes(path), b'after-release')

    def test_directory_cannot_be_read_as_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises((InvariantViolation, OSError)):
                n.pinned_file_bytes(Path(directory))

    def test_real_junction_root_refused(self):
        import os, subprocess
        if os.name != 'nt':
            self.skipTest('Windows junction')
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            target = parent / 'target'
            target.mkdir()
            link = parent / 'junction'
            command = "New-Item -ItemType Junction -Path '" + str(link) + "' -Target '" + str(target) + "' | Out-Null"
            subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], check=True, capture_output=True)
            try:
                with self.assertRaisesRegex(InvariantViolation, 'ROOT_REPARSE'):
                    with n.held_root(link):
                        self.fail('junction admitted')
            finally:
                link.rmdir()

    def test_registry_reader_keeps_same_file_pinned(self):
        # ACL enforcement is a separate OS prerequisite. This test bypasses only
        # ACL checking on a disposable file and proves lifetime of its read handle.
        import os
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'registry.json'
            data = {'schema': 'HGK-NATIVE-REGISTRY/1', 'canonical_profile': n.PROFILE,
                    'status': 'ACTIVE', 'owner_os_sid': 'fixture-owner',
                    'checker_os_sid': 'fixture-checker', 'maker_os_sid': 'fixture-maker',
                    'root': directory, 'approved_files': [{'path': 'fixture', 'sha256': '1' * 64}]}
            path.write_text(__import__('json').dumps(data))
            with patch.object(n, 'REGISTRY', path), patch.object(n, 'assert_protected'):
                with n.ProtectedRegistry().hold_snapshot() as actual:
                    self.assertEqual(actual, data)
                    if os.name == 'nt':
                        with self.assertRaises(OSError):
                            path.write_text('{}')
                path.write_text('{}')

    def test_actual_acl_rejects_maker_owned_registry(self):
        import os
        if os.name != 'nt':
            self.skipTest('Windows ACL')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'registry.json'
            path.write_text('{}')
            with self.assertRaisesRegex(InvariantViolation, 'TRUST_ACL_UNPROTECTED'):
                n.assert_protected(path)


class AdmissionBoundaryTests(unittest.TestCase):
    setUp = fixture.NativeAdmissionTests.setUp
    tearDown = fixture.NativeAdmissionTests.tearDown
    permit = fixture.NativeAdmissionTests.permit
    create = fixture.NativeAdmissionTests.create
    rows = fixture.NativeAdmissionTests.rows
    rejected = fixture.NativeAdmissionTests.rejected

    def test_dirty_artifact_mismatch_refused_before_mutation(self):
        path = self.root / 'candidate.py'
        path.write_bytes(b'changed')
        self.registry.update(root=str(self.root), approved_files=[{'path': path.name, 'sha256': '0' * 64}])
        self.rejected(self.permit(self.request), 'ARTIFACT_CHANGED')

    def test_artifact_traversal_refused(self):
        self.registry.update(root=str(self.root), approved_files=[{'path': '../outside', 'sha256': '0' * 64}])
        self.rejected(self.permit(self.request), 'ARTIFACT_SCOPE')

    def test_pinned_artifact_held_until_commit(self):
        import hashlib, os
        path = self.root / 'candidate.py'
        path.write_bytes(b'approved-source')
        self.registry.update(root=str(self.root), approved_files=[{'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}])
        original = self.spine._insert_taskspec
        def insert(*args):
            original(*args)
            if os.name == 'nt':
                with self.assertRaises(OSError):
                    path.write_bytes(b'changed')
        with patch.object(self.spine, '_insert_taskspec', side_effect=insert), patch.object(n, 'verify_signature', return_value=None):
            self.create(self.permit(self.request))
        path.write_bytes(b'after-commit')
    def test_malformed_payload_has_named_refusal_and_zero_rows(self):
        bundle = self.permit(self.request)
        bundle['references'][0]['payload'] = None
        self.rejected(bundle, 'PAYLOAD_SHAPE')

    def test_workorder_failure_restores_draft_and_all_admission_rows(self):
        with patch.object(n, 'verify_signature', return_value=None):
            self.create(self.permit(self.request))
        before = self.rows()
        with self.spine.connect() as conn:
            task = conn.execute('SELECT * FROM taskspecs').fetchone()
            request = n.workorder_request('WO', task, 'codex', self.root, self.head)
        original = self.spine._insert_workorder
        def fault(*args):
            original(*args)
            raise RuntimeError('workorder-insert-fault')
        bundle = self.permit(request, 'create_workorder', seed='W')
        with patch.object(self.spine, '_insert_workorder', side_effect=fault), \
             patch.object(n, 'verify_signature', return_value=None):
            with self.assertRaisesRegex(RuntimeError, 'workorder-insert-fault'):
                self.spine.create_workorder('WO', 'TS', 'codex', self.root, self.head,
                                            admission_bundle=bundle)
        self.assertEqual(self.rows(), before)
        with self.spine.connect() as conn:
            self.assertEqual(conn.execute('SELECT state FROM taskspecs').fetchone()[0], 'DRAFT')
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM workorders').fetchone()[0], 0)

    def test_restart_replay_uses_existing_canonical_database(self):
        bundle = self.permit(self.request)
        with patch.object(n, 'verify_signature', return_value=None):
            self.create(bundle)
        self.spine = SharedSpine(self.spine.database, admission=self.service)
        self.rejected(bundle, 'REPLAY_OR_LEASE_CONFLICT')

    def test_post_insert_policy_drift_rolls_back(self):
        original = self.spine._insert_taskspec
        def drift(*args):
            original(*args)
            self.registry['policy_epoch'] = 2
        with patch.object(self.spine, '_insert_taskspec', side_effect=drift):
            self.rejected(self.permit(self.request), 'POLICY_CHANGED_BEFORE_COMMIT')

    def test_real_commit_holds_root_until_after_commit(self):
        import os
        if os.name != 'nt':
            self.skipTest('Windows share-delete test')
        spine = self.spine
        original = spine._open
        results = []
        class Connection(sqlite3.Connection):
            def commit(conn):
                with self.assertRaises(OSError):
                    self.root.rename(self.root.with_name(self.root.name + '-moved'))
                results.append('pinned-at-commit')
                return super(Connection, conn).commit()
        def opened():
            conn = sqlite3.connect(spine.database, factory=Connection)
            conn.row_factory = sqlite3.Row
            return conn
        with patch.object(spine, '_open', side_effect=opened), \
             patch.object(n, 'verify_signature', return_value=None):
            self.create(self.permit(self.request))
        self.assertEqual(results, ['pinned-at-commit'])
        moved = self.root.with_name(self.root.name + '-moved')
        self.root.rename(moved)
        moved.rename(self.root)


if __name__ == '__main__':
    unittest.main()
