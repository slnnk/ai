---
system: android-farm
status: verified
checked: 2026-11-09
tags: [selenium, grid, appium, restart]
---
# DevOps-912: Android Grid hub01 restart after tests stopped

## Task and authorization
User confirmed tests were stopped, said leftover sessions were not needed and requested restarting the Grid container. Agent described exact target and impact before remote mutation. After restart exposed remaining node sessions, agent described closing only those3unneeded sessions through exact-ID Appium DELETE; scoped cleanup authorized by the user's declaration and tool approval. No blanket node/device restart or new test execution.

## Context and target discovery
Fresh Enabled Selenium inventory15:49:47UTC /18:49:47MSK selects M-K0056 `192.168.30.30` as Hub. Read-only Docker inspection found hub01, hub02, selenium-hub-ios and unrelated UniFi containers. Host PID1639 listening192.168.30.30:4444 belonged to hub01 (selenium/hub:3.141.59-20201010, container076ce6973384). Thus hub01 identified independently of container naming; hub02/iOS not touched.

## Actions and findings
- Executed `docker restart --time 20 hub01` only. Docker warned that --time is deprecated in favor of --timeout; restart succeeded. New started_at2026-11-09T15:51:20.788759896Z /18:51:20MSK, runningtrue/PID2366138.
-15:51:33UTC /18:51:33MSK: Hub ready,6registered slots,6free/0busy/queue0; all6proxies found and Appium statusready. Xiaomi remains unregistered.
- Read-only GET/sessions revealed a layer mismatch: all3M-K0057Appium endpoints had0sessions, but M-K0058emulator5554/TECNO/Samsung each retained1old session despite Grid reportingfree. This directly demonstrates that Hub restart resets Hub accounting without necessarily terminating Appium sessions.
- Captured exact IDs, rechecked unchanged session identity immediately before DELETE, then removed only M-K0058session0ec170ac-928c-4f0e-a385-c4d721a3dce0(port15001),7320d237-27f1-43ec-8483-64c5b89f4485(port15002),af0333ed-320e-4a13-b0ca-665f60c6b44f(port15004). All3DELETEs returnedHTTP200 and follow-up session counts0. No stale-session broad kill or service restart.
- Read-only ADB-forward list onM-K0058now empty; no15901/15902/15904listeners remain. This establishes clean baseline for subsequent canaries, not the cause of earlier spontaneous failures.
Generated evidence in `~/ai-data/android-dig/DevOps-912/`: grid-after-restart.json, appium-sessions-after-grid-restart.json, old-appium-session-cleanup.json, grid-after-session-cleanup.json.

## Changes and final state
Only requested Android Hub container restart and exact cleanup of3unneeded Appium sessions. Other Grid containers, Appium services, devices and existing Xiaomi isolation not changed. No diagnostic test/session creation, timeout edits or CI rerun. All task background commands completed.

## Status and remaining work
Restart/cleanup completed. Original plan's leftover-session forensic investigation waived by user; direct-Appium versus Grid serial canary, then bounded concurrency1/2/4/6and evidence-based fix remain proposed. Existing central [TODO](../../../../TODO.md), android-farm session-lifecycle task, covers remaining diagnosis. No assumption that Hub restart fixed historical session lifecycle defects; clean slots alone were insufficient until node sessions were separately closed.

## Portable lesson
none
