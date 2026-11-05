---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [agnix, maintenance, daily-update]
---
# Knowledge base: daily stable agnix updates

## Task and authorization

User requested keeping agnix current with daily version checking and local updating,
analogous to Git synchronization. This authorizes the local install maintenance.
KB edits are exempt from the first repository gate; unrelated working changes were
preserved. No manual Git mutation or external service write was performed.

## Changes

- Added `general/scripts/agnix_update.py` before lint and the same-day Git skip in
  `ai-sync.sh`. Uses the official `agent-sh/agnix` latest stable release API.
- Successful checks persist the local date in `~/ai-data/agnix/update.json`; failures
  remain pending for retry. A lock prevents concurrent updates. Read-only sync modes
  exit before maintenance. This runs when agents call sync, without an unattended timer.
- Verify official API SHA-256, copy only the regular executable from the archive,
  verify its reported version, then atomically switch the local `current` symlink.
  Retain previous version directories and never downgrade.
- Lint prefers `~/.local/share/agnix/current/agnix`, then the legacy0.59.0 path, then
  PATH; resolved binary hashes already invalidate the lint checkpoint after updates.
- Updated AGENTS.md, README and the [new-PC guide](../../../general/knowledge/knowledge-base/setup-another-pc.md).
  The earlier pinned install instructions are superseded; historical pilot evidence
  remains accurate for its original date.

## Verification

- Seven updater tests passed: daily skip/force, verified activation, no downgrade,
  checksum failure/retry, binary version failure, archive link rejection, stable release
  and URL validation, first installation. Existing23lint and5sync preview tests passed.
- Live update from0.59.0 to0.60.3 verified archive SHA-256 and binary version; repeated
  same-day invocation returned silently without network activity.
- Forced lint using0.60.3:9files,0errors,1warning (`CDX-CFG-025` in global Codex settings),
  2informational findings. The0.59.0-only compatibility recheck remains bounded to that
  old version; the new warning is retained, without changing agent settings.
- KB lint:0errors,0warnings. Network access initially failed in the sandbox; the live
  updater completed after an approved network-enabled command.

## Status and risks

Completed2026-11-04. No remaining action from this request and no new backlog item.
Updates depend on GitHub availability and API digests. Failures preserve the selected
binary and do not block Git sync. Other OS/CPU paths are implemented but not exercised
on real hosts; Linux x86_64 was verified. Background work finished.

## Portable lesson

Maintenance policy and installation entry points are canonical in
[README](../../../general/knowledge/README.md#agent-instruction-lint).

Subsequent user decision: the three accepted findings are now excluded by
[scoped lint exceptions](2026-11-04-knowledge-base-agnix-accepted-exceptions.md); the
above warning count records the initial update check before those exceptions.
