---
system: rp
status: verified
checked: 2026-06-29
tags: [rp, reports, youtrack, sprint-181, sprint-182, youtrack_current_sprint]
---
# youdo-ai rp: report for the previous week (2026-06-29)

## Task

- Context: `/home/slnnk/mygit/youdo-ai`, request `rp за прошлую неделю` ("rp for last week").
- Date period resolved as 2026-06-22..2026-06-28 in Europe/Moscow.

## Findings

- Important correction from user: that past week belonged to `DevOps sprint - 181`; `DevOps sprint - 182` started on 2026-06-29 and must not be used for previous-week reports.
- Correct command for this period: `python3 scripts/youtrack_current_sprint.py --sprint 181`.

## Changes

- Updated `scripts/youtrack_current_sprint.py` to support `--sprint` by sprint number, full name, or YouTrack sprint id.
- Generated source snapshots:
  - `reports/mattermost/2026-06-22..2026-06-26.{md,json}`
  - `reports/youtrack/2026-W26-devops-sprint-181.{md,json}`
- Generated final reports:
  - `reports/final/daily/2026-06-22.md` through `reports/final/daily/2026-06-26.md`
  - `reports/final/weekly/2026-W26-devops-sprint-181.md`
- Updated repository instructions in `AGENTS.md` and `skills/rp/SKILL.md` to avoid using current sprint blindly for past-week/past-sprint reports.

## Portable lesson

none
