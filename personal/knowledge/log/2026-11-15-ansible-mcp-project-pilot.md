---
system: ansible-mcp
status: verified
checked: 2026-11-15
tags: [ansible, mcp, codex]
---
# Project-scoped Ansible MCP pilot

## Task

Connect Ansible MCP to the personal Ansible repository as a reference-only pilot.
The user explicitly required shared files in `~/ai`, without changing global
`~/.codex`. This constraint applies to this integration.

## Context and approvals

- Repository: `/home/slnnk/mygit/ansible`, existing `master`, base `master`.
- The user approved reuse of that branch with `Да` after the concrete proposal.
- Preserve unrelated untracked repository contents. No publication or deployment.
- Shared source belongs to `~/ai`; generated dependencies belong to `~/ai-data`.

## Changes

- Shared launcher: `~/ai/general/scripts/ansible-mcp.sh`.
- Canonical project settings: `~/ai/personal/codex/ansible/config.toml`.
- Repository `.codex/config.toml` links to those settings. An existing empty
  regular file `.codex` was preserved as `.codex.empty-backup` before creating
  the directory; no existing contents were discarded.
- Repository `AGENTS.md` describes the integration and consulting reference
  guidance before Ansible edits, subject to project instructions.
- Runtime: `~/ai-data/ansible-mcp`, with exact dependencies
  `@ansible/ansible-mcp-server@26.6.0` and `node@24.22.3` plus npm lockfile.
- Global Codex configuration and system Node.js were not changed.

## Verification

- Bash syntax check passed.
- `codex mcp list --json` discovers the project server with the expected launcher.
- A real stdio MCP client initialized the server, listed its ten upstream tools,
  and called all four allowed tools successfully.
- Detailed `roles` guidance returned 2,890 characters; the complete best-practices
  resource returned 27,444 characters.
- Environment info identified the exact workspace, `.ansible-venv`, Python
  3.12.13 and Ansible core 2.20.5. Ansible lint, ADE and ADT are not installed;
  no installation tools were called.
- The upstream package version is 26.6.0 but the MCP handshake reports the
  upstream hard-coded server version 0.1.0; do not confuse the two.
- Instruction lint: zero errors, one existing-context warning CDX-AG-005 at
  repository `AGENTS.md:49`, where `defaults/main.yml` denotes the conventional
  role-relative path. No unrelated instruction rewrite was made.
- Probe evidence: `~/ai-data/ansible-mcp/smoke-receipt.json`; the test client
  explicitly closed the transport and exited. No background server remains.

## Status and limits

The local installation and project configuration are verified. The running chat
has not reloaded its MCP tool catalog; open a fresh Codex session in this project
and inspect `/mcp` to use the new connection. Live invocation through a fresh
Codex conversation has not been observed in this task.

Only `zen_of_ansible`, `ansible_content_best_practices`,
`list_available_tools` and `ade_environment_info` are enabled in Codex. Direct
stdio probing sees the full upstream catalog; the allowlist is enforced by
the Codex configuration, not a server sandbox. Playbook execution, scaffolding,
autofix and dependency installation remain outside this pilot.

Other projects were not connected. No commits, pushes, remote changes or
deployments were performed. No new backlog action is required for the completed
pilot; additional project connections remain an optional extension.

## Portable lesson

The shared launcher passes both `VIRTUAL_ENV` and a venv-first `PATH`:
the upstream common-name discovery does not include `.ansible-venv`.

## Task metrics: ansible-mcp-project-pilot-20261115

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "ansible-mcp-project-pilot-20261115",
  "created": "2026-11-15T02:51:07.923334+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "configuration",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Verified stdio handshake, four reference tools, detailed role guidance, full resource and project Python environment; Codex discovers project settings.",
  "updated": "2026-11-15T02:51:07.923387+03:00"
}
```
