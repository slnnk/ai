---
system: knowledge-base
status: verified
checked: 2026-11-04
tags: [agnix, lint, exceptions]
---
# Knowledge base: scoped agnix exceptions

## Task and authorization

User explicitly requested excluding the three explained findings from lint output:
CDX-CFG-025 for valid service_tier, AGM-004 and CDX-AG-008 for the shared root policy.
Local KB tooling edits are authorized and exempt from the first Git approval gate.

## Changes

Extended the existing TOML and exact-line service-tier recheck from agnix0.59.0 to
verified0.60.3. Only warning-level CDX-CFG-025 for parsed default/priority values in
scanned Codex configuration files is excluded. Invalid values, unrelated diagnostics,
unknown versions and parse failures remain visible. Compatibility counts stay in
sanitized report metadata; accepted findings no longer print a separate stdout line.

Excluded info-level AGM-004 only for the canonical root AGENTS.md; it holds shared
policy and delegates project context. Excluded info-level CDX-AG-008 for that same file
only when a sibling AGENTS.override.md exists; this override avoids duplicate loading.
Other repository paths and warning/error levels remain checked. No native binary,
agent settings or repository-local instructions were changed.

Canonical behavior: [README](../../../general/knowledge/README.md#agent-instruction-lint).
The previous version-only compatibility limitation is superseded by this decision.

## Verification and status

Completed2026-11-04. All25agent-lint tests passed, including new scope/severity/version boundaries.
Forced live agnix0.60.3 scanned9files:0errors,0warnings,0info; exit0. No remaining action or new TODO item; existing closed agnix
adoption records remain historical. No external writes or manual Git mutations.

## Portable lesson

Keep exceptions bounded to the verified file, finding severity and affected versions.
