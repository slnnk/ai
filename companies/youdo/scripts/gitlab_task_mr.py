#!/usr/bin/env python3
"""Inspect, publish or verify a task MR; publication requires prior user approval."""
import argparse
import json
import shlex
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
    args = parser.parse_args()
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

    project = api('projects/' + quote(args.project, safe=''))
    me = api('user')
    prefix = 'projects/' + str(project['id'])
    if args.phase == 'inspect' and args.iid and args.body_file:
        remote = api(prefix + '/merge_requests/' + str(args.iid))['description']
        desired = args.body_file.read_text().rstrip('\n')
        print(json.dumps({'exact_match': remote == desired, 'strip_match': remote.strip() == desired.strip(),
                          'remote_length': len(remote), 'desired_length': len(desired),
                          'remote_end': repr(remote[-12:]), 'desired_end': repr(desired[-12:])}))
        return
    if args.phase == 'update-description':
        if not args.iid or not args.body_file:
            parser.error('update-description requires --iid and --body-file')
        path = prefix + '/merge_requests/' + str(args.iid)
        before = api(path)
        if before['source_branch'] != args.branch or before['target_branch'] != args.target:
            raise SystemExit('MR source/target mismatch; description not changed')
        desired = args.body_file.read_text().rstrip('\n')
        if before['description'] != desired:
            api(path, method='PUT', payload={'description': desired})
        after = api(path)
        if after['description'] != desired:
            raise SystemExit('MR description verification failed')
        for key in ['title', 'source_branch', 'target_branch', 'squash', 'assignees']:
            if before[key] != after[key]:
                raise SystemExit('Unexpected MR metadata change: ' + key)
        print(json.dumps({'mr': after['web_url'], 'description_verified': True}, ensure_ascii=False))
        return
    existing = api(prefix + '/merge_requests', state='opened', source_branch=args.branch, per_page=100)
    if len(existing) > 1:
        raise SystemExit('Multiple open MRs for source branch; investigate before writing')
    if args.phase == 'inspect':
        recent = api(prefix + '/merge_requests', author_id=me['id'], per_page=3, order_by='updated_at', sort='desc')
        print(json.dumps({'project':args.project, 'id':project['id'], 'default_branch':project['default_branch'],
                          'squash_option':project.get('squash_option'),
                          'remove_source_branch_after_merge':project.get('remove_source_branch_after_merge'),
                          'assignee':me['username'], 'open_mrs':[{'iid':m['iid'],'target':m['target_branch'],'url':m['web_url']} for m in existing],
                          'recent_preferences':[{'squash':m['squash'],'remove_source_branch':m.get('force_remove_source_branch') or m.get('should_remove_source_branch')} for m in recent]}))
        return
    if args.phase == 'publish':
        if not args.title or not args.body_file or not args.expected_sha:
            parser.error('publish requires --title, --body-file and --expected-sha')
        branch = api(prefix + '/repository/branches/' + quote(args.branch, safe=''))
        if branch['commit']['id'] != args.expected_sha:
            raise SystemExit('Remote source SHA differs from approved local commit')
        if existing:
            mr = existing[0]
            if mr['target_branch'] != args.target or mr['title'] != args.title:
                raise SystemExit('Existing MR has different target/title; investigate before changing')
        else:
            payload = {'source_branch':args.branch, 'target_branch':args.target, 'title':args.title,
                       'description':args.body_file.read_text(), 'assignee_id':me['id'],
                       'squash':project.get('squash_option') in ('always','default_on'),
                       'remove_source_branch':project.get('remove_source_branch_after_merge') if project.get('remove_source_branch_after_merge') is not None else True}
            mr = api(prefix + '/merge_requests', method='POST', payload=payload)
    else:
        if not existing:
            raise SystemExit('Open MR not found')
        mr = existing[0]
    mr = api(prefix + '/merge_requests/' + str(mr['iid']))
    branch = api(prefix + '/repository/branches/' + quote(args.branch, safe=''))
    if args.expected_sha and branch['commit']['id'] != args.expected_sha:
        raise SystemExit('Remote branch SHA mismatch')
    if mr['source_branch'] != args.branch or mr['target_branch'] != args.target:
        raise SystemExit('MR source/target mismatch')
    pipelines = api(prefix + '/pipelines', sha=branch['commit']['id'], per_page=5)
    print(json.dumps({'project':args.project, 'mr':mr['web_url'], 'iid':mr['iid'], 'title':mr['title'],
                      'source':mr['source_branch'], 'target':mr['target_branch'], 'sha':branch['commit']['id'],
                      'assignees':[x['username'] for x in mr.get('assignees',[])], 'squash':mr['squash'],
                      'remove_source_branch':mr.get('force_remove_source_branch') or mr.get('should_remove_source_branch'),
                      'pipelines':[{'id':p['id'],'status':p['status'],'url':p['web_url']} for p in pipelines]}))


if __name__ == '__main__':
    main()
