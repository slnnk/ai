#!/usr/bin/env python3
"""Run report-only agnix after agent configuration changes; cache successful input hashes.

Default scope: shared KB instructions/skills and this machine's Claude/Codex settings.
Additional files/directories may be supplied for repository-local agent instructions.
No installation, model calls, fixes or Git operations. Reports omit source/message text.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

INSTRUCTIONS = {'AGENTS.md', 'AGENTS.override.md', 'CLAUDE.md', 'GEMINI.md'}
EXTENSIONS = {'.md', '.py', '.sh', '.js', '.ts', '.json', '.toml', '.yaml', '.yml', '.txt'}
EXCLUDED = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}


def eligible(path):
    return not any(p in EXCLUDED for p in path.parts) and not path.name.startswith('.env')


def discover(root, runtime_home, extra):
    """Return watched files and agnix entry points. Skill resources invalidate SKILL.md."""
    watched, entries = set(), {}
    def add(path, lint=True):
        path = Path(path)
        if not eligible(path) or not eligible(path.resolve()):
            raise ValueError('excluded input')
        watched.add(path)
        if lint and path.is_file():
            entries.setdefault((str(path.resolve()), path.name), path)
    for name in INSTRUCTIONS:
        for path in root.rglob(name):
            if eligible(path):
                add(path)
    for skill in root.rglob('SKILL.md'):
        if not eligible(skill):
            continue
        add(skill)
        for resource in skill.parent.rglob('*'):
            if resource.is_file() and eligible(resource) and resource.suffix in EXTENSIONS:
                add(resource, lint=False)
    # Also monitor KB-local configuration/rules, without ever discovering .env files.
    for directory in [root] + [p.parent for p in root.rglob('AGENTS.md') if eligible(p)]:
        for rel in ['.codex/config.toml', '.claude/settings.json', '.claude/settings.local.json', '.mcp.json']:
            add(directory / rel)
        rules = directory / '.claude/rules'
        if rules.is_dir():
            for path in rules.rglob('*.md'):
                add(path)
    for rel in ['.codex/AGENTS.md', '.codex/AGENTS.override.md', '.codex/config.toml', '.claude/CLAUDE.md', '.claude/settings.json', '.claude/settings.local.json']:
        add(runtime_home / rel)
    rules = runtime_home / '.claude/rules'
    if rules.is_dir():
        for path in rules.rglob('*.md'):
            add(path)
    # User skill links are settings too. Avoid installed system/plugin catalogs.
    for rel in ['.codex/skills', '.claude/skills', '.agents/skills']:
        directory = runtime_home / rel
        add(directory, lint=False)
        if directory.is_dir():
            for child in directory.iterdir():
                if child.name.startswith('.') or not (child / 'SKILL.md').is_file():
                    continue
                add(child, lint=False)
                add(child / 'SKILL.md')
                for resource in child.rglob('*'):
                    if resource.is_file() and eligible(resource) and resource.suffix in EXTENSIONS:
                        add(resource, lint=False)
    add(root / '.agnix.toml', lint=False)
    add(root / 'general/knowledge/README.md', lint=False)
    for name in ['agent_lint.py', 'ai-sync.sh']:
        add(root / 'general/scripts' / name, lint=False)
    for item in extra:
        path = Path(item).expanduser().absolute()
        if path.is_dir():
            found = False
            for name in INSTRUCTIONS | {'SKILL.md'}:
                for candidate in path.rglob(name):
                    if eligible(candidate):
                        add(candidate); found = True
                        if name == 'SKILL.md':
                            for resource in candidate.parent.rglob('*'):
                                if resource.is_file() and eligible(resource) and resource.suffix in EXTENSIONS:
                                    add(resource, lint=False)
            if not found:
                raise ValueError('no instruction or skill files in additional directory')
        elif path.is_file():
            add(path)
        else:
            raise ValueError('additional input does not exist')
    return watched, sorted(entries.values(), key=str)


def snapshot(watched):
    result = {}
    for path in sorted(watched, key=str):
        result[str(path)] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
                             'link': os.readlink(str(path)) if path.is_symlink() else None}
    return result


def atomic_json(path, data):
    fd, temporary = tempfile.mkstemp(prefix=path.name+'.', dir=str(path.parent))
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as handle:
            json.dump(data, handle, indent=2); handle.write('\n')
        os.replace(temporary, str(path))
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def check(args):
    watched, entries = discover(args.root, args.runtime_home, args.paths)
    executable = args.agnix or str(args.runtime_home / '.local/share/agnix/v0.59.0/agnix')
    if not Path(executable).is_file():
        if args.agnix:
            executable = shutil.which(args.agnix)
        else:
            executable = shutil.which('agnix')
    if not executable:
        print('agent-lint: NOT CHECKED: agnix missing; install the documented version; retry remains pending')
        return 1
    executable = str(Path(executable).resolve())
    watched.add(Path(executable))
    before = snapshot(watched)
    state_path = args.state_dir / 'success.json'
    try:
        previous = json.loads(state_path.read_text()) if state_path.exists() else None
    except (ValueError, OSError):
        previous = None
    if not args.force and isinstance(previous, dict) and previous.get('schema') == 1 and previous.get('inputs') == before:
        return 0
    if not entries:
        print('agent-lint: NOT CHECKED: no supported inputs')
        return 1
    command = [executable, '--format', 'json'] + [str(p) for p in entries]
    try:
        process = subprocess.run(command, cwd=str(args.root), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, timeout=args.timeout)
        raw = json.loads(process.stdout)
        diagnostics = raw['diagnostics']
        if not isinstance(diagnostics, list) or process.returncode not in (0, 1) or not isinstance(raw.get('files_checked'), int) or raw['files_checked'] < 1:
            raise ValueError('invalid result')
        # Never persist raw settings, source snippets or linter messages (may contain secrets).
        safe = []
        for item in diagnostics:
            if not isinstance(item, dict) or item.get('level') not in ('error', 'warning', 'info'):
                raise ValueError('unknown diagnostic severity')
            safe.append({k: item.get(k) for k in ('level', 'rule', 'file', 'line', 'column')})
        # An executable can exit1 for a crash too; require real diagnostics in that case.
        if process.returncode == 1 and not safe:
            raise ValueError('failed without diagnostics')
    except (subprocess.TimeoutExpired, ValueError, KeyError, TypeError, OSError):
        print('agent-lint: NOT CHECKED: execution/timeout/JSON failure; success state retained; retry pending')
        return 1
    counts = {level: sum(d['level'] == level for d in safe) for level in ('error', 'warning', 'info')}
    report = {'version': raw.get('version'), 'files_checked': raw.get('files_checked'),
              'counts': counts, 'diagnostics': safe, 'exit': process.returncode}
    atomic_json(args.state_dir / 'report.json', report)
    print('agent-lint: {} files; {} errors, {} warnings, {} info; report {}'.format(
        raw['files_checked'], counts['error'], counts['warning'], counts['info'], args.state_dir / 'report.json'))
    if counts['error'] or process.returncode:
        print('agent-lint: findings require review; no successful checkpoint saved; retry pending')
        return 1
    after_watched, _ = discover(args.root, args.runtime_home, args.paths)
    after_watched.add(Path(executable))
    if snapshot(after_watched) != before:
        print('agent-lint: inputs changed during check; no successful checkpoint saved; retry pending')
        return 1
    atomic_json(state_path, {'schema': 1, 'inputs': before})
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', help='additional repository files or instruction/skill directories')
    parser.add_argument('--root', type=Path, default=Path(os.environ.get('AI_ROOT', str(Path.home() / 'ai'))))
    parser.add_argument('--runtime-home', type=Path, default=Path.home(), help='override only for isolated tests/other profiles')
    parser.add_argument('--state-dir', type=Path, default=Path(os.environ.get('AI_LINT_STATE_DIR', str(Path.home() / 'ai-data/agnix'))))
    parser.add_argument('--agnix', help='executable override, otherwise pinned install then PATH')
    parser.add_argument('--force', action='store_true', help='check even if successful input hashes are unchanged')
    parser.add_argument('--timeout', type=float, default=30)
    args = parser.parse_args()
    args.root = args.root.expanduser().absolute()
    args.runtime_home = args.runtime_home.expanduser().absolute()
    args.state_dir = args.state_dir.expanduser().absolute()
    try:
        args.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        with (args.state_dir / 'check.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                print('agent-lint: NOT CHECKED: another check is running; retry pending')
                return 1
            return check(args)
    except (OSError, ValueError):
        print('agent-lint: NOT CHECKED: input/state access failure; retry pending')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
