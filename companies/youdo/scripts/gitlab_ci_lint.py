#!/usr/bin/env python3
"""Validate local CI content through GitLab CI Lint without creating a pipeline."""
import argparse
import json
import shlex
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--ref', default='master')
    parser.add_argument('--simulate', action='store_true', help='Simulate pipeline creation without running jobs')
    parser.add_argument('--output', type=Path, help='Save a summary without merged YAML or job scripts')
    args = parser.parse_args()
    token = None
    for line in Path('/home/slnnk/ai/current/.env').read_text().splitlines():
        if line.startswith('GITLAB_YOUDO_TOKEN='):
            token = shlex.split(line.split('=', 1)[1])[0]
    if not token:
        raise SystemExit('GITLAB_YOUDO_TOKEN not configured')
    payload = {'content': args.file.read_text(), 'dry_run': args.simulate,
               'include_jobs': True, 'ref': args.ref}
    url = 'https://gitlab.youdo.sg/api/v4/projects/' + quote(args.project, safe='') + '/ci/lint'
    request = Request(url, data=json.dumps(payload).encode(), method='POST',
                      headers={'PRIVATE-TOKEN': token, 'Content-Type': 'application/json'})
    with urlopen(request, timeout=60) as response:
        result = json.load(response)
    summary = {k: result.get(k) for k in ['valid', 'errors', 'warnings']}
    summary['jobs'] = [{'name': j['name'], 'stage': j.get('stage'), 'when': j.get('when')}
                       for j in result.get('jobs', [])]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))
    if not result.get('valid'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
