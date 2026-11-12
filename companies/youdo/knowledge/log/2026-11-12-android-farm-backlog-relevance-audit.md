---
system: android-farm
status: verified
checked: 2026-11-12
tags: [backlog, ci, zabbix, review]
---
# Android backlog: relevance audit after recovery

## Task and method

The user asked what remains and whether the remaining Android backlog is relevant. Reviewed all9open entries in the central TODO after accepted A55/session recovery and cancellation of manual resource checks. Read-only investigation; no implementation, CI runs, deployment or monitoring changes.

Refreshed existing local checkouts with `git fetch origin` without switching branches or modifying worktrees. Inspected autotest `origin/master` f126825b, product default `origin/develop`3461102079, infrastructure `origin/master`a87ac230. Product AGENTS build prohibition honored. Queried GitLab project79/hot-fix pipeline history, YouTrack DevOps-833 and Zabbix M-K0056 items/templates. Compact API evidence: `~/ai-data/android-dig/backlog-audit-20261112.json`.

## Results in backlog order

1. **DEBUG output: optional improvement with a verified risk.** Autotest CI still passes Gradle `-d`. Prior job3282427 exceeded the trace limit at209MB; final job3285160trace was104MB. This does not establish a current failed job from logging after recovery. Keep as a proposal, not an incident.
2. **APK publication HTTP handling: confirmed remaining defect.** Product default-branch `.publish_for_tests` still has2curl calls without HTTP-failure handling. Prior job3273026 falsely succeeded on HTTP500. Nexus restoration/publication already completed November5; remove stale storage-repair prerequisite from the active task. No new upload requested.
3. **ADB preparation contract: confirmed remaining defect, with stale wording corrected.** Autotest master restarts both emulators on each node and runs `/opt/adb/adb.sh` with `|| true`; known missing per-host emulator service can be masked. It no longer invokes `adb_pkg.sh`, so restoring that unused script is not a present requirement. Preserve completed DevOps-912Settings handling; improve fail-fast checks within a separately approved implementation.
4. **Gate_K cleanup/docs: optional maintenance, current completion unknown.** October1DNS routing incident was resolved. Disabled srv0rules, unrelated legacy network settings and office documentation cleanup are a separate historical proposal. No fresh router inspection; do not call these an active farm outage or claim cleanup completed.
5. **Failed-suite download validation: confirmed remaining defect.** Autotest master downloads failed-suite XML with curl lacking HTTP-error failure handling and no XML validation before Gradle. Successful job3285160download does not remove this unhandled failure path.
6. **Watchdog/overlays/Appium upgrade: optional improvement, no confirmed current blocker.** Latest farm checks still show Appium1.22.3. HTTP-only readiness is weaker than command health, but session/A55recovery is accepted and no current overlay blockage was demonstrated. Keep as a proposal requiring concrete need/owner decision; no automatic watchdog or upgrade authorized.
7. **DevOps-833: completed; separate release-control suggestions remain proposals.** YouTrack returns Fixed/resolved. Local patch227f7518c3 is an ancestor of current default develop; its hotfix job includes Rustore producer/artifact and both store jobs use fastlane-docker0.0.9. Close stale merge/fix request. Existing suggestions for store-job environment protection and image-digest pinning remain an explicitly separate proposal. No project-wide permissions audit performed. Legacy `hot-fix` branch has not received this commit; GitLab's latest pipeline for that ref is from July2022. Do not launch a pipeline/store publish to prove an obsolete branch flow or claim a post-fix hotfix run occurred.
8. **Suite options: current code fact requiring QA ownership.** Autotest master still exposes InfoMessagesTestSuite although its XML/class are absent. After excluding comments, MindBox has20@Test annotations, all disabled. Deliberate disabling versus obsolete UI options is a QA decision; enabling product tests is not an infrastructure repair.
9. **Grid monitoring: confirmed remaining gap; old active-check timeout not a proven active defect.** Fresh Zabbix query: M-K0056only has YouDo OS Linux template,84items, no item key/name matching Grid/Selenium/4444/TCP/web checks,0active-check items. Existing OS monitoring is healthy in the earlier full-job review. Keep application-level Grid monitoring; do not confuse it with cancelled resource checks. Remove old standalone active-check timeout investigation from the current action; no fresh agent-log diagnosis or claim the old timeout was repaired.

## Changes and reconciliation

Updated existing TODO entries and Russian cache titles to distinguish confirmed gaps, optional proposals and QA scope. Closed stale DevOps-833entry; split its already-existing protection/digest suggestions into one proposal at the same backlog position.9open items remain:4confirmed CI/monitoring gaps,4optional proposals,1QAdecision. Optional proposals remain proposals, not authorized work. Added dated corrections to existing CI/CD, suite and farm maps; source evidence is preserved. No unrelated backlog scan, deletion or changes. All network/fetch commands completed; no background operations remain.

## Portable lesson

None.

## QA handoff update — 2026-11-12

The user confirmed the InfoMessages/MindBox findings were handed to QA and requested closure. Closed the corresponding central TODO entry as handoff complete; code findings remain historical evidence, not a claim of test repair. This supersedes the pending QA handoff in item8above.8Android backlog entries remain open. No external change or background work.

## Gate_K ownership update — 2026-11-12

The user assigned the Gate_K cleanup to another employee. Closed item4in the central backlog as transferred, not implemented. This supersedes the optional agent-owned cleanup proposal above.7Android entries remain open; no external changes or background operations.

## DEBUG reduction proposal withdrawn — 2026-11-12

The user clarified that test logs are emitted only in DEBUG mode. Preserve DEBUG; the agent withdrew the blanket logging-reduction follow-up and closed its central TODO entry. Historical trace overflow remains evidence, not a current mandate to suppress required logs. No logging change or replacement task. [Scoped constraint](../systems/android-farm/ci-cd.md#autotest-debug-logging-constraint--2026-11-12).

## Preparation scope corrected by user — 2026-11-12

The user rejected the suggestion to stop the whole job on an individual device preparation failure, because tests can run on the remaining devices. This supersedes blanket fail-fast language in item3above. The remaining proposal is accurate per-host emulator selection and visible device-level errors while preserving partial-capacity execution. [Canonical scoped policy](../systems/android-farm/system-map.md#partial-device-failure-policy--2026-11-12). No implementation or external change performed.

## adb.sh device-loop clarification — 2026-11-12

The user clarified that individual device failure must also not abort adb.sh preparation for other devices. The earlier assessment that lack of a script-wide stop was itself a defect was incorrect. Preserve device-loop tolerance; reporting may expose individual failures while processing remaining devices. This extends the existing [partial-device policy](../systems/android-farm/system-map.md#partial-device-failure-policy--2026-11-12), not a new independent work item. No code or external changes performed.

## Stopped emulator constraint — 2026-11-12

The user rejected restarting stopped emulator services. The proposed existence-only check is superseded: preparation must preserve stopped state and only restart running services. Partial-device tolerance remains, adb.sh unchanged. [Scoped constraint](../systems/android-farm/system-map.md#emulator-preparation-preserves-stopped-services--2026-11-12). No code/service changes.

## Emulator preparation proposal cancelled — 2026-11-12

After narrowing the discussion to emulator services only (skip absent services, try-restart to preserve stopped state, retain partial-device tolerance), the user declined the change because the farm currently works and the change is not worth doing. Closed the existing central preparation TODO as cancelled, not implemented. This supersedes pending preparation proposals and follow-ups in item3and later discussion sections above, including existence checks, try-restart and reporting/fail-fast work. No repository edits, runtime tests, service changes or adb.sh changes were performed for this proposal. Do not revive it from historical missing-unit messages without a new request or concrete newly reported problem. The completed DevOps-921APK-publication fix is separate and retained. No background operations remain.

## Store CI improvement proposal cancelled — 2026-11-12

After explanation, the user rejected the optional Android store-job protection and image-digest pinning proposal as unnecessary. Closed the corresponding central TODO entry as cancelled, not implemented. This supersedes item7optional release-control suggestions above; completed DevOps-833 remains complete. Do not recreate these suggestions as pending work without a new user request. No code, GitLab settings, release or image changes performed. No background operations.
