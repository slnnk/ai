#!/usr/bin/env python3
"""Task metrics in existing KB notes; daily snapshots and review receipts outside Git.

No model calls, scheduling, transcript copying or automatic policy edits.
record updates one stable task ID; prepare does not mean reviewed.
"""
import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

import agent_learning as learning

MARKER = '```agent-task-metrics-json\n'
BLOCK = re.compile(re.escape(MARKER) + r'(.*?)\n```', re.S)
OUTCOMES = ('unknown', 'pass', 'fail')
COUNTS = ('corrections', 'unnecessary_actions', 'critical_events', 'tokens', 'active_seconds')


def stamp():
    return dt.datetime.now().astimezone().isoformat()


def today():
    return dt.datetime.now().astimezone().date()


def note_path(root, value):
    path = Path(value.split('#', 1)[0]).expanduser()
    path = (path if path.is_absolute() else root / path).resolve(strict=True)
    try:
        path.relative_to(root.resolve())
    except ValueError:
        raise learning.Invalid('source must be within the KB')
    if path.suffix != '.md':
        raise learning.Invalid('source must be an existing Markdown note within the KB')
    if path.parent not in [(root / layer / 'knowledge/log').resolve() for layer in ('personal', 'current')]:
        raise learning.Invalid('source must be an existing personal/current task log')
    return path


def validate(data):
    if not isinstance(data, dict):
        raise learning.Invalid('task metrics must be an object')
    if data.get('version') != 1 or not re.fullmatch(r'[a-zA-Z0-9_.:-]{1,160}', data.get('task_id', '')):
        raise learning.Invalid('invalid task metric identity')
    if data.get('state') not in ('open', 'closed') or data.get('first_result') not in OUTCOMES:
        raise learning.Invalid('invalid task state or first result')
    if data.get('final_result') not in (*OUTCOMES, 'partial'):
        raise learning.Invalid('invalid final result')
    for key in COUNTS:
        value = data.get(key)
        if value is not None and (type(value) is not int or value < 0):
            raise learning.Invalid('invalid counter: ' + key)
    for key in ('created', 'updated'):
        dt.datetime.fromisoformat(data[key])
    if not data.get('evidence'):
        raise learning.Invalid('evidence reference required, including for unknown outcomes')
    learning.reject_secrets(data)


def tasks(root):
    found = {}
    for layer in ('personal', 'current'):
        folder = root / layer / 'knowledge' / 'log'
        if not folder.is_dir():
            raise learning.Invalid('missing task evidence root: ' + str(folder))
        for path in sorted(folder.glob('*.md')):
            text = path.read_text()
            matches = list(BLOCK.finditer(text))
            if text.count(MARKER) != len(matches):
                raise learning.Invalid('unterminated metrics block: ' + str(path))
            for match in matches:
                data = json.loads(match[1])
                validate(data)
                key = data['task_id']
                if key in found:
                    raise learning.Invalid('duplicate task ID: ' + key)
                found[key] = (path, data)
    return found


def record(root, args):
    path = note_path(root, args.source)
    inventory = tasks(root)
    existing = inventory.get(args.task_id)
    if existing and existing[0].resolve() != path:
        raise learning.Invalid('task already belongs to another note')
    old = existing[1] if existing else None
    data = dict(old) if old else dict(version=1, task_id=args.task_id, created=stamp(),
                                     first_result='unknown', final_result='unknown', state='open',
                                     kind='unknown', model='unknown', session_id='unknown',
                                     **{key: None for key in COUNTS})
    for key in ('state', 'first_result', 'final_result', 'kind', 'model', 'session_id', 'evidence', *COUNTS):
        value = getattr(args, key)
        if value is not None:
            data[key] = value
    if old and old['first_result'] != 'unknown' and data['first_result'] == 'unknown':
        raise learning.Invalid('do not erase an evidenced first-attempt result')
    if old and old['first_result'] == 'fail' and data['first_result'] != 'fail':
        raise learning.Invalid('retain failed first attempt; record recovery in final_result')
    if old and all(old.get(k) == v for k, v in data.items()):
        print('agent-metrics: unchanged task ' + args.task_id)
        return
    data['updated'] = stamp()
    validate(data)
    text = path.read_text()
    payload = MARKER + json.dumps(data, indent=2, ensure_ascii=False) + '\n```'
    if old:
        text = BLOCK.sub(lambda m: payload if json.loads(m[1])['task_id'] == args.task_id else m[0], text)
    else:
        text = text.rstrip() + '\n\n## Task metrics: ' + args.task_id + '\n\n' + payload + '\n'
    learning.atomic_write(path, text)
    print('agent-metrics: recorded task ' + args.task_id)


def local_day(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone().date()


def snapshot(root, start, end):
    inventory = tasks(root)
    selected = [dict(d, source=str(p.relative_to(root))) for p, d in inventory.values()
                if start <= local_day(d['updated']) < end]
    closed = [d for d in selected if d['state'] == 'closed']
    events = []
    for path, rule in learning.records(root):
        for event in rule['evaluations']:
            if start <= local_day(event['at']) < end:
                events.append(dict(key=rule['key'], outcome=event['outcome'], at=event['at'],
                                   source=event['source'], rule_loaded=event['rule_loaded'],
                                   cause=event.get('cause', ''), record=str(path.relative_to(root)),
                                   current_revision=event['revision'] == rule['revision']))
    counts = {}
    for key in COUNTS:
        known = [d[key] for d in closed if d[key] is not None]
        counts[key] = dict(total=sum(known) if known else None, assessed=len(known), eligible=len(closed))
    return dict(version=1, generated=stamp(), start=str(start), end_exclusive=str(end),
                tasks=selected, rule_evaluations=events,
                summary=dict(recorded_tasks=len(inventory), changed_tasks=len(selected), closed_tasks=len(closed),
                             first_result=dict(Counter(d['first_result'] for d in closed)),
                             final_result=dict(Counter(d['final_result'] for d in closed)), counts=counts),
                limits=['Task coverage outside recorded notes is unknown; absence is not success.',
                        'Changed task snapshots are not new independent trials; do not sum daily task counts.',
                        'Rule evaluation events are not unique tasks or independently graded outcomes.',
                        'Counts are evidence-backed agent observations, not automatic semantic judgments.',
                        'Token/time fields are unknown unless attributable evidence was supplied.'])


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def prepare(root, data_dir):
    state_path = data_dir / 'state.json'
    state = read_json(state_path, {})
    date = today()
    if state.get('reviewed_on') == str(date):
        return
    pending = read_json(data_dir / 'pending.json')
    if not pending:
        start = dt.date.fromisoformat(state['end_exclusive']) if state else date - dt.timedelta(days=7)
        if start >= date:
            return
        report = snapshot(root, start, date)
        report_path = data_dir / ('snapshot-' + str(date) + '.json')
        learning.atomic_write(report_path, json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        # Reuse existing resource accounting; its rolling session cohort is NOT a calendar-day/task total.
        usage_path = data_dir / ('usage-' + str(date) + '.txt')
        try:
            usage = subprocess.run(['python3', '-B', str(root / 'general/scripts/token_usage.py'),
                                    '--days', '7', '--brief'], capture_output=True, text=True, timeout=30)
            usage_text = ('Rolling 7-day session-cohort reference; not the snapshot interval or task cost.\n'
                          + (usage.stdout if usage.returncode == 0 else 'Usage collection unavailable.\n'))
        except (OSError, subprocess.TimeoutExpired):
            usage_text = 'Usage collection unavailable; task cost remains unknown.\n'
        learning.atomic_write(usage_path, usage_text)
        pending = dict(snapshot=str(report_path), sha256=digest(report_path), usage=str(usage_path),
                       start=str(start), end_exclusive=str(date))
        learning.atomic_write(data_dir / 'pending.json', json.dumps(pending, indent=2) + '\n')
    if not Path(pending['snapshot']).is_file() or digest(Path(pending['snapshot'])) != pending['sha256']:
        raise learning.Invalid('pending snapshot missing or changed; do not mark reviewed')
    print('agent-metrics: daily analysis pending: ' + pending['snapshot'])
    print('agent-metrics: usage reference: ' + pending['usage'])
    print('agent-metrics: follow agent-learning Daily metrics; save findings before complete; sha256=' + pending['sha256'])


def complete(root, data_dir, source):
    pending = read_json(data_dir / 'pending.json')
    if not pending:
        raise learning.Invalid('no pending daily review')
    if digest(Path(pending['snapshot'])) != pending['sha256']:
        raise learning.Invalid('snapshot changed since preparation')
    path = note_path(root, source)
    text = path.read_text()
    if pending['sha256'] not in text or any('\n## ' + h + '\n' not in text for h in ('Findings', 'Actions', 'Limits')):
        raise learning.Invalid('review note must reference snapshot hash and contain Findings, Actions, Limits')
    if len(text.strip()) < 300:
        raise learning.Invalid('review note is empty or incomplete')
    receipt = dict(pending, reviewed_on=str(today()), source=str(path.relative_to(root)), completed=stamp())
    learning.atomic_write(data_dir / ('review-' + str(today()) + '.json'), json.dumps(receipt, indent=2) + '\n')
    learning.atomic_write(data_dir / 'state.json', json.dumps(receipt, indent=2) + '\n')
    (data_dir / 'pending.json').unlink()
    print('agent-metrics: daily review recorded: ' + str(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.home() / 'ai')
    parser.add_argument('--data-dir', type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    rec = sub.add_parser('record')
    for key in ('task-id', 'source', 'evidence'):
        rec.add_argument('--' + key, required=True)
    rec.add_argument('--state', choices=('open', 'closed'))
    rec.add_argument('--first-result', choices=OUTCOMES)
    rec.add_argument('--final-result', choices=(*OUTCOMES, 'partial'))
    for key in ('kind', 'model', 'session-id'):
        rec.add_argument('--' + key)
    for key in COUNTS:
        rec.add_argument('--' + key.replace('_', '-'), type=int)
    sub.add_parser('prepare')
    sub.add_parser('status')
    done = sub.add_parser('complete')
    done.add_argument('--source', required=True)
    args = parser.parse_args(argv)
    root = args.root.expanduser().absolute()
    default_data = (Path.home() / 'ai-data/agent-metrics' if root.resolve() == (Path.home() / 'ai').resolve()
                    else root.parent / (root.name + '-metrics'))
    data_dir = args.data_dir or default_data
    try:
        if args.command == 'status':
            print(json.dumps(dict(state=read_json(data_dir / 'state.json'),
                                  pending=read_json(data_dir / 'pending.json')), indent=2))
            return 0
        with learning.locked(root):
            if args.command == 'record':
                record(root, args)
            elif args.command == 'prepare':
                prepare(root, data_dir)
            else:
                complete(root, data_dir, args.source)
        return 0
    except (learning.Invalid, OSError, ValueError, KeyError, TypeError) as error:
        print('agent-metrics: ERROR: ' + str(error))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
