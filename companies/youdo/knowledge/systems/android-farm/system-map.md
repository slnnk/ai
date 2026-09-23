---
system: android-farm
status: verified
checked: 2026-09-08
tags: [android, appium, selenium-grid, adb, emulator, zabbix, loki, alloy, ansible, system-map]
---
# YouDo Android: system map

- Last checked: 2026-08-20
- Scope: infrastructure-first overview of application delivery, CI/CD, UI autotests, and the office Android/Appium farm.
- Evidence: local Git worktrees and operational notes under `~/ai/current/knowledge/log`.
- Detailed CI/CD map: `~/ai/current/knowledge/systems/android-farm/ci-cd.md`.

## Repositories and responsibilities

- `/home/slnnk/git/android-youdo4` (`team-youdo-android/android-youdo4`) — main Android application and product pipeline. Large modular Kotlin/Gradle project with `youdoapp` launcher and Google, Huawei, and RuStore variants. Current checkout at the time of inspection: `develop` (branch is not permanent metadata).
- `/home/slnnk/git/gradle` (`sysadmins/devops-tools/gradle`) — internal Gradle/Android SDK build image; Android product CI uses registry tag `18`, autotest CI uses tag `12`.
- `/home/slnnk/git/fastlane-docker` (`sysadmins/devops-tools/mobile/fastlane-docker`) — containerized Fastlane lanes and plugins used by Android CI to publish to Google Play, Huawei AppGallery, and RuStore.
- `/home/slnnk/git/youdo-android-testing` (`youdo/Test/youdo-android-testing`) — Java 11, TestNG, Selenium 3, Appium Java client UI/API test project. CI chooses TestNG XML suites and runs against Selenium/Grid and Appium nodes.
- `/home/slnnk/git/automation-services` (`sysadmins/automation-services`) — Ansible roles/inventory for Android SDK, Android Studio, AVDs, ADB preparation, Appium systemd units, and certificate preparation.
- `/home/slnnk/git/android-docker-image` (`sysadmins/devops-tools/mobile/android-docker-image`) — Android Selenium image build based on Aerokube images; README records an Android 13 image workflow.
- `/home/slnnk/git/android-exporter` (`sysadmins/devops-tools/mobile/android-exporter`) — Prometheus exporter polling ADB devices; currently documents CPU and battery collectors, with RAM collector as TODO.
- `/home/slnnk/git/mstatic-android` (`team-youdo-android/mobile-static`) — Android static assets synchronized to Yandex Object Storage for test and Selectel S3-compatible storage for production.

## Application build and artifact route

- Application compile/target SDK is 36 and minimum SDK is 23 in `android-youdo4/buildSrc/src/main/kotlin/Dependencies.kt` as checked on 2026-08-13.
- GitLab CI runs on tag `gitlab-runner-android-dind01-runner` using an internal Gradle image.
- The dedicated privileged Docker runner is defined in `automation-services` as `gitlab-runner-android-dind01.youdo.corp` / `172.28.0.175` in the Selectel production inventory; configured concurrency is 3 and cache is stored in Yandex Object Storage.
- Feature builds produce a beta APK. Staging/regression builds produce beta/release APK and release AAB variants for Google, Huawei, and RuStore.
- CI can upload build artifacts to BrowserStack. Manual regression store jobs use `fastlane-docker:0.0.9`; local branch `DevOps-833-fix-hotfix` updates hotfix store jobs to the same version and adds the missing RuStore APK producer artifact, pending merge and pipeline verification.
- Test APK and version metadata are published to Nexus `raw-private` under the `android/` path; Android autotest CI downloads them by logical test job ID.
- Full route, image build rules, store lanes, runners, variables, and confirmed pipeline gaps are documented in `ci-cd.md`.

## Test execution route

`GitLab test runner -> Selenium Grid hub 192.168.30.30:4444 -> Appium node on farm host -> ADB -> emulator or physical device`

- Tests run from `/home/slnnk/git/youdo-android-testing`; environments are selected by `STAND` (currently test through test17 in CI), suites by `SUITE`, and two logical jobs select separate Selenium/Appium pools.
- The framework is Java 11 + Gradle + TestNG 7.7.1 + Selenium 3.141.59 + Appium Java client 7.6.0, with shared internal `autotest-core` and `youdo-api-testing` artifacts from Nexus.
- CI restarts emulator services and invokes `/opt/adb/adb.sh` plus package cleanup on Appium hosts before running tests.
- Reports and artifacts are uploaded under report/job IDs. The investigated report path used `reports.youdo.com` and a Yandex Object Storage mirror.
- Static suite audit dated 2026-08-12 found 577 active application-regression tests. `MindBoxTestSuite` had zero active tests and the configured `InfoMessagesTestSuite` XML/class was absent.

## Farm map (last live verification 2026-08-13)

- Network placement: subnet `192.168.30.0/24` is the office network in Kazan. The Grid hub and farm hosts listed below are therefore located in the Kazan office.
- Hub: `M-K0056` / `192.168.30.30:4444`.
- M-K0058 / `192.168.30.147`: Android 10 emulator, TECNO CM7 Android 16, Samsung A12 Android 11, Redmi Note 13 Pro Android 13.
- M-K0057 / `192.168.30.148`: two Android 10 emulators, Redmi Note 14 Pro Android 14, Samsung A55 Android 14.
- An extra USB device `GHKBB23B15002735` on M-K0057 is explicitly outside the Appium farm scope.
- Appium on the inspected hosts is 1.22.3 with UiAutomator2 driver 1.70.1. Nodes are systemd units, generally using Appium ports 15001-15004 and separate UiAutomator2 `systemPort` values.
- M-K0058 has an Ansible-managed API 29 Google Play x86 AVD (`Nexus_5X_1`, emulator-5554), Android SDK under `/root/Android/Sdk`, and Appium on port 15001/systemPort 15901.
- On 2026-08-14 the previous manually created `Nexus_5X_1` on M-K0058 was stopped and deleted, then recreated by `roles/adb_devices` from the canonical Nexus template archive. The role download passed its pinned checksum, the fresh AVD booted as Android 10/API 29 with ADB state `device` and `sys.boot_completed=1`; `emulator_1.service` and `phone_emulator_1.service` were active/enabled and Appium listened on TCP 15001. The emulator definition is enabled in `inventories/office/host_vars/M-K0058.yml`.

## Monitoring (last live verification 2026-08-13)

- Prod panel/API: `http://zabbix-selectel.youdo.local`; access token is stored only as `ZABBIX_PROD_TOKEN` in `~/ai/current/.env`.
- `M-K0056`, `M-K0057`, and `M-K0058` are monitored by Zabbix Agent 2 on TCP `10050`. Device hosts have templates `YouDo OS Linux template` and `ADB Devices Monitoring`; the Selenium hub currently has only `YouDo OS Linux template`.
- Zabbix reaches hosts in Kazan through NAT and is observed by agents as `192.168.30.1`. The Android-farm group therefore adds this address to the passive `Server=` allowlist in `automation-services/inventories/office/group_vars/adb_devices.yml`.
- Verified end-to-end on M-K0058: agent interface `available=1`, first OS value received, and local ADB discovery returns TECNO, Samsung A12, and Redmi Note 13 Pro. Discovery runs every 30 minutes; device status prototypes run every 2 minutes after discovery.
- Verified end-to-end on M-K0057: agent interface `available=1`, 61 enabled items already have values, and ADB device-status values are arriving. Out-of-scope USB device `GHKBB23B15002735` is explicitly filtered by `roles/zabbix-agent2/files/adb_devices/adb_devices.sh`; verified discovery output contains only farm serials `5b2d4fe2` and `RZCY20AXJHN` even while the excluded device is present as `unauthorized` in raw ADB output.
- Verified end-to-end on Selenium hub M-K0056: Zabbix host `M-K0056-selenium-hub`, interface `192.168.30.30:10050`, `available=1`, OS values arriving. The NAT source `192.168.30.1` is allowed for this inventory group by `automation-services/inventories/office/group_vars/selenium_hub.yml`. There is no Selenium/Grid-specific Zabbix template yet. Active-check connections from the hub to `172.24.0.107:10051` time out, while the configured passive checks work.
- Inventory-driven Hub HTTP check verified on 2026-08-20: `~/ai/current/skills/android-dig/scripts/selenium_hub.py` selected the unique Enabled Zabbix visible name ending in `-selenium-hub`, derived `192.168.30.30` from its main agent interface, and received HTTP 200 from `/wd/hub/status` in 98.4 ms. The current service identified itself as Selenium 3.141.59 and returned `ready=true` / `Hub has capacity`. This is point-in-time status only and does not prove historical job health or Grid-to-Appium reachability.
- The same Hub checker now inventories Selenium 3 registrations through `/grid/console`, confirms each with `/grid/api/proxy`, reads aggregate slots from `/grid/api/hub`, and performs direct Appium status checks only when the proxy IP matches a current Enabled Zabbix host. Live snapshot at 2026-08-20 16:38:20 UTC contained 8 registered/idle/ready Appium 1.22.3 proxies: M-K0057 `.31` ports 15001–15004 mapped to `emulator-5554`, `emulator-5556`, `RZCY20AXJHN`, and `5b2d4fe2`; M-K0058 `.32` ports 15001–15004 mapped to `emulator-5554`, `15888255AE004773`, `x4pf5l5haegykni7`, and `RZ8R71ZRK8H`. Hub totals were 8 free of 8. This is a dated dynamic registration snapshot, not a permanent device assignment guarantee.
- A second snapshot at 2026-08-20 16:40:36 UTC caught all 8 slots busy during an active run. All proxy and Appium checks still passed. Selenium 3 returned raw `ready=false` solely because `free=0`; the checker records the operational state as `saturated`, preserving the distinction between healthy full utilization and a Hub outage.

### Dynamic Android-dig inventory (verified 2026-08-20)

- The authoritative current machine scope for Android infrastructure diagnostics is the exact Zabbix host group `Selenium`, restricted to hosts with Zabbix host status `Enabled` (`status=0`). Nodes can change; static notes and old farm lists must not be used to construct the current scope.
- Read-only collector: `~/ai/current/skills/android-dig/scripts/zabbix_hosts.py --group Selenium --pretty`.
- The live snapshot returned groupid `61` and Enabled technical hosts `M-K0056`, `M-K0057`, and `M-K0058`; all three main agent interfaces reported `available=1`, and none was in maintenance.
- Zabbix monitoring-interface IPs were `192.168.30.30`, `192.168.30.31`, and `192.168.30.32`. The M-K0057/M-K0058 values differ from the historical Appium/SSH addresses `192.168.30.148`/`.147`. Use the Zabbix technical hostname as the cross-source join key and treat monitoring, Appium, SSH, and NAT IPs as source-specific attributes.

### Alloy/Loki delivery incident (2026-08-20)

- Current Loki read endpoint for `android-dig`: `http://loki.dev.youdo.corp` (user-provided update on 2026-09-08; reachability was not checked during this configuration-only change).
- Later read-side verification on 2026-08-20 through `http://loki-read.yandex-test.youdo.local` found current `integrations/journal` operational streams for all three Enabled Selenium hosts M-K0056, M-K0057, and M-K0058, with samples close to both boundaries of a 15-minute query window. This proves current ingestion was available at that check; it does not by itself identify which write endpoint/configuration restored delivery.
- Read-only collector: `~/ai/current/skills/android-dig/scripts/loki_logs.py`. Canonical selector label is `instance`; confirmed stream labels include `job`, `service_name`, `unit`, and `filename`. The collector excludes the Falco `integrations/security` stream from operational-health evidence.
- Historical retention/coverage is incomplete: for GitLab job 3066275's 2026-08-14 correlation window, M-K0056/M-K0057 had no `instance` value and M-K0058 exposed only its Falco stream. Never interpret such empty operational results as host health.

- `automation-services/adb_devices.yml` applies the `alloy` role to `M-K0057` and `M-K0058`. With no office-specific `alloy_services`, the role default `common` deploys the base journald collector plus the always-deployed security collector. The configured push URL is `http://loki.infra.youdo.corp/loki/api/v1/push`.
- Live verification on `M-K0057`: Alloy is enabled and active, `/etc/default/alloy` loads `/etc/alloy/`, and the rendered base config contains the expected journald source and Loki writer. DNS resolves `loki.infra.youdo.corp` to `172.31.2.5`.
- Delivery is failing at the network layer, not in Alloy configuration. Alloy repeatedly logs `context deadline exceeded` and intermittent `dial tcp 172.31.2.5:80: connect: no route to host`; a direct HTTP readiness request also times out.
- The failure is not host-specific: `M-K0058` through gateway `192.168.30.1` and office server `srv0` through `192.168.60.1` also time out to `172.31.2.5:80`. A Selectel production host (`msk3-balancer02`, `172.24.0.22`) reaches the same endpoint in about 20 ms and receives HTTP 301, confirming the Loki ingress is alive.
- Recovery owner/action: restore office-to-Selectel-Kubernetes connectivity for destination `172.31.2.5:80` (and preferably validate the intended route for `172.31.0.0/16`) on the office gateways/VPN/firewall. Do not override `alloy_loki_address` per Android host unless network design explicitly provides a separate office-reachable Loki endpoint. After recovery, verify `curl http://loki.infra.youdo.corp/ready`, absence of new Alloy send errors, and recent Loki entries with `instance="M-K0057"`.
- Alternative Yandex test endpoint check: `M-K0057` cannot resolve `loki-write.yandex-test.youdo.local` through its configured DNS, so the hostname is not directly usable as of 2026-08-20. Inside Yandex test it resolves to `10.16.26.55`, `10.16.26.33`, and `10.16.26.50`; direct requests from `M-K0057` to each address with the correct HTTP Host header returned `HTTP 200` and body `ready` in about 42 ms. Routing is therefore available, but office DNS must resolve the `yandex-test.youdo.local` zone before this endpoint can safely be configured. Avoid pinning one dynamic backend address in `/etc/hosts` or Alloy configuration.
- Repository update on 2026-08-20: `automation-services/inventories/office/group_vars/all` now sets `alloy_version: "1.5.1"` and `alloy_loki_address: "http://loki-write.yandex-test.youdo.local/loki/api/v1/push"` for every host in the office inventory. Inventory resolution was verified for both `M-K0057` and `srv0`; the change has not yet been deployed. Rollout remains dependent on office DNS resolving `yandex-test.youdo.local`.
- DNS incident and live recovery on 2026-08-20: both `M-K0057` and `M-K0058` used `systemd-resolved` with upstream `192.168.30.1`, but an interface drop-in initially advertised only the route-only domain `~local`. That made `eno1` `DefaultRoute=no`, so ordinary names such as `github.com` failed through `127.0.0.53` with `SERVFAIL` even though direct `dig @192.168.30.1` queries worked. The host-side drop-in `/etc/systemd/network/10-netplan-eno1.network.d/local-domain.conf` now contains `Domains=~local ~.`, which preserves unicast resolution for `.local` and makes the same link the catch-all DNS route. Live checks subsequently resolved `github.com`, `loki-write.yandex-test.youdo.local`, and `loki.infra.youdo.corp` successfully on both hosts. This drop-in is not currently represented in `automation-services`, so it is an unmanaged configuration risk and should be added to an appropriate Ansible role if it is intended to remain.

## Known operational issues and risks

- M-K0057 preparation drift reconfirmed by direct SSH on 2026-09-08: `/opt/adb/adb_pkg.sh` is absent even though the autotest CI invokes it. The failure is currently non-fatal in CI and can leave Appium helper-package state unnormalized. Restore the managed helper or update the CI contract, then make unexpected preparation failures fatal.
- M-K0057 `phone_samsung_galaxy_a55.service` is configured for `RZCY20AXJHN` with fixed `systemPort=15903`; its Selenium 3 node config sets both `maxInstances=1` and `maxSession=1`. During job 3121092 it logged 109 port-busy failures over 11:10:09–11:13:29 MSK. Direct SSH observation at 11:58:52 showed the normal active-session ownership: the ADB server listened on `127.0.0.1:15903`, `adb forward --list` mapped that port from `RZCY20AXJHN` to device port `6790`, and Appium reported the corresponding session. The incident is an overlap between session creation and an existing/tearing-down session on the same device, not a foreign port owner; capture request/cleanup timing to isolate the race.
- TECNO/HiOS `com.transsion.usf` froze UiAutomator2. On 2026-08-13 it was removed for Android user 0, the device passed direct and Appium smoke tests, and returned to Grid. Factory APK remains available for rollback via `install-existing`; monitor for power/network/thermal side effects.
- MIUI/HyperOS control center can remain over the app; the test helper recognizes only legacy notification-panel IDs. Pre-session foreground/overlay reset needs hardening.
- Some sessions were abandoned without timely `driver.quit()`, leaving stale instrumentation until Appium's 600-second new-command timeout. `/status` alone does not prove UiAutomator2 or session health; watchdog coverage is incomplete.
- Appium 1.22.3 is old, particularly for Android 16. Upgrade should be staged with a canary and Android 10 emulator regression checks.
- Report HTML and Appium capabilities have exposed credential-bearing URLs; do not publish raw session listings/logs. The investigated Yandex report artifacts were `public-read`.
- Nexus `raw-private` was observed anonymously downloadable by known URL. Never upload an unencrypted archive containing the shared ADB private key.
- A key-free canonical AVD archive is published at `raw-private/android/emulator.tar.zst` with a sibling `.sha256`. It contains only `Nexus_5X.avd`; publication was performed directly to the Nexus backend because nginx buffers large PUT bodies on the small root filesystem. Do not route multi-gigabyte uploads through the current nginx path until its client temp storage/buffering is fixed.
- `roles/adb_devices/tasks/android.yml` provisions new managed AVDs from that canonical archive rather than `avdmanager create avd`. Farm hosts download it directly from the internal Nexus backend on port 8081 with a pinned SHA-256, extract one renamed copy per `adb_device_avd_name`, generate the registration `.ini`, and rewrite per-instance identity/RAM/skin settings. Existing `<name>.avd` directories are never overwritten.
- Redmi Note 13 Pro requires MIUI's `USB debugging (Security settings)` for injected Vysor/ADB input; ordinary shell cannot toggle the protected property.
- Android user CA installation is interactive on normal non-root devices: automation pushes certificates and opens the credentials installer, then needs UI confirmation.
- Hotfix publication inconsistency has a prepared fix on `DevOps-833-fix-hotfix`, but remains operationally unverified until merge and a real hotfix pipeline confirms artifact production and manual publication startup.
- Android build/test jobs use version tags rather than immutable image digests; registry tag mutation is a CI reproducibility risk.
- Runner host variables currently contain plaintext access material; values must not be copied to notes. Migrate them to Ansible Vault/approved secret storage and rotate as appropriate.

## Where to inspect and recover

- Farm state: `adb devices -l`, systemd Appium/emulator units, journal for the relevant unit, Grid registration, and a real UiAutomator2 command—not only Appium `/status`.
- Reports: report HTML, per-test logs, screenshots, page source, GitLab artifacts, Appium journal, device logcat, and host kernel journal.
- Infrastructure definition: `automation-services/roles/adb_devices` and `inventories/office/host_vars`.
- Detailed incident/recovery history: `~/ai/current/knowledge/log/2026-08-12-android-farm-appium-147-148.md` and `~/ai/current/knowledge/log/2026-08-04-android-farm-avd-template-transfer.md`.

## Recent role maintenance

- 2026-08-13: `roles/adb_devices/tasks/main.yml` was reduced to ordered imports of `system.yml`, `android.yml`, `appium.yml`, and `vnc.yml`. SDK, Studio, AVD provisioning, emulator units, and the ADB helper are consolidated in `android.yml`; CPU setup is part of `system.yml`. SMS Forwarder and both AVD/Appium smoke-test stages were removed. An isolated `ansible-playbook --syntax-check` for the role passed. The repository-wide `adb_devices.yml` syntax check is currently blocked locally by the absent external `zabbix` role.
- 2026-08-13: After the Ansible update, Android SDK archive download was migrated from a hand-written `curl` command and separate checksum tasks to `ansible.builtin.get_url`; Android Studio PPA management was migrated from `add-apt-repository` commands to `ansible.builtin.apt_repository`; Appium HTTP readiness checks now use `ansible.builtin.uri`. The role no longer installs or invokes `curl`.
- 2026-08-13: SDK and Android Studio tasks were consolidated into `roles/adb_devices/tasks/android.yml`, with separate `android-sdk`/`adb` and `android-studio` tagged blocks. Command-line tools are extracted directly into their versioned SDK directory, removing the previous `stat`, temporary extraction, and `mv` sequence; redundant post-install SDK package listing/assertion was removed.
- 2026-08-13: AVD creation/configuration and the `adb.sh` helper were also consolidated into `android.yml`; `avd.yml`, `avd_config_device.yml`, and `adb_script.yml` were removed. AVD configuration no longer needs a per-emulator task include, and redundant post-creation `stat`/`assert` checks were removed. Input validation for emulator definitions remains. The ADB server is now restarted only when the managed host key pair changes.
- 2026-08-13: Emulator systemd management was consolidated into `android.yml`, and `emulators.yml` plus the broad `emulator-restart` handler were removed. Each changed unit is now restarted individually while unchanged units are only ensured started/enabled. Emulator selection uses block-local variables instead of `set_fact`; the redundant standalone ADB transport wait was removed because the authorization script already waits for `device`. Boot-completion waiting remains.
- 2026-08-13: Appium session smoke tests and the HTTP `/status` readiness check were removed from `tasks/appium.yml`. Appium tasks use block-local present/absent device lists. Unit reload and change-driven restart are handled by `daemon-reload` and `appium-restart`; an explicit `started/enabled` task still restores unchanged but stopped services, and handlers are flushed before the role completes. An Appium npm package change also triggers service restart.
- 2026-08-13: Automatic headless ADB authorization was temporarily disabled: the emulator unit's `ExecStartPost` call is commented and the duplicate direct invocation was removed from `android.yml`. The script remains installed for quick rollback. New/recreated AVDs or a changed host ADB key may remain `unauthorized` until this is restored or authorization is handled another way.
- 2026-08-13: `templates/adb.sh.j2` was documented inline. It prepares connected/authorized devices by locking portrait orientation, disabling/resetting autofill, granting the test application storage/location permissions, and removing Appium helper packages so the next session installs clean copies.
- 2026-08-14: SDK license acceptance and package installation gained local marker checks. A full rerun on M-K0058 had previously timed out after 300 seconds because command-line tools 22.0's deprecated `sdkmanager --licenses` needlessly fetched the Google repository despite installed licenses/packages. The role now skips those network calls when `licenses/android-sdk-license` and the API 29 Google Play x86 `package.xml` already exist; the subsequent full-role run completed with `failed=0`.

## Related log entries

Newest first, all under `~/ai/current/knowledge/log/`:

- `2026-09-08-android-farm-android-dig-loki-endpoint.md` — Loki read endpoint for `android-dig` changed to `http://loki.dev.youdo.corp`.
- `2026-09-08-android-farm-android-dig-job-3121092.md` — port `15903` busy race on M-K0057 Samsung A55; missing `adb_pkg.sh`; direct SSH verification.
- `2026-09-07-android-farm-android-dig-job-3120554.md` — no infrastructure failure; TestNG `SAXParseException` on retry suite XML; Loki 404.
- `2026-08-20-android-farm-android-dig-job-3078215.md` — Redmi Note 13 Pro `UnicodeIME` missing; confirmed preparation drift.
- `2026-08-20-android-farm-android-dig-job-3077287.md` — `No route to host` to `.147/.148` Appium addresses.
- `2026-08-20-android-farm-android-dig-job-3066275.md` — first collector pass; Zabbix and Loki correlation.
- `2026-08-20-android-farm-global-skill-android-dig.md` — creation of the `android-dig` skill and its collectors.
- `2026-08-13-android-farm-selenium-hub-zabbix.md` — Zabbix agent on hub M-K0056 behind NAT.
- `2026-08-12-android-farm-appium-147-148.md` — TECNO USF freeze, farm recovery, autofill rollout, `adb.sh` drift.
- `2026-08-12-android-farm-vysor-redmi-note-13-pro-input.md` — MIUI `persist.security.adbinput` blocks injected input.
- `2026-08-12-android-farm-autotests-report-3063278.md` — report 3063278 failure analysis.
- `2026-08-04-android-farm-avd-template-transfer.md` — AVD template transfer M-K0057 -> M-K0058, sparse `userdata-qemu.img`, Nexus archive, Ansible bootstrap.
- `2026-07-22-automation-services-adb-devices-ca-certificates.md` — `roles/adb_devices` CA certificate tasks.
