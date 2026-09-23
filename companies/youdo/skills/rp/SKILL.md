---
name: rp
description: Generate YouDo operational daily and sprint reports from Mattermost and YouTrack when the user invokes /rp, asks for an rp report, or asks to prepare daily/weekly/sprint work reports. Collect Mattermost source messages, refresh the current YouTrack sprint snapshot, synchronize clear task matches, write final daily and weekly sprint reports, and avoid automated event noise.
---

# rp

Use this skill for `/rp`, `/rp <date>`, and requests to prepare YouDo work reports.

## Sources

Always refresh YouTrack first:

```bash
python3 scripts/youtrack_current_sprint.py
```

Collect Mattermost for each needed date:

```bash
python3 scripts/mattermost_daily_report.py --date YYYY-MM-DD --include-sources
```

Both scripts need network access. If sandbox DNS/network fails, rerun the same command with network permissions.

## Paths

- Mattermost sources: `reports/mattermost/YYYY-MM-DD.md` and `.json`
- YouTrack sprint snapshot: `reports/youtrack/YYYY-Www-<sprint>.md` and `.json`
- Daily final reports: `reports/final/daily/YYYY-MM-DD.md`
- Sprint weekly reports: `reports/final/weekly/YYYY-Www-<sprint>.md`

Do not write final reports into `reports/mattermost`; that directory is only for Mattermost sources.

## Invocation

For `/rp` with no date:

1. Use today's local date.
2. Refresh YouTrack current sprint.
3. Collect Mattermost for today.
4. Write today's daily final report.
5. Update the current sprint weekly report.

For `/rp <date>`:

1. Resolve the date explicitly. If the user gives only a day number, infer month/year from the current local date.
2. Refresh YouTrack current sprint.
3. Collect Mattermost for that date.
4. Write the daily final report for that date.
5. Update the sprint weekly report that belongs to the refreshed YouTrack sprint.

Weekends are normally skipped when filling missing days, but if the requested date is a weekend, collect it, write its daily report, and include it in the sprint weekly report.

## Filling Missing Days

When updating a sprint weekly report:

1. Read the refreshed YouTrack sprint start/finish.
2. Consider dates from sprint start through min(sprint finish, today), using local report timezone.
3. Include Monday-Friday by default.
4. Include Saturday/Sunday only when the user explicitly requested that weekend date or an existing daily final report is already present.
5. If a required daily final report is missing, collect Mattermost for that date and write the missing daily report before updating weekly.

## Daily Report Rules

Analyze Mattermost JSON/Markdown and synchronize with YouTrack JSON.

Include sections only when useful:

- `Выполненные работы`
- `Участие в тестировании и консультации`
- `Кандидаты для задач`
- `Требует уточнения`

Omit automated event posts, empty messages, build/release notifications, and failed test reports unless a human thread explicitly discusses troubleshooting/action on that exact event.

Add a YouTrack issue key only for explicit references or clear matches to current sprint issues. Do not force weak matches and do not add YouTrack-only items without supporting Mattermost context.

If confirmed Mattermost work is not covered by a current sprint issue, explicitly propose creating/adding a sprint task for it in both the daily report and the sprint weekly report.

For completed fixes in `Кандидаты для задач`, use concise `Проблема / Причина / Решение` wording when messages support all three parts.

If a relevant context has unclear outcome or completion, ask targeted clarification before finalizing the daily report, unless the user explicitly asks to proceed without clarification.

## Sprint Weekly Report Rules

Use the freshest YouTrack snapshot as the source of sprint scope and states. Structure weekly reports briefly:

- `Сделано` - completed work confirmed by daily reports and/or fixed current-sprint issues with Mattermost support.
- `В процессе` - current-sprint issues or report topics still open/in progress, with supporting daily context when available.
- `Рекомендации по недостающим задачам` - confirmed Mattermost work missing a clear current-sprint task, weak matches that should be checked, or sprint tasks that appear to need follow-up. For uncovered confirmed work, phrase the recommendation as a proposal to create/add a task to the sprint.

Do not paste full daily reports into the weekly report. Summarize by task/topic and cite dates.
