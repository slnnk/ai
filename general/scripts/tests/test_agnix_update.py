"""Offline release verification, activation and daily checkpoint checks."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('agnix_update', Path(__file__).resolve().parents[1] / 'agnix_update.py')
UP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UP)


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.state = self.home / 'state'
        self.state.mkdir()
        self.install = self.home / '.local/share/agnix'
        self.old = self.install / 'v0.59.0/agnix'
        self.old.parent.mkdir(parents=True)
        self.old.write_text('#!/bin/sh\necho agnix 0.59.0\n')
        self.old.chmod(0o755)
        self.body = b'#!/bin/sh\necho agnix 0.60.3\n'
        self.make_release()

    def make_release(self, name='agnix', kind=tarfile.REGTYPE):
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as tar:
            member = tarfile.TarInfo(name)
            member.type = kind
            member.size = len(self.body) if kind == tarfile.REGTYPE else 0
            tar.addfile(member, io.BytesIO(self.body) if member.size else None)
        self.archive = buffer.getvalue()
        asset = 'agnix-x86_64-unknown-linux-musl.tar.gz'
        self.release = {'tag_name': 'v0.60.3', 'draft': False, 'prerelease': False,
                        'assets': [{'name': asset, 'digest': 'sha256:' + hashlib.sha256(self.archive).hexdigest(),
                                    'browser_download_url': 'https://github.com/agent-sh/agnix/releases/download/v0.60.3/' + asset}]}

    def run_update(self, force=False):
        def fetch(url, *args):
            return json.dumps(self.release).encode() if url == UP.API else self.archive
        with patch.object(UP, 'fetch', side_effect=fetch) as download, \
             patch.object(UP.platform, 'system', return_value='Linux'), \
             patch.object(UP.platform, 'machine', return_value='x86_64'):
            result = UP.update(self.home, self.state, force)
            return result, download.call_count

    def test_verified_update_then_daily_skip_and_force(self):
        self.assertEqual(self.run_update(), (0, 2))
        self.assertEqual(UP.binary_version(UP.installed_binary(self.home)), (0, 60, 3))
        self.assertTrue(self.old.exists())
        self.assertEqual(self.run_update(), (0, 0))
        self.assertEqual(self.run_update(force=True), (0, 1))

    def test_failed_checksum_keeps_selection_and_retries(self):
        self.release['assets'][0]['digest'] = 'sha256:' + '0' * 64
        for attempt in range(2):
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                self.run_update()
            self.assertEqual(UP.installed_binary(self.home), self.old)
            self.assertFalse((self.state / 'update.json').exists())

    def test_wrong_binary_version_does_not_activate(self):
        self.body = b'#!/bin/sh\necho agnix 0.1.0\n'
        self.make_release()
        with self.assertRaisesRegex(ValueError, 'version mismatch'):
            self.run_update()
        self.assertFalse((self.install / 'current').exists())

    def test_archive_link_rejected_and_no_paths_extracted(self):
        self.make_release('../../agnix', tarfile.SYMTYPE)
        with self.assertRaisesRegex(ValueError, 'invalid binary archive'):
            self.run_update()
        self.assertFalse((self.install / 'current').exists())

    def test_no_downgrade(self):
        self.old.write_text('#!/bin/sh\necho agnix 1.0.0\n')
        self.assertEqual(self.run_update(), (0, 1))
        self.assertFalse((self.install / 'current').exists())

    def test_prerelease_and_untrusted_url_rejected(self):
        self.release['prerelease'] = True
        with self.assertRaisesRegex(ValueError, 'not stable'):
            self.run_update()
        self.release['prerelease'] = False
        self.release['assets'][0]['browser_download_url'] = 'https://example.com/agnix'
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            self.run_update()

    def test_first_install(self):
        self.old.unlink()
        with patch.object(UP.shutil, 'which', return_value=None):
            self.assertEqual(self.run_update(), (0, 2))


if __name__ == '__main__':
    unittest.main()
