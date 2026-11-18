#!/usr/bin/env python3
"""Collect GitLab runner jobs overlapping an explicit window into runner-jobs.json."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
from pathlib import Path
import shlex
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener


API = 'https://gitlab.youdo.sg/api/v4'
TOKEN_KEY = 'GITLAB_YOUDO_TOKEN'
ENV_FILE = Path(__file__).resolve().parents[1] / '.env'
PAGE_SIZE = 100


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_token():
    token = None
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith(TOKEN_KEY + '='):
            values = shlex.split(line.split('=', 1)[1], comments=True)
            token = values[0] if values else None
    if not token:
        raise RuntimeError(f'{TOKEN_KEY} not configured')
    return token


def timestamp(value):
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError('Timestamp must include a timezone')
    return parsed


def collect_runner(get, runner, start, end):
    runner_id = runner['id']
    runner_path = f'/runners/{runner_id}'
    contacted_at = get(runner_path).get('contacted_at')
    result = {
        'id': runner_id,
        'description': runner['description'],
        'contacted_at': contacted_at,
        'jobs': [],
    }
    if runner.get('status') != 'online' and (not contacted_at or timestamp(contacted_at) < start):
        result['skipped_old'] = True
        return result

    for page in range(1, 201):
        batch = get(f'{runner_path}/jobs', per_page=PAGE_SIZE, page=page, order_by='id', sort='desc')
        for job in batch:
            started = job.get('started_at')
            finished = job.get('finished_at')
            if not started or timestamp(started) >= end or (finished and timestamp(finished) < start):
                continue
            project = job.get('project') or {}
            pipeline = job.get('pipeline') or {}
            result['jobs'].append({
                'id': job['id'],
                'project_id': project.get('id'),
                'project': project.get('path_with_namespace') or project.get('name_with_namespace') or project.get('name'),
                'name': job['name'],
                'status': job['status'],
                'stage': job.get('stage'),
                'created_at': job['created_at'],
                'started_at': started,
                'finished_at': finished,
                'runner_id': runner_id,
                'runner_description': runner['description'],
                'pipeline_id': pipeline.get('id'),
                'ref': job.get('ref'),
                'commit': job.get('commit'),
                'web_url': job.get('web_url'),
            })
        if len(batch) < PAGE_SIZE or max(timestamp(job['created_at']) for job in batch) < start:
            return result
    raise RuntimeError('Runner jobs truncated')


def collect(get, start, end):
    runners = []
    for page in range(1, 8):
        batch = get('/runners/all', per_page=PAGE_SIZE, page=page)
        runners.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
    else:
        raise RuntimeError('Runner listing truncated')

    results = []
    errors = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(collect_runner, get, runner, start, end): runner['id'] for runner in runners}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
                errors.append({'runner': futures[future], 'error': error_summary(error)})
    return {'start': start.isoformat(), 'end': end.isoformat(), 'runners': results, 'errors': errors}


def error_summary(error):
    if isinstance(error, HTTPError):
        return f'HTTP {error.code}'
    if isinstance(error, RuntimeError):
        return str(error)
    return type(error).__name__


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', required=True, help='ISO 8601 timestamp with timezone')
    parser.add_argument('--end', required=True, help='ISO 8601 timestamp with timezone')
    parser.add_argument('--output', type=Path, required=True, help='Path to the local runner-jobs.json report')
    args = parser.parse_args()
    try:
        start, end = timestamp(args.start), timestamp(args.end)
    except ValueError:
        parser.error('--start and --end must be ISO 8601 timestamps with timezones')
    if start >= end:
        parser.error('--start must be earlier than --end')

    try:
        with TemporaryDirectory(dir=args.output.parent) as temporary:
            token = read_token()
            opener = build_opener(NoRedirect())

            def get(path, **query):
                url = f'{API}{path}'
                if query:
                    url += '?' + urlencode(query)
                with opener.open(Request(url, headers={'PRIVATE-TOKEN': token}), timeout=35) as response:
                    return json.load(response)

            report = collect(get, start, end)
            output = Path(temporary) / 'report.json'
            output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            output.chmod(0o600)
            # Replace only after collection and serialization have finished.
            output.replace(args.output)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f'Collection failed: {error_summary(error)}\n')

    jobs = sum(len(runner['jobs']) for runner in report['runners'])
    errors = len(report['errors'])
    print(f'Collected {jobs} jobs from {len(report["runners"])} runners; runner errors: {errors}')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
