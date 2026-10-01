#!/usr/bin/env python3
"""
Collect YouTrack issues from a sprint on an agile board.

The script intentionally uses only the Python standard library so it can run in
minimal SRE environments without installing project dependencies.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BOARD = "DevOps Scrum Board"
DEFAULT_ENV_FILE = Path(os.getenv("RP_ENV_FILE", "~/ai/current/.env")).expanduser()
DEFAULT_OUTPUT_DIR = Path(os.getenv("RP_DATA_DIR", "~/ai-data/rp")).expanduser() / "youtrack"
DEFAULT_YOUTRACK_URL = "https://youtrack.youdo.com/youtrack"
# Sprint periods and week numbers follow the report timezone (Europe/Moscow, no DST).
REPORT_TZ = dt.timezone(dt.timedelta(hours=3), "Europe/Moscow")


class YouTrackClient:
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
                "User-Agent": "youdo-ai-youtrack-report/1.0",
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
        url = f"{self.base_url}/api{path}"
        if query:
            clean = {key: value for key, value in query.items() if value is not None}
            url = f"{url}?{urllib.parse.urlencode(clean)}"
        return url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect YouTrack sprint issues.")
    parser.add_argument("--url", default=os.getenv("YOUTRACK_URL", DEFAULT_YOUTRACK_URL))
    parser.add_argument("--board", default=os.getenv("YOUTRACK_BOARD", DEFAULT_BOARD))
    parser.add_argument(
        "--sprint",
        help=(
            "Sprint name, id, or number to collect. Defaults to the current sprint. "
            "Examples: 'DevOps sprint - 181', '181', '91-14942'."
        ),
    )
    parser.add_argument(
        "--goal",
        type=int,
        default=int(os.getenv("RP_SPRINT_GOAL", "10")),
        help="Target number of resolved sprint issues assigned to the token owner (default 10).",
    )
    parser.add_argument(
        "--backlog-query",
        default=os.getenv("YOUTRACK_BACKLOG_QUERY"),
        help="YouTrack query for backlog issues. Defaults to unresolved board-project issues not on the board.",
    )
    parser.add_argument("--output", type=Path, help="Markdown output path.")
    parser.add_argument("--json-output", type=Path, help="JSON output path with selected sprint issues.")
    parser.add_argument("--stdout", action="store_true", help="Print Markdown report to stdout.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification.")
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


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def find_board(client: YouTrackClient, board_name: str) -> dict[str, Any]:
    fields = "id,name,projects(shortName),currentSprint(id,name,start,finish,archived,isDefault,unresolvedIssuesCount)"
    agiles = client.get("/agiles", {"fields": fields, "$top": 1000})
    exact = [agile for agile in agiles if agile.get("name") == board_name]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise SystemExit(f"Found multiple YouTrack boards named {board_name!r}")

    available = ", ".join(sorted(agile.get("name", agile.get("id", "")) for agile in agiles))
    raise SystemExit(f"YouTrack board {board_name!r} was not found. Available boards: {available}")


def get_current_sprint(client: YouTrackClient, board: dict[str, Any]) -> dict[str, Any]:
    fields = "id,name,start,finish,archived,isDefault,goal,unresolvedIssuesCount"
    try:
        return client.get(f"/agiles/{board['id']}/sprints/current", {"fields": fields})
    except RuntimeError:
        sprint = board.get("currentSprint")
        if sprint:
            return sprint
        raise


def find_sprint(client: YouTrackClient, board_id: str, sprint_selector: str) -> dict[str, Any]:
    fields = "id,name,start,finish,archived,isDefault,goal,unresolvedIssuesCount"
    sprints = client.get(f"/agiles/{board_id}/sprints", {"fields": fields, "$top": 1000})
    selector = sprint_selector.strip()
    if not selector:
        raise SystemExit("--sprint value must not be empty")

    exact = [
        sprint
        for sprint in sprints
        if selector in {sprint.get("id", ""), sprint.get("name", "")}
    ]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise SystemExit(f"Found multiple YouTrack sprints matching {selector!r}")

    selector_slug = slugify(selector)
    matches = [sprint for sprint in sprints if slugify(sprint.get("name") or "") == selector_slug]
    if not matches and selector.isdigit():
        suffix = f"-{selector}"
        spaced_suffix = f" {selector}"
        matches = [
            sprint
            for sprint in sprints
            if (slugify(sprint.get("name") or "").endswith(suffix) or (sprint.get("name") or "").endswith(spaced_suffix))
        ]

    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(sorted(sprint.get("name", sprint.get("id", "")) for sprint in matches))
        raise SystemExit(f"Found multiple YouTrack sprints matching {selector!r}: {names}")

    available = ", ".join(sorted(sprint.get("name", sprint.get("id", "")) for sprint in sprints))
    raise SystemExit(f"YouTrack sprint {selector!r} was not found. Available sprints: {available}")


def get_sprint_issues(client: YouTrackClient, board_id: str, sprint_id: str) -> list[dict[str, Any]]:
    fields = (
        "id,idReadable,summary,description,created,updated,resolved,"
        "project(id,name,shortName),reporter(login,fullName),"
        "customFields(name,value(name,fullName,login,presentation,isResolved,localizedName,id)),"
        "tags(name)"
    )
    issues: list[dict[str, Any]] = []
    skip = 0
    page_size = 100
    while True:
        page = client.get(
            f"/agiles/{board_id}/sprints/{sprint_id}/issues",
            {"fields": fields, "$skip": skip, "$top": page_size},
        )
        if not page:
            break
        issues.extend(page)
        if len(page) < page_size:
            break
        skip += page_size
    return issues


def get_backlog_issues(client: YouTrackClient, query: str) -> list[dict[str, Any]]:
    fields = (
        "id,idReadable,summary,description,created,updated,resolved,"
        "project(id,name,shortName),reporter(login,fullName),"
        "customFields(name,value(name,fullName,login,presentation,isResolved,localizedName,id)),"
        "tags(name)"
    )
    return client.get("/issues", {"query": query, "fields": fields, "$top": 500})


def default_backlog_query(board: dict[str, Any]) -> str:
    projects = " ".join(f"project: {project['shortName']}" for project in board.get("projects", []))
    return f"{projects} #Unresolved has: -{{Board {board['name']}}}".strip()


def working_days_left(sprint: dict[str, Any]) -> int:
    finish = sprint.get("finish")
    if not finish:
        return 0
    last = dt.datetime.fromtimestamp(int(finish) / 1000, tz=REPORT_TZ).date()
    day = dt.datetime.now(REPORT_TZ).date()
    count = 0
    while day <= last:
        if day.weekday() < 5:
            count += 1
        day += dt.timedelta(days=1)
    return count


def goal_summary(issues: list[dict[str, Any]], me: dict[str, Any], sprint: dict[str, Any], target: int) -> dict[str, Any]:
    names = {me.get("fullName"), me.get("login")} - {None, ""}
    mine = [issue for issue in issues if issue["assignee"] in names]
    closed = [issue["idReadable"] for issue in mine if issue["resolved"]]
    return {
        "target": target,
        "assignee": me.get("fullName") or me.get("login"),
        "closed": closed,
        "open": [issue["idReadable"] for issue in mine if not issue["resolved"]],
        "missing": max(target - len(closed), 0),
        "workingDaysLeft": working_days_left(sprint),
    }


def get_issue_comments(client: YouTrackClient, issue_id: str) -> list[dict[str, Any]]:
    fields = "id,text,created,updated,author(login,fullName)"
    comments = client.get(f"/issues/{issue_id}/comments", {"fields": fields, "$top": 100})
    return comments if isinstance(comments, list) else []


def is_reportable_issue(issue: dict[str, Any]) -> bool:
    id_readable = issue.get("idReadable") or ""
    summary = issue.get("summary") or ""
    return bool(summary.strip()) and id_readable != "Issue.Draft"


def normalize_issue(issue: dict[str, Any], base_url: str) -> dict[str, Any]:
    fields = issue_custom_fields(issue)
    display_fields = {name: field_value(value) for name, value in fields.items() if name != "Sprint"}
    id_readable = issue["idReadable"]
    return {
        "id": issue["id"],
        "idReadable": id_readable,
        "summary": issue.get("summary") or "",
        "description": issue.get("description") or "",
        "url": f"{base_url.rstrip('/')}/issue/{urllib.parse.quote(id_readable)}",
        "project": issue.get("project", {}),
        "created": format_millis(issue.get("created")),
        "updated": format_millis(issue.get("updated")),
        "resolved": format_millis(issue.get("resolved")),
        "state": field_value(fields.get("State")),
        "assignee": field_value(fields.get("Assignee")),
        "priority": field_value(fields.get("Priority")),
        "type": field_value(fields.get("Type")),
        "customFields": display_fields,
        "tags": [tag.get("name", "") for tag in issue.get("tags", []) if tag.get("name")],
        "comments": [normalize_comment(comment) for comment in issue.get("comments", [])],
    }


def normalize_comment(comment: dict[str, Any]) -> dict[str, Any]:
    author = comment.get("author") or {}
    return {
        "id": comment.get("id", ""),
        "text": comment.get("text") or "",
        "created": format_millis(comment.get("created")),
        "updated": format_millis(comment.get("updated")),
        "author": author.get("fullName") or author.get("login") or "",
    }


def issue_custom_fields(issue: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field in issue.get("customFields", []):
        name = field.get("name")
        if not name:
            continue
        result[name] = field.get("value")
    return result


def field_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(filter(None, [field_value(item) for item in value]))
    if isinstance(value, dict):
        for key in ("presentation", "fullName", "localizedName", "name", "login", "id"):
            if value.get(key):
                return str(value[key])
        return ""
    return str(value)


def format_millis(value: Any) -> str:
    if not value:
        return ""
    timestamp = int(value) / 1000
    return dt.datetime.fromtimestamp(timestamp, tz=REPORT_TZ).isoformat(timespec="seconds")


def sprint_output_base(sprint: dict[str, Any]) -> Path:
    start = sprint.get("start")
    if start:
        day = dt.datetime.fromtimestamp(int(start) / 1000, tz=REPORT_TZ).date()
    else:
        day = dt.datetime.now(REPORT_TZ).date()
    if day.weekday() == 6:
        day = day + dt.timedelta(days=1)
    iso_year, iso_week, _ = day.isocalendar()
    sprint_name = slugify(sprint.get("name") or sprint["id"])
    return DEFAULT_OUTPUT_DIR / f"{iso_year}-W{iso_week:02d}-{sprint_name}"


def slugify(value: str) -> str:
    result = []
    previous_dash = False
    for char in value.lower():
        if char.isascii() and char.isalnum():
            result.append(char)
            previous_dash = False
        elif not previous_dash:
            result.append("-")
            previous_dash = True
    return "".join(result).strip("-") or "sprint"


def render_report(
    board: dict[str, Any],
    sprint: dict[str, Any],
    issues: list[dict[str, Any]],
    goal: dict[str, Any],
    backlog: list[dict[str, Any]],
) -> str:
    unresolved = [issue for issue in issues if not issue["resolved"]]
    lines = [
        f"# YouTrack sprint for {board['name']}",
        "",
        f"Доска: {board['name']} (`{board['id']}`)",
        f"Спринт: {sprint.get('name', sprint['id'])} (`{sprint['id']}`)",
        f"Период: {format_millis(sprint.get('start')) or 'не задан'} - {format_millis(sprint.get('finish')) or 'не задан'}",
        f"Задач: {len(issues)}; незавершенных: {len(unresolved)}.",
        "",
        "Этот файл содержит только задачи выбранного спринта YouTrack. Итоговый рабочий отчет должен синхронизировать Mattermost-контексты с этими задачами, не добавляя задачи без подтверждения из сообщений.",
        "",
        f"Цель: {goal['target']} закрытых задач ({goal['assignee']}); закрыто {len(goal['closed'])}"
        f" ({', '.join(goal['closed']) or '-'}); открыто {len(goal['open'])} ({', '.join(goal['open']) or '-'});"
        f" не хватает {goal['missing']}; рабочих дней до конца спринта: {goal['workingDaysLeft']}.",
        "",
        "## Issues",
    ]

    for issue in sorted(issues, key=lambda item: item["idReadable"]):
        state = f"; state: {issue['state']}" if issue["state"] else ""
        assignee = f"; assignee: {issue['assignee']}" if issue["assignee"] else ""
        description = "; description: yes" if issue.get("description") else ""
        comments = f"; comments: {len(issue.get('comments', []))}" if issue.get("comments") else ""
        lines.append(f"- `{issue['idReadable']}` {issue['summary']}{state}{assignee}{description}{comments}; {issue['url']}")

    lines.extend(["", f"## Backlog (без спринта, {len(backlog)})"])
    for issue in sorted(backlog, key=lambda item: item["idReadable"]):
        state = f"; state: {issue['state']}" if issue["state"] else ""
        assignee = f"; assignee: {issue['assignee']}" if issue["assignee"] else "; assignee: -"
        lines.append(f"- `{issue['idReadable']}` {issue['summary']}{state}{assignee}; updated: {issue['updated'][:10]}; {issue['url']}")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    load_dotenv()
    args = parse_args()
    token = get_required_env("YOUTRACK_TOKEN")

    client = YouTrackClient(args.url, token, insecure=args.insecure)
    board = find_board(client, args.board)
    sprint = find_sprint(client, board["id"], args.sprint) if args.sprint else get_current_sprint(client, board)
    raw_issues = [issue for issue in get_sprint_issues(client, board["id"], sprint["id"]) if is_reportable_issue(issue)]
    for issue in raw_issues:
        issue["comments"] = get_issue_comments(client, issue["id"])
    issues = [normalize_issue(issue, args.url) for issue in raw_issues]
    me = client.get("/users/me", {"fields": "id,login,fullName"})
    goal = goal_summary(issues, me, sprint, args.goal)
    backlog_query = args.backlog_query or default_backlog_query(board)
    backlog = [
        normalize_issue(issue, args.url)
        for issue in get_backlog_issues(client, backlog_query)
        if is_reportable_issue(issue)
    ]
    report = render_report(board, sprint, issues, goal, backlog)

    output = args.output or sprint_output_base(sprint).with_suffix(".md")
    json_output = args.json_output or output.with_suffix(".json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    json_output.write_text(
        json.dumps(
            {
                "board": board,
                "sprint": sprint,
                "goal": goal,
                "issues": issues,
                "backlogQuery": backlog_query,
                "backlog": backlog,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if args.stdout:
        print(report)
    else:
        print(f"Wrote {output}")
        print(f"Wrote {json_output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
