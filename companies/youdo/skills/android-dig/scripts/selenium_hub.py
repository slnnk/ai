#!/usr/bin/env python3
"""Check the current Selenium Hub selected from a Zabbix inventory snapshot.

The script is read-only. It accepts only an Enabled Selenium inventory from
zabbix_hosts.py and derives the Hub address from the unique visible host name
ending in ``-selenium-hub``.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPHandler, HTTPRedirectHandler, Request, build_opener


DEFAULT_GROUP = "Selenium"
DEFAULT_HUB_SUFFIX = "-selenium-hub"
DEFAULT_PORT = 4444
STATUS_PATHS = ("/wd/hub/status", "/status")
GRID_HUB_PATH = "/grid/api/hub"
GRID_CONSOLE_PATH = "/grid/console"
GRID_PROXY_PATH = "/grid/api/proxy"


class ScriptError(Exception):
    """Expected user-facing failure."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


class GridConsoleParser(HTMLParser):
    """Extract registered Selenium 3 proxies without retaining console HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.proxies: List[Dict[str, Any]] = []
        self.current: Optional[Dict[str, Any]] = None
        self.proxy_depth = 0
        self.capture: Optional[str] = None
        self.capture_parts: List[str] = []

    @staticmethod
    def attributes(attrs: Sequence[Tuple[str, Optional[str]]]) -> Dict[str, str]:
        return {key: value or "" for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: Sequence[Tuple[str, Optional[str]]]) -> None:
        attributes = self.attributes(attrs)
        classes = set(attributes.get("class", "").split())
        if tag == "div" and self.current is None and "proxy" in classes:
            self.current = {"busy": "busy" in classes}
            self.proxy_depth = 1
            return
        if self.current is None:
            return
        if tag == "div":
            self.proxy_depth += 1
        if "busy" in classes:
            self.current["busy"] = True
        if tag == "p" and "proxyid" in classes:
            self.capture = "proxyid"
            self.capture_parts = []
        if tag == "img":
            title = attributes.get("title", "")
            device_match = re.search(r"custom:device\s*[=:]\s*([^,}]+)", title, re.I)
            version_match = re.search(r"(?:^|[, {])version\s*[=:]\s*([^,}]+)", title, re.I)
            platform_match = re.search(r"platformName\s*[=:]\s*([^,}]+)", title, re.I)
            if device_match:
                self.current["device"] = device_match.group(1).strip()
            if version_match:
                self.current["platform_version"] = version_match.group(1).strip()
            if platform_match:
                self.current["platform"] = platform_match.group(1).strip()

    def handle_data(self, data: str) -> None:
        if self.current is not None and self.capture:
            self.capture_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        if tag == "p" and self.capture == "proxyid":
            text = "".join(self.capture_parts).strip()
            match = re.search(r"\bid\s*:\s*(https?://[^,\s]+)", text, re.I)
            if match:
                self.current["id"] = match.group(1)
            os_match = re.search(r"\bOS\s*:\s*([^,\s<]+)", text, re.I)
            if os_match:
                self.current["os"] = os_match.group(1)
            self.capture = None
            self.capture_parts = []
        if tag == "div":
            self.proxy_depth -= 1
            if self.proxy_depth == 0:
                if self.current.get("id"):
                    self.proxies.append(self.current)
                self.current = None


def load_inventory(path: str) -> Dict[str, Any]:
    try:
        if path == "-":
            document = json.load(sys.stdin)
        else:
            document = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScriptError(f"cannot read inventory JSON from {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise ScriptError("inventory must be a JSON object from zabbix_hosts.py")
    return document


def validate_inventory(
    inventory: Dict[str, Any], expected_group: str, max_age_seconds: int
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], datetime]:
    source = inventory.get("source")
    hosts = inventory.get("hosts")
    if inventory.get("schema_version") != 1 or not isinstance(source, dict) or not isinstance(hosts, list):
        raise ScriptError("inventory schema is not a supported zabbix_hosts.py document")
    group = source.get("group")
    if not isinstance(group, dict) or group.get("name") != expected_group:
        actual = group.get("name") if isinstance(group, dict) else None
        raise ScriptError(f"inventory group mismatch: expected {expected_group}, got {actual}")
    if source.get("host_status_filter") != "Enabled":
        raise ScriptError("inventory is not restricted to Enabled hosts")
    fetched_raw = source.get("fetched_at_utc")
    if not isinstance(fetched_raw, str):
        raise ScriptError("inventory has no fetched_at_utc timestamp")
    try:
        fetched_at = datetime.fromisoformat(fetched_raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ScriptError("inventory fetched_at_utc is invalid") from exc
    if fetched_at.tzinfo is None:
        raise ScriptError("inventory fetched_at_utc must include a timezone")
    age = (datetime.now(timezone.utc) - fetched_at.astimezone(timezone.utc)).total_seconds()
    if age < -300:
        raise ScriptError("inventory timestamp is more than five minutes in the future")
    if max_age_seconds and age > max_age_seconds:
        raise ScriptError(
            f"inventory is stale ({int(age)} seconds old; maximum {max_age_seconds}); refresh zabbix_hosts.py"
        )

    normalized: List[Dict[str, Any]] = []
    seen_ids = set()
    for host in hosts:
        if not isinstance(host, dict) or host.get("enabled") is not True:
            raise ScriptError("inventory contains a host that is not Enabled")
        hostid = str(host.get("hostid") or "")
        if not hostid.isdigit() or hostid in seen_ids:
            raise ScriptError("inventory contains a missing or duplicate numeric hostid")
        seen_ids.add(hostid)
        normalized.append(host)
    if not normalized:
        raise ScriptError("inventory contains no Enabled hosts")
    return normalized, source, fetched_at.astimezone(timezone.utc)


def select_hub(hosts: Sequence[Dict[str, Any]], suffix: str) -> Dict[str, Any]:
    suffix_folded = suffix.casefold()
    matches = [
        host
        for host in hosts
        if isinstance(host.get("visible_name"), str)
        and str(host["visible_name"]).casefold().endswith(suffix_folded)
    ]
    if len(matches) != 1:
        names = sorted(
            str(host.get("visible_name") or host.get("technical_name") or host.get("hostid"))
            for host in matches
        )
        raise ScriptError(
            f"expected exactly one Enabled Zabbix host with visible-name suffix {suffix!r}, "
            f"got {len(matches)}: {names}"
        )
    return matches[0]


def select_ip(host: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    interfaces = host.get("interfaces")
    if not isinstance(interfaces, list):
        raise ScriptError("selected Hub host has no interface list")
    agent_interfaces = [
        interface
        for interface in interfaces
        if isinstance(interface, dict)
        and interface.get("type") == "agent"
        and isinstance(interface.get("ip"), str)
        and interface.get("ip")
    ]
    main_interfaces = [interface for interface in agent_interfaces if interface.get("main") is True]
    candidates = main_interfaces or agent_interfaces
    if len(candidates) != 1:
        raise ScriptError(
            f"selected Hub host must have exactly one usable {'main ' if main_interfaces else ''}agent IP; "
            f"got {len(candidates)}"
        )
    raw_ip = str(candidates[0]["ip"])
    try:
        normalized_ip = str(ipaddress.ip_address(raw_ip))
    except ValueError as exc:
        raise ScriptError(f"selected Hub interface IP is invalid: {raw_ip!r}") from exc
    return normalized_ip, candidates[0]


def parse_status(document: Any) -> Dict[str, Any]:
    if not isinstance(document, dict):
        return {"recognized": False, "ready": None}
    value = document.get("value") if isinstance(document.get("value"), dict) else {}
    ready: Optional[bool] = value.get("ready") if isinstance(value.get("ready"), bool) else None
    legacy_status = document.get("status")
    if ready is None and legacy_status == 0:
        ready = True
    result: Dict[str, Any] = {
        "recognized": bool(value) or "status" in document,
        "ready": ready,
        "message": value.get("message") if isinstance(value.get("message"), str) else None,
        "legacy_status": legacy_status,
    }
    build = value.get("build")
    if isinstance(build, dict):
        result["build"] = {
            key: build.get(key) for key in ("version", "revision", "time") if key in build
        }
    nodes = value.get("nodes")
    if isinstance(nodes, list):
        normalized_nodes = []
        for node in nodes:
            if not isinstance(node, dict):
                continue
            slots = node.get("slots") if isinstance(node.get("slots"), list) else []
            normalized_nodes.append(
                {
                    "id": node.get("id"),
                    "uri": node.get("uri"),
                    "availability": node.get("availability"),
                    "max_sessions": node.get("maxSessions"),
                    "slot_count": len(slots),
                    "active_sessions": sum(
                        1 for slot in slots if isinstance(slot, dict) and slot.get("session") is not None
                    ),
                }
            )
        result["nodes"] = normalized_nodes
        result["node_count"] = len(normalized_nodes)
    return result


def fetch_bytes(
    opener: Any, url: str, accept: str, timeout: float, max_bytes: int
) -> Tuple[Dict[str, Any], Optional[bytes]]:
    request = Request(url, headers={"Accept": accept}, method="GET")
    started = time.monotonic()
    try:
        with opener.open(request, timeout=timeout) as response:
            status_code = int(response.status)
            content_type = response.headers.get("Content-Type")
            payload = response.read(max_bytes + 1)
    except HTTPError as exc:
        status_code = int(exc.code)
        content_type = exc.headers.get("Content-Type") if exc.headers else None
        payload = exc.read(max_bytes + 1)
    except (URLError, TimeoutError, socket.timeout) as exc:
        reason = exc.reason if isinstance(exc, URLError) else str(exc)
        return (
            {
                "url": url,
                "reachable": False,
                "latency_ms": round((time.monotonic() - started) * 1000, 1),
                "error": str(reason)[:500],
            },
            None,
        )
    latency_ms = round((time.monotonic() - started) * 1000, 1)
    if len(payload) > max_bytes:
        return (
            {
                "url": url,
                "reachable": True,
                "http_status": status_code,
                "latency_ms": latency_ms,
                "error": f"response exceeded {max_bytes} bytes",
            },
            None,
        )
    return (
        {
            "url": url,
            "reachable": True,
            "http_status": status_code,
            "content_type": content_type,
            "latency_ms": latency_ms,
        },
        payload,
    )


def get_json(
    opener: Any, url: str, timeout: float, max_bytes: int
) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    result, payload = fetch_bytes(opener, url, "application/json", timeout, max_bytes)
    if payload is None:
        return result, None
    try:
        document = json.loads(payload)
    except json.JSONDecodeError:
        result["json"] = False
        return result, None
    result["json"] = isinstance(document, dict)
    return result, document if isinstance(document, dict) else None


def get_status(opener: Any, url: str, timeout: float, max_bytes: int) -> Dict[str, Any]:
    result, document = get_json(opener, url, timeout, max_bytes)
    result["status"] = parse_status(document)
    return result


def get_console_proxies(
    opener: Any, url: str, timeout: float, max_bytes: int
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    result, payload = fetch_bytes(opener, url, "text/html", timeout, max_bytes)
    if payload is None or result.get("http_status") != 200:
        return result, []
    parser = GridConsoleParser()
    try:
        parser.feed(payload.decode("utf-8", errors="replace"))
        parser.close()
    except Exception as exc:
        result["parse_error"] = str(exc)[:500]
        return result, []
    result["registered_proxy_count"] = len(parser.proxies)
    return result, parser.proxies


def inventory_ip_map(hosts: Sequence[Dict[str, Any]], hub_hostid: Any) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for host in hosts:
        if str(host.get("hostid")) == str(hub_hostid):
            continue
        technical_name = str(host.get("technical_name") or "")
        interfaces = host.get("interfaces") if isinstance(host.get("interfaces"), list) else []
        for interface in interfaces:
            if not isinstance(interface, dict) or not isinstance(interface.get("ip"), str):
                continue
            try:
                normalized = str(ipaddress.ip_address(interface["ip"]))
            except ValueError:
                continue
            result[normalized] = technical_name
    return result


def normalize_hub_api(document: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(document, dict):
        return {"recognized": False}
    slots = document.get("slotCounts") if isinstance(document.get("slotCounts"), dict) else {}
    total = slots.get("total") if isinstance(slots.get("total"), int) else None
    free = slots.get("free") if isinstance(slots.get("free"), int) else None
    return {
        "recognized": document.get("success") is True,
        "success": document.get("success"),
        "new_session_request_count": document.get("newSessionRequestCount"),
        "slots": {
            "total": total,
            "free": free,
            "busy": total - free if total is not None and free is not None else None,
        },
    }


def proxy_capability(document: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(document, dict):
        return {}
    request = document.get("request") if isinstance(document.get("request"), dict) else {}
    configuration = (
        request.get("configuration") if isinstance(request.get("configuration"), dict) else {}
    )
    capabilities = (
        configuration.get("capabilities")
        if isinstance(configuration.get("capabilities"), list)
        else []
    )
    for capability in capabilities:
        if isinstance(capability, dict):
            return capability
    return {}


def validate_proxy_id(proxy_id: str) -> Tuple[str, int]:
    parsed = urlparse(proxy_id)
    if (
        parsed.scheme != "http"
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/"}
        or not parsed.hostname
        or parsed.port is None
    ):
        raise ScriptError(f"Grid returned an unsafe proxy id: {proxy_id!r}")
    try:
        host_ip = str(ipaddress.ip_address(parsed.hostname))
    except ValueError as exc:
        raise ScriptError(f"Grid proxy id does not contain an IP address: {proxy_id!r}") from exc
    return host_ip, parsed.port


def check_proxy(
    proxy: Dict[str, Any],
    base_url: str,
    allowed_node_ips: Dict[str, str],
    timeout: float,
    max_bytes: int,
) -> Dict[str, Any]:
    proxy_id = str(proxy.get("id") or "")
    host_ip, port = validate_proxy_id(proxy_id)
    result: Dict[str, Any] = {
        "proxy_id": proxy_id,
        "host_ip": host_ip,
        "host": allowed_node_ips.get(host_ip),
        "port": port,
        "device": proxy.get("device"),
        "platform": proxy.get("platform") or proxy.get("os"),
        "platform_version": proxy.get("platform_version"),
        "slot_state": "busy" if proxy.get("busy") is True else "idle",
        "inventory_match": host_ip in allowed_node_ips,
    }
    opener = build_opener(NoRedirect(), HTTPHandler())
    proxy_url = base_url + GRID_PROXY_PATH + "?" + urlencode({"id": proxy_id})
    proxy_check, proxy_document = get_json(opener, proxy_url, timeout, max_bytes)
    capability = proxy_capability(proxy_document)
    if not result.get("device") and isinstance(capability.get("custom:device"), str):
        result["device"] = capability["custom:device"]
    if not result.get("platform"):
        result["platform"] = capability.get("platformName") or capability.get("platform")
    if not result.get("platform_version") and capability.get("version") is not None:
        result["platform_version"] = str(capability["version"])
    result["grid_proxy_api"] = {
        **proxy_check,
        "success": proxy_document.get("success") if proxy_document else None,
        "message": proxy_document.get("msg") if proxy_document else None,
    }

    if host_ip not in allowed_node_ips:
        result["appium_status"] = {
            "skipped": True,
            "reason": "proxy IP is absent from current Enabled Zabbix inventory",
        }
        return result

    appium_base = f"http://{host_ip}:{port}"
    attempts = []
    selected: Optional[Dict[str, Any]] = None
    for path in STATUS_PATHS:
        attempt = get_status(opener, appium_base + path, timeout, max_bytes)
        attempts.append(attempt)
        status = attempt.get("status")
        if (
            attempt.get("http_status") == 200
            and isinstance(status, dict)
            and status.get("recognized") is True
        ):
            selected = attempt
            break
    result["appium_status"] = {
        "selected": selected,
        "attempts": attempts,
        "reachable": selected is not None,
        "ready": selected.get("status", {}).get("ready") if selected else None,
    }
    return result


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the current Selenium Hub selected from a fresh Enabled Zabbix inventory."
    )
    parser.add_argument("--inventory", required=True, help="zabbix_hosts.py JSON file, or - for stdin")
    parser.add_argument("--expected-group", default=DEFAULT_GROUP, help="required Zabbix group")
    parser.add_argument(
        "--hub-suffix",
        default=DEFAULT_HUB_SUFFIX,
        help=f"visible-name suffix selecting the Hub host (default: {DEFAULT_HUB_SUFFIX})",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Selenium HTTP port")
    parser.add_argument(
        "--max-inventory-age",
        type=int,
        default=900,
        help="maximum inventory age in seconds; 0 disables",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout per status path")
    parser.add_argument(
        "--max-response-bytes",
        type=int,
        default=2 * 1024 * 1024,
        help="maximum accepted response size per status path",
    )
    parser.add_argument(
        "--max-devices",
        type=int,
        default=64,
        help="maximum registered Grid proxies to inspect",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="maximum concurrent read-only proxy/Appium checks",
    )
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(argv)
    if not args.hub_suffix or args.port < 1 or args.port > 65535:
        parser.error("hub-suffix must not be empty and port must be in 1..65535")
    if (
        args.max_inventory_age < 0
        or args.timeout <= 0
        or args.max_response_bytes <= 0
        or args.max_devices <= 0
        or args.workers <= 0
    ):
        parser.error(
            "max-inventory-age must be non-negative; timeout, max-response-bytes, "
            "max-devices, and workers must be positive"
        )
    return args


def run(args: argparse.Namespace) -> Dict[str, Any]:
    inventory = load_inventory(args.inventory)
    hosts, source, fetched_at = validate_inventory(
        inventory, args.expected_group, args.max_inventory_age
    )
    hub = select_hub(hosts, args.hub_suffix)
    hub_ip, interface = select_ip(hub)
    url_host = f"[{hub_ip}]" if ":" in hub_ip else hub_ip
    base_url = f"http://{url_host}:{args.port}"
    opener = build_opener(NoRedirect(), HTTPHandler())
    attempts = []
    selected: Optional[Dict[str, Any]] = None
    for path in STATUS_PATHS:
        attempt = get_status(opener, base_url + path, args.timeout, args.max_response_bytes)
        attempts.append(attempt)
        status = attempt.get("status")
        if (
            attempt.get("http_status") == 200
            and isinstance(status, dict)
            and status.get("recognized") is True
        ):
            selected = attempt
            break

    any_reachable = any(attempt.get("reachable") is True for attempt in attempts)
    if selected:
        ready = selected["status"].get("ready")
        raw_hub_verdict = "ready" if ready is True else "not_ready" if ready is False else "responding_unknown"
    else:
        raw_hub_verdict = "responding_unrecognized" if any_reachable else "unreachable"

    hub_api_check, hub_api_document = get_json(
        opener, base_url + GRID_HUB_PATH, args.timeout, args.max_response_bytes
    )
    hub_api = normalize_hub_api(hub_api_document)
    console_check, proxies = get_console_proxies(
        opener, base_url + GRID_CONSOLE_PATH, args.timeout, args.max_response_bytes
    )
    if len(proxies) > args.max_devices:
        raise ScriptError(
            f"Grid console returned {len(proxies)} proxies; maximum is {args.max_devices}"
        )

    allowed_node_ips = inventory_ip_map(hosts, hub.get("hostid"))
    device_results: List[Dict[str, Any]] = []
    worker_errors: List[Dict[str, Any]] = []
    if proxies:
        with ThreadPoolExecutor(max_workers=min(args.workers, len(proxies))) as executor:
            futures = {
                executor.submit(
                    check_proxy,
                    proxy,
                    base_url,
                    allowed_node_ips,
                    args.timeout,
                    args.max_response_bytes,
                ): proxy
                for proxy in proxies
            }
            for future in as_completed(futures):
                proxy = futures[future]
                try:
                    device_results.append(future.result())
                except (ScriptError, ValueError) as exc:
                    worker_errors.append(
                        {"proxy_id": proxy.get("id"), "error": str(exc)[:500]}
                    )
    device_results.sort(key=lambda item: (str(item.get("host_ip")), int(item.get("port") or 0)))

    registered = len(device_results)
    busy = sum(item.get("slot_state") == "busy" for item in device_results)
    idle = sum(item.get("slot_state") == "idle" for item in device_results)
    inventory_matched = sum(item.get("inventory_match") is True for item in device_results)
    proxy_api_ok = sum(
        item.get("grid_proxy_api", {}).get("success") is True for item in device_results
    )
    appium_reachable = sum(
        item.get("appium_status", {}).get("reachable") is True for item in device_results
    )
    appium_ready = sum(
        item.get("appium_status", {}).get("ready") is True for item in device_results
    )
    hub_total_slots = hub_api.get("slots", {}).get("total")
    hub_free_slots = hub_api.get("slots", {}).get("free")
    hub_busy_slots = hub_api.get("slots", {}).get("busy")
    console_matches_hub_total = (
        registered == hub_total_slots if isinstance(hub_total_slots, int) else None
    )
    console_busy_matches_hub = (
        busy == hub_busy_slots if isinstance(hub_busy_slots, int) else None
    )
    if (
        console_check.get("http_status") != 200
        or hub_api.get("recognized") is not True
        or worker_errors
    ):
        devices_verdict = "coverage_gap"
    elif registered == 0:
        devices_verdict = "none_registered"
    elif console_matches_hub_total is False or console_busy_matches_hub is False:
        devices_verdict = "inconsistent_snapshot"
    elif (
        inventory_matched != registered
        or proxy_api_ok != registered
        or appium_reachable != registered
        or appium_ready != registered
    ):
        devices_verdict = "degraded"
    else:
        devices_verdict = "healthy"

    hub_verdict = raw_hub_verdict
    if (
        raw_hub_verdict == "not_ready"
        and isinstance(hub_total_slots, int)
        and hub_total_slots > 0
        and hub_free_slots == 0
        and hub_api.get("recognized") is True
    ):
        hub_verdict = "saturated"

    if hub_verdict not in {"ready", "saturated"}:
        verdict = hub_verdict
    elif devices_verdict == "healthy":
        verdict = hub_verdict
    elif devices_verdict == "degraded":
        verdict = "degraded"
    else:
        verdict = "ready_device_coverage_gap"

    return {
        "schema_version": 1,
        "source": {
            "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "inventory_fetched_at_utc": fetched_at.isoformat(timespec="seconds"),
            "inventory_group": source["group"]["name"],
            "selection": f"Enabled host visible_name suffix {args.hub_suffix!r}",
        },
        "hub": {
            "hostid": hub.get("hostid"),
            "technical_name": hub.get("technical_name"),
            "visible_name": hub.get("visible_name"),
            "ip": hub_ip,
            "port": args.port,
            "base_url": base_url,
            "zabbix_interface": {
                "interfaceid": interface.get("interfaceid"),
                "availability": interface.get("availability"),
                "main": interface.get("main"),
            },
        },
        "verdict": verdict,
        "hub_verdict": hub_verdict,
        "raw_hub_status_verdict": raw_hub_verdict,
        "selected_status": selected,
        "attempts": attempts,
        "grid_hub_api": {"check": hub_api_check, "status": hub_api},
        "devices": {
            "verdict": devices_verdict,
            "summary": {
                "registered": registered,
                "idle": idle,
                "busy": busy,
                "active_slots": busy,
                "inventory_matched": inventory_matched,
                "grid_proxy_api_ok": proxy_api_ok,
                "appium_reachable": appium_reachable,
                "appium_ready": appium_ready,
                "hub_reported_total_slots": hub_total_slots,
                "hub_reported_free_slots": hub_free_slots,
                "hub_reported_busy_slots": hub_busy_slots,
                "console_matches_hub_total": console_matches_hub_total,
                "console_busy_matches_hub": console_busy_matches_hub,
            },
            "console_check": console_check,
            "worker_errors": worker_errors,
            "items": device_results,
        },
        "limitations": [
            "This is a current point-in-time HTTP check, not evidence of historical Hub health during a finished job.",
            "Console busy/idle is a point-in-time slot state and may change immediately after collection.",
            "A registered proxy and Appium status response do not prove ADB transport or UiAutomator2 command health.",
        ],
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
        print(f"selenium_hub.py: error: {exc}", file=sys.stderr)
        return 2
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
