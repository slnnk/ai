# TODO: knowledge base backlog

Owner: the user. Agents read this file when asked to review the backlog and add entries only
when the user asks. Mark done items with `[x]` and the date; do not delete them for a month.

## Open

- [ ] Staleness review. Add `build_index.py --stale <days>` (or an INDEX section) listing
      system maps whose `checked` is older than the threshold, then review monthly: confirm,
      update, or set `status: outdated`. Include the `hypothesis` recipes in `general/`.
      (proposed 2026-09-23)
- [ ] Feed `knowledge/log/` into the `rp` skill as a third source for daily and sprint
      reports, next to Mattermost and YouTrack. (proposed 2026-09-23)
- [ ] Observe agent behaviour for two weeks: do daily sync commits have a non-empty
      "Work recorded by agents" section when "Files" is non-empty? If not, tighten the
      wording in AGENTS.md or move the rule into a skill. (proposed 2026-09-23)
- [ ] `companies/youdo/.env`: key `ZABBIZ_DEV_TOKEN` looks like a typo of `ZABBIX_DEV_TOKEN`;
      there is also an empty line. Rename if no script depends on it. (proposed 2026-09-23)
- [ ] Review the Claude per-project memory directories under `~/.claude/projects/*/memory`
      (automation-services, sorm, youdo-mcp, home) and move anything durable into `~/ai`.
      (proposed 2026-09-23)
- [ ] Read `companies/youdo/CONTEXT.md` once and correct the inferred stack and conventions.
      (proposed 2026-09-23)
- [ ] Keep `AGENTS.md` at or below about 5 KB; move anything domain-specific to
      `general/knowledge/README.md` or `CONTEXT.md`. Check quarterly. (proposed 2026-09-23)
- [ ] Decide whether to link the team skills repository `~/git/ai-skills/skills/*` into
      `companies/youdo/skills/` via symlinks. (proposed 2026-09-23)

## Done
