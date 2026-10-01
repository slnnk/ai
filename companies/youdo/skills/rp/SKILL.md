---
name: rp
description: Generate YouDo operational daily and sprint reports from Mattermost, YouTrack and the agents' work log when the user invokes /rp, asks for an rp report, or asks to prepare daily/weekly/sprint work reports (including "за прошлую неделю" or a given sprint). Collect Mattermost source messages, snapshot the YouTrack sprint that covers the report period, add work recorded in ~/ai work-log entries, synchronize clear task matches, write final daily and sprint weekly reports, and avoid automated event noise.
---

# rp

Use this skill for `/rp`, `/rp <date>`, `/rp <sprint N>`, "rp за прошлую неделю" and other
requests to prepare YouDo work reports.

## Locations

Scripts live next to this file; run them by absolute path from any directory:

    S=~/ai/current/skills/rp/scripts

Data lives outside the `~/ai` repository (it contains private messages), in `~/ai-data/rp/`:

| Path | Written by | Content |
| --- | --- | --- |
| `mattermost/YYYY-MM-DD.{md,json}` | `mattermost_daily.py` | source messages of one day |
| `youtrack/YYYY-Www-<sprint>.{md,json}` | `youtrack_sprint.py` | sprint issues snapshot |
| `daily/YYYY-MM-DD.md` | agent | final daily report |
| `weekly/YYYY-Www-<sprint>.md` | agent | final sprint weekly report |

Never write final reports into `mattermost/` or `youtrack/`. Overrides: `RP_DATA_DIR`
(data root), `RP_ENV_FILE` (default `~/ai/current/.env`).

Access variables in `~/ai/current/.env`: `MATTERMOST_URL`, `MATTERMOST_TOKEN`,
`YOUTRACK_TOKEN`; optional `MATTERMOST_REPORT_TZ` (default `Europe/Moscow`),
`MATTERMOST_TEAM`, `MATTERMOST_INCLUDE_PRIVATE_CHANNELS` (default `true`), `YOUTRACK_URL`,
`YOUTRACK_BOARD` (default `DevOps Scrum Board`). Never print their values. If one is
missing, name it and stop.

Both scripts call the APIs (GET only) and need network access. In a sandbox the first run
can fail with `socket.gaierror: [Errno -2] Name or service not known`; rerun the same
command with network permission.

## Sources

1. **YouTrack** (always first):

       python3 $S/youtrack_sprint.py              # current sprint
       python3 $S/youtrack_sprint.py --sprint 181 # sprint number, full name or id

   Sprints run Sunday 03:00 to Sunday 02:59 Moscow time; the file week is the week of the
   Monday. Ignore draft placeholders such as `Issue.Draft` and issues without a real
   summary.

   The snapshot also holds `goal` (resolved vs open sprint issues assigned to the token
   owner, target `--goal`/`RP_SPRINT_GOAL`, default 10, working days left) and `backlog`:
   unresolved issues of the board projects that are in no sprint (default query
   `project: DevOps #Unresolved has: -{Board DevOps Scrum Board}`, override
   `--backlog-query`/`YOUTRACK_BACKLOG_QUERY`).

2. **Mattermost**, for each needed date:

       python3 $S/mattermost_daily.py --date YYYY-MM-DD --include-sources

   The script selects threads in direct and group chats, and channel threads where the owner
   wrote that day. Threads that only mention the owner are excluded. Webhook, bot and system
   posts (release, autotest, iOS events) come under the owner's user id; they are dropped
   unless they start a thread with human messages, and are labelled `бот`
   (`--include-automated` keeps them all). Code blocks are kept as `[code: <first 300
   chars>]`. It only collects and groups messages; it does not infer tasks, causes or
   solutions.

3. **Agent work log**: `~/ai/current/knowledge/log/YYYY-MM-DD-*.md` for the report date. These
   entries record what the user did with AI agents (diagnostics, fixes, changes), which is
   often absent from Mattermost. Read each entry's task and findings sections only. Skip
   entries about the knowledge base itself or about `rp` runs. A log entry alone is
   evidence of work done, but not of its outcome: report it only as far as the entry
   states.

4. **YouTrack activity of the owner**: comments by the token owner and issues resolved on the
   report date (from the snapshot JSON) count as evidence of that day's work, with or
   without Mattermost context. Comments by others only give context.

5. **Backlog**: open items in the `## YouDo` part of `~/ai/TODO.md`, used only to match
   report topics with known open work in `В процессе`. Do not list backlog items that have
   no activity in the period.

## Resolving the period

- `/rp`: today's local date and the current sprint.
- `/rp <date>`: resolve the full date (a bare day number takes the current month and year).
  If the date is outside the current sprint, find its sprint and pass `--sprint`.
- "за прошлую неделю": the previous Monday-Sunday. Example: on 2026-06-29 that is
  2026-06-22..2026-06-28, `DevOps sprint - 181`, not the new current sprint 182.
- `/rp <sprint N>`: `--sprint N`, all working days from sprint start to
  min(sprint finish, today).

State the resolved dates and sprint in the first line of the answer, and for the current
sprint the goal progress: `Цель: N/10 закрыто, не хватает M, рабочих дней: K`.

## Workflow

1. Snapshot YouTrack for the resolved sprint.
2. For each working day of the sprint period up to today that has no daily report in
   `daily/`, and for the requested date(s): collect Mattermost, read the work log, write the
   daily report. Monday-Friday by default; a Saturday or Sunday only when requested or when
   its daily report already exists.
3. Read the previous working day's daily report. Carry its unresolved `Требует уточнения`
   items forward when the new day's sources settle them, or keep asking about them.
4. Ask the targeted clarification questions (see below), apply the answers.
5. Update the sprint weekly report.
6. Show the daily report (and the changed weekly sections) in the answer.

## Daily report

Sections, only when non-empty:

- `Выполненные работы`
- `Участие в тестировании и консультации`
- `Кандидаты для задач`
- `Требует уточнения`

Rules:

- Cover every user request or task found in the contexts, not only topics that match known
  keywords; read the JSON or `--include-sources` output, not just the context list.
- Omit automated event posts, empty messages, build/release notifications and failed test
  reports, unless a human thread discusses troubleshooting or action on that exact event.
  No separate section for releases or automated events.
- Do not merge unrelated events because they share a broad keyword; group by thread,
  channel and intent, and split or drop weak matches.
- Add a YouTrack key only for an explicit reference or a clear match (summary, description,
  custom fields, comments). Do not force weak matches; do not add YouTrack-only items.
- Confirmed work with no sprint issue: propose creating/adding a sprint task, in the daily
  and the weekly report.
- For completed fixes in `Кандидаты для задач`, write `Проблема / Причина / Решение` when the
  sources support all three. A pure clarification question is not a task candidate unless
  the user did work, committed to a follow-up, or an actionable task clearly follows.
- State causes, diagnostics and solutions only when the sources support them; otherwise say
  "не подтверждено в сообщениях", "требует проверки".

Clarification: if a relevant context has an unclear outcome (help or testing moved to a
call or private chat, a deploy without a completion message), ask targeted questions before
finalizing the report, unless the user asked to proceed without them. Leave items the user
does not answer under `Требует уточнения`.

## Sprint weekly report

Based on the freshest snapshot of the report-period sprint, brief, by task or topic with
dates; never paste daily reports:

- `Сделано`: completed work confirmed by daily reports, and fixed sprint issues with
  supporting context.
- `В процессе`: sprint issues or topics still open, with daily context when available.
- `Рекомендации по недостающим задачам`: confirmed work with no sprint task (as a proposal
  to create/add it), weak matches to check, sprint tasks that need follow-up.
- `До цели спринта` (current sprint only; for a finished sprint give just the final count):
  the goal line from the snapshot, then proposals, cheapest first, enough to cover the gap
  (at most 8), and say honestly whether they can close it:
  1. confirmed done work without a task: "завести и закрыть";
  2. the owner's open sprint issues with activity: what is left to close them;
  3. `backlog` issues worth taking into the sprint: related to this period's work, small, or
     already assigned to the owner or unassigned; give the reason and the first step;
  4. open items of the `## YouDo` part of `~/ai/TODO.md` that could become a task.
  Show this section in the `/rp` answer too.

The user creates, moves and closes YouTrack issues personally: never create or change
issues, only propose. Do not propose splitting one piece of work into several tasks or
tasks for trivial one-off consultations just to reach the goal.

## After the run

- Do not write a work-log entry for a routine run; the reports in `~/ai-data/rp/` are the
  record.
- Open follow-ups the user wants to track go to the system's section of `~/ai/TODO.md`, not
  only into `Рекомендации`.
- When the user corrects a report in a way that changes how reports should be made,
  update this file (rules here, deterministic behavior in the scripts; no hard-coded
  topics in the scripts) and add a line to `~/ai/.sync-notes`.
