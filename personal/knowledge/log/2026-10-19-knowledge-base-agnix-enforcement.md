---
system: knowledge-base
status: verified
checked: 2026-10-19
tags: [agents, agnix, sync, checks]
---
# Knowledge base: mandatory agnix checks and change-aware sync fallback

## Summary
The user explicitly requested both proposed mechanisms: mandatory agent checks after instruction/skill/settings edits and an automatic change-aware fallback through the existing sync entrypoint. Implemented in AGENTS, README, agent_lint.py and ai-sync.sh. This supersedes the original optional manual adoption mode without changing Git publication permissions or enabling auto-fix. Sixteen new isolated lint/integration tests and ten existing sync tests passed; live pinned agnix scanned9files with0errors,4previously classified warnings and2informational findings.

## Task and authorization
Actual user request: "Сделай сразу и обязательную и через синхронизацию." This authorizes local implementation of the two mechanisms discussed immediately beforehand. It does not authorize external changes, installation elsewhere, auto-fix or a blocking Git publication gate. The [initial agnix pilot](2026-10-19-knowledge-base-agnix-instruction-loading-pilot.md) is retained as history. The prior optional personal learning record was resolved as superseded; the new global expectation points to AGENTS.

## Implementation
- `~/ai/AGENTS.md`: after changing agent instructions, skills including resources/scripts, or settings, run `python3 ~/ai/general/scripts/agent_lint.py --force` before the final response; add external repository-local paths when needed, review findings and report results or pending failure.
- `~/ai/general/scripts/agent_lint.py`: report-only wrapper; prefers the pinned0.59.0 binary then PATH, supports explicit binary and additional input paths, watches content hashes and link targets, serializes concurrent checks with a local lock, writes atomic successful snapshots and sanitized reports.
- `~/ai/general/scripts/ai-sync.sh`: normal calls run the change-aware check after dry-run handling and before the same-day Git skip. Changed instructions are therefore checked between tasks even after today's Git sync. Unchanged successful input snapshots are quiet. Lint errors or execution failures are printed and leave retry pending; normal Git synchronization continues.
- `~/ai/general/knowledge/README.md`: updated daily-sync behavior, script catalog, exact inventory, explicit post-edit command, state/report location, retry semantics and coverage limits.
- `~/ai/general/scripts/tests/test_agent_lint.py`:16isolated tests; no actual Git publication or infrastructure calls.

## Inventory and state
Default coverage: KB AGENTS/override/CLAUDE/GEMINI instruction entrypoints; SKILL bodies and their text/code resources; settings/rules near discovered KB instruction roots; root agnix config; global Claude/Codex instructions/settings, including Claude local settings/rules; user skill links/resources in `.codex/skills`, `.claude/skills`, `.agents/skills`; the canonical KB rule README and lint/sync code. Runtime system/plugin catalogs are excluded. Additional directory arguments include instruction/skill entrypoints/resources; supply additional repository-local settings files explicitly.

Deduplication preserves different instruction filenames because they select tool-specific agnix checks: the Claude CLAUDE alias is checked separately from its canonical AGENTS target. Link rewiring, deletions, new files, resource edits, changed executable and changed root agnix settings invalidate the snapshot. Agnix runs from the deterministic KB root. Inputs are rediscovered after checking to detect concurrent file creation/editing. Only successful complete scans advance the snapshot; warnings are permitted, error findings and infrastructure failures are not. Missing executables are reported without automatic installation.

Machine-local `~/ai-data/agnix/` contains success.json, report.json and check.lock, outside Git. Snapshot data is hashes/link locations, not file contents. Reports retain severity/rule/file/line/column and counts, stripping raw settings, source text and diagnostic messages. Subprocess stdout/stderr are never forwarded raw. Existing secrets files are excluded. A user-facing failed-check message takes precedence over an older retained report.

## Validation
New16tests cover successful unchanged skip, explicit force, resource edits/deletions, instruction creation/deletion, runtime settings changes, binary changes, persistent lint errors, malformed output/timeouts retaining prior checkpoint, missing binary, concurrent changes, sanitized diagnostics, extra repository inputs, same-day sync with no Git calls, root linter config and deterministic cwd, runtime skill rewiring/resources, alias-sensitive entrypoints, and global Claude settings/rules. The same-day integration also confirms error findings remain visible while Git skip succeeds, and status/help do not invoke lint. Existing10sync tests include strict dry-run zero-mutation snapshots of working files/index/Git objects/state and unsupported shared-storage handling. Bash syntax check passed.

Live check command: `python3 -B ~/ai/general/scripts/agent_lint.py --force`:9files,0errors,4warnings,2info. Warnings are the previously reviewed3prompt-engineering prohibitions and service-tier schema warning; informational results cover the generic overview and intentional project override. No policy weakening or model-setting change follows from these heuristics. Static lint does not replace behavioral tests or grant permission for fixes.

## Reconciliation and limits
The original optional/manual decision is preserved and explicitly superseded in its pilot note and learning history. Central TODO records this completed request; other-PC setup and blocked Claude model evaluation remain open. This is not a general hook framework, runtime guarantee of agent obedience or a full implementation of the later explicit-invocation-control pilot. No scheduled job, model call, automatic installation, auto-fix or new external write permission was added. Existing agent startup calls provide the sync trigger; no call means no fallback execution.

The wrapper and policies travel with the KB repository; binary and successful state remain per machine. On a new PC absence is visible and retried until installation is authorized/completed. No new standalone portable recipe or duplicate system map was created; README is the canonical operational documentation. Final verification: live unchanged same-day ai-sync completed quietly, skipping both repeat lint and daily Git work. KB lint reported0errors and6existing warning categories; indexes rebuilt with0missing frontmatter in the affected personal layer. No manual staging, commit, push or external publication was performed.
