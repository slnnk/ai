#!/usr/bin/env python3
"""Record agent corrections and retrieve scoped evidence (standard library only).

Examples:
  agent_learning.py record --key respect-discussion --event-id session-1-msg-4 \\
    --scope global --system agents --kind explicit --summary 'Respect discussion mode' \\
    --expected 'Wait for implementation authorization' --source 'session:1/message:4'
  agent_learning.py query --scope global discussion
  agent_learning.py report

Canonical targets are references only: this tool never edits policy or executes sources.
Queries default to global records, plus exact repo records when --repo is supplied.
Explicit --scope current/personal includes that scope, matching repo layer, and globals.
Active global rules bypass keyword/system filters; candidates follow keywords.
resolve records actual user decisions; its --source must identify that authorization.
Secret detection rejects basic obvious patterns; it is not exhaustive.
Writer locks persist in the OS temporary directory, keyed by user and resolved KB root;
they are not KB content and must not be unlinked while writers may be active.
"""
import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SECRET = re.compile(r'(?i)bearer\s+[a-z0-9._~+/=-]{8,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?:password|passwd|token|secret)\s*[=:]\s*[\"\']?(?!\$|<)[^\s\"\']{6,}|glpat-[a-z0-9_-]{15,}|gh[pousr]_[a-z0-9]{30,}')
MARKER = '```agent-learning-json\n'


class Invalid(ValueError):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def reject_secrets(value):
    if SECRET.search(json.dumps(value, ensure_ascii=False)):
        raise Invalid('obvious secret pattern detected; redact input before recording')


def target_ref(value):
    path, sep, fragment = value.partition('#')
    p = Path(path).expanduser().resolve(strict=True)
    if p.suffix.lower() != '.md' or not p.is_file():
        raise Invalid('canonical target must be an existing Markdown file')
    with p.open(encoding='utf-8') as stream:
        stream.read(1)
    return str(p) + (sep + fragment if sep else '')


def identity(data):
    return tuple(data[k] for k in ('layer', 'key', 'scope', 'repo', 'task_id'))


def validate(d, check_target=True):
    required = {'version', 'key', 'scope', 'layer', 'repo', 'system', 'kind', 'summary',
                'expected', 'task_id', 'target', 'occurrences', 'evaluations', 'created', 'updated', 'decisions', 'revision'}
    if not isinstance(d, dict) or not required <= d.keys() or d['version'] != 1:
        raise Invalid('invalid record schema')
    for key in ('key', 'system'):
        if not isinstance(d[key], str) or not SLUG.fullmatch(d[key]):
            raise Invalid('invalid ' + key)
    if d['scope'] not in ('global', 'current', 'personal', 'repo') or d['layer'] not in ('current', 'personal'):
        raise Invalid('invalid scope or layer')
    if d['kind'] not in ('explicit', 'inferred', 'task', 'fact'):
        raise Invalid('invalid kind')
    for key in ('summary', 'expected', 'created', 'updated'):
        if not isinstance(d[key], str) or not d[key].strip():
            raise Invalid('missing string field: ' + key)
    if not isinstance(d['repo'], str) or not isinstance(d['task_id'], str):
        raise Invalid('invalid applicability')
    if d['scope'] == 'global' and d['layer'] != 'personal':
        raise Invalid('global evidence belongs in personal')
    if d['scope'] in ('current', 'personal') and d['scope'] != d['layer']:
        raise Invalid('scope/layer mismatch')
    if (d['scope'] == 'repo') != bool(d['repo']):
        raise Invalid('repo applicability mismatch')
    if d['repo'] and str(Path(d['repo']).resolve()) != d['repo']:
        raise Invalid('repo must be a resolved absolute path')
    if (d['kind'] == 'task') != bool(d['task_id']):
        raise Invalid('task kind requires task-id; other kinds forbid task-id')
    if d['target']:
        if not isinstance(d['target'], str):
            raise Invalid('invalid canonical target')
        target_path = Path(d['target'].partition('#')[0])
        if not target_path.is_absolute() or target_path.suffix.lower() != '.md':
            raise Invalid('invalid canonical target path')
        if check_target and disposition(d) not in ('rejected', 'superseded') and target_ref(d['target']) != d['target']:
            raise Invalid('invalid canonical target')
    elif d['target'] is not None:
        raise Invalid('invalid canonical target')
    for collection in ('occurrences', 'evaluations'):
        if not isinstance(d[collection], list):
            raise Invalid('invalid event collection')
        ids = set()
        for event in d[collection]:
            if not isinstance(event, dict) or not all(isinstance(event.get(k), str) and event[k] for k in ('event_id', 'source', 'at')):
                raise Invalid('invalid event schema')
            if event['event_id'] in ids:
                raise Invalid('duplicate event id')
            ids.add(event['event_id'])
            if collection == 'evaluations' and (not isinstance(event.get('revision'), int) or event['revision'] < 1 or not isinstance(event.get('expected'), str) or event.get('target') is not None and not isinstance(event['target'], str)):
                raise Invalid('invalid evaluation revision snapshot')
            if collection == 'evaluations' and (event.get('outcome') not in ('pass', 'fail', 'not-applicable') or event.get('rule_loaded') not in ('yes', 'no', 'unknown')):
                raise Invalid('invalid evaluation')
    if not isinstance(d['revision'], int) or d['revision'] < 1 or not isinstance(d['decisions'], list):
        raise Invalid('invalid lifecycle schema')
    for decision in d['decisions']:
        if not isinstance(decision, dict) or decision.get('decision') not in ('adopted', 'rejected', 'superseded') or not decision.get('source') or not decision.get('at'):
            raise Invalid('invalid decision')
    if not d['occurrences']:
        raise Invalid('record has no evidence')
    reject_secrets(d)


def render(d):
    date = dt.date.today().isoformat()
    status = 'outdated' if disposition(d) in ('rejected', 'superseded') else 'hypothesis' if d['kind'] == 'inferred' and disposition(d) != 'adopted' else 'verified'
    body = json.dumps(d, ensure_ascii=False, indent=2, sort_keys=True)
    return (f'---\nsystem: {d["system"]}\nstatus: {status}\nchecked: {date}\n'
            'tags: [agents, learning]\n---\n'
            f'# Agent learning: {d["key"]}\n\n## Summary\n\n'
            'Correction evidence and scoped application history. Canonical instructions remain authoritative.\n\n'
            f'{MARKER}{body}\n```\n')


def records(root, repair=None):
    result, seen = [], set()
    for layer in ('personal', 'current'):
        folder = root / layer / 'knowledge' / 'log'
        for path in sorted(folder.glob('*-agent-learning-record-*.md')):
            try:
                text = path.read_text(encoding='utf-8')
                if text.count(MARKER) != 1:
                    raise Invalid('missing or duplicate data block')
                payload, end, _ = text.split(MARKER, 1)[1].partition('\n```')
                if not end:
                    raise Invalid('unterminated data block')
                data = json.loads(payload)
                repair_this = (repair is not None and isinstance(data, dict) and data.get('key') == repair.key
                               and data.get('scope') == repair.scope
                               and (not repair.layer or data.get('layer') == repair.layer)
                               and (not repair.repo or data.get('repo') == repo_for(repair))
                               and (not repair.task_id or data.get('task_id') == repair.task_id))
                validate(data, check_target=not repair_this)
                header = text.split('---', 2)
                if len(header) != 3 or header[0].strip():
                    raise Invalid('missing frontmatter')
                meta = dict(line.split(':', 1) for line in header[1].strip().splitlines() if ':' in line)
                meta = {k.strip(): v.strip() for k, v in meta.items()}
                if (meta.get('system') != data['system'] or meta.get('status') not in ('verified', 'hypothesis', 'outdated')
                        or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', meta.get('checked', ''))
                        or 'tags' not in meta):
                    raise Invalid('invalid frontmatter')
                if meta['status'] == 'outdated' and disposition(data) not in ('rejected', 'superseded'):
                    raise Invalid('outdated frontmatter requires resolve rejected/superseded')
                if data['layer'] != layer:
                    raise Invalid('record stored in wrong layer')
                ident = identity(data)
                if ident in seen:
                    raise Invalid('duplicate record identity')
                seen.add(ident)
                result.append((path, data))
            except (ValueError, OSError, TypeError, KeyError) as error:
                raise Invalid(f'corrupted store: {path}: {error}') from error
    return result


def layer_for(a):
    return 'personal' if a.scope == 'global' else a.scope if a.scope != 'repo' else a.layer


def repo_for(a):
    return str(Path(a.repo).expanduser().resolve()) if getattr(a, 'repo', None) else ''


def select(items, a):
    found = [(p, d) for p, d in items if d['key'] == a.key
             and (not a.scope or d['scope'] == a.scope)
             and (not a.layer or d['layer'] == a.layer)
             and (not a.repo or d['repo'] == repo_for(a))
             and (not a.task_id or d['task_id'] == a.task_id)]
    if len(found) != 1:
        raise Invalid('record missing' if not found else 'ambiguous key; specify scope/layer/repo')
    return found[0]


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.' + path.name, dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextlib.contextmanager
def locked(root):
    # Persistent user-owned lock outside the synced KB; never unlink a live lock.
    digest = hashlib.sha256(str(root).encode()).hexdigest()
    path = Path(tempfile.gettempdir()) / f'agent-learning-{os.getuid()}-{digest}.lock'
    fd = os.open(str(path), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise Invalid('unsafe lock ownership or permissions')
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def mutate(root, a):
    items = records(root, repair=a if a.command in ('link-rule', 'resolve') else None)
    stamp = now()
    if a.command == 'record':
        if not SLUG.fullmatch(a.key) or not SLUG.fullmatch(a.system):
            raise Invalid('key and system must be lowercase kebab-case')
        if a.scope == 'repo' and (not a.repo or not a.layer):
            raise Invalid('repo scope requires --repo and --layer')
        if a.scope != 'repo' and (a.repo or a.layer):
            raise Invalid('--repo and --layer are only for repo scope')
        if (a.kind == 'task') != bool(a.task_id):
            raise Invalid('use --task-id exactly for task kind')
        layer = layer_for(a)
        repo = repo_for(a)
        target = target_ref(a.target) if a.target else None
        ident = (layer, a.key, a.scope, repo, a.task_id)
        existing = [(p, d) for p, d in items if identity(d) == ident]
        if existing:
            path, d = existing[0]
            same = [e for e in d['occurrences'] if e['event_id'] == a.event_id]
            if same:
                if any(same[0].get(k) != v for k, v in [('source', a.source), ('summary', a.summary), ('expected', a.expected), ('cause', a.cause)]):
                    raise Invalid('event id already has different content')
                print('unchanged: event already recorded')
                return
            if d['summary'] != a.summary or d['expected'] != a.expected:
                raise Invalid('correction wording changed; use resolve with summary/expected first')
            if any(d[k] != v for k, v in [('kind', a.kind), ('system', a.system), ('task_id', a.task_id)]):
                raise Invalid('existing identity has different kind/system/task; use another key')
            if target and d['target'] != target:
                raise Invalid('use link-rule to change canonical target')
        else:
            d = dict(version=1, key=a.key, scope=a.scope, layer=layer, repo=repo,
                     system=a.system, kind=a.kind, summary=a.summary, expected=a.expected,
                     task_id=a.task_id, target=target, occurrences=[], evaluations=[], decisions=[], revision=1, created=stamp, updated=stamp)
            digest = hashlib.sha256(json.dumps(ident).encode()).hexdigest()[:20]
            path = root / layer / 'knowledge' / 'log' / f'{stamp[:10]}-{a.system}-agent-learning-record-{a.key}-{digest}.md'
        d['occurrences'].append(dict(event_id=a.event_id, source=a.source, agent=a.agent,
                                     summary=a.summary, expected=a.expected, cause=a.cause, at=stamp))
    else:
        path, d = select(items, a)
        if a.command == 'resolve':
            if a.decision == 'adopted' and not (a.target or d['target']):
                raise Invalid('adopted decision requires canonical target')
            d['revision'] += 1
            if a.target:
                d['target'] = target_ref(a.target)
            if a.summary:
                d['summary'] = a.summary
            if a.expected:
                d['expected'] = a.expected
            d['decisions'].append(dict(decision=a.decision, source=a.source, at=stamp, revision=d['revision'], target=d['target'], expected=d['expected']))
        elif a.command == 'link-rule':
            new_target = target_ref(a.target)
            if d['target'] != new_target:
                d['revision'] += 1
            d['target'] = new_target
        else:
            existing = [e for e in d['evaluations'] if e['event_id'] == a.event_id]
            if existing:
                if any(existing[0].get(k) != v for k, v in [('outcome', a.outcome), ('source', a.source), ('rule_loaded', a.rule_loaded), ('cause', a.cause)]):
                    raise Invalid('evaluation id already has another outcome or source')
                print('unchanged: evaluation already recorded')
                return
            d['evaluations'].append(dict(event_id=a.event_id, source=a.source, outcome=a.outcome,
                                          rule_loaded=a.rule_loaded, cause=a.cause, at=stamp, revision=d['revision'], target=d['target'], expected=d['expected']))
    d['updated'] = stamp
    validate(d)
    if not a.dry_run:
        atomic_write(path, render(d))
    print(('planned: ' if a.dry_run else 'saved: ') + str(path))


def disposition(d):
    return d['decisions'][-1]['decision'] if d['decisions'] else 'pending'


def state(d):
    decision = disposition(d)
    if decision in ('rejected', 'superseded'):
        return decision
    return 'active' if d['target'] and (d['kind'] == 'explicit' or decision == 'adopted') else 'linked' if d['target'] else 'recorded'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path.home() / 'ai')
    sub = ap.add_subparsers(dest='command', required=True)
    rec = sub.add_parser('record', help='record a correction occurrence')
    for arg in ('key', 'event-id', 'system', 'summary', 'expected', 'source'):
        rec.add_argument('--' + arg, required=True)
    rec.add_argument('--scope', choices=['global', 'current', 'personal', 'repo'], required=True)
    rec.add_argument('--kind', choices=['explicit', 'inferred', 'task', 'fact'], required=True)
    rec.add_argument('--layer', choices=['current', 'personal'])
    rec.add_argument('--repo')
    rec.add_argument('--task-id', default='')
    rec.add_argument('--agent', default='unknown')
    rec.add_argument('--target')
    rec.add_argument('--cause', default='')
    rec.add_argument('--dry-run', action='store_true')
    for name in ('link-rule', 'verify', 'resolve'):
        p = sub.add_parser(name)
        p.add_argument('--key', required=True)
        p.add_argument('--scope', choices=['global', 'current', 'personal', 'repo'], required=True)
        p.add_argument('--layer', choices=['current', 'personal'])
        p.add_argument('--repo')
        p.add_argument('--task-id', default='')
        p.add_argument('--dry-run', action='store_true')
        if name == 'resolve':
            p.add_argument('--decision', choices=['adopted', 'rejected', 'superseded'], required=True)
            p.add_argument('--source', required=True, help='reference to actual user approval/decision; never inferred')
            p.add_argument('--target')
            p.add_argument('--summary')
            p.add_argument('--expected')
        elif name == 'link-rule':
            p.add_argument('--target', required=True)
        else:
            p.add_argument('--event-id', required=True)
            p.add_argument('--source', required=True)
            p.add_argument('--outcome', choices=['pass', 'fail', 'not-applicable'], required=True)
            p.add_argument('--rule-loaded', choices=['yes', 'no', 'unknown'], default='unknown')
            p.add_argument('--cause', default='')
    q = sub.add_parser('query', help='read scoped evidence; no writes')
    q.add_argument('--scope', choices=['global', 'current', 'personal', 'repo'])
    q.add_argument('--system')
    q.add_argument('--repo')
    q.add_argument('--task-id', default='')
    q.add_argument('--include-history', action='store_true')
    q.add_argument('--limit', type=int, default=8)
    q.add_argument('keywords', nargs='*')
    sub.add_parser('report', help='count evidence and actual evaluations; no writes')
    sub.add_parser('check', help='validate store and canonical references; no writes')
    a = ap.parse_args(argv)
    root = a.root.expanduser().resolve()
    try:
        if a.command in ('record', 'link-rule', 'verify', 'resolve'):
            reject_secrets({k: v for k, v in vars(a).items() if isinstance(v, str)})
            if a.dry_run:
                mutate(root, a)
            else:
                with locked(root):
                    mutate(root, a)
            return 0
        items = records(root)
        if a.command == 'query':
            if a.limit < 1:
                raise Invalid('limit must be positive')
            matches = []
            for path, d in items:
                if disposition(d) in ('rejected', 'superseded') and not a.include_history:
                    continue
                if d['scope'] != 'global':
                    if d['scope'] == 'repo':
                        if not a.repo or d['repo'] != repo_for(a):
                            continue
                        if a.scope in ('current', 'personal') and d['layer'] != a.scope:
                            continue
                    elif not a.scope or a.scope != d['scope']:
                        continue
                if a.scope == 'global' and d['scope'] != 'global':
                    continue
                if a.system and d['scope'] != 'global' and d['system'] != a.system:
                    continue
                if d['task_id'] and d['task_id'] != a.task_id:
                    continue
                hay = json.dumps(d, ensure_ascii=False).casefold()
                if not (d['scope'] == 'global' and state(d) == 'active') and not all(word.casefold() in hay for word in a.keywords):
                    continue
                matches.append((path, d))
            for path, d in sorted(matches, key=lambda item: (state(item[1]) == 'active', item[1]['updated']), reverse=True)[:a.limit]:
                print(f'{d["key"]} [{state(d)}; {d["kind"]}; {d["scope"]}; {d["system"]}] {d["summary"]}')
                print(f'  expected: {d["expected"]}; applicability: {d["repo"] or d["scope"]}' + (f'; task: {d["task_id"]}' if d['task_id'] else ''))
                print(f'  canonical: {d["target"] or "none"}; evidence: {path}; occurrences: {len(d["occurrences"])}')
            if len(matches) > a.limit:
                print(f'showing {a.limit} of {len(matches)}; use --limit {len(matches)} to see all')
            if not matches:
                print('no matching records' if items else 'store missing or empty (no records)')
        elif a.command == 'check':
            print(f'valid: {len(items)} records' if items else 'store missing or empty (no records)')
        else:
            historical = [e for _, d in items for e in d['evaluations'] if e.get('revision') != d['revision'] or disposition(d) in ('rejected', 'superseded')]
            evaluated = [e for _, d in items for e in d['evaluations'] if e.get('revision') == d['revision'] and disposition(d) not in ('rejected', 'superseded')]
            tested = [e for e in evaluated if e['outcome'] in ('pass', 'fail')]
            passed = sum(e['outcome'] == 'pass' for e in tested)
            print(f'recorded: {len(items)}; linked: {sum(bool(d["target"]) for _, d in items)}; active: {sum(state(d) == "active" for _, d in items)}')
            print(f'evaluated: {len(evaluated)}; applicable tested: {len(tested)}; pass: {passed}; fail: {len(tested)-passed}; not-applicable: {len(evaluated)-len(tested)}')
            print(f'historical evaluations (excluded): {len(historical)}')
            print('success rate: ' + (f'{passed}/{len(tested)}' if tested else 'unknown (no applicable tests)'))
        return 0
    except (Invalid, OSError) as error:
        print(f'agent-learning: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
