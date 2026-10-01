---
system: knowledge-base
status: verified
checked: 2026-09-30
tags: [knowledge-base, claude-memory]
---
# Knowledge base: Claude memory moved into ~/ai, .env cleanup, staleness report

## Task

Two TODO items from the "Knowledge base" section: remove the empty line in
`companies/youdo/.env`; review Claude per-project memory under `~/.claude/projects/*/memory`
and move durable facts into `~/ai`.

## Context

Agent memory is a cache per AGENTS.md; durable facts must live in `~/ai`.

## Actions

- `companies/youdo/.env`: deleted empty line 9 (`sed -i '9{/^[[:space:]]*$/d}'`); 16 lines,
  no empty lines left. Values were not printed.
- Listed all memory directories: 9 under `~/.claude/projects/`, only two non-empty:
  - `-home-slnnk-git-yandex-tf/memory/scope-cleanup-to-task.md` (feedback, DevOps-866):
    "remove what is not needed" means only task-related code.
  - `-home-slnnk/memory/ai-knowledge-base-git-policy.md` (feedback): `~/ai` is one private
    repo, company layer tracked, only `.env` ignored.
  - Empty: automation-services, gitlab-ci-templates, lenochka, sorm, youdo-giveaway-bot,
    youdo-mcp, home-infra.

## Findings

- Neither fact was recorded in `~/ai` before.
- Remotes checked with `git remote -v`: `origin` fetches `git@github.com:slnnk/ai.git` and
  pushes to both it and `git@gitflic.ru:slnnk/ai.git`; a separate `gitflic` remote also
  exists. The memory was correct (a first reading of truncated output was wrong).

## Changes

- `AGENTS.md` (symlinked as `~/.claude/CLAUDE.md`): new section "Code changes" with the
  scope-of-cleanup rule; size 5268 bytes (lint limit 5.5 KB).
- `general/knowledge/README.md`, "Daily sync": paragraph on the repository policy (remotes,
  company layer tracked, `.gitignore` holds only `.env` and sync state files).
- `companies/youdo/.env`: empty line removed.
- Memory files left in place as cache.

## Staleness report (same day)

- `general/scripts/build_index.py --stale DAYS`: prints maps and topic notes (not `log/`,
  not `outdated`) with `checked` older than DAYS or missing, plus all `hypothesis` notes;
  writes nothing. Not put into `INDEX.md` on purpose: a date-dependent section would change
  the index every day and break `--check`.
- First run with 30 days for everything: 45 notes due, 34 of them `general` recipes. Recipes
  age slowly, so the user agreed to split thresholds: maps 30 days, recipes and other
  non-map notes `--recipe-days 180` (default). Result: 13 due (11 maps, 2 recipes; 6
  hypothesis). `--count` prints only the number.
- `ai-sync.sh` step 1c: on the first sync of a month, if notes are due, adds
  `Monthly staleness review YYYY-MM` to `TODO.md` "## Knowledge base" and prints a reminder;
  the TODO item is the state (no extra state file). Tested twice on a copy of `~/ai`: one
  item added, second run no-op. First real item: first sync on 2026-10-01.
- `AGENTS.md` "Before a task": do not hide `ai-sync.sh` output, pass reminders to the user.

- Dated reminders (same day): `ai-sync.sh` step 1d prints open `TODO.md` items
  `- [ ] due YYYY-MM-DD: ...` whose date has come, on every daily sync until closed. Tested
  with `TODAY=2026-10-11/12/14`: 0, 1, 2 reminders. Set on the agent-behaviour observation
  (due 2026-10-12) and the token usage comparison (due 2026-10-14). Team-skills symlink item
  closed as not relevant (user).
- `companies/youdo/CONTEXT.md` reviewed with the user (same day). From notes: ticket format
  `DevOps-832` (not `DEVOPS-`), `Site-*`, articles `DevOps-A-*`; added VictoriaMetrics/vmagent,
  Grafana, Sentry, Jaeger, RabbitMQ, Redis, Hangfire, Yandex Object Storage, Temporal, AWX
  `awx-ee`, Loki in the dev cluster. From the user: Jenkins is active only for test stands
  (Nomad deploys, web autotests); Nomad + Consul for test/prod, K8s for dev, migrating to K8s;
  only sorm is out of scope; `~/git/ai-skills` line removed. The dev-deployment map shows the
  B2B ephemeral K8s deploy also runs via Jenkins job `test`; the user clarified that ephemeral
  dev environments are the replacement for the Nomad test stands (target direction).

## Open items

none; the first review arrives as the 2026-10 TODO item.

## Portable lesson

none
