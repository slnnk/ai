---
system: android-farm
status: verified
checked: 2026-08-12
tags: [android, autotests, report, appium, tecno, miui, sbr]
---
# Android autotests: report 3063278

## Task

Analyse the seven failed tests of Android autotest report `3063278` (suite `[Упавшие тесты]` of the SBR regression on stand `test9`) and separate test defects from device/infrastructure failures.

Date: 2026-08-12 (Europe/Moscow)

## Context
- Repository: `/home/slnnk/git/youdo-android-testing`, branch `master`, HEAD `d8993d0f`.
- Environment: `test9`, Android, CI job/report ID `3063278`.
- Report URL: `https://reports.youdo.com/yandex/youdo-android-testing/3063278/report/report.html`.
- The public CI artifact is also available at `https://storage.yandexcloud.net/youdo-smokus/yandex/youdo-android-testing/3063278/`; this follows `.gitlab-ci.yml` upload configuration and avoids ServicePipe blocking automated HTML requests.
- Basic Auth is stored only as `YOUDO_REPORT_BASIC_AUTH` in `~/ai/current/.env`; the value is not duplicated here.

## Findings: result summary
- Suite: `[Failed(Failed(Failed(СБР)))] [Упавшие тесты]`.
- 7 tests, 0 passed, 7 failed; each log contains a retry and the failures are reproduced.

## Findings: per test
1. `testTaskSearch`: expected two task rows, but the generic `titleView` locator also counts the new promotional card `Попробуйте смены`. The screenshot/page source has two matching task titles plus the promotional title. `AllTasksScreen.assertCountItemTask()` subtracts only rows containing `Промо`, so it now counts 3. Restrict the task-row locator to a task container or exclude non-task cards.
2. `testCardPaymentFilter`: after `clickButtonClear()` the screenshot is already the task list, but the test immediately checks the filter switch. The common clear helper uses several generic IDs and repeated clicks. Verify current UX and either reopen the filter before asserting or use a screen-specific clear/reset locator and wait for the expected screen.
3. `testEnableDisableSbr`: screenshot shows `Сделка без риска` visually selected. Compose page source represents the selectable card as `android.view.View checkable=true checked=true` with child `TextView resource-id=titleOption`. `assertRadioButtonPayment()` still targets the old ViewGroup/TextView `com...:id/title` plus `android.widget.RadioButton`; update it to the Compose checked ancestor.
4. `testMoreThanMaxSbr`: the fourth suggested budget is now only `до 14 000 ₽`, so the expected warning for a budget over `150 000 ₽` cannot appear. The test name says manual input but the implementation clicks `priceRange3`. Use actual manual entry above the active product limit, or derive/assert the current limit and choose suitable data.
5. `testMoreThanMaxSbrControls`: failed during login on Xiaomi 24115RA8EG before the scenario. The first onboarding page and clickable `Войти` remain visible after the logged click; subsequent wait for `Войти через электронную почту` times out. Even after stabilizing login, the same obsolete fourth-budget assumption as item 4 should be corrected.
6. `testFilterOnMaps`: failed during login on Xiaomi 23117RA68G before reaching the map; screenshot/page source show the MIUI quick-settings shade, not the app. `MainScreen` does call the notification-panel close check in its constructor, but the shade was open at failure. Add a foreground/package check and robustly close system UI before login; retry the login transition when the expected auth screen does not appear.
7. `testOfferChangingCashToSbr`: infrastructure failure. Both attempts time out after 240000 ms while Appium proxies a click to UiAutomator2 on TECNO CM7 / Android 16; screenshot, page source and device info also fail afterward. Check Appium/UiAutomator2 and ADB/device logs for UDID `15888255AE004773`; recycle the session/device. This does not indicate an SBR assertion failure.

## Open items: priority / next steps
- First fix the Compose payment-option locator, task-row counting, and over-limit test data; these are deterministic test defects.
- Confirm/reset semantics on the filter screen and make `clickButtonClear` screen-specific.
- Harden `authByEmail`: assert the transition after clicking `Войти`, retry/relaunch if still on onboarding, and ensure the AUT is foreground with the system shade closed.
- Quarantine/recycle the TECNO Android 16 device/session on UiAutomator2 proxy timeout and inspect Appium server logs.
- Re-run this seven-test failed suite after the above changes to separate product regressions from framework/device failures.

## Open items: security risk
- The Yandex Object Storage artifact path is readable without the report-domain Basic Auth because CI uploads it with `--acl public-read`.
- The HTML logs include sensitive request headers and an application-download URL containing embedded repository credentials. No values were copied into this note. Remove/redact secrets during report generation, stop embedding credentials in capabilities/URLs, and reconsider public-read access for test artifacts.

## Portable lesson

none
