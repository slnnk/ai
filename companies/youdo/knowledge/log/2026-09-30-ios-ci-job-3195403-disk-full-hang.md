---
system: ios-ci
status: verified
checked: 2026-10-08
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

- Default `~/Library/Developer/Xcode/DerivedData/YDMainApp-*` (5.9G) is not a build dir (Fastfile `scan`/`gym` use `derived_data_path: './build'`, `Build/` there is 0B); it holds only `SourcePackages` 5.8G; "recreated on each run" (hypothesis refuted 2026-10-06, see below).

## Changes
- By the user on idcn-10: removed the whole checkout `~/builds/6gfbuVYj/0/team-youdo-ios/YouDoApp` (14G), then `Dead/*` and `var/db/diagnostics/*` of simulator `C0F24BAE-...`. Result: `/System/Volumes/Data` 69%, 65G free; simulator 6.1G, still listed (Shutdown). Job 3195403 cancelled by the user.

## Open items
- Free disk on idcn-10 (needs user approval) and add a disk check. The missing job timeout was later confirmed as intentional; do not change it.

## Follow-up 2026-10-05

Read-only check over ssh (`iosdev@192.168.30.144`):
- `/System/Volumes/Data` 89%, 23G free (65G free on 2026-09-30): about 42G regrown in 5 days.
- Usage: `~/builds` 17G, `Xcode/Archives` 15G (9 archives, one per day), `CoreSimulator/Devices` 14G (simulator `C0F24BAE-...` 8.2G, its `containermanagerd/Dead` 2.1G again), `DerivedData` 5.9G, `Library/Caches` 4.7G, simulator runtimes 31.8G (iOS 18.0, 18.4, 26.4, 26.5).
- No cleanup job: crontab empty, `~/Library/LaunchAgents` holds only `gitlab-runner.plist`.
- No Zabbix agent (no binary, process, package or LaunchDaemon); host absent in `zabbix-selectel` and `zabbix-test`.
- fastlane `2.240.0` installed in rbenv `3.2.2` and Homebrew Ruby 3.3; system Ruby 2.6 still has 2.188.0/2.225.0.
- macOS has no `timeout` binary: remote scripts must not rely on it.
- Zabbix agent install and cron disk cleanup tracked in DevOps-881.

## Follow-up 2026-10-06 (DevOps-881 planning, read-only)

- idcn-10: `arm64`, macOS 26.4.1, Homebrew 5.1.14 at `/opt/homebrew/bin/brew` (not in non-login ssh PATH), passwordless `sudo -n` works; `/System/Volumes/Data` 86%, 30G free.
- Zabbix `zabbix-selectel` is 6.4.21; no autoregistration actions (hosts are created by hand); only macOS template is `Template OS Mac OS X`. Official 6.4 macOS agent builds on cdn.zabbix.com are amd64 tarballs only; Homebrew `zabbix` formula is 7.4.x (`zabbix_agentd`, agent 1). Agent newer than server is not officially supported (hypothesis: passive basic items work).
- automation-services: `roles/zabbix-agent2` handles only Ubuntu and Windows; `inventories/office/hosts` has `idcn-10 ansible_host=192.168.50.10` (real address 192.168.30.144); office farm hosts on 192.168.30.x need NAT source `192.168.30.1` in `serverpassive`; `osx-builder.yml` targets a non-existent group `ios-builder` (legacy).

## Follow-up 2026-10-06 (DevOps-881 changes, branch `DevOps-881-zabbix-macos`, not applied)

- Decision (user): Zabbix agent 6.4 to match the server; official `zabbix_agent-6.4.21-macos-amd64-openssl.tar.gz` (static, only system dylibs) under Rosetta 2 (present on idcn-10); macOS firewall is disabled.
- automation-services: `roles/zabbix-agent2/tasks/darwin.yml` (+ `zabbix_agentd.darwin.conf.j2`, `zabbix_agentd.plist.j2`, LaunchDaemon `com.zabbix.zabbix_agentd` as `nobody`, install in `/usr/local/opt/zabbix_agent-<ver>`, sha256-pinned); `roles/gitlab-runner/tasks/cleanup-macos.yml` + `macos-disk-cleanup.sh.j2` (user cron 03:30, skips while gitlab-runner has children or xcodebuild runs; Archives >3d, DerivedData >1d, checkout `build` >1d, simulator `Dead`/diagnostics of non-booted devices, `simctl delete unavailable`); `gitlab-runners.yml` macOS play gets `zabbix-agent2`; office inventory IP fixed to 192.168.30.144; `serverpassive` with NAT 192.168.30.1.
- Apply only with tags: `ansible-playbook -i inventories/office gitlab-runners.yml -l idcn-10 --tags zabbix-agent2,macos-cleanup` (full play would also run runner register/config). `--check --diff` passes (launchd start/restart errors are ignored in check mode only).
- Remaining: create Zabbix host `idcn-10` (192.168.30.144:10050, `Template OS Mac OS X`, item/trigger on `vfs.fs.size[/System/Volumes/Data,pfree]`).
- DerivedData origin (checked 2026-10-06): `YDMainApp-gamgmxgznxhophabjlsqvyzjmkdm` (5.8G, `SourcePackages` only, `Build` 0B) was created 2026-09-29 17:05 MSK and nothing in it changed since. Its logs are four Xcode IDE "Resolve Packages" runs (17:08-17:18) and an empty Build log; `Blueprint.xcscmblueprint` is IDE source-control metadata. It started between jobs 3193786 (ended 17:03) and 3193885 (started 17:09), and every xcodebuild call in 3193885 (`-resolvePackageDependencies`, `-showBuildSettings`, archive) passes `-derivedDataPath ./build`. Conclusion: a one-off leftover of the project opened in the Xcode GUI, not CI; safe to delete.
- `git clean -ffdx` (default with `GIT_STRATEGY: fetch`) removes `build/` at every job start (traces 3206251, 3202370, 3201922), so the checkout `build` dir is no cache between jobs; it only holds ~13G until the next job in that checkout.
- Fastfile `develop:392` already deletes Archives day dirs with `find ... -ctime +10`, run by the lane.
- Cleanup script revised (user decision 2026-10-06: keep both the Fastfile 10-day Archives cleanup and the cron): checkout `build` dirs are deleted without an age limit; ages use `-mtime +Nd`. On macOS (BSD find) plain `-mtime +3` behaves like "4+ days" (0 of 6 archives aged 3d15h-3d22h matched, `+3d` matched all 6). Dry list on 2026-10-06 12:20: archives >3d 12.2G, DerivedData >1d 5.9G, `build` dirs 17.3G; disk 89%, 24G free.

## Follow-up 2026-10-06 (applied by the user, verified read-only)

- Playbook applied by the user. LaunchDaemon `com.zabbix.zabbix_agentd` running as `nobody` (`/usr/local/opt/zabbix_agent-6.4.21`); user cron `30 3 * * * /Users/iosdev/bin/gitlab-runner-disk-cleanup.sh` installed; first cleanup run due 2026-10-07 03:30 (log `~/Library/Logs/gitlab-runner-disk-cleanup.log`).
- Zabbix host `idcn-10` (hostid 10596, groups `Gitlab-Runners`, `All`, `Template OS Mac OS X`, interface 192.168.30.144:10050) created by the user; interface available, passive items arrive (via NAT 192.168.30.1). Active checks reach 172.28.0.120:10051 from this host.
- Gap: the template's `vfs.fs.discovery` filters `{#FSTYPE}` by global regexp "File systems for discovery" (no `apfs`), so no disk items are discovered on macOS (agent reports 14 apfs volumes, including simulator runtime volumes; adding `apfs` globally would alert on those full read-only volumes). Fix: host-level item `vfs.fs.size[/System/Volumes/Data,pfree]` and trigger. Agent test mode: `zabbix_agentd -c /usr/local/etc/zabbix/zabbix_agentd.conf -t 'vfs.fs.size[/System/Volumes/Data,pfree]'` returned 8.59 (21G free during a job).
- Created via API on user request 2026-10-06: item `vfs.fs.size[/System/Volumes/Data,pfree]` (itemid 4049627, 5m, `%`) and trigger "Free disk space is less than 10% on /System/Volumes/Data" `max(/idcn-10/vfs.fs.size[/System/Volumes/Data,pfree],30m)<10`, Warning (triggerid 568940). First value 7.72 at 12:30:47, trigger went to PROBLEM at once (real: ~17G free during a job).
- 2026-10-06 ~12:40, on user request: deleted `~/Library/Developer/Xcode/DerivedData/*` (5.9G: `YDMainApp-gamgmxgznxhophabjlsqvyzjmkdm`, `SymbolCache.noindex`, `.DS_Store`) during two running jobs (`build_beta_adhoc` in checkout 0, `test` in checkout 1). Free space still 16G right after: the running builds consumed more than was freed. Old Archives and the iPhone 16 Pro simulator junk were left for the nightly cleanup (user decision).
- 2026-10-06 ~12:50, on user request: deleted idle `~/builds/6gfbuVYj/1/team-youdo-ios/YouDoApp/build` (14G) while a new `build_beta_adhoc` ran in checkout 0; free space 24G -> 33G (84%). Earlier at 12:44 free space had dropped to 12G (5.2%) with two concurrent jobs; `git clean` at the next job start freed checkout 0. MR `DevOps-881-zabbix-macos` merged as `0c421bd0`.
- Read-only check 2026-10-08: cron cleanup completed successfully on both nights. The 2026-10-07 run freed 30,923M (17G -> 47G); the 2026-10-08 run freed 17,612M (25G -> 42G). At check time `/System/Volumes/Data` had 43Gi available (80% used). Daily cleanup is effective, but the second run began with only 25G free, close to the 10% alert threshold; keep observing peak build consumption. The log contained no errors.
- Zabbix API check 2026-10-08: trigger 568940 is enabled and OK (`value=0`, `state=0`, no error); it recovered at 2026-10-07 16:18:47 MSK. Item 4049627 reported 18.6492% free at 2026-10-08 09:18:47 MSK.
- User decision 2026-10-08: the YouDoApp job intentionally has no `timeout:`. Do not add or change it.
- User decision 2026-10-08: the two successful nightly runs and recovered Zabbix trigger are sufficient observation; close the remaining disk-monitoring TODO. Reopen only if the trigger or cleanup failures recur.

## Portable lesson

none
