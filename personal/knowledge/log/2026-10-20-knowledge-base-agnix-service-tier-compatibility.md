---
system: knowledge-base
status: verified
checked: 2026-10-20
tags: [agnix, codex, lint]
---
# Knowledge base: correct agnix service tier validation in local lint runner

## Task and authorization

User explicitly requested fixing the agnix check after the
[verification](2026-10-20-knowledge-base-service-tier-validation.md), retaining the rule
and the configured service mode. This is a local KB tooling edit, exempt from repository
task edit gates. No external operation, Git mutation, installation or model call occurred.

## Changes

Added a narrow compatibility recheck to general/scripts/agent_lint.py, scoped to agnix
version0.59.0 and warning-level CDX-CFG-025 diagnostics on scanned .codex/config.toml
inputs. Valid TOML with an exact diagnostic line setting default or priority passes the
recheck. All other values, findings, versions and error severities retain native handling.
Full-source and prefix parsing prevent invalid TOML or multiline-string content from
qualifying. Missing TOML parsing support retains the warning. Uses standard tomllib or
already installed tomli; no dependency was installed.

Compatibility corrections are counted visibly in stdout and the sanitized JSON report.
The original binary remains untouched, so invoking it directly still produces its stale
warning; ai-sync and the mandatory agent lint entry point use the corrected local runner.
No rule was disabled and no source/config secret is added to reports.
README documents this compatibility behavior and its boundary.

## Verification

23 agent-lint tests passed, including seven new regressions for accepted values, invalid
values, other versions/rules/severities, malformed TOML, multiline strings, wrong input
paths/line numbers, mixed profiles, redacted reports and checkpoint behavior.
An initial integration fixture exposed that changing HOME hides user-site tomli on
Python3.10; the fixture now retains its installed parser while isolating lint inputs via
--runtime-home. The missing-parser production path retains native warnings as intended.

A separate live run with real pinned agnix in temporary directories accepted default,
priority, fast and flex, and retained CDX-CFG-025 for an invalid control value.
Forced live lint:9files,0errors,0warnings,2informational findings,1visible compatibility
recheck. KB lint and whitespace checks passed; indexes regenerated.

## Reconciliation and limits

Completed; no new open backlog action. Related historical audit and verification notes
link to this outcome. Existing task records were preserved. The two informational
findings remain intentional and are unrelated. This compatibility change does not rebuild
upstream agnix or establish request-time tier fulfillment; future binary versions retain
native behavior until separately verified.

## Portable lesson

The existing README documents local lint behavior.
