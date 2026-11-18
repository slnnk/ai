#!/usr/bin/env python3
"""Read an issue and check existing YouTrack comments before drafting or posting."""

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import quote


def inspect(get, issue, draft, keywords):
    issue_path = '/issues/' + quote(issue, safe='')
    metadata = get(issue_path, {'fields': 'id,idReadable,summary'})
    if not isinstance(metadata, dict) or not metadata.get('idReadable'):
        raise ValueError('Unexpected issue metadata')

    exact_matches = []
    relevant = []
    seen = set()
    page_size = 100
    while True:
        comments = get(issue_path + '/comments', {'fields': 'id,text', '$top': page_size, '$skip': len(seen)})
        if not isinstance(comments, list):
            raise ValueError('Unexpected comments response')
        if not comments:
            break
        for comment in comments:
            comment_id = comment['id']
            if comment_id in seen:
                raise ValueError('Comment list changed during pagination')
            seen.add(comment_id)
            text = comment.get('text') or ''
            if draft is not None and text == draft:
                exact_matches.append(comment_id)
            if any(keyword in text.casefold() for keyword in keywords):
                relevant.append({'id': comment_id, 'text': text})
    return {'issue': metadata, 'comments_count': len(seen), 'exact_matches': exact_matches, 'relevant': relevant}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('issue', help='YouTrack issue ID, for example PROJ-123')
    parser.add_argument('--draft', type=Path, help='Local draft file for exact matching')
    parser.add_argument('--match', action='append', default=[], help='Case-insensitive text to look for, repeatable')
    args = parser.parse_args()
    keywords = [value.strip().casefold() for value in args.match if value.strip()]
    if not args.draft and not keywords:
        parser.error('provide --draft, --match, or both')

    # Reuse the reporting skill's established read-only YouTrack client and token loading.
    company = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(company / 'skills' / 'rp' / 'scripts'))
    from youtrack_sprint import DEFAULT_YOUTRACK_URL, YouTrackClient, get_required_env, load_dotenv

    try:
        draft = args.draft.read_text(encoding='utf-8') if args.draft else None
        if draft is not None and not draft.strip():
            parser.error('--draft must contain text')
        load_dotenv(company / '.env')
        client = YouTrackClient(DEFAULT_YOUTRACK_URL, get_required_env('YOUTRACK_TOKEN'))
        result = inspect(client.get, args.issue, draft, keywords)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(1, f'Comment inspection failed ({type(exc).__name__})\n')
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
