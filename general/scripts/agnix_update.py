#!/usr/bin/env python3
"""Check the official stable agnix release once a day and update the local install."""
import argparse
import datetime
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

API = 'https://api.github.com/repos/agent-sh/agnix/releases/latest'


def fetch(url, limit, timeout):
    request = urllib.request.Request(url, headers={'User-Agent': 'ai-agnix-update'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError('download exceeds size limit')
    return data


def version(value):
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)', value)
    if not match:
        raise ValueError('invalid stable version')
    return tuple(map(int, match.groups()))


def binary_version(binary):
    result = subprocess.run([str(binary), '--version'], check=True, capture_output=True,
                            text=True, timeout=10)
    output = result.stdout.strip()
    if not output.startswith('agnix '):
        raise ValueError('unexpected binary version output')
    return version(output[len('agnix '):])


def installed_binary(home):
    for path in [home / '.local/share/agnix/current/agnix',
                 home / '.local/share/agnix/v0.59.0/agnix']:
        if path.is_file():
            return path
    found = shutil.which('agnix')
    return Path(found) if found else None


def update(home, state_dir, force=False):
    today = datetime.date.today().isoformat()
    checkpoint = state_dir / 'update.json'
    binary = installed_binary(home)
    try:
        previous = json.loads(checkpoint.read_text())
    except (OSError, ValueError):
        previous = {}
    if not force and previous.get('date') == today and binary:
        return 0
    release = json.loads(fetch(API, 2_000_000, 15))
    tag = release['tag_name']
    latest = version(tag)
    if release.get('draft') is not False or release.get('prerelease') is not False:
        raise ValueError('release is not stable')
    current = binary_version(binary) if binary else None
    if current is None or latest > current:
        targets = {('Linux', 'x86_64'): 'x86_64-unknown-linux-musl',
                   ('Linux', 'aarch64'): 'aarch64-unknown-linux-gnu',
                   ('Darwin', 'arm64'): 'aarch64-apple-darwin',
                   ('Darwin', 'x86_64'): 'x86_64-apple-darwin'}
        target = targets.get((platform.system(), platform.machine()))
        if not target:
            raise ValueError('unsupported OS/CPU')
        name = 'agnix-' + target + '.tar.gz'
        asset = next(a for a in release['assets'] if a['name'] == name)
        url = 'https://github.com/agent-sh/agnix/releases/download/' + tag + '/' + name
        if asset['browser_download_url'] != url:
            raise ValueError('unexpected release asset URL')
        digest = asset.get('digest', '')
        if not re.fullmatch(r'sha256:[a-f0-9]{64}', digest):
            raise ValueError('missing SHA-256 in official release metadata')
        archive = fetch(url, 100_000_000, 45)
        if 'sha256:' + hashlib.sha256(archive).hexdigest() != digest:
            raise ValueError('release SHA-256 mismatch')
        install = home / '.local/share/agnix'
        install.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.update-', dir=install) as temp:
            candidate = Path(temp) / 'agnix'
            with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
                members = [m for m in tar.getmembers() if Path(m.name).name == 'agnix']
                if len(members) != 1 or not members[0].isfile() or members[0].size > 200_000_000:
                    raise ValueError('invalid binary archive')
                # Copy only the regular binary; never extract paths or links from the archive.
                with tar.extractfile(members[0]) as source, candidate.open('wb') as dest:
                    shutil.copyfileobj(source, dest)
            candidate.chmod(0o755)
            if binary_version(candidate) != latest:
                raise ValueError('downloaded binary version mismatch')
            destination = install / tag
            destination.mkdir(exist_ok=True)
            os.replace(candidate, destination / 'agnix')
            link = Path(temp) / 'current'
            link.symlink_to(destination, target_is_directory=True)
            os.replace(link, install / 'current')
        print('agnix-update: installed ' + tag + ' (SHA-256 and binary version verified)')
    else:
        print('agnix-update: current version is up to date; latest stable ' + tag)
    temporary = state_dir / 'update.json.tmp'
    temporary.write_text(json.dumps({'date': today, 'latest': tag}) + '\n')
    os.replace(temporary, checkpoint)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-home', type=Path, default=Path.home())
    parser.add_argument('--state-dir', type=Path, default=Path(os.environ.get(
        'AI_LINT_STATE_DIR', str(Path.home() / 'ai-data/agnix'))))
    parser.add_argument('--force', action='store_true', help='ignore the daily checkpoint')
    args = parser.parse_args()
    try:
        args.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        with (args.state_dir / 'update.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                print('agnix-update: another update is running; retry pending')
                return 1
            return update(args.runtime_home, args.state_dir, args.force)
    except (OSError, ValueError, KeyError, TypeError, StopIteration,
            subprocess.SubprocessError, tarfile.TarError):
        print('agnix-update: FAILED: release/download/verification error; existing selection retained; retry pending')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
