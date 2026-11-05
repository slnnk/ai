---
system: android-farm
status: verified
checked: 2026-11-05
tags: [android, gitlab-ci, diagnosis]
---
# Android job 3278160: suite setup HTTP 404 and monitoring gap

## Task and verdict
Read-only android-dig diagnosis of [job 3278160](https://gitlab.youdo.sg/youdo/Test/youdo-android-testing/-/jobs/3278160).
Confirmed infrastructure dependency failure: suite setup uses an obsolete Houston mock Yandex endpoint and receives HTTP404. Farm health remains unverified.

## Job and timeline
Project69 `youdo/Test/youdo-android-testing`, pipeline142391, branch `DevOps-908-gradle-image-18`, SHA `7ac4940501f03dcabeae0a35bad49a1733cc39dc`.
Job failed with `script_failure`; runner108 `gitlab-runner-docker-1 integrations-tests (172.28.0.171)`.
2026-11-05 15:04:08–15:10:56 UTC / 18:04:08–18:10:56 Moscow; query window14:54:08–15:20:56 UTC /17:54:08–18:20:56 Moscow.
`JOB_ID=1`, `STAND=test5`, `SUITE=[Debug]`.
Image `gradle:18` pulled successfully; Gradle8.13/JDK21 ran compilation and TestNG setup.
At15:10:38 UTC /18:10:38 Moscow, POST to `http://v2.houston-classifier-mock.test5.yandex-test.youdo.local/experiments/login_via_sms_mobile` returned404 in56ms.
`Debug.init` failed at `HoustonApi.createExperimentInHoustonV2:69` / `AndroidTestSuite.init:105`, expecting200. Result:5 tests,1 failed,4 skipped. No assertion/locator investigation performed.
At15:10:41 UTC /18:10:41 Moscow Gradle reported `:test FAILED`. Report upload to S3 and archive/JUnit GitLab uploads succeeded (201). Missing failed-suite artifact is secondary.

## Corroboration
At15:14:27 UTC /18:14:27 Moscow, read-only GETs to `/api/doc/index.html` and `/experiments/all` returned404 on the old Yandex hostname and200 on `v2.houston-classifier-mock.test5.vk-test.youdo.local`.
Local config at the job commit, `config/selenium.conf:401`, contains `houstonV2.url = "http://v2.houston-classifier-mock.<env>.yandex-test.youdo.local/"`.
This matches [the recovered VK mock documentation](2026-10-16-nomad-test-houston-mock-experiment-setup.md). GETs do not prove POST success or experiment persistence.

## Inventory, Zabbix, Grid and Loki
The mandatory inventory fetch failed: `Unable to determine current Zabbix database version: the table "dbversion" was not found.` No Enabled Selenium inventory snapshot is available.
Consequently no host list was substituted and no Hub, Appium, Zabbix-history or Loki machine query was attempted. Historical and current farm health, slots, ADB, log ingestion and coverage remain unknown; no selectors can be authorized from inventory.
Current project variables (15:13:30 UTC) scope `*`: APPIUM_NODES_1=`192.168.30.31 192.168.30.32`, SELENIUM_SERVER_1=`http://192.168.30.30:4444/wd/hub`.
These are routing clues only, outside a verified Enabled inventory. Group/pipeline/schedule/dotenv/runner overrides are not covered.

## Other observed issues and limits
Preparation reports missing `emulator_2.service` and package removal `DELETE_FAILED_INTERNAL_ERROR`, masked by CI continuation. They do not explain the observed setup HTTP404.
Trace preparation includes a historically excluded non-farm USB device; no device/host diagnosis was performed without current inventory.
Nexus checksum parse warnings occurred during dependency resolution, but compilation and suite setup proceeded; they are not the terminal cause.
The aggregate job collector emitted no categorized events; a temporary sanitized trace was therefore inspected and deleted after analysis. Only compact evidence is retained.

## Status and recommendations
Diagnosis complete. No repository edit, POST to mock, retry, restart, deployment or external tracker update performed. No background operations remain.
Endpoint correction and Zabbix inventory restoration are proposals tracked in [central TODO](../../../../TODO.md) under YouDo / android-farm; neither has implementation approval.
Prioritize the Houston endpoint correction using supervised repository workflow; rollback would restore the previous config but also the demonstrated404. Then verify with an explicitly authorized run.
Restore monitoring access before drawing conclusions about farm health; device preparation drift remains covered by existing backlog entries.

## Portable lesson
none

## Endpoint follow-up (2026-11-05)
The user subsequently approved local changes for all Yandex endpoints and three large MSSQL hosts. The [DevOps-908 publication log](2026-11-05-gitlab-ci-devops-908-gradle-image-18.md) supersedes the earlier no-implementation-approval status for that work. Local config validation passed; expanded MR publication remains pending renewed approval in the central backlog. No runtime recovery is claimed.

## Endpoint source publication verified (2026-11-05)
Follow-up commit `cdea347741d72635371e4bdd80becd645a2efadf` is published in MR1163 with all221 VK domain substitutions and three MSSQL hostname updates. Publication is complete; the earlier pending-publication status is superseded. No merge or new test run occurred, so this does not establish runtime recovery. Zabbix inventory restoration remains a separate open proposal in the central backlog.

## Zabbix error rechecked (2026-11-05)
At15:20:51 UTC /18:20:51 Moscow, DNS resolved `zabbix-selectel.youdo.local` to172.28.0.120. HTTP200 from `/api_jsonrpc.php` contained JSON-RPC error1 with the same missing `dbversion` message, even for unauthenticated `apiinfo.version`. Repeating the Selenium inventory collector failed identically.
This establishes that the error is returned by the Zabbix frontend independently of the inventory token. It does not establish database loss or Zabbix server collection health. Possible database target/schema/permissions or routing issues remain hypotheses; no DB/config/host inspection or modification performed.

## Zabbix SSH diagnosis (2026-11-05)
User-authorized read-only SSH established [Docker startup before /data mount](2026-11-05-zabbix-docker-before-data-mount.md): frontend uses a new empty PostgreSQL cluster on the root filesystem, while the original data directory is on the subsequently mounted disk. Server container is stopped due to an ODBC bind-mount type mismatch. This supersedes the earlier unknown root cause; no remediation or historical farm correlation performed.

## Zabbix availability restored under DevOps-909 (2026-11-05)
The separately approved [Zabbix recovery](2026-11-05-zabbix-docker-before-data-mount.md) restored the original PostgreSQL cluster, server and frontend. At15:41:31 UTC authenticated Enabled Selenium inventory again returns M-K0056/M-K0057/M-K0058. Earlier API-unavailable status is superseded for current access. No historical farm correlation for job3278160 was resumed; original diagnostic coverage limits remain.
