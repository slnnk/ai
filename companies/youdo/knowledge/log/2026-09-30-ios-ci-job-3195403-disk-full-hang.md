---
system: ios-ci
status: verified
checked: 2026-10-05
tags: [gitlab-ci, ios, disk, idcn-10]
---
# iOS CI job 3195403 hung: idcn-10 disk full

## Task
Check whether GitLab job 3195403 (`team-youdo-ios/YouDoApp`, `Build beta ad-hoc`, MR 3265, pipeline 139791) hung.

## Context
Runner `idcn-10` (id 93, gitlab-runner 17.9.3, darwin), host `iosdev@192.168.30.144`, shell executor, builds in `~/builds/6gfbuVYj/`. Job has no timeout set. Normal duration of this job on idcn-10: 30-47 min.

## Actions
- GitLab API: job status, trace (`/jobs/3195403/trace`), last successful same-name jobs, `/runners/93/jobs?status=running`.
- ssh read-only: `ps` (children of gitlab-runner PID 737), `df -h`, `du -sh` of Xcode/Simulator/builds dirs.
- Job was cancelled by the user.

## Findings
- Trace stopped at 10:55:29 MSK during `xcodebuild` of `YDSettingsApp` (second gym run, after `YDMainApp` built and uploaded to Firebase); no error in trace, size unchanged for 45+ min, GitLab still `running` at 78 min.
- On the Mac: no `xcodebuild`/`swift-frontend`/`fastlane` processes, gitlab-runner has no child processes; the build process died without the runner reporting it.
- `/System/Volumes/Data` 100% full (988 MiB free of 228 GiB). Likely cause of the build death (hypothesis: no explicit "No space left" line found).
- Space: `~/Library/Developer/CoreSimulator/Devices` 53G (45 shutdown simulators), `~/builds` 28G (`YouDoApp/build` 14G), `Xcode/Archives` 9.1G, `DerivedData` 5.9G, `Library/Caches` 4.6G.

- `xcrun simctl delete unavailable` freed nothing: all 45 simulators use installed runtimes (iOS 18.0, 18.4, 26.4, 26.5).
- 46.5G of the 53G is one simulator: iPhone 11 / iOS 18.0, UDID `C0F24BAE-D4E2-4656-8E94-3BE8132A6759`, used by `fastlane/Fastfile` (last boot 2026-09-29). Inside: `data/Library/Caches/com.apple.containermanagerd/Dead` 37.2G (containers of apps removed by repeated test reinstalls), `data/var/db/diagnostics` 3.3G. Fix: `xcrun simctl erase <UDID>` while shut down.

- `xcrun simctl erase <UDID>` failed with `NSCocoaErrorDomain code=513` / POSIX `code=1`. Not file permissions: no flags, ACLs or foreign owners in `data`. The system log shows `kernel ... System Policy: com.apple.CoreSimulator.CoreSimu(731) deny(1) file-write-unlink .../Devices/<UDID>/data` when CoreSimulatorService moved `data` to `/var/folders/.../T/Deleting-<uuid>`. The service (PID 731, user `iosdev`, macOS 26.4.1) had been running since 2026-09-14. Hypothesis: a stale service after Xcode/runtime updates; fix by restarting the service, or delete `data/Library/Caches/com.apple.containermanagerd/Dead` directly as `iosdev`. Diagnose with `log show --last 1h --predicate 'eventMessage CONTAINS "<UDID>"'`.

- Restarting CoreSimulatorService (`killall`, new PID 45047) did not help: the new PID got the same `deny(1) file-write-unlink`, so the stale-service hypothesis is refuted. The cause is in the macOS 26.4.1 sandbox policy for CoreSimulatorService (not investigated further). Workaround: delete `Dead/*` and `var/db/diagnostics/*` directly as `iosdev`.
- The user deleted the workspace `build` dir: `/System/Volumes/Data` went from 100% to 88% (25G free).

- Default `~/Library/Developer/Xcode/DerivedData/YDMainApp-*` (5.9G) is not a build dir (Fastfile `scan`/`gym` use `derived_data_path: './build'`, `Build/` there is 0B); it holds only `SourcePackages` 5.8G, recreated on each run (hypothesis: `gym`'s `-showBuildSettings` resolves SPM without `-derivedDataPath`; about 4.5 min between `Step: gym` and `xcodebuild`).

## Changes
- By the user on idcn-10: removed the whole checkout `~/builds/6gfbuVYj/0/team-youdo-ios/YouDoApp` (14G), then `Dead/*` and `var/db/diagnostics/*` of simulator `C0F24BAE-...`. Result: `/System/Volumes/Data` 69%, 65G free; simulator 6.1G, still listed (Shutdown). Job 3195403 cancelled by the user.

## Open items
- Free disk on idcn-10 (needs user approval) and add a job timeout / disk check.

## Follow-up 2026-10-05

Read-only check over ssh (`iosdev@192.168.30.144`):
- `/System/Volumes/Data` 89%, 23G free (65G free on 2026-09-30): about 42G regrown in 5 days.
- Usage: `~/builds` 17G, `Xcode/Archives` 15G (9 archives, one per day), `CoreSimulator/Devices` 14G (simulator `C0F24BAE-...` 8.2G, its `containermanagerd/Dead` 2.1G again), `DerivedData` 5.9G, `Library/Caches` 4.7G, simulator runtimes 31.8G (iOS 18.0, 18.4, 26.4, 26.5).
- No cleanup job: crontab empty, `~/Library/LaunchAgents` holds only `gitlab-runner.plist`.
- No Zabbix agent (no binary, process, package or LaunchDaemon); host absent in `zabbix-selectel` and `zabbix-test`.
- fastlane `2.240.0` installed in rbenv `3.2.2` and Homebrew Ruby 3.3; system Ruby 2.6 still has 2.188.0/2.225.0.
- macOS has no `timeout` binary: remote scripts must not rely on it.
- Zabbix agent install and cron disk cleanup tracked in DevOps-881.

## Portable lesson

none
