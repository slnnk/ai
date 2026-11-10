---
system: android-farm
status: verified
checked: 2026-11-09
tags: [appium, ansible, ci, unicodeime]
---
# DevOps-912: preserve Appium Settings during device preparation

## Task and authorization
User requested item1: edit `/opt/adb/adb.sh` locally on each Appium farm machine and update the Ansible role, under DevOps-912. This explicitly authorized the targeted remote-file changes. No service/device restart, APK/helper mutation, CI run or tracker write was requested.
First repository gate proposal: `/home/slnnk/git/automation-services`, new branch `DevOps-912-preserve-appium-settings` from fresh `origin/master` at `2a3b864f`. User explicitly approved creating the branch and changing the role. At initial implementation, second publication gate was not requested/granted and no stage/commit/push/MR was performed. Later approved publication is recorded below.

## Context
A controlled [Settings reinstall experiment](2026-11-09-android-farm-xiaomi-settings-reinstall.md) reproduced Xiaomi UnicodeIME failure after a successful reinstall; prior3serial UnicodeIME-enabled sessions had passed. Existing device recovery/isolation and multi-device Grid session problems are separate tasks.
Remote machines verified by SSH hostname: M-K0057 `192.168.30.31`, M-K0058 `192.168.30.32`. Existing scripts had755/root:root. Both also removed UiAutomator2 helpers and the test APK; the managed template did not contain the deployed extra test-APK removal. That drift was preserved.
Repository inspected at original branch DevOps-907-fix-public-test-dns/cedd1283. Fetch refreshed master2a3b864f (merged public DNS change); original HEAD and fresh master had identical trees. All23unrelated modified/untracked paths were preserved across approved branch creation; target template was initially clean and index empty.

## Changes
- Both `/opt/adb/adb.sh` files: removed only the `uninstall io.appium.settings` command and clarified the comment to preserve Settings for Android IME registration while keeping the UiAutomator2 cleanup unchanged. Existing deployed test APK cleanup retained.
- Remote edit checked the inspected original SHA256, copied a timestamped backup, validated candidate shell syntax and atomically replaced the script while preserving owner/mode. No preparation script was executed.
- Same scope in `roles/adb_devices/templates/adb.sh.j2`, in the approved local branch. Existing android.yml template task already installs it to `/opt/adb/adb.sh` as root:root/0755; no task changes needed.

## Verification
- Both remote copies read back with matching post-edit SHA256,755/root:root, `bash -n` pass, Settings uninstall absent and both original UiAutomator2 uninstall commands present.
- Local template Jinja rendering with StrictUndefined and `bash -n` passed; output matched the prepared proposal. Task-only `git diff --check -- roles/adb_devices/templates/adb.sh.j2` passed. Actual diff2added/2removed lines, only one task file; no staged task files.
- Whole-checkout diff check additionally reported pre-existing trailing whitespace in unrelated `roles/gitlab-runner/templates/cron-docker-clean.j2` lines1–2; untouched and outside DevOps-912. No blanket clean-checkout claim.
- No Molecule/full Ansible rollout was performed for this small script deletion: no YAML/task wiring changed, and running live preparation would mutate devices serving tests. Runtime effectiveness on future CI is not yet demonstrated.

## Backups and rollback
- M-K0057: `/opt/adb/adb.sh.DevOps-912.20261109T153857Z.bak`; before SHA256`3bc7c6b614009dde08dc62a897f9e279409f9a71480dc61ffef717d7940e2064`; after SHA256`f85922b8dcc8128f69ee3d89a5fc4ba03c73d15dca68945aaffc9fc5044e6702`.
- M-K0058: `/opt/adb/adb.sh.DevOps-912.20261109T153917Z.bak`; before SHA256`c71af22c4446ea79acd72295159e77b3dbbc0fa92be0979a745210c6ba3a30f1`; after SHA256`a599ca72e12cc638dedb0ef580552d1d0c90a07b801bb8ea53d4c12234f11a2d`.
Rollback would restore only the respective backup with preserved metadata, after separate authorization. Do not run old preparation for verification because it removes Settings.

## Status and risks
Requested host edits and local Ansible role update completed. New CI preparation executions on these hosts preserve installed Settings, but the script still prepares every connected device and deletes UiAutomator2 helpers: broader lifecycle/concurrency risks remain unresolved. This change does not repair the already-broken Xiaomi IME or return it to Grid. Production Xiaomi isolation unchanged by this task. Matching Ansible change published as MR1390/8dbbec31 and independently observed user-merged as6d467c2e at18:46MSK. Existing live host changes remain verified; no post-merge role deployment performed by the agent.
Central [TODO](../../../../TODO.md), android-farm section, records completed preservation/publication and observed user merge, plus existing device recovery and multi-device investigation tasks. No background task remains.

## Portable lesson
none

## Publication approval and commit — 2026-11-09

User requested commit and MR. Prepared snapshot/proposal/body under `~/ai-data/gitlab-workflow/DevOps-912/automation-services/`. Presented actual one-file2+/2-diff, Jinja/bash/task-diff checks, commit `preserve appium settings during device preparation`, ready MR title `DevOps-912 preserve Appium Settings during device preparation`, exact short Russian body with task link, source DevOps-912-preserve-appium-settings/target master, assignee a.solonenko, squashfalse/source-removaltrue. User explicitly confirmed publication (`Да, опубликовать`). Names accepted unchanged.
CI inspection: root `.gitlab-ci.yml` contains only Molecule nginx/consul/nomad tests, no includes/deploy/release. First branch push zero-before-SHA rules suppress jobs; MR context may expose optional manual molecule-nomad fallback. No manual test authorized or started.
Snapshot comparison immediately before staging passed. Index initially empty; staged only target template and reviewed full staged diff. Commit `8dbbec318ccd1cd0acffb7f984c469a25099e4b6` contains exactly the approved template contents and one task path. Unrelated changes preserved. Publication outcomes recorded below after remote verification.

### Verified publication outcome

Push of approved source branch succeeded without force. Created ready [MR1390](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1390), SHA `8dbbec318ccd1cd0acffb7f984c469a25099e4b6`, exact approved title/body/source/target, assigned a.solonenko, squashfalse/source-removaltrue. Helper reports write_statecreated/verifiedtrue. Pipeline142579 is `skipped`, not a passed test run. No merge/auto-merge/manual job/deployment performed. Publication task completed, unrelated worktree files remain preserved and no task background operation remains.

### Final remote-state reconciliation

After successful create/verify, a separate helper verification returned `Open MR not found`. Agent stopped writes and inspected read-only; no retry/create/push was performed. Direct GETMR1390 confirmed state`merged`, merged_at2026-11-09T18:46:04.219+03:00, merge_usera.solonenko, merge_commit_sha`6d467c2e196f347bfe500bb96f0af0ce4e03f111`, source SHA8dbbec31 and exact approved title/body/source/target. Thus the helper's open-only lookup failed because the user merged during final checks. Agent did not perform merge. Previous pending-merge references are superseded by this observation; MR pipeline142579 remains skipped, post-merge deployment not performed/claimed. Publication task complete; no task background operations.

## Read-only Grid baseline for next diagnosis — 2026-11-09 18:48 MSK

User confirmed merge and reported stopping active autotests, permitting Grid use for diagnosis, and asked for a plan. No diagnostic sessions/cleanup were started in this planning turn. Fresh Enabled inventory15:47:56UTC, Hub15:48:04UTC:6registered/reachable/ready Appium endpoints,3busy/3free slots,0queued requests. All3M-K0057slots idle; all3remaining M-K0058slots busy (emulator5554, TECNO15888255AE004773, SamsungRZ8R71ZRK8H). Xiaomi remains unregistered. Busy slots after reported job cancellation are a clue, not proof of orphaning: compare actual Appium sessions, Grid session ownership, last commands and ADB forwards before any cleanup.
Proposed next work: preserve leftover-session evidence onM-K0058, identify/test cleanup ownership, compare one-device serial direct-Appium versus Grid lifecycle, then increase concurrency1/2/4/6with only healthy slots. Stop at first mismatch, correlate timestamps/ports with Loki. Scope remains proposal until user requests execution; no service restart, session deletion or parallel test run in this turn. Existing central android-farm session-lifecycle task covers this follow-up.

## Superseding Xiaomi recovery — 2026-11-09 18:57 MSK

User-approved reboot followed by3UnicodeIME-enabled serial cycles passed with existing Settings3.4.0; production Appium started and Xiaomi registeredidle in Grid. Earlier isolated/broken state is historical. See [recovery and limits](2026-11-09-android-farm-devops-912-xiaomi-recovered.md).
