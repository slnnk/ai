#!/usr/bin/env python3
"""List enabled hosts in a Zabbix host group for android-dig.

The script uses read-only JSON-RPC calls and emits normalized JSON.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPHandler, HTTPRedirectHandler, HTTPSHandler, Request, build_opener


DEFAULT_ENDPOINT = "http://zabbix-selectel.youdo.local/api_jsonrpc.php"
DEFAULT_HOST = "zabbix-selectel.youdo.local"
DEFAULT_GROUP = "Selenium"
DEFAULT_TOKEN_ENV = "ZABBIX_PROD_TOKEN"
DEFAULT_ENV_FILE = "~/ai/current/.env"
INTERFACE_TYPES = {"1": "agent", "2": "snmp", "3": "ipmi", "4": "jmx"}
AVAILABILITY = {"0": "unknown", "1": "available", "2": "unavailable"}


class ScriptError(Exception):
    """Expected user-facing failure."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


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


def validate_endpoint(raw_endpoint: str, allowed_hosts: Iterable[str]) -> str:
    parsed = urlsplit(raw_endpoint)
    allowed = {host.lower() for host in allowed_hosts}
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"}:
        raise ScriptError("Zabbix endpoint must use http or https")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ScriptError("Zabbix endpoint must not contain userinfo, query parameters, or a fragment")
    if host not in allowed:
        raise ScriptError(f"refusing to send a token to unapproved Zabbix host: {host or '<empty>'}")
    if not parsed.path.endswith("/api_jsonrpc.php"):
        raise ScriptError("Zabbix endpoint path must end in /api_jsonrpc.php")
    return raw_endpoint


def make_opener(ca_file: Optional[str]) -> Any:
    try:
        context = ssl.create_default_context(cafile=ca_file)
    except (OSError, ssl.SSLError) as exc:
        raise ScriptError(f"cannot initialize TLS trust: {exc}") from exc
    return build_opener(HTTPHandler(), HTTPSHandler(context=context), NoRedirect())


def rpc_call(
    opener: Any,
    endpoint: str,
    token: str,
    method: str,
    params: Dict[str, Any],
    request_id: int,
    timeout: float,
) -> Any:
    body = json.dumps(
        {"jsonrpc": "2.0", "method": method, "params": params, "id": request_id},
        separators=(",", ":"),
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json-rpc",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            payload = response.read(10 * 1024 * 1024 + 1)
    except HTTPError as exc:
        detail = exc.read(512).decode("utf-8", errors="replace").strip()
        raise ScriptError(f"Zabbix returned HTTP {exc.code}: {detail or exc.reason}") from exc
    except URLError as exc:
        raise ScriptError(f"cannot reach Zabbix at {endpoint}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise ScriptError(f"Zabbix request timed out at {endpoint}") from exc
    if len(payload) > 10 * 1024 * 1024:
        raise ScriptError("Zabbix response exceeded 10 MiB")
    try:
        document = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ScriptError(f"Zabbix returned invalid JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise ScriptError("Zabbix returned an unexpected JSON-RPC document")
    if "error" in document:
        error = document.get("error") or {}
        code = error.get("code", "unknown") if isinstance(error, dict) else "unknown"
        message = error.get("message", "JSON-RPC error") if isinstance(error, dict) else str(error)
        data = error.get("data", "") if isinstance(error, dict) else ""
        raise ScriptError(f"Zabbix JSON-RPC error {code}: {message}: {data}".rstrip(": "))
    if "result" not in document:
        raise ScriptError("Zabbix JSON-RPC response has no result")
    return document["result"]


def normalize_interface(interface: Dict[str, Any]) -> Dict[str, Any]:
    interface_type = str(interface.get("type", ""))
    available = str(interface.get("available", "0"))
    return {
        "interfaceid": interface.get("interfaceid"),
        "type": INTERFACE_TYPES.get(interface_type, interface_type or None),
        "main": str(interface.get("main", "0")) == "1",
        "connect_by": "ip" if str(interface.get("useip", "1")) == "1" else "dns",
        "ip": interface.get("ip") or None,
        "dns": interface.get("dns") or None,
        "port": interface.get("port") or None,
        "availability": AVAILABILITY.get(available, available),
        "error": interface.get("error") or None,
        "errors_from_epoch": int(interface.get("errors_from") or 0),
        "disable_until_epoch": int(interface.get("disable_until") or 0),
    }


def normalize_host(host: Dict[str, Any]) -> Dict[str, Any]:
    interfaces = host.get("interfaces") if isinstance(host.get("interfaces"), list) else []
    return {
        "hostid": host.get("hostid"),
        "technical_name": host.get("host"),
        "visible_name": host.get("name"),
        "enabled": str(host.get("status", "1")) == "0",
        "maintenance": {
            "active": str(host.get("maintenance_status", "0")) == "1",
            "type": host.get("maintenance_type"),
            "from_epoch": int(host.get("maintenance_from") or 0),
        },
        "interfaces": [normalize_interface(item) for item in interfaces if isinstance(item, dict)],
    }


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List Enabled hosts from a Zabbix group as normalized JSON for android-dig."
    )
    parser.add_argument("--group", default=DEFAULT_GROUP, help=f"exact host-group name (default: {DEFAULT_GROUP})")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help=f"Zabbix JSON-RPC endpoint (default: {DEFAULT_ENDPOINT})")
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
        help=f"approved Zabbix hostname; repeatable (default: {DEFAULT_HOST})",
    )
    parser.add_argument("--ca-file", help="custom CA bundle when the endpoint uses HTTPS")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("timeout must be positive")
    if not args.group.strip():
        parser.error("group must not be empty")
    return args


def run(args: argparse.Namespace) -> Dict[str, Any]:
    allowed_hosts = args.allowed_hosts or [DEFAULT_HOST]
    endpoint = validate_endpoint(args.endpoint, allowed_hosts)
    env_file = Path(args.env_file).expanduser()
    token = get_token(args.token_env, env_file)
    opener = make_opener(args.ca_file)

    groups = rpc_call(
        opener,
        endpoint,
        token,
        "hostgroup.get",
        {"output": ["groupid", "name"], "filter": {"name": [args.group]}},
        1,
        args.timeout,
    )
    if not isinstance(groups, list) or not groups:
        raise ScriptError(f"Zabbix host group not found: {args.group}")
    exact_groups = [item for item in groups if isinstance(item, dict) and item.get("name") == args.group]
    if len(exact_groups) != 1:
        raise ScriptError(f"expected one exact Zabbix group named {args.group}, got {len(exact_groups)}")
    group = exact_groups[0]

    hosts = rpc_call(
        opener,
        endpoint,
        token,
        "host.get",
        {
            "output": [
                "hostid",
                "host",
                "name",
                "status",
                "maintenance_status",
                "maintenance_type",
                "maintenance_from",
            ],
            "groupids": [group["groupid"]],
            "filter": {"status": "0"},
            "selectInterfaces": [
                "interfaceid",
                "type",
                "main",
                "useip",
                "ip",
                "dns",
                "port",
                "available",
                "error",
                "errors_from",
                "disable_until",
            ],
            "sortfield": "name",
        },
        2,
        args.timeout,
    )
    if not isinstance(hosts, list):
        raise ScriptError("Zabbix host.get returned an unexpected result")
    normalized = [normalize_host(item) for item in hosts if isinstance(item, dict)]
    normalized.sort(key=lambda item: ((item.get("technical_name") or "").casefold(), item.get("hostid") or ""))

    interface_states: Dict[str, int] = {"available": 0, "unavailable": 0, "unknown": 0}
    for host in normalized:
        for interface in host["interfaces"]:
            state = interface.get("availability")
            if state in interface_states:
                interface_states[state] += 1

    return {
        "schema_version": 1,
        "source": {
            "endpoint": endpoint,
            "group": {"groupid": group.get("groupid"), "name": group.get("name")},
            "host_status_filter": "Enabled",
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "counts": {
            "enabled_hosts": len(normalized),
            "hosts_in_maintenance": sum(1 for host in normalized if host["maintenance"]["active"]),
            "interfaces": interface_states,
        },
        "loki_instances": [host["technical_name"] for host in normalized if host.get("technical_name")],
        "hosts": normalized,
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
        print(f"zabbix_hosts.py: error: {exc}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
