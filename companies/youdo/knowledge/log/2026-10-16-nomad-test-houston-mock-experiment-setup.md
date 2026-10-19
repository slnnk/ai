---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [houston, mock, youtrack, testing]
---
# Houston mock experiment setup from documentation and autotests

## Summary

Both manual and automated setup are confirmed. YouTrack documents manual setup through stand-specific Swagger. The user's hypothesis was verified in youdo.static: WebTestSuite.beforeSuite creates seven experiments through the mock API; individual tests create others. Real Hub/classifier are not dependencies. Mock data is in process memory and resets on restart. Current origin/testFixTests already selects the VK mock; origin/master still selects the old Yandex domain. Earlier absence-of-automation findings applied only to the four reviewed articles and the mock service repository, not the UI test repository.

## Task and sources

User asked how mock experiments had been populated and whether YouTrack KB had instructions. Read-only YouTrack article search and four article GETs, plus delegated source review. No article bodies saved, no data-writing API requests or experiment changes performed.

- [Testing experiment events](https://youtrack.youdo.com/youtrack/articles/Test-A-77007405), updated2022-04-21: main instruction. Deploy relevant branch to the stand, open that stand mock Swagger, select /experiments/{experimentLabel}, Try it out, enter experiment identifier from the task and body, Execute. For website testing set the intended group to100%; mobile testing also needs the experiment enabled and the expected group selected.
- [Houston test environment](https://youtrack.youdo.com/youtrack/articles/Test-A-58461053), updated2025-02-19: distinguishes Mock from Staging Hub+classifier and links mock repo/Swagger. Historical domains refer to proxy-test/yandex-test, not currentVK.
- [Creating experiments](https://youtrack.youdo.com/youtrack/articles/AND-A-8), updated2022-05-27: Android client integration, not mock seeding.
- [Houston v2 REST operations](https://youtrack.youdo.com/youtrack/articles/BI-A-53938778), updated2019-12-27: real Hub CRUD/Postman, different schema; do not replay directly against mock.

## Current VK procedure and source verification

Use http://v2.houston-classifier-mock.test5.vk-test.youdo.local/api/doc/index.html for test5. Hostname selects stand-specific data. POST /experiments/{label} creates or replaces an experiment; choose the label and settings from the product/test task. Consult actual Swagger schema before submission. Code requires top-level subject; existing repo README sample omits it and has a trailing comma, so cannot be copied as valid complete JSON. SubjectType values Visitor/User/Task/Url; actual wire serialization should follow live Swagger. POST /experiments/{label}/subject configures subject-to-group binding. Choice requests do not create missing experiments.

GET /experiments/all lists configured records, but its response schema differs from POST and is not a direct replayable backup. No seed/default/Hub synchronization code was found. Restart loses experiments. Existing deployment metadata: release0.0.35, one shared allocation, stand isolation by testN hostname. No request to populate experiments has yet been given; documentation retrieval authorizes no POST.

## Changed files and limits

KB log and existing Nomad system map updated, no repository or external-state change. Need the intended task/experiment definitions before any separately authorized setup; do not invent records. Other unreviewed automation may exist.

## UI autotest seeding confirmed (user hypothesis, 2026-10-16)

Read-only fetched youdo.static and inspected origin/master 1058542dc2254e0ed717b42b9d50bc6eddc49f5f and origin/testFixTests e7b9963a4ec8bc9a00cf7363d8f6c9fa61672f41. Existing clean DevOps-852-disable-autotests checkout preserved. No test execution or API writes.

WebTestSuite.beforeSuite (@BeforeSuite(alwaysRun=true), uitests/src/test/java/portal/suites/WebTestSuite.java:23) calls HoustonApi.createExperimentInHoustonV2 for seven experiments, initially100%control/0%alternative:

- seo_landing_new_design_v2
- offers_price_sort
- no_additional_filters_other_platforms
- show_phone_user_profile_web
- categories_block_without_links_web
- categories_block_with_select_subcategory_web
- remove_button_suggest_task_on_landings

The setup path requires a nonproduction host (!contains("youdo.com")) and getRemote()!=null. Earlier Venus/Admin setup calls can fail before seeding. afterSuite (:348 onward) resets seo_landing_new_design_v2 to5%control/95%with_new_design rather than clearing all experiments. ShortCodesTestSuite:5728 separately creates/overwrites review_area_redesign_on_landings with group toggles.

Client dependency in uitests/pom.xml:90 is youdo-api-testing:youdo-api-testing:1.2.2-SNAPSHOT. Local cached JAR version20261012.142311-1 bytecode confirms POST /experiments/{label}, JSON groups+subject, and replacement of <env> in houstonV2.url with active environment. Example observed payload for seo_landing_new_design_v2: {"groups":[{"group":"control","proportion":100},{"group":"with_new_design","proportion":0}],"subject":"visitor"}. This example was read from test helper behavior, not submitted.

Critical branch difference at uitests/config/selenium.conf:537:
- origin/master uses http://v2.houston-classifier-mock.<env>.yandex-test.youdo.local/.
- origin/testFixTests already uses http://v2.houston-classifier-mock.<env>.vk-test.youdo.local/ and has the same seeding hook.

The URL getter uses TestConfig.getValue, not getValueFromEnvOrConfig; a plain -Dautotests.houstonV2.url override is not supported by that getter. Do not propose it without changing/validating resolution. API helper source repository was not identified; HTTP behavior evidence is the cached JAR, while test call sites and config are repository source. No endpoint change is needed for the already-updated testFixTests branch. Actual future seeding depends on the selected branch/environment and successful execution reaching setup; no new test run was authorized here.

Primary source links:
- https://gitlab.youdo.sg/youdo/youdo.static/-/blob/1058542dc2254e0ed717b42b9d50bc6eddc49f5f/uitests/src/test/java/portal/suites/WebTestSuite.java#L23
- https://gitlab.youdo.sg/youdo/youdo.static/-/blob/e7b9963a4ec8bc9a00cf7363d8f6c9fa61672f41/uitests/config/selenium.conf#L537
