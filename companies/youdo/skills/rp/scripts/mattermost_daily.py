#!/usr/bin/env python3
"""
Collect Mattermost messages for a daily work report.

The script intentionally uses only the Python standard library so it can run in
minimal SRE environments without installing project dependencies.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python 3.8 compatibility.
    ZoneInfo = None  # type: ignore[assignment]


DEFAULT_TZ = "Europe/Moscow"
DEFAULT_ENV_FILE = Path(os.getenv("RP_ENV_FILE", "~/ai/current/.env")).expanduser()
DEFAULT_OUTPUT_DIR = Path(os.getenv("RP_DATA_DIR", "~/ai-data/rp")).expanduser() / "mattermost"


@dataclass(frozen=True)
class Window:
    day: dt.date
    tz: dt.tzinfo
    start_ms: int
    end_ms: int


class MattermostClient:
    def __init__(self, base_url: str, token: str, insecure: bool = False) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.context = ssl._create_unverified_context() if insecure else None

    def get(self, path: str, query: dict[str, Any] | None = None) -> Any:
        url = self._url(path, query)
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "User-Agent": "youdo-ai-mattermost-report/1.0",
            },
        )
        try:
            with urllib.request.urlopen(request, context=self.context, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GET {path} failed: HTTP {exc.code}: {body}") from exc

    def _url(self, path: str, query: dict[str, Any] | None) -> str:
        if not path.startswith("/"):
            path = "/" + path
        url = f"{self.base_url}/api/v4{path}"
        if query:
            clean = {key: value for key, value in query.items() if value is not None}
            url = f"{url}?{urllib.parse.urlencode(clean)}"
        return url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Mattermost daily work report.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD. Defaults to today in report timezone.")
    parser.add_argument("--timezone", default=os.getenv("MATTERMOST_REPORT_TZ", DEFAULT_TZ))
    parser.add_argument("--output", type=Path, help="Markdown output path.")
    parser.add_argument("--json-output", type=Path, help="JSON output path with selected source messages.")
    parser.add_argument("--stdout", action="store_true", help="Print Markdown report to stdout.")
    parser.add_argument("--include-sources", action="store_true", help="Include selected source messages in Markdown.")
    parser.add_argument("--include-private-channels", default=os.getenv("MATTERMOST_INCLUDE_PRIVATE_CHANNELS", "true"))
    parser.add_argument("--team", default=os.getenv("MATTERMOST_TEAM"), help="Limit regular channel scan to this team name.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification.")
    parser.add_argument(
        "--include-automated",
        action="store_true",
        help="Keep webhook/bot/system posts even outside threads with human messages.",
    )
    return parser.parse_args()


def load_dotenv(path: Path = DEFAULT_ENV_FILE) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def build_window(date_arg: str | None, timezone: str) -> Window:
    tz = get_timezone(timezone)
    day = dt.date.fromisoformat(date_arg) if date_arg else dt.datetime.now(tz).date()
    start = dt.datetime.combine(day, dt.time.min, tzinfo=tz)
    end = start + dt.timedelta(days=1)
    return Window(day=day, tz=tz, start_ms=int(start.timestamp() * 1000), end_ms=int(end.timestamp() * 1000))


def get_timezone(name: str) -> dt.tzinfo:
    if ZoneInfo is not None:
        return ZoneInfo(name)

    if name in {"UTC", "Etc/UTC", "Z"}:
        return dt.timezone.utc
    if name == "Europe/Moscow":
        return dt.timezone(dt.timedelta(hours=3), name)

    match = re.fullmatch(r"([+-])(\d{2}):?(\d{2})", name)
    if match:
        sign, hours, minutes = match.groups()
        offset = dt.timedelta(hours=int(hours), minutes=int(minutes))
        if sign == "-":
            offset = -offset
        return dt.timezone(offset, name)

    raise SystemExit(
        f"Timezone {name!r} requires Python 3.9+ zoneinfo. "
        "Use UTC, Europe/Moscow, or an offset like +03:00."
    )


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def list_relevant_channels(
    client: MattermostClient,
    user_id: str,
    team_filter: str | None,
    include_private: bool,
) -> list[dict[str, Any]]:
    channels_by_id: dict[str, dict[str, Any]] = {}

    for channel in client.get(f"/users/{user_id}/channels"):
        channels_by_id[channel["id"]] = channel

    teams = client.get("/users/me/teams")
    for team in teams:
        if team_filter and team.get("name") != team_filter:
            continue
        for channel in client.get(f"/users/{user_id}/teams/{team['id']}/channels"):
            if channel.get("type") == "P" and not include_private:
                continue
            channels_by_id[channel["id"]] = channel

    return list(channels_by_id.values())


def get_channel_posts(client: MattermostClient, channel_id: str, window: Window) -> list[dict[str, Any]]:
    payload = client.get(f"/channels/{channel_id}/posts", {"since": window.start_ms, "per_page": 200})
    posts = list(payload.get("posts", {}).values())
    return [post for post in posts if window.start_ms <= post.get("create_at", 0) < window.end_ms and not post.get("delete_at")]


def is_direct_or_group(channel: dict[str, Any]) -> bool:
    return channel.get("type") in {"D", "G"}


def is_automated(post: dict[str, Any]) -> bool:
    # Webhook posts carry the webhook creator's user_id, so they look like the owner's own messages.
    props = post.get("props") or {}
    return (
        str(props.get("from_webhook")).lower() == "true"
        or str(props.get("from_bot")).lower() == "true"
        or (post.get("type") or "").startswith("system_")
    )


def select_messages(
    posts: list[dict[str, Any]],
    channel: dict[str, Any],
    current_user: dict[str, Any],
    include_automated: bool = False,
) -> list[dict[str, Any]]:
    # Direct/group chats: threads with any human post. Channels: threads with a human post by the owner.
    relevant_roots = {
        post.get("root_id") or post["id"]
        for post in posts
        if (include_automated or not is_automated(post))
        and (is_direct_or_group(channel) or post.get("user_id") == current_user["id"])
    }
    selected = []
    for post in posts:
        root_id = post.get("root_id") or post.get("id")
        if root_id in relevant_roots:
            selected.append(post)
    return selected


def compact_message(post: dict[str, Any], channel: dict[str, Any], user: dict[str, Any], window: Window) -> dict[str, Any]:
    created = dt.datetime.fromtimestamp(post["create_at"] / 1000, tz=window.tz)
    return {
        "id": post["id"],
        "channel_id": channel["id"],
        "channel_name": channel.get("display_name") or channel.get("name") or channel["id"],
        "channel_type": channel.get("type"),
        "root_id": post.get("root_id") or "",
        "is_own": post.get("user_id") == user["id"] and not is_automated(post),
        "is_automated": is_automated(post),
        "created_at": created.isoformat(timespec="seconds"),
        "message": normalize_message(post.get("message", "") or attachment_text(post)),
    }


def attachment_text(post: dict[str, Any]) -> str:
    attachments = (post.get("props") or {}).get("attachments") or []
    parts = []
    for attachment in attachments[:1]:
        for key in ("pretext", "title", "text", "fallback"):
            value = attachment.get(key)
            if value and value not in parts:
                parts.append(str(value))
    return " ".join(parts)


def normalize_message(message: str) -> str:
    message = re.sub(
        r"```[^\n]*\n?(.*?)```",
        lambda match: "[code: " + trim_sentence(re.sub(r"\s+", " ", match.group(1)), 300) + "]",
        message,
        flags=re.DOTALL,
    )
    message = re.sub(r"\s+", " ", message).strip()
    return message


def trim_sentence(message: str, limit: int = 180) -> str:
    message = message.strip()
    if len(message) <= limit:
        return message
    return message[: limit - 1].rstrip() + "..."


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def context_key(message: dict[str, Any]) -> str:
    if message["channel_type"] in {"D", "G"}:
        return f"{message['channel_id']}:direct"
    return f"{message['channel_id']}:{message['root_id'] or message['id']}"


def group_contexts(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for message in messages:
        grouped.setdefault(context_key(message), []).append(message)

    contexts = []
    for items in grouped.values():
        first = items[0]
        last = items[-1]
        own_count = sum(1 for item in items if item["is_own"])
        title_message = next((item["message"] for item in items if item["message"]), "")
        contexts.append(
            {
                "channel_name": first["channel_name"],
                "channel_type": first["channel_type"],
                "root_id": first["root_id"] or first["id"],
                "start": first["created_at"],
                "end": last["created_at"],
                "messages": len(items),
                "own": own_count,
                "preview": trim_sentence(title_message, 220) if title_message else "[empty message]",
                "items": items,
            }
        )

    contexts.sort(key=lambda item: item["start"])
    return contexts


def render_report(messages: list[dict[str, Any]], user: dict[str, Any], window: Window, include_sources: bool) -> str:
    own_count = sum(1 for item in messages if item["is_own"])
    inbound_count = len(messages) - own_count
    channel_names = sorted({item["channel_name"] for item in messages})
    contexts = group_contexts(messages)

    lines = [
        f"# Mattermost source data for {window.day.isoformat()}",
        "",
        f"Владелец токена: @{user.get('username', user['id'])}",
        f"Сообщений в релевантном контексте: {len(messages)}; исходящих: {own_count}; входящих: {inbound_count}.",
        f"Контекстов: {len(contexts)}; каналов: {len(channel_names)}.",
        "",
        "Этот файл содержит только собранные источники. Итоговый рабочий отчет должен составить агент после анализа всех контекстов в Markdown/JSON, без паттернов и предзаданных тем.",
        "",
        "## Contexts",
    ]

    for index, context in enumerate(contexts, start=1):
        lines.append(
            f"- {index}. `{context['start']}`-`{context['end']}` "
            f"[{context['channel_name']}] сообщений: {context['messages']}, "
            f"исходящих: {context['own']}; preview: {context['preview']}"
        )

    if not include_sources:
        lines.append("")
        return "\n".join(lines)

    lines.extend(["", "## Источники"])
    for index, context in enumerate(contexts, start=1):
        lines.append("")
        lines.append(f"### Context {index}: {context['channel_name']} ({context['start']})")
        for item in context["items"]:
            if not item["message"]:
                continue
            author = "бот" if item.get("is_automated") else "я" if item["is_own"] else "другой участник"
            lines.append(f"- {item['created_at']} {author}: {item['message']}")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    load_dotenv()
    args = parse_args()
    base_url = get_required_env("MATTERMOST_URL")
    token = get_required_env("MATTERMOST_TOKEN")
    window = build_window(args.date, args.timezone)
    include_private = str(args.include_private_channels).lower() in {"1", "true", "yes", "y"}

    client = MattermostClient(base_url, token, insecure=args.insecure)
    user = client.get("/users/me")

    selected: list[dict[str, Any]] = []
    channels = list_relevant_channels(client, user["id"], args.team, include_private)
    for channel in channels:
        posts = get_channel_posts(client, channel["id"], window)
        for post in select_messages(posts, channel, user, args.include_automated):
            selected.append(compact_message(post, channel, user, window))

    selected.sort(key=lambda item: item["created_at"])
    report = render_report(selected, user, window, args.include_sources)

    output = args.output or DEFAULT_OUTPUT_DIR / f"{window.day.isoformat()}.md"
    json_output = args.json_output or output.with_suffix(".json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    json_output.write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.stdout:
        print(report)
    else:
        print(f"Wrote {output}")
        print(f"Wrote {json_output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
