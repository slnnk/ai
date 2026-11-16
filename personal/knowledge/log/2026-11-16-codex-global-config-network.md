---
system: codex
status: verified
checked: 2026-11-16
tags: [codex, configuration, sandbox]
---
# Codex global configuration moved into the knowledge repository

## Task
The user explicitly requested moving the global Codex configuration into ~/ai and enabling command network access in workspace-write mode.

## Context
Runtime config was a regular file at ~/.codex/config.toml. Project-specific Ansible configuration already lives separately at ~/ai/personal/codex/ansible/config.toml.

## Actions
Created ~/ai/personal/codex/config.toml with the original settings and two additions: root sandbox_mode = "workspace-write" and sandbox_workspace_write.network_access = true. Replaced the runtime file with an absolute symlink to the canonical file. The protected runtime-path replacement completed using approved elevated execution.

## Findings
Parsed TOML comparison confirmed all original settings were preserved and only the requested sandbox/network settings were added. The runtime symlink resolves to the canonical file, which retains mode 0600. Agent instruction lint completed with zero errors, warnings or informational findings.

## Changes
- Canonical configuration: ~/ai/personal/codex/config.toml.
- Runtime link: ~/.codex/config.toml.
- Original backup: ~/ai-data/codex-config/2026-11-16-config.toml.before (local generated data).

## Status and risks
Completed local configuration change on 2026-11-16. Restart Codex to load the configuration; command networking in the current session remains governed by its existing managed policy. Actual connectivity after restart was not tested. Managed restrictions can override local configuration. No background operation remains and no agent follow-up or backlog change is required. No explicit Git publication was performed.

## Portable lesson
None.
