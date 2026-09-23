#!/usr/bin/env python3
"""Fetch project-level GitLab CI/CD variables for an Android autotest job.

The script is read-only. It derives the project from a concrete job URL and
never emits masked, hidden, file, or secret-like variable values.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern, Sequence

from gitlab_job import (
    DEFAULT_ENV_FILE,
    DEFAULT_HOST,
    DEFAULT_TOKEN_ENV,
    ScriptError,
    get_token,
    http_get,
    make_opener,
    parse_job_url,
    sanitize,
)


VISIBLE_VALUE_KEY_RE = re.compile(
    r"^(?:APPIUM_NODES(?:_[A-Z0-9]+)?|SELENIUM_SERVER(?:_[A-Z0-9]+)?|"
    r"JOB_ID|STAND|SUITE|EMULATORS)$",
    re.I,
)
SECRET_KEY_RE = re.compile(
    r"(?:TOKEN|PASSWORD|PASSWD|SECRET|PRIVATE_KEY|CREDENTIAL|COOKIE|AUTH|"
    r"SSH_KEY|NEXUS_CREDS|NOTIFICATIONS?_URL|WEBHOOK)",
    re.I,
)
REDACTED = "<redacted>"


def parse_json(payload: bytes, description: str) -> Any:
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ScriptError(f"GitLab {description} is not valid JSON: {exc}") from exc


def compile_key_patterns(raw_patterns: Sequence[str]) -> List[Pattern[str]]:
    patterns: List[Pattern[str]] = []
    for raw_pattern in raw_patterns:
        try:
            patterns.append(re.compile(raw_pattern, re.I))
        except re.error as exc:
            raise ScriptError(f"invalid --key-regex {raw_pattern!r}: {exc}") from exc
    return patterns


def value_redaction_reason(variable: Dict[str, Any]) -> Optional[str]:
    key = str(variable.get("key") or "")
    if bool(variable.get("hidden")):
        return "hidden"
    if bool(variable.get("masked")):
        return "masked"
    if str(variable.get("variable_type") or "env_var") == "file":
        return "file_variable"
    if SECRET_KEY_RE.search(key):
        return "secret_like_key"
    if not VISIBLE_VALUE_KEY_RE.fullmatch(key):
        return "not_diagnostic_allowlist"
    return None


def normalize_variable(variable: Dict[str, Any]) -> Dict[str, Any]:
    key = str(variable.get("key") or "")
    reason = value_redaction_reason(variable)
    raw_value = str(variable.get("value") or "")
    value = REDACTED if reason else sanitize(raw_value)[:4000]
    result: Dict[str, Any] = {
        "key": key,
        "value": value,
        "value_redacted": reason is not None,
        "variable_type": variable.get("variable_type") or "env_var",
        "protected": bool(variable.get("protected")),
        "masked": bool(variable.get("masked")),
        "hidden": bool(variable.get("hidden")),
        "raw": bool(variable.get("raw")),
        "environment_scope": variable.get("environment_scope") or "*",
    }
    if reason:
        result["redaction_reason"] = reason
    return result


def fetch_project_variables(
    opener: Any,
    api_root: str,
    token: str,
    timeout: float,
    max_response_bytes: int,
) -> List[Dict[str, Any]]:
    variables: List[Dict[str, Any]] = []
    for page in range(1, 1001):
        url = f"{api_root}/variables?per_page=100&page={page}"
        document = parse_json(
            http_get(opener, url, token, timeout, max_response_bytes),
            "project variables response",
        )
        if not isinstance(document, list):
            raise ScriptError("GitLab returned an unexpected project variables document")
        page_variables = [item for item in document if isinstance(item, dict)]
        variables.extend(page_variables)
        if len(document) < 100:
            return variables
    raise ScriptError("GitLab project variables pagination exceeded 1000 pages")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch project-level GitLab CI/CD variables for the repository derived from an "
            "Android-autotest job URL. Diagnostic routing values are visible; secrets are redacted."
        )
    )
    parser.add_argument("job_url", help="GitLab job URL ending in /-/jobs/<id>")
    parser.add_argument(
        "--key-regex",
        action="append",
        default=[],
        help="include only keys matching this regular expression; repeatable",
    )
    parser.add_argument(
        "--token-env",
        default=DEFAULT_TOKEN_ENV,
        help=f"environment variable holding the API token (default: {DEFAULT_TOKEN_ENV})",
    )
    parser.add_argument(
        "--env-file",
        default=DEFAULT_ENV_FILE,
        help=f"fallback env file containing the token (default: {DEFAULT_ENV_FILE})",
    )
    parser.add_argument(
        "--allowed-host",
        action="append",
        dest="allowed_hosts",
        help=f"approved GitLab hostname; repeatable (default: {DEFAULT_HOST})",
    )
    parser.add_argument("--ca-file", help="custom CA bundle for GitLab TLS verification")
    parser.add_argument("--timeout", type=float, default=60.0, help="HTTP timeout in seconds")
    parser.add_argument(
        "--max-response-bytes",
        type=int,
        default=10 * 1024 * 1024,
        help="maximum accepted response size per GitLab request",
    )
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.max_response_bytes <= 0:
        parser.error("timeout and max-response-bytes must be positive")
    return args


def run(args: argparse.Namespace) -> Dict[str, Any]:
    allowed_hosts = args.allowed_hosts or [DEFAULT_HOST]
    target = parse_job_url(args.job_url, allowed_hosts)
    patterns = compile_key_patterns(args.key_regex)
    token = get_token(args.token_env, Path(args.env_file).expanduser())
    opener = make_opener(args.ca_file)
    project_api_root = f"{target['origin']}/api/v4/projects/{target['encoded_project_path']}"

    job_document = parse_json(
        http_get(
            opener,
            f"{project_api_root}/jobs/{target['job_id']}",
            token,
            args.timeout,
            args.max_response_bytes,
        ),
        "job metadata response",
    )
    if not isinstance(job_document, dict):
        raise ScriptError("GitLab returned an unexpected job metadata document")

    raw_variables = fetch_project_variables(
        opener,
        project_api_root,
        token,
        args.timeout,
        args.max_response_bytes,
    )
    if patterns:
        raw_variables = [
            variable
            for variable in raw_variables
            if any(pattern.search(str(variable.get("key") or "")) for pattern in patterns)
        ]
    variables = sorted(
        (normalize_variable(variable) for variable in raw_variables),
        key=lambda item: (str(item["key"]).casefold(), str(item["environment_scope"]).casefold()),
    )
    visible_count = sum(not item["value_redacted"] for item in variables)

    return {
        "schema_version": 1,
        "source": {
            "job_url": target["job_url"],
            "gitlab_origin": target["origin"],
            "project_path": target["project_path"],
            "job_id": target["job_id"],
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "scope": "project-level CI/CD variables",
        },
        "job": {
            "id": job_document.get("id"),
            "name": job_document.get("name"),
            "ref": job_document.get("ref"),
            "status": job_document.get("status"),
            "environment": job_document.get("environment"),
        },
        "filters": {"key_regex": args.key_regex},
        "counts": {
            "variables": len(variables),
            "values_visible": visible_count,
            "values_redacted": len(variables) - visible_count,
        },
        "variables": variables,
        "limitations": [
            "Only project-level variable definitions are returned.",
            "Values are current at fetch time; GitLab does not return a historical project-variable snapshot for the job.",
            "Group, instance, pipeline, trigger, schedule, dotenv, and runner variables are not included.",
            "Environment scopes are reported but not resolved into a single effective job value.",
        ],
        "value_policy": (
            "Values are visible only for diagnostic routing keys; masked, hidden, file, "
            "secret-like, and non-allowlisted values are redacted."
        ),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = parse_args(argv)
        result = run(args)
        json.dump(
            result,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=args.pretty,
        )
        sys.stdout.write("\n")
        return 0
    except ScriptError as exc:
        print(f"gitlab_ci_variables.py: error: {exc}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
