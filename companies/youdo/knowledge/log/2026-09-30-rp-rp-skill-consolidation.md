---
system: rp
status: verified
checked: 2026-09-30
tags: [rp, mattermost, youtrack]
---
# rp skill moved into ~/ai, data into ~/ai-data

## Task
Review the `rp` skill and consolidate it: one copy in `~/ai`, data outside the repo,
`~/mygit/youdo-ai` retired.

## Context
`~/.claude/skills/rp` and `~/.codex/skills/rp` link to `~/ai/current/skills/rp`. That copy
lacked the 2026-06-29 fix (`--sprint` for past periods, `Issue.Draft` filter), which only
existed in `~/mygit/youdo-ai/skills/rp/SKILL.md`. Scripts and reports lived in
`~/mygit/youdo-ai` and were addressed by relative paths, so `/rp` only worked from that
directory. Its `.git` is broken (not a working clone).

## Actions
- Copied `scripts/mattermost_daily_report.py` -> `skills/rp/scripts/mattermost_daily.py`,
  `scripts/youtrack_current_sprint.py` -> `skills/rp/scripts/youtrack_sprint.py`.
- Scripts now read `~/ai/current/.env` (`RP_ENV_FILE`) and write to `~/ai-data/rp/<source>`
  (`RP_DATA_DIR`), independent of the working directory.
- `youtrack_sprint.py` prints sprint periods in Moscow time (was UTC).
- Added `MATTERMOST_URL`, `MATTERMOST_TOKEN`, `MATTERMOST_REPORT_TZ`, `MATTERMOST_TEAM`,
  `MATTERMOST_INCLUDE_PRIVATE_CHANNELS` to `~/ai/current/.env` (from the old repo `.env`).
- Copied all reports to `~/ai-data/rp/{mattermost,youtrack,daily,weekly}` (77 files).
- Rewrote `SKILL.md`: merged the reporting rules from the old `AGENTS.md`, added past-week
  and sprint-N resolution, work-log (`knowledge/log/<date>-*.md`) and `TODO.md` as sources,
  carry-over of `Требует уточнения`, no work-log entry per routine run.
- Added `~/ai-data/` to the Layout in `~/ai/AGENTS.md`.

## Findings
- Sprints run Sunday 03:00 to Sunday 02:59 MSK (= 00:00 UTC), so ISO-week file names were
  already correct under UTC; no rename needed.
- Test runs from `/` worked for both scripts (`--sprint 185`, `--date 2026-07-22`).
  Mattermost returned 77 messages for 2026-07-22 vs 21 in the old snapshot, presumably
  because the old one was taken during that day (hypothesis).

## Changes
- `companies/youdo/skills/rp/SKILL.md`, `companies/youdo/skills/rp/scripts/*.py`
- `companies/youdo/.env` (variable names above; values not recorded)
- `AGENTS.md` (Layout)
- `~/ai-data/rp/` (outside git)

- Follow-up same day: `mattermost_daily.py` now drops webhook/bot/system posts. Webhook posts
  (`props.from_webhook = "true"`, `type = slack_attachment`, `override_username` IOS,
  autotests, youdo-business) carry the owner's user id, so they counted as the owner's own
  messages and pulled in whole bot threads (2026-09-29: 55 -> 7 messages, 2026-09-28:
  50 -> 29, no human context lost). Code blocks keep their first 300 chars instead of
  `[code block]`. `--include-automated` restores the old selection. The "25 sources" limit
  in the old `AGENTS.md` does not exist in the code.

- Sprint goal: `youtrack_sprint.py` adds `goal` (resolved vs open sprint issues assigned to
  the token owner, target `RP_SPRINT_GOAL` default 10, working days left) and `backlog`
  (`project: DevOps #Unresolved has: -{Board DevOps Scrum Board}`, 19 issues on 2026-09-30;
  `Board DevOps Scrum Board: {No sprint}` returns 0). SKILL.md: weekly section
  `До цели спринта`; the user creates and closes YouTrack issues personally, the skill
  only proposes.

## Open items
- `~/mygit/youdo-ai` can be deleted by the user; everything is copied.

## Portable lesson

none
