#!/usr/bin/env python3
"""Find/inspect a local GitLab checkout; explicitly clone/fetch or bind a proposal to its diff.

Default inspect is local-only. No staging, commits, push, switching or remote writes.
Snapshots detect changes; they are not approval tokens. See --help for usage.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from urllib.parse import urlsplit

HOST = 'gitlab.youdo.sg'
CURRENT = Path.home() / 'ai/current'


def git(repo, *args, optional=False):
    result = subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=dict(os.environ, GIT_TERMINAL_PROMPT='0',
                                                           GIT_OPTIONAL_LOCKS='0'))
    if result.returncode and not optional:
        # Git errors may include credential-bearing origins. Do not echo raw stderr.
        raise ValueError('git {} failed (exit {}); inspect locally'.format(args[0], result.returncode))
    return result.stdout if result.returncode == 0 else b''


def project_path(value):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+', value):
        raise ValueError('Use a full GitLab group/project path')
    if any(part in ('.', '..') for part in value.split('/')):
        raise ValueError('Invalid project path')
    return value


def origin_project(url):
    """Return project only for this host; never emit origin credentials."""
    if '://' in url:
        parsed = urlsplit(url)
        if parsed.hostname != HOST or parsed.scheme not in ('ssh', 'https', 'http'):
            return None
        path = parsed.path.strip('/')
    else:
        match = re.fullmatch(r'(?:[^@\s]+@)?' + re.escape(HOST) + r':(.+)', url)
        if not match:
            return None
        path = match.group(1).strip('/')
    return path[:-4] if path.endswith('.git') else path


def origin(repo):
    return git(repo, 'remote', 'get-url', 'origin', optional=True).decode().strip()


def origin_urls(repo, push=False):
    flags = ('--push', '--all') if push else ('--all',)
    return git(repo, 'remote', 'get-url', *flags, 'origin').decode().splitlines()


def verify_repo(repo, project):
    repo = Path(repo).expanduser().resolve()
    root = git(repo, 'rev-parse', '--show-toplevel').decode().strip()
    if Path(root).resolve() != repo:
        raise ValueError('Expected the checkout root, not a parent repository/subdirectory')
    fetch_urls = origin_urls(repo)
    if not fetch_urls or any(origin_project(url) != project for url in fetch_urls):
        raise ValueError('Origin does not match the requested GitLab project; no mutation allowed')
    push_urls = origin_urls(repo, push=True)
    if not push_urls or any(origin_project(url) != project for url in push_urls):
        raise ValueError('Origin push URL points to another project; inspect before publication')
    return repo


def registry_rows(registry):
    if registry.exists():
        for line in registry.read_text().splitlines():
            if line.startswith('|'):
                fields = [x.strip().strip('`') for x in line.split('|')[1:-1]]
                if len(fields) >= 2 and fields[0].startswith(('/', '~/')):
                    yield Path(fields[0]).expanduser(), fields[1]


def locate(project, root, registry, explicit=None):
    if explicit:
        return verify_repo(explicit, project)
    candidates = set()
    # Consult the catalog before scanning immediate checkout directories.
    for path, url in registry_rows(registry):
        if origin_project(url) == project and path.exists():
            candidates.add(verify_repo(path, project))
    if root.exists():
        for path in root.iterdir():
            if path.is_dir() and (path / '.git').exists() and origin_project(origin(path)) == project:
                candidates.add(verify_repo(path, project))
    if len(candidates) > 1:
        raise ValueError('Multiple matching checkouts; choose one explicitly with --repo')
    return next(iter(candidates), None)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def status_entries(repo):
    parts = iter(git(repo, 'status', '--porcelain=v1', '-z', '--untracked-files=all', '--ignore-submodules=none').split(b'\0'))
    entries = []
    for part in parts:
        if not part:
            continue
        code = part[:2].decode()
        item = {'status': code, 'path': os.fsdecode(part[3:])}
        if 'R' in code or 'C' in code:
            item['from'] = os.fsdecode(next(parts))
        entries.append(item)
    return entries


def repo_state(repo):
    entries = status_entries(repo)
    untracked = []
    for entry in entries:
        if entry['status'] != '??':
            continue
        path = repo / entry['path']
        h = hashlib.sha256()
        if path.is_symlink():
            h.update(os.fsencode(os.readlink(path)))
        else:
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(chunk)
        untracked.append([entry['path'], stat.S_IMODE(path.lstat().st_mode), h.hexdigest()])
    diff_args = ('--binary', '--no-ext-diff', '--no-textconv', '--ignore-submodules=none')
    return {'head': git(repo, 'rev-parse', 'HEAD').decode().strip(),
            'branch': git(repo, 'symbolic-ref', '--short', '-q', 'HEAD', optional=True).decode().strip() or None,
            'origin_hash': digest(json.dumps(origin_urls(repo)).encode()),
            'push_origin_hash': digest(json.dumps(origin_urls(repo, push=True)).encode()),
            'status': entries,
            'tracked_diff_hash': digest(git(repo, 'diff', *diff_args, 'HEAD', '--')),
            'staged_diff_hash': digest(git(repo, 'diff', '--cached', *diff_args, '--')),
            'untracked': untracked}


def ensure_clean_submodules(repo):
    for entry in git(repo, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry.startswith(b'160000 '):
            continue
        path = repo / os.fsdecode(entry.split(b'\t', 1)[1])
        if (path / '.git').exists() and status_entries(path):
            raise ValueError('Dirty submodule cannot be snapshotted safely; preserve its changes and resolve scope first')


def proposal_state(repo, project, proposal_file):
    raw = proposal_file.read_bytes()
    proposal = json.loads(raw)
    required = ('project', 'source', 'target', 'base_ref', 'task_paths', 'commit_message',
                'title', 'body_file', 'checks', 'ci_effects')
    if any(not proposal.get(key) for key in required):
        raise ValueError('Proposal requires: ' + ', '.join(required))
    if proposal['project'] != project:
        raise ValueError('Proposal project mismatch')
    if not isinstance(proposal['task_paths'], list):
        raise ValueError('task_paths must be a list of explicit relative paths')
    for path in proposal['task_paths']:
        if not isinstance(path, str) or not path or Path(path).is_absolute() or '..' in Path(path).parts or '.git' in Path(path).parts or path.startswith(':'):
            raise ValueError('Unsafe task path')
    body_path = Path(proposal['body_file']).expanduser()
    if not body_path.is_absolute():
        body_path = proposal_file.parent / body_path
    ensure_clean_submodules(repo)
    state = repo_state(repo)
    if state['branch'] != proposal['source']:
        raise ValueError('Current branch differs from the proposed source')
    if any('U' in entry['status'] or entry['status'] in ('AA', 'DD') for entry in state['status']):
        raise ValueError('Resolve the checkout conflict before publication preparation')
    base = git(repo, 'rev-parse', '--verify', '--end-of-options', proposal['base_ref'] + '^{commit}').decode().strip()
    target = git(repo, 'rev-parse', '--verify', '--end-of-options', 'refs/remotes/origin/' + proposal['target'] + '^{commit}').decode().strip()
    return {'schema': 1, 'repo': str(repo), 'project': project, 'state': state,
            'proposal_hash': digest(raw), 'body_hash': digest(body_path.read_bytes()),
            'base_sha': base, 'target_sha': target}


def register(registry, repo, project, purpose, system):
    if not registry.exists():
        raise ValueError('Repository catalog not found; register manually after cloning')
    for path, url in registry_rows(registry):
        if path.resolve() == repo:
            if origin_project(url) != project:
                raise ValueError('Catalog maps this checkout to another project; reconcile manually')
            return
    from datetime import date
    fields = [str(repo), 'git@' + HOST + ':' + project + '.git', purpose, system, date.today().isoformat()]
    if any('\n' in value or '|' in value or '`' in value for value in fields):
        raise ValueError('Invalid catalog field; register manually')
    lines = registry.read_text().splitlines(keepends=True)
    header = next((i for i, line in enumerate(lines) if line.startswith('| Path | Origin |')), None)
    if header is None:
        raise ValueError('Repository catalog table header not found; register manually')
    end = header + 1
    while end < len(lines) and lines[end].startswith('|'):
        end += 1
    lines.insert(end, '| `{}` | `{}` | {} | {} | {} |\n'.format(*fields))
    registry.write_text(''.join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['inspect', 'clone', 'refresh', 'snapshot', 'check'])
    parser.add_argument('--project', required=True, type=project_path)
    parser.add_argument('--repo', type=Path, help='Explicit checkout; origin must match')
    parser.add_argument('--root', type=Path, default=Path.home() / 'git')
    parser.add_argument('--registry', type=Path, default=CURRENT / 'knowledge/repos.md')
    parser.add_argument('--purpose', default='Project source checkout')
    parser.add_argument('--system', default='gitlab-ci')
    parser.add_argument('--record', type=Path, help='Snapshot JSON outside the checkout; never grants permission')
    parser.add_argument('--proposal-file', type=Path, help='Publication proposal JSON; see skill reference')
    args = parser.parse_args()
    repo = locate(args.project, args.root.expanduser(), args.registry.expanduser(), args.repo)
    if args.phase == 'clone':
        if repo is None:
            repo = (args.root.expanduser() / args.project.rsplit('/', 1)[-1]).resolve()
            if repo.exists() or repo.is_symlink():
                raise ValueError('Clone destination occupied; do not overwrite it')
            for path, url in registry_rows(args.registry):
                if path.resolve() == repo and origin_project(url) != args.project:
                    raise ValueError('Catalog reserves clone destination for another project')
            repo.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(['git', 'clone', '--', 'git@' + HOST + ':' + args.project + '.git', str(repo)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    env=dict(os.environ, GIT_TERMINAL_PROMPT='0'))
            if result.returncode:
                raise ValueError('Clone failed; inspect the destination before retrying; no cleanup performed')
            repo = verify_repo(repo, args.project)
        register(args.registry, repo, args.project, args.purpose, args.system)
    if repo is None:
        print(json.dumps({'project': args.project, 'found': False, 'next_action': 'clone'}))
        return 1
    if args.phase == 'refresh':
        git(repo, 'fetch', 'origin')  # Never pull, prune, checkout or merge.
    if args.phase in ('snapshot', 'check'):
        if not args.record or not args.proposal_file:
            parser.error('snapshot/check require --record and --proposal-file')
        if repo == args.record.resolve() or repo in args.record.resolve().parents:
            raise ValueError('Keep snapshots outside the checkout')
        state = proposal_state(repo, args.project, args.proposal_file.resolve())
        if args.phase == 'snapshot':
            args.record.parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(str(args.record), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w') as stream:
                json.dump(state, stream, sort_keys=True, ensure_ascii=True)
                stream.write('\n')
        elif json.loads(args.record.read_text()) != state:
            raise ValueError('Checkout, proposal, body or base/target changed; inspect and renew approval as needed')
        print(json.dumps({'repo': str(repo), 'project': args.project, 'matches': True,
                          'record': str(args.record), 'grants_approval': False}))
        return 0
    entries = status_entries(repo)
    branch = git(repo, 'symbolic-ref', '--short', '-q', 'HEAD', optional=True).decode().strip() or None
    upstream = git(repo, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}', optional=True).decode().strip() or None
    divergence = git(repo, 'rev-list', '--left-right', '--count', 'HEAD...@{upstream}', optional=True).decode().split()
    print(json.dumps({'repo': str(repo), 'project': args.project, 'found': True,
                      'origin': 'git@' + HOST + ':' + args.project + '.git', 'branch': branch,
                      'head': git(repo, 'rev-parse', 'HEAD').decode().strip(), 'upstream': upstream,
                      'ahead': int(divergence[0]) if divergence else None,
                      'behind': int(divergence[1]) if divergence else None,
                      'changes': entries[:50], 'change_count': len(entries), 'truncated': len(entries) > 50,
                      'network_refresh': args.phase == 'refresh'}, ensure_ascii=True))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        # OSError filenames may be sensitive; expose type only.
        print(json.dumps({'error': str(error) if isinstance(error, ValueError) else type(error).__name__}))
        sys.exit(2)
