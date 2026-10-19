#!/usr/bin/env python3
"""Inspect, publish or verify a task MR; publication requires prior user approval."""
import argparse
import json
import shlex
import sys
from urllib.error import HTTPError, URLError
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['inspect', 'publish', 'verify', 'update-description'])
    parser.add_argument('--project', required=True, help='GitLab project path')
    parser.add_argument('--branch', required=True)
    parser.add_argument('--target', default='master')
    parser.add_argument('--title')
    parser.add_argument('--body-file', type=Path)
    parser.add_argument('--expected-sha')
    parser.add_argument('--iid', type=int)
    parser.add_argument('--draft', action='store_true', help='Create a new draft MR; never change existing readiness')
    args = parser.parse_args()
    if args.draft and args.title and not args.title.startswith('Draft: '):
        args.title = 'Draft: ' + args.title
    token = None
    for line in Path('/home/slnnk/ai/current/.env').read_text().splitlines():
        if line.startswith('GITLAB_YOUDO_TOKEN='):
            token = shlex.split(line.split('=', 1)[1])[0]
    if not token:
        raise SystemExit('GITLAB_YOUDO_TOKEN not configured')

    def api(path, method='GET', payload=None, **params):
        url = 'https://gitlab.youdo.sg/api/v4/' + path
        if params:
            url += '?' + urlencode(params)
        headers = {'PRIVATE-TOKEN': token}
        data = None
        if payload is not None:
            data = json.dumps(payload).encode()
            headers['Content-Type'] = 'application/json'
        with urlopen(Request(url, data=data, headers=headers, method=method), timeout=30) as response:
            return json.load(response)

    result, code = run(args, api)
    print(json.dumps(result, ensure_ascii=False))
    return code


NETWORK_ERRORS = (HTTPError, URLError, TimeoutError, OSError)


def error_summary(error):
    # Do not echo URLs, headers or server response bodies into logs.
    return 'HTTP ' + str(error.code) if isinstance(error, HTTPError) else type(error).__name__


def run(args, api):
    """Execute only the requested MR phase. No git writes, retries, merge or deployment.

    Inject api for offline tests. Exit 0 means MR verification passed; pipeline
    availability/status is reported independently and never implies runtime success.
    Exit 2 after a write means reconcile remotely before considering another write.
    """
    project = api('projects/' + quote(args.project, safe=''))
    me = api('user')
    prefix = 'projects/' + str(project['id'])
    body = args.body_file.read_text().rstrip('\n') if args.body_file else None
    mr = None
    write_state = 'not_requested'

    def opened():
        found = api(prefix + '/merge_requests', state='opened', source_branch=args.branch, per_page=100)
        if len(found) > 1:
            raise ValueError('Multiple open MRs for source branch; no write allowed')
        return found

    def identity(item):
        return {'project': args.project, 'mr': item.get('web_url'), 'iid': item.get('iid')}

    def check_project(item):
        if item.get('source_project_id') != project['id'] or item.get('target_project_id') != project['id']:
            raise ValueError('MR belongs to another source/target project; no write allowed')

    def verify(item):
        check_project(item)
        branch = api(prefix + '/repository/branches/' + quote(args.branch, safe=''))
        sha = branch['commit']['id']
        if item['source_branch'] != args.branch or item['target_branch'] != args.target:
            raise ValueError('MR source/target mismatch')
        if args.expected_sha and sha != args.expected_sha:
            raise ValueError('Remote branch SHA differs from expected commit')
        if args.expected_sha and item.get('sha') != args.expected_sha:
            raise ValueError('MR SHA differs from expected commit; inspect remote state')
        if args.title and item['title'] != args.title:
            raise ValueError('MR title mismatch')
        if body is not None and (item.get('description') or '') != body:
            raise ValueError('MR description mismatch')
        return sha

    if args.phase == 'inspect' and args.iid and args.body_file:
        remote = api(prefix + '/merge_requests/' + str(args.iid)).get('description') or ''
        return {'exact_match': remote == body, 'strip_match': remote.strip() == body.strip(),
                'remote_length': len(remote), 'desired_length': len(body)}, 0

    if args.phase == 'update-description':
        if not args.iid or body is None:
            raise ValueError('update-description requires --iid and --body-file')
        path = prefix + '/merge_requests/' + str(args.iid)
        mr = before = api(path)
        check_project(before)
        if before['source_branch'] != args.branch or before['target_branch'] != args.target:
            raise ValueError('MR source/target mismatch; description not changed')
        desired_change = before.get('description') != body
        if desired_change:
            write_state = 'description_update_uncertain'
            try:
                api(path, method='PUT', payload={'description': body})
                write_state = 'description_updated'
            except NETWORK_ERRORS:
                pass  # One read-back, never repeat a write after a timeout.
        try:
            after = api(path)
            if (after.get('description') or '') != body:
                raise ValueError('MR description verification failed')
            for key in ['title', 'source_branch', 'target_branch', 'squash', 'assignees',
                        'draft', 'work_in_progress', 'force_remove_source_branch', 'should_remove_source_branch']:
                if before.get(key) != after.get(key):
                    raise ValueError('Unexpected MR metadata change: ' + key)
        except (ValueError,) + NETWORK_ERRORS as error:
            return dict(identity(mr), write_state=write_state, verified=False,
                        error=str(error) if isinstance(error, ValueError) else error_summary(error),
                        next_action='inspect_read_only_before_any_retry'), 2
        return dict(identity(after), description_verified=True,
                    write_state='description_verified' if desired_change else 'unchanged'), 0

    existing = opened()
    if args.phase == 'inspect':
        recent = api(prefix + '/merge_requests', author_id=me['id'], per_page=3, order_by='updated_at', sort='desc')
        return {'project': args.project, 'id': project['id'], 'default_branch': project['default_branch'],
                'squash_option': project.get('squash_option'),
                'remove_source_branch_after_merge': project.get('remove_source_branch_after_merge'),
                'assignee': me['username'],
                'open_mrs': [{'iid': m['iid'], 'target': m['target_branch'], 'title': m['title'],
                              'url': m['web_url']} for m in existing],
                'recent_preferences': [{'squash': m['squash'], 'remove_source_branch': deletion_setting(m)}
                                       for m in recent]}, 0
    if args.phase == 'publish':
        if not args.title or body is None or not args.expected_sha:
            raise ValueError('publish requires --title, --body-file and --expected-sha')
        branch = api(prefix + '/repository/branches/' + quote(args.branch, safe=''))
        if branch['commit']['id'] != args.expected_sha:
            raise ValueError('Remote source SHA differs from approved local commit; no write allowed')
        if existing:
            mr = existing[0]
            check_project(mr)
            if mr['target_branch'] != args.target or mr['title'] != args.title:
                raise ValueError('Existing MR has different target/title; review before changing')
            # Verify source revision before any description mutation too.
            if mr.get('sha') != args.expected_sha:
                raise ValueError('Existing MR SHA differs from expected commit; no write allowed')
            write_state = 'existing'
            if (mr.get('description') or '') != body:
                before = mr
                write_state = 'description_update_uncertain'
                try:
                    api(prefix + '/merge_requests/' + str(mr['iid']), method='PUT', payload={'description': body})
                    write_state = 'description_updated'
                except NETWORK_ERRORS:
                    pass
        else:
            before = None
            payload = {'source_branch': args.branch, 'target_branch': args.target, 'title': args.title,
                       'description': body, 'assignee_id': me['id'],
                       'squash': project.get('squash_option') in ('always', 'default_on'),
                       'remove_source_branch': project.get('remove_source_branch_after_merge')
                       if project.get('remove_source_branch_after_merge') is not None else True}
            write_state = 'creation_uncertain'
            try:
                mr = api(prefix + '/merge_requests', method='POST', payload=payload)
                write_state = 'created'
            except NETWORK_ERRORS:
                try:
                    recovered = opened()
                    mr = recovered[0] if recovered else None
                except (ValueError,) + NETWORK_ERRORS:
                    mr = None
                if mr is None:
                    return {'project': args.project, 'source': args.branch, 'write_state': write_state,
                            'verified': False, 'next_action': 'inspect_read_only_before_any_retry'}, 2
                write_state = 'found_after_uncertain_creation'
    else:
        before = None
        if not existing:
            raise ValueError('Open MR not found')
        mr = existing[0]
    try:
        mr = api(prefix + '/merge_requests/' + str(mr['iid']))
        sha = verify(mr)
        if args.phase == 'publish' and not existing:
            if mr['squash'] != payload['squash'] or deletion_setting(mr) != payload['remove_source_branch']:
                raise ValueError('Created MR settings differ from project defaults')
            if not any(item.get('username') == me['username'] for item in mr.get('assignees', [])):
                raise ValueError('Created MR assignee differs from requested user')
        if args.phase == 'publish' and existing and write_state != 'existing':
            for key in ['title', 'source_branch', 'target_branch', 'squash', 'assignees',
                        'draft', 'work_in_progress', 'force_remove_source_branch', 'should_remove_source_branch']:
                if before.get(key) != mr.get(key):
                    raise ValueError('Unexpected MR metadata change: ' + key)
    except (ValueError,) + NETWORK_ERRORS as error:
        return dict(identity(mr), write_state=write_state, verified=False,
                    error=str(error) if isinstance(error, ValueError) else error_summary(error),
                    next_action='inspect_read_only_before_any_retry'), 2
    result = dict(identity(mr), title=mr['title'], source=mr['source_branch'], target=mr['target_branch'],
                  sha=sha, verified=True, write_state=write_state,
                  assignees=[x['username'] for x in mr.get('assignees', [])], squash=mr['squash'],
                  remove_source_branch=deletion_setting(mr),
                  draft=mr.get('draft', mr.get('work_in_progress', mr['title'].startswith('Draft: '))))
    try:
        pipelines = api(prefix + '/pipelines', sha=sha, per_page=5)
        result['pipelines'] = [{'id': p['id'], 'status': p['status'], 'url': p['web_url']} for p in pipelines]
        result['pipeline_verification'] = 'available'
    except NETWORK_ERRORS as error:
        result.update(pipelines=None, pipeline_verification='unavailable', pipeline_error=error_summary(error))
    return result, 0


def deletion_setting(mr):
    for key in ['force_remove_source_branch', 'should_remove_source_branch']:
        if mr.get(key) is not None:
            return mr[key]
    return None


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError,) + NETWORK_ERRORS as error:
        print(json.dumps({'verified': False, 'error': str(error) if isinstance(error, ValueError)
                          else error_summary(error), 'next_action': 'inspect_read_only_before_any_retry'}))
        sys.exit(2)
