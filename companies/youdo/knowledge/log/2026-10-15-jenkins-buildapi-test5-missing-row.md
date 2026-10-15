---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, buildapi, diagnosis]
---
# Jenkins successful build5826 did not publish test5 to BuildAPI

## Summary

Jenkins dynamic_deploy Update buildsinfo still has four hardcoded old BuildAPI URLs. Old endpoint returns404; curl has no fail flag, so build5826 remains SUCCESS despite post-update404 responses. New BuildAPI builds collection is empty and test5/current/history records are absent. Correct Ansible upload/static calls do not create the missing row. No remote changes made.

## Task and context

User supplied screenshot of empty builds table at buildapi.dev.youdo.corp and asked why test5 was missing. Read-only inspection of Jenkins API/config/console, BuildAPI API, Kubernetes pods/logs and local BuildAPI source. No superpowers skills used.

## Findings

- Current Jenkins dynamic_deploy config Update buildsinfo has four old base URLs http://buildapi.yandex-test.youdo.local, targeting /builds and /builds/$TEST_INSTANCE with PUT/POST; curl does not use --fail/-f.
- Read-only old /builds/test5 returns404. Build5826 post-update console has two404 Not Found responses; no secret-bearing commands copied.
- Authenticated new GET /builds returns builds=[]; /builds/test5 returns Error: No such name; /allbuilds/test5 returns empty list.
- app.py125/mongo_utils.py192 render home from current builds collection; default whitelist includes test5.
- app.py315 PUT /builds/test5 upserts the current row. POST /builds only appends history.
- Monolith POST /upload does not create a builds row (app.py474). Static PUT /builds/test5/static/version uses upsert=False and can return200 without matching document (app.py364).
- All five BuildAPI pods Running with zero restarts. No application exception classes found in sampled recent logs; unrelated full health claims are not inferred.

## Changes and limits

KB/TODO updated only. Jenkins endpoint correction, HTTP fail handling and replay of result publication were not requested or executed. Full redeploy is unnecessary to restore metadata; a separately authorized targeted publication can create the row with verified build5826 fields.

## Portable lesson

None.
