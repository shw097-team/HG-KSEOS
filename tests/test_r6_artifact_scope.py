"""Scope regressions on disposable DBs with synthetic signature verification only."""
import hashlib
import os
import unittest
from pathlib import Path
from unittest.mock import patch

try:  # tests/ is a package: pytest imports this module as tests.<name>
    from . import test_native_admission as fixture
except ImportError:  # pragma: no cover - direct file execution
    import test_native_admission as fixture
from hg_kseos import native_admission as n


class ArtifactScopeTests(unittest.TestCase):
    def setUp(self):
        self.control = fixture.NativeAdmissionTests('test_transaction_positive_synthetic_verifier')
        self.control.setUp()
        self.addCleanup(self.control.tearDown)
        self.control.registry['root'] = str(self.control.root)

    def pin(self, relative, digest):
        self.control.registry['approved_files'] = [{'path': relative, 'sha256': digest}]

    @unittest.skipUnless(os.name == 'nt', 'Windows rooted-relative semantics')
    def test_rooted_relative_existing_outside_file_rejected_before_read_or_write(self):
        outside = self.control.root.parent / (self.control.root.name + '-outside.txt')
        outside.write_bytes(b'outside-root-preimage')
        self.addCleanup(outside.unlink)
        relative = str(outside)[2:]
        self.assertFalse(Path(relative).is_absolute())
        self.assertFalse((self.control.root / relative).is_relative_to(self.control.root))
        self.pin(relative, hashlib.sha256(outside.read_bytes()).hexdigest())
        with patch.object(n, 'pinned_file', wraps=n.pinned_file) as reader:
            self.control.rejected(self.control.permit(self.control.request), 'ARTIFACT_SCOPE')
        reader.assert_not_called()
        self.assertEqual(outside.read_bytes(), b'outside-root-preimage')

    @unittest.skipUnless(os.name == 'nt', 'Windows root and drive semantics')
    def test_other_root_drive_unc_and_traversal_forms_rejected(self):
        for relative in ('/outside.txt', 'C:outside.txt', r'C:\outside.txt',
                         r'\\server\share\outside.txt', r'..\outside.txt', '../outside.txt'):
            with self.subTest(relative=relative):
                self.pin(relative, '1' * 64)
                self.control.rejected(self.control.permit(self.control.request), 'ARTIFACT_SCOPE')

    def test_nested_relative_pin_admits_then_replay_refuses(self):
        path = self.control.root / 'nested' / 'source.bin'
        path.parent.mkdir()
        path.write_bytes(b'approved-source\r\n')
        self.pin('nested/source.bin', hashlib.sha256(path.read_bytes()).hexdigest())
        bundle = self.control.permit(self.control.request)
        with patch.object(n, 'verify_signature', return_value=None):
            self.control.create(bundle)
        self.assertEqual(self.control.rows(), (1, 3, 1, 1))
        self.control.rejected(bundle, 'REPLAY_OR_LEASE_CONFLICT')

    def test_changed_nested_pin_rolls_back_without_nonce_or_entity(self):
        path = self.control.root / 'source.bin'
        path.write_bytes(b'changed-source')
        self.pin('source.bin', hashlib.sha256(b'approved-source').hexdigest())
        self.control.rejected(self.control.permit(self.control.request), 'ARTIFACT_CHANGED')
        self.assertEqual(self.control.rows(), (0, 0, 0, 0))
