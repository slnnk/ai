---
system: knowledge-base
status: verified
checked: 2026-11-18
tags: [setup, agents, sync]
---
# Knowledge base: audit the other-PC setup guide

## Task

## Context

## Actions

## Findings

## Changes

## Open items

## Portable lesson

none

## Task

Audit the other-PC setup guide against the current workstation and helper scripts.

## Context

The standalone setup refresh remains open in [the central backlog](../../../TODO.md#knowledge-base).
The [setup guide](../../../general/knowledge/knowledge-base/setup-another-pc.md) was last checked on 2026-11-04.

## Findings

- The documented Git ignore command exits 128 with `fatal: pathspec 'current/.env' is beyond a symbolic link`. Checking the actual tracked company directory and the personal layer succeeds. The guide should show how to resolve the relative target for this check.
- A clean local TODO display cache is absent by default. A probe with a missing cache yielded exit 2. Move the cache bootstrap before the final checklist and distinguish the derived file from the Git-tracked backlog.
- The guide requires Python 3.11 or newer but does not check the interpreter used by the shell. On the reference workstation `python3` is 3.8.10 while `python3.12` is installed separately. Document a version check and ensure `python3` used inside sync resolves to the selected interpreter. The agnix updater uses Python for downloading, hashing and extraction. The summary still calls agnix pinned, whereas the body describes the daily stable updater.
- The Git clone step cannot restore additional push URLs from local Git configuration. Document the active two-destination origin layout, including an explicit primary push URL, the secondary push URL and verification of both. Sync runs SSH in batch mode, so interactive access during clone alone is insufficient. A dry run checks the local publication payload and does not exercise remote access.
- The Codex setup section omits the tracked global configuration and its runtime symlink, introduced on 2026-11-16. The current config includes absolute trusted project paths and an MCP header helper. Document per-machine review, the symlink when applicable, and a fresh session check. Existing plugin settings and account access should be tested only for workflows selected for the new machine.
- The normal sync path also prepares daily metrics even when Git sync skips. Document regenerated metrics state, the pending-review message and the existing review workflow. Node.js and Acorn are used for optional Codex KB extraction coverage. A dry run skips both updater and metrics preparation, as well as weekly and monthly outputs.
- Graphyfi has a separate backlog entry and has no implemented setup contract to include yet.

## Actions

Ran the required startup sync. Compared the guide with the working tree, canonical rules, runtime symlinks and current helper source. A disposable local clone with an explicit repository root passed KB search, KB lint, index generation and sync preview. Tested the documented Git ignore check, its resolved-path alternative and missing-cache TODO behavior without creating real secret files.

## Status and risks

The audit was delivered before editing the guide. Its local probes did not validate remote Git access, agent authentication or a full installation on a clean workstation.

## Guide refresh

The user then requested implementation of all six audit items. Updated the guide with a Python interpreter preflight, two explicit origin push URLs and read checks, a Codex configuration link and fresh-session check, physical-path Git ignore checks, TODO cache bootstrap, and the current agnix and daily sync workflow.

In a disposable clone, the guide commands passed with Python 3.12, both Git destinations resolved to local test repositories, both ignore paths matched, and the Codex configuration symlink resolved to valid TOML. The TODO probe returned exit 2 with an absent cache and rendered the affected task after restoring the cache. KB search, lint, index generation, and the read-only sync preview passed. The preview preserved working tree status and created no sync marker.

The guide refresh is closed in [the central backlog](../../../TODO.md#knowledge-base). The tests used local Git endpoints and verified only filesystem and TOML setup for Codex. Real remote access, client authentication, agnix installation on a fresh PC, and the full workstation setup remain unverified.

## MCP setup follow-up

The user clarified that the guide must give concrete MCP setup steps. Added a dedicated section covering the two tracked global servers and the project-scoped Ansible server. It identifies the HetrixTools secret location and header helper, Ansible's local runtime and project dependencies, and a read-only check for each server. Client-owned plugin connections have a separate restoration step within the same section.

Verified that `codex mcp list --json` sees both global servers and includes `ansible` in the trusted checkout. The Ansible dependency paths exist, the HetrixTools helper passed with a synthetic key, and the OpenAI Docs MCP returned the official Codex MCP documentation. Runtime configs and credentials were preserved. Integration setup on another PC remains untested.

## Task metrics: kb-setup-guide-audit-2026-11-18

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "kb-setup-guide-audit-2026-11-18",
  "created": "2026-11-18T22:25:29.715646+03:00",
  "first_result": "unknown",
  "final_result": "pass",
  "state": "closed",
  "kind": "analysis",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Guide and scripts compared; local clone checks and two bootstrap failures documented; clean PC installation outside audit scope.",
  "updated": "2026-11-18T22:25:29.715695+03:00"
}
```
