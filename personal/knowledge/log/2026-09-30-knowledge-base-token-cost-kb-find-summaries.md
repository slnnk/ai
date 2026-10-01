---
system: knowledge-base
status: verified
checked: 2026-09-30
tags: [token-cost, kb_find, kb_lint]
---
# Knowledge base: token cost step 1 (kb_find, summaries, AGENTS.md, token_usage)

## Task

First step of the "Token cost optimization" block in `~/ai/TODO.md`: stop agents from reading
`INDEX.md` and whole 20-40 KB system maps on every task.

## Context

- Before: `AGENTS.md` told agents to `grep -ril` and open `INDEX.md` plus the system map.
- 37 notes over 8 KB (20 logs, 15 non-log incl. `repos.md`), none had a `## Summary`.
- `AGENTS.md` was 6829 bytes (target about 5 KB, separate TODO item).

## Actions

- New `general/scripts/kb_find.py <keywords>`: AND (or `--any`) search over the three
  layers; per note prints path, system, status, checked, size, summary flag, title and the
  first `-n` matching lines with line numbers; ranked by hits in filename/title/system.
  Options `-l layer`, `-s system`, `-m max notes`, `--regex`, `--files`. Exit 1 on no hits.
- `kb_lint.py`: new warning `summary` for notes over 8 KB outside `knowledge/log/`
  (and not `repos.md`) without `## Summary`.
- `AGENTS.md` "Before a task": the `grep -ril` bullet replaced by `kb_find.py` plus
  "read a long note by its Summary and the needed section"; size 6829 -> 6822 bytes.
- `general/knowledge/README.md`: `## Summary` in the system map template, `kb_find.py` in
  the scripts table.
- Summaries (10-15 bullets) added by three parallel Sonnet subagents to:
  `dev-deployment/{overview,gitlab-ci-deploy-dev,post-deploy-autotests,jenkins-deploy-dev-b2b}.md`,
  `yandex-cloud/terraform-test-k8s.md`, `android-farm/system-map.md`. Verified with
  `git diff --numstat` that only lines were inserted.
- `overview.md` summary corrected by hand from `TODO.md` Done: TKB fix deployed (job
  `3120801`), `auto_stop_in` expiry verified (job `3120803`), DevOps-832 merged 2026-09-29.

### Second pass (same day)

- Summaries (about 230-290 words, `Stale:` bullet) added by four Sonnet subagents to the
  remaining 8 maps: `android-farm/ci-cd`, `automation-services/{local-vault-ansible-access,
  yandex-test-nginx}`, `gitlab-ci/{android-youdo4-dynamic-runner,resource-groups}`, `sorm`,
  `yandex-cloud/{terraform-network,terraform-test-infra}`. `Stale:` bullets added by hand to
  `android-farm/system-map` and `terraform-test-k8s` from the subagent reports. All 14 maps
  over 8 KB now have a Summary; `git diff --numstat` shows insertions only.
- `AGENTS.md` rewritten from 6829 to 5084 bytes: compact layout, merged note rules, new
  "Token economy" section (check `scripts/` first, 3+ commands twice -> script, delegate
  reading >3 files to a subagent, compact output, `model:` line in prompts). Git, remote
  changes and secrets sections kept verbatim. "Connecting an agent" moved to
  `general/knowledge/README.md`. Backup of the old file only in the session scratchpad.
- `general/prompts/{extract-recipe,normalize-notes}.md`: `model:` tier line.
- New `general/scripts/token_usage.py [--days N] [--top N]`: reads Claude Code transcripts
  (`~/.claude/projects/**/*.jsonl`, usage deduplicated by message id, subagents roll into
  the parent session) and Codex sessions (`~/.codex/sessions/**`, last cumulative
  `token_count`); prints fresh input, cache read, cache write, output per agent/project/model
  and the top sessions. No prices.

### Baseline (token_usage.py --days 7, 2026-09-30)

- Claude, 12 sessions: fresh 9k, cache read 95.3M, cache write 3.5M, output 539k. Codex: no
  sessions in 7 days (45 days: 90 sessions, 466M cache read, mostly `gpt-5.6-sol`).
- Top Claude sessions: 2026-09-28 `~` 47.2M in, 2026-09-23 `~` 26.9M in (hypothesis from the dates: the
  TODO consolidation and the knowledge-base setup), 2026-09-25 `~/mygit/home-infra` 9.7M in.
- Input is dominated by cache reads, i.e. long sessions re-reading their context; shorter
  sessions and less file content in context matter more than output length.
  (Interpretation, not measured per cause.)

### Third pass: stale sections (same day)

- Eight Sonnet subagents reconciled 12 maps (the 11 with a Stale bullet plus
  `post-deploy-autotests`), rule: never delete facts; mark history inline
  `(superseded YYYY-MM-DD: see <section>)`; correct current-state tables only from evidence
  inside the note or `TODO.md` Done; unresolved items stay in the Summary. Diff vs HEAD:
  +331 -129 lines over 14 maps; removed word chunks reviewed.
- Review found and fixed: android `system-map` header lost `Scope` and the CI/CD map link
  (restored); my earlier hand insertion put that map's Stale bullet after the header block
  instead of inside Summary (moved). Body `Last checked/verified` dates changed by
  subagents all equal frontmatter `checked`.
- Resolved read-only from local clones after `git fetch`: `gitlab-ci-templates`
  `origin/master` `76347cd` has `.rules-mr-manual` and `GITLAB_PROJECT_ID` in
  `v3/.deploy-dev.yml`; docvalidation `origin/master` `a87c447` includes it without `ref`;
  `helm-charts` `origin/master` `4ab8743` has the `PGDATA` fix and a shortened migration Job
  name without `trunc 63`. Template commits `12b72c9`, `76347cd`, `29734d7`, `7ddb8813`
  exist in `gitlab-ci-templates`.
- Summaries of `overview` (~450 words) and `gitlab-ci-deploy-dev` (~510) stayed over the
  300-word target.

### Fourth pass: measurement automation (same day)

- `token_usage.py --kb`: classifies Claude `tool_use` (Bash command, Read path/offset) and
  Codex `custom_tool_call`/`function_call` text into kb_find / search / index / full /
  partial by `~/ai` knowledge paths; paths reached via `cd` + bare file name are missed.
  First run flagged Codex greps over the old `~/.codex/knowledge` as KB searches; the
  directory regex was narrowed to `~/ai` layer paths. `--brief` prints one line.
- Baseline `--kb`, 7 days to 2026-09-30, Claude, 10 sessions: kb_find 8 (all from this
  session), search 142, INDEX 7, full reads 47 (1086 KB by current file size), partial 79.
  Most read in full: `general/knowledge/README.md` 8x, `repos.md` 4x,
  `post-deploy-autotests.md` 4x. Codex had no `~/ai` access in the window.
- `ai-sync.sh` step 1b: when the newest `personal/usage/????-??-??.txt` is 7+ days old (or
  none), writes `token_usage.py --days 7 --kb` there, logs `--brief` and appends it to
  `.sync-notes`; skipped on `--dry-run`, never fails the sync. Tested in isolation twice
  (second run skipped); not run for real today because the daily sync was already done.
  `--help` now prints the header up to `set -u`.
- `kb_lint.py`: now also scans root `AGENTS.md`; warning `size` above 5632 bytes. Tested on
  a padded copy in a temporary `AI_ROOT`.

## Findings

- First-pass summaries are wordy (360-720 words); second pass with a 300-word cap gave
  230-290 words. Both are 5-10x smaller than the notes.
- Subagents reported internal contradictions: chronological notes where older sections
  were never updated (stale "pending" states, superseded variable names, body
  `Last verified` older than frontmatter `checked`). 11 of 14 summaries end with an
  "Oddities"/"Stale:" bullet listing them. A summary inherits staleness from the body; it was only corrected
  for `overview.md`.

## Changes

- `general/scripts/kb_find.py`, `general/scripts/token_usage.py` (new),
  `general/scripts/kb_lint.py`, `AGENTS.md`, `general/knowledge/README.md`,
  `general/prompts/*.md`, 14 system maps in `current/knowledge/systems/`.

## Open items

Tracked in `~/ai/TODO.md`, section "Knowledge base".

## Portable lesson

none
