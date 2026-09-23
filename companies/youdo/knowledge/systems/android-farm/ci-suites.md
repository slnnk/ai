---
system: android-farm
status: verified
checked: 2026-08-12
tags: [android, autotests, testng, suites, gitlab-ci]
---
# YouDo Android testing: CI suites

- Date: 2026-08-12
- Repository: `/home/slnnk/git/youdo-android-testing`
- Context: static audit of suites selected by `.gitlab-ci.yml` rules.
- Counting method: TestNG methods annotated with `@Test`; active excludes `enabled = false`. No `dataProvider` or `invocationCount` usages were found in `src/test/java/app/suites`.

## Results

| GitLab option | XML | Active | Declared | Disabled |
|---|---|---:|---:|---:|
| Регресс приложения | AllTestSuiteParallel | 577 | 728 | 151 |
| Регресс сайта | RegressusMobileTestSuite | 194 | 261 | 67 |
| MindBox | MindBoxTestSuite | 0 | 20 | 20 |
| Авторизация и регистрация | AuthTestSuite | 16 | 39 | 23 |
| Задания | TasksTestSuite | 248 | 294 | 46 |
| Чат | ChatTestSuite | 30 | 30 | 0 |
| Уведомления | NotificationsTestSuite | 19 | 33 | 14 |
| Пакеты предложений | PackagesTestSuite | 15 | 22 | 7 |
| Верификация | VerificationTestSuite | 45 | 98 | 53 |
| Профиль | ProfileTestSuite | 211 | 234 | 23 |
| Создание задания | CreateTaskTestSuite | 92 | 96 | 4 |
| СБР | SbrTestSuite | 10 | 25 | 15 |
| test | DeepLinksTestSuite | 3 | 3 | 0 |
| Debug | Debug | 4 | 6 | 2 |

`TasksTestSuite.xml` includes both `app.suites.TasksTestSuite` (238 active / 269 declared) and `app.suites.SbrTestSuite` (10 active / 25 declared), hence 248 active in the actual CI suite.

## Findings / risks

- `[Упавшие тесты]` points to dynamically downloaded `FailedTestSuite_${FAILED_JOB_ID}.xml`; its count depends on the selected failed job and cannot be determined statically.
- `[InfoMessagesTestSuite]` points to `TestSuites/InfoMessagesTestSuite.xml`, but that XML and the corresponding Java class are absent in the repository. This CI option appears broken.
- `MindBoxTestSuite` declares 20 tests, all with `enabled = false`, so it currently has zero runnable tests.

## Relevant locations

- CI mapping: `.gitlab-ci.yml`, rules around lines 69-117.
- TestNG XML files: `TestSuites/`.
- Test classes: `src/test/java/app/suites/`.
