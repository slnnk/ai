#!/usr/bin/env python3
"""Preview ai-sync changes using disposable Git index and object storage.

Usage: ai_sync_preview.py [--root PATH]
Rebuilds knowledge indexes in memory, stages the current working tree only in
private temporary storage and prints the proposed changes. Does not generate
weekly usage reports/monthly reminders, commit, pull, push or change sync state.
"""
import argparse
from collections import Counter
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# Prevent imports from writing __pycache__ in the knowledge repository.
sys.dont_write_bytecode = True
import build_index


def git(root, *args, env=None, data=None):
    return subprocess.check_output(
        ['git', '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false', *args],
        cwd=str(root), env=env, input=data,
    )


def preview(root):
    root = root.resolve()
    if Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel')).strip()).resolve() != root:
        raise ValueError('--root must be the knowledge repository root')
    index = Path(os.fsdecode(git(root, 'rev-parse', '--git-path', 'index')).strip())
    objects = Path(os.fsdecode(git(root, 'rev-parse', '--git-path', 'objects')).strip())
    if not index.is_absolute():
        index = root / index
    if not objects.is_absolute():
        objects = root / objects
    # Even reading a split index can refresh the shared index's mtime.
    # Detect its files directly, before any Git command that loads the index.
    if any(index.parent.glob('sharedindex.*')):
        raise ValueError('split Git indexes are not supported by the read-only preview')
    with tempfile.TemporaryDirectory(prefix='ai-sync-preview-') as directory:
        temporary = Path(directory)
        private_index, private_objects = temporary / 'index', temporary / 'objects'
        # Git may refresh mtimes of existing objects even through read-only
        # alternates. Copy objects (never hardlink) to isolate those writes too.
        alternates = objects / 'info/alternates'
        if os.environ.get('GIT_ALTERNATE_OBJECT_DIRECTORIES') or (alternates.exists() and alternates.read_text().strip()):
            raise ValueError('external object alternates are not supported by the read-only preview')
        shutil.copytree(str(objects), str(private_objects))
        if index.exists():
            shutil.copyfile(str(index), str(private_index))
        env = dict(os.environ, GIT_INDEX_FILE=str(private_index),
                   GIT_OBJECT_DIRECTORY=str(private_objects), GIT_OPTIONAL_LOCKS='0')
        env.pop('GIT_ALTERNATE_OBJECT_DIRECTORIES', None)
        git(root, 'add', '-A', env=env)
        for layer_name in build_index.DEFAULT_LAYERS:
            layer = root / layer_name
            knowledge = layer / 'knowledge'
            if not knowledge.is_dir():
                continue
            notes, missing = build_index.collect(knowledge)
            content = build_index.render(layer.resolve().name, notes, missing).encode('utf-8')
            target = (knowledge / 'INDEX.md').resolve()
            # Match normal generation, including current -> companies/<name>.
            relative = target.relative_to(root).as_posix()
            blob = git(root, 'hash-object', '-w', '--stdin', env=env, data=content).decode().strip()
            git(root, 'update-index', '--add', '--cacheinfo', '100644', blob, relative, env=env)
        raw = git(root, 'diff', '--cached', '--name-status', '--no-renames', '-z', env=env)
        fields = raw.split(b'\0')
        changes = [(os.fsdecode(fields[i]), os.fsdecode(fields[i + 1]))
                   for i in range(0, len(fields) - 1, 2)]
        counts = Counter(status for status, _ in changes)
        print('ai-sync: dry run: {} added, {} modified, {} deleted'.format(
            counts['A'], counts['M'], counts['D']))
        for status, path in changes:
            # repr avoids ambiguous multiline filenames and terminal control chars.
            print('  {}\t{}'.format(status, repr(path)))
        print('ai-sync: indexes rebuilt in memory; working files, staging, objects and sync state unchanged')
        print('ai-sync: weekly usage reports and monthly TODO updates are not generated in this preview')
        return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(os.environ.get('AI_ROOT', Path.home() / 'ai')))
    args = parser.parse_args()
    try:
        return preview(args.root)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print('ai-sync: preview failed: {}'.format(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
