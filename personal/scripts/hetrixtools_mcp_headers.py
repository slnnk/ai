#!/usr/bin/env python3
"""Provide MCP authentication headers from the personal secret store."""

import json
from pathlib import Path
import sys


def load_key():
    path = Path.home() / 'ai/personal/.env'
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith('export '):
            line = line[7:].strip()
        name, sep, value = line.partition('=')
        if sep and name.strip() == 'HETRIXTOOLS_API_KEY':
            value = value.strip()
            if value.startswith(('"', "'")):
                if len(value) < 2 or value[-1] != value[0]:
                    raise ValueError('Invalid quoting for HETRIXTOOLS_API_KEY')
                value = value[1:-1]
            if not value or any(c.isspace() for c in value):
                raise ValueError('HETRIXTOOLS_API_KEY is empty or invalid')
            return value
    raise ValueError('HETRIXTOOLS_API_KEY is missing from personal/.env')


if __name__ == '__main__':
    try:
        headers = {'api-key': load_key()}
    except (OSError, ValueError):
        print('Cannot load HETRIXTOOLS_API_KEY from personal/.env', file=sys.stderr)
        sys.exit(1)
    print(json.dumps(headers))
