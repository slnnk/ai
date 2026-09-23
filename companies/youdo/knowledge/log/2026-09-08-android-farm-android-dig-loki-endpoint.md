---
system: android-farm
status: verified
checked: 2026-09-08
tags: [android, android-dig, loki, skill]
---
# Android-dig Loki endpoint update — 2026-09-08

## Task

Update the `android-dig` skill to the new Loki read endpoint supplied by the user.

## Changes

- Context: global local skill `~/ai/current/skills/android-dig`.
- User-provided change: Loki read origin is now `http://loki.dev.youdo.corp`.
- Updated `scripts/loki_logs.py` defaults (`DEFAULT_ENDPOINT` and the default allowlisted host).
- Updated both endpoint references and the dated context note in `references/runbook.md`.
- Preserved older endpoint references in historical operational notes as dated evidence.
- No credential changes were needed. Endpoint reachability was not tested because this was a configuration-only request.

## Portable lesson

none
