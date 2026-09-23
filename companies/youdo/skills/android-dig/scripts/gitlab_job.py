#!/usr/bin/env python3
"""Fetch and normalize a GitLab job and its trace for android-dig.

The script is read-only. It never emits the access token or an unsanitized trace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Pattern, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener, HTTPSHandler


DEFAULT_HOST = "gitlab.youdo.sg"
DEFAULT_TOKEN_ENV = "GITLAB_YOUDO_TOKEN"
DEFAULT_ENV_FILE = "~/ai/current/.env"
MOSCOW = timezone(timedelta(hours=3), name="Europe/Moscow")
JOB_PATH_RE = re.compile(r"^/(?P<project>.+?)/-/jobs/(?P<job_id>[0-9]+)/?$")
ANSI_RE = re.compile(r"\x1b(?:[@-_]|\[[0-?]*[ -/]*[@-~])")

SIGNALS: Sequence[Tuple[str, Pattern[str]]] = (
    (
        "runner",
        re.compile(
            r"runner_system_failure|stuck_or_timeout_failure|ERROR: Preparation failed|"
            r"prepare environment.*(?:error|fail)|failed to pull image|docker daemon.*(?:error|fail)|"
            r"no space left on device|\bout of memory\b|\bOOM(?:Killed)?\b|killed process [0-9]+|"
            r"Job failed \(system failure\)|Job exceeded maximum duration|"
            r"execution took longer than",
            re.I,
        ),
    ),
    (
        "network_dependency",
        re.compile(
            r"EAI_AGAIN|NXDOMAIN|temporary failure in name resolution|could not resolve|unknown host|"
            r"network is unreachable|connection refused|connection reset|i/o timeout|"
            r"TLS handshake (?:timeout|error)|x509:|certificate verify failed|"
            r"(?:HTTP(?:/[0-9.]+)?\s+|status(?: code)?[:= ]+)(?:502|503|504)\b",
            re.I,
        ),
    ),
    (
        "selenium_grid",
        re.compile(
            r"SessionNotCreatedException|Unable to create a new remote session|"
            r"(?:Selenium Grid|Grid hub|RemoteWebDriver).{0,300}(?:error|fail|timeout|refused|unreachable|queue)|"
            r"(?:error|fail|timeout|refused|unreachable).{0,300}(?:Selenium Grid|Grid hub)",
            re.I,
        ),
    ),
    (
        "appium_uiautomator",
        re.compile(
            r"SessionNotCreatedException|Could not proxy command|"
            r"UiAutomator2.{0,300}(?:error|fail|timeout|crash|not running|stopped|cannot|unable)|"
            r"instrumentation.{0,300}(?:fail|crash|not running|stopped)|"
            r"New Command Timeout.{0,100}expired|"
            r"systemPort.{0,200}(?:already in use|error|fail|timeout)|socket hang up|"
            r"Appium server.{0,300}(?:error|fail|timeout|cannot|unable)",
            re.I,
        ),
    ),
    (
        "adb_device",
        re.compile(
            r"Error executing adbExec|adb.{0,300}(?:exited with code [1-9][0-9]*|device offline|"
            r"unauthorized|device not found|no devices|command timed out|timed out)|"
            r"device (?:offline|unauthorized|not found)|Unknown input method|"
            r"usb.{0,200}(?:disconnect|reset|error)",
            re.I,
        ),
    ),
    (
        "device_preparation",
        re.compile(
            r"/opt/adb/(?:adb|adb_pkg)\.sh.*(?:no such file|not found|permission denied)|"
            r"ssh:.*(?:error|fail|refused|unreachable|timed out)|"
            r"systemctl.*(?:error|fail|not found)",
            re.I,
        ),
    ),
    (
        "artifact_delivery",
        re.compile(
            r"ERROR: Uploading artifacts|WARNING: Uploading artifacts.{0,300}(?:error|failed to)|"
            r"failed to upload|artifact upload.{0,300}(?:error|failed to)|"
            r"nexus.{0,300}(?:EAI_AGAIN|could not resolve|refused|reset|timed out|"
            r"HTTP(?:/[0-9.]+)?\s+[45][0-9]{2}\b|status(?: code)?[:= ]+[45][0-9]{2}\b)",
            re.I,
        ),
    ),
)

CONTEXT_RE = re.compile(
    r"^\s*(JOB_ID|STAND|SUITE|FAILED_JOB_ID|APP_VERSION|FAILED_PIPELINE_ID)\s*=\s*(.*?)\s*$"
)
HOST_CLUE_RE = re.compile(
    r"\b(?:M-K005[678]|192\.168\.30\.(?:30|147|148)|172\.28\.0\.171)\b", re.I
)
CAPABILITY_FIELDS = ("deviceUDID", "deviceManufacturer", "deviceModel", "platformVersion", "systemPort")


class ScriptError(Exception):
    """Expected user-facing failure."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def parse_job_url(raw_url: str, allowed_hosts: Iterable[str]) -> Dict[str, Any]:
    parsed = urlsplit(raw_url)
    allowed = {host.lower() for host in allowed_hosts}
    if parsed.scheme != "https":
        raise ScriptError("job URL must use https")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ScriptError("job URL must not contain userinfo, query parameters, or a fragment")
    host = (parsed.hostname or "").lower()
    if host not in allowed:
        raise ScriptError(f"refusing to send a token to unapproved GitLab host: {host or '<empty>'}")
    match = JOB_PATH_RE.match(parsed.path)
    if not match:
        raise ScriptError("expected a GitLab URL ending in /-/jobs/<numeric-id>")
    project_path = match.group("project").strip("/")
    if not project_path or "/" not in project_path:
        raise ScriptError("could not derive a namespaced GitLab project path")
    port = parsed.port
    origin = f"https://{host}" + (f":{port}" if port else "")
    return {
        "origin": origin,
        "host": host,
        "project_path": project_path,
        "encoded_project_path": quote(project_path, safe=""),
        "job_id": int(match.group("job_id")),
        "job_url": raw_url.rstrip("/"),
    }


def env_file_value(path: Path, key: str) -> Optional[str]:
    if not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ScriptError(f"cannot read env file {path}: {exc}") from exc
    for line in lines:
        candidate = line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        if candidate.startswith("export "):
            candidate = candidate[7:].lstrip()
        name, separator, value = candidate.partition("=")
        if separator and name.strip() == key:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            return value or None
    return None


def get_token(token_env: str, env_file: Path) -> str:
    token = os.environ.get(token_env) or env_file_value(env_file, token_env)
    if not token:
        raise ScriptError(f"missing {token_env}; export it or define it in {env_file}")
    return token


def make_opener(ca_file: Optional[str]) -> Any:
    try:
        context = ssl.create_default_context(cafile=ca_file)
    except (OSError, ssl.SSLError) as exc:
        raise ScriptError(f"cannot initialize TLS trust: {exc}") from exc
    return build_opener(HTTPSHandler(context=context), NoRedirect())


def http_get(opener: Any, url: str, token: str, timeout: float, max_bytes: int) -> bytes:
    request = Request(
        url,
        headers={"PRIVATE-TOKEN": token, "Accept": "application/json, text/plain;q=0.9"},
        method="GET",
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            payload = response.read(max_bytes + 1)
    except HTTPError as exc:
        detail = exc.read(512).decode("utf-8", errors="replace")
        detail = sanitize(detail).strip()
        raise ScriptError(f"GitLab returned HTTP {exc.code} for {url}: {detail or exc.reason}") from exc
    except URLError as exc:
        raise ScriptError(f"cannot reach GitLab at {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise ScriptError(f"GitLab request timed out for {url}") from exc
    if len(payload) > max_bytes:
        raise ScriptError(f"GitLab response exceeded configured limit of {max_bytes} bytes")
    return payload


def strip_control(text: str) -> str:
    text = ANSI_RE.sub("", text).replace("\r", "")
    return "".join(character for character in text if character in "\n\t" or ord(character) >= 32)


def sanitize(text: str) -> str:
    text = strip_control(text)
    text = re.sub(r"(?i)(https?://)[^/@\s]+@", r"\1<redacted>@", text)
    text = re.sub(
        r"(?i)([?&](?:access_token|private_token|token|password|passwd|secret|signature|x-amz-credential)=)[^&\s]+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(r"(?i)\b(Authorization\s*:\s*(?:Bearer|Basic)|PRIVATE-TOKEN\s*:)\s*\S+", r"\1 <redacted>", text)
    text = re.sub(
        r"(?i)\b([A-Z0-9_]*(?:TOKEN|PASSWORD|PASSWD|SECRET|PRIVATE_KEY|NEXUS_CREDS)[A-Z0-9_]*\s*=\s*)\S+",
        r"\1<redacted>",
        text,
    )
    text = re.sub(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b", "<redacted-jwt>", text)
    return text


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        result = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if result.tzinfo is None:
        result = result.replace(tzinfo=timezone.utc)
    return result


def iso(dt: datetime, zone: timezone) -> str:
    return dt.astimezone(zone).isoformat(timespec="seconds")


def epoch_nanoseconds(dt: datetime) -> int:
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    delta = dt.astimezone(timezone.utc) - epoch
    return ((delta.days * 86400 + delta.seconds) * 1_000_000_000) + delta.microseconds * 1000


def normalize_runner(runner: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(runner, dict):
        return None
    keys = ("id", "description", "runner_type", "active", "online", "status", "is_shared", "ip_address")
    return {key: runner.get(key) for key in keys if key in runner}


def normalize_job(job: Dict[str, Any]) -> Dict[str, Any]:
    commit = job.get("commit") if isinstance(job.get("commit"), dict) else {}
    pipeline = job.get("pipeline") if isinstance(job.get("pipeline"), dict) else {}
    return {
        "id": job.get("id"),
        "status": job.get("status"),
        "failure_reason": job.get("failure_reason"),
        "name": job.get("name"),
        "stage": job.get("stage"),
        "created_at": job.get("created_at"),
        "started_at": job.get("started_at"),
        "finished_at": job.get("finished_at"),
        "erased_at": job.get("erased_at"),
        "duration_seconds": job.get("duration"),
        "queued_duration_seconds": job.get("queued_duration"),
        "ref": job.get("ref"),
        "tag": job.get("tag"),
        "allow_failure": job.get("allow_failure"),
        "web_url": job.get("web_url"),
        "commit": {
            "id": commit.get("id"),
            "short_id": commit.get("short_id"),
            "title": commit.get("title"),
        },
        "pipeline": {"id": pipeline.get("id"), "web_url": pipeline.get("web_url")},
        "runner": normalize_runner(job.get("runner")),
    }


def correlation_window(job: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    start = parse_datetime(job.get("started_at")) or parse_datetime(job.get("created_at"))
    if not start:
        return None
    finish = parse_datetime(job.get("finished_at")) or parse_datetime(job.get("erased_at"))
    effective_finish = finish or datetime.now(timezone.utc)
    window_start = start - timedelta(minutes=10)
    window_end = effective_finish + timedelta(minutes=10)
    return {
        "job_start_utc": iso(start, timezone.utc),
        "job_start_moscow": iso(start, MOSCOW),
        "job_finish_utc": iso(effective_finish, timezone.utc),
        "job_finish_moscow": iso(effective_finish, MOSCOW),
        "job_is_finished": finish is not None,
        "query_start_utc": iso(window_start, timezone.utc),
        "query_end_utc": iso(window_end, timezone.utc),
        "query_start_epoch_seconds": int(window_start.timestamp()),
        "query_end_epoch_seconds": int(window_end.timestamp()),
        "query_start_epoch_nanoseconds": epoch_nanoseconds(window_start),
        "query_end_epoch_nanoseconds": epoch_nanoseconds(window_end),
    }


def analyze_trace(trace: bytes, max_events_per_category: int) -> Tuple[Dict[str, Any], str]:
    decoded = trace.decode("utf-8", errors="replace")
    cleaned = sanitize(decoded)
    lines = cleaned.splitlines()
    counts = {name: 0 for name, _ in SIGNALS}
    stored = {name: 0 for name, _ in SIGNALS}
    events: List[Dict[str, Any]] = []
    context: Dict[str, str] = {}
    host_clues = set()
    devices: List[Dict[str, str]] = []
    device_keys = set()

    for line_number, line in enumerate(lines, start=1):
        compact = line.strip()
        if not compact:
            continue
        context_match = CONTEXT_RE.match(compact)
        if context_match:
            context[context_match.group(1)] = context_match.group(2)[:500]
        host_clues.update(match.group(0) for match in HOST_CLUE_RE.finditer(compact))
        if "Capabilities {" in compact:
            device: Dict[str, str] = {}
            for field in CAPABILITY_FIELDS:
                field_match = re.search(r"\b" + re.escape(field) + r":\s*([^,}\s]+(?: [^,}]*)?)", compact)
                if field_match:
                    device[field] = field_match.group(1).strip()[:200]
            device_key = tuple(device.get(field, "") for field in CAPABILITY_FIELDS)
            if device.get("deviceUDID") and device_key not in device_keys:
                device_keys.add(device_key)
                devices.append(device)
            continue
        categories = []
        for category, pattern in SIGNALS:
            if pattern.search(compact):
                counts[category] += 1
                categories.append(category)
        if not categories:
            continue
        if all(stored[category] >= max_events_per_category for category in categories):
            continue
        for category in categories:
            if stored[category] < max_events_per_category:
                stored[category] += 1
        events.append(
            {
                "line": line_number,
                "categories": categories,
                "text": compact[:1500],
            }
        )

    return (
        {
            "bytes": len(trace),
            "lines": len(lines),
            "sha256": hashlib.sha256(trace).hexdigest(),
            "ci_context": context,
            "host_clues": sorted(host_clues, key=str.casefold),
            "devices": devices,
            "signal_counts": counts,
            "events": events,
            "events_truncated": {
                category: counts[category] > stored[category] for category in counts
            },
            "sanitization": "credentials and common secret forms redacted; output is not a substitute for source access controls",
        },
        cleaned,
    )


def write_private(path: Path, text: str) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.chmod(path, 0o600)
    except OSError as exc:
        raise ScriptError(f"cannot write sanitized trace to {path}: {exc}") from exc


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a GitLab job and emit normalized, secret-safe JSON for android-dig."
    )
    parser.add_argument("job_url", help="GitLab job URL ending in /-/jobs/<id>")
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
        "--metadata-only", action="store_true", help="fetch job metadata without downloading its trace"
    )
    parser.add_argument(
        "--max-trace-bytes",
        type=int,
        default=100 * 1024 * 1024,
        help="maximum accepted trace size (default: 104857600)",
    )
    parser.add_argument(
        "--max-events-per-category",
        type=int,
        default=30,
        help="maximum stored matches per signal category (counts remain complete)",
    )
    parser.add_argument(
        "--sanitized-trace-output",
        type=Path,
        help="optional path for a redacted full trace written with mode 0600",
    )
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.max_trace_bytes <= 0 or args.max_events_per_category < 0:
        parser.error("timeout and max-trace-bytes must be positive; max-events must be non-negative")
    if args.metadata_only and args.sanitized_trace_output:
        parser.error("--sanitized-trace-output cannot be used with --metadata-only")
    return args


def run(args: argparse.Namespace) -> Dict[str, Any]:
    allowed_hosts = args.allowed_hosts or [DEFAULT_HOST]
    target = parse_job_url(args.job_url, allowed_hosts)
    env_file = Path(args.env_file).expanduser()
    token = get_token(args.token_env, env_file)
    opener = make_opener(args.ca_file)
    api_root = f"{target['origin']}/api/v4/projects/{target['encoded_project_path']}/jobs/{target['job_id']}"

    metadata_bytes = http_get(opener, api_root, token, args.timeout, 2 * 1024 * 1024)
    try:
        metadata = json.loads(metadata_bytes)
    except json.JSONDecodeError as exc:
        raise ScriptError(f"GitLab job metadata is not valid JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ScriptError("GitLab returned an unexpected metadata document")

    result: Dict[str, Any] = {
        "schema_version": 1,
        "source": {
            "job_url": target["job_url"],
            "gitlab_origin": target["origin"],
            "project_path": target["project_path"],
            "job_id": target["job_id"],
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "job": normalize_job(metadata),
        "correlation_window": correlation_window(metadata),
    }

    if not args.metadata_only:
        trace = http_get(opener, api_root + "/trace", token, args.timeout, args.max_trace_bytes)
        analysis, sanitized_trace = analyze_trace(trace, args.max_events_per_category)
        result["trace"] = analysis
        if args.sanitized_trace_output:
            output_path = args.sanitized_trace_output.expanduser()
            write_private(output_path, sanitized_trace)
            result["trace"]["sanitized_trace_output"] = str(output_path)

    return result


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
        print(f"gitlab_job.py: error: {exc}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
