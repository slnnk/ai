---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [jenkins, web-autotests, data, mock]
---
# Web testing build2020 missing dependency diagnosis

## Task
User explicitly requested parallel read-only diagnosis of https://build.youdo.sg/job/youdo_web_testing_two/2020/ while preparing subcategory-predictor VK changes. Parallel agent inspected bounded console evidence; parent reviewed sanitized summary. No implementation or external changes authorized by this log request.

## Context
Build FAILURE on test1, rerun FailedTestSuite_0002019. Reported113executions/59failures/52skipped. Freestyle Jenkins job has no JUnit API results (404); console contains final TestNG summary and request traces. Console9MB/192k lines filtered in memory, no raw/full console or user payload retained in KB.

## Findings
Two dependencies are directly demonstrated as missing-route errors:

| Dependency | Exact failing request | Request occurrences including retries | Final failed tests |
| --- | --- | --- | --- |
| sysadmins/taskqualitycontrolfortest | POST http://taskqualitycontrol.vk-test.youdo.local/evaluation/testdata/ ->404 |16|8|
| sysadmins/youdo_recommendations_mock | POST http://recommendations-mock.vk-test.youdo.local/save ->404 |12|6|

Thus14of59final failures directly correspond to the two unavailable test setup APIs. Example tests: testTQQDecisionPublishTask, testDeleteTaskWithoutReason, testDisplayRecommendedTask, testTaskDisplayForExecutorWithMoreThan10TasksDone. Existing live inventory independently found both targets absent in VK Nomad/Consul and root404; see dependency-audit note.

Two other tests fail because expected subcategory `Генеральная уборка` is missing: testCreateTaskFromMainPage and testDisplayTaskFormWhenSetTextInCigaretteAndClickEnterOnManePage. Missing subcategory-predictor is a plausible explanation, not proven by this console: no direct predictor HTTP request/error shown. No confirmed link to price-predictor or customer-task-recommendations failures in this build.

Remaining43failures classified only by visible symptom:8HTTP500 (cards/SBR/insurance-related flows),1HTTP403documents,1HTTP429dialogs,13Seleniummissing-element,16UI/dataassertions,4`ТЕСТ НЕ НАПИСАН`. Together with14directmock404 and2subcategoryassertions, these account for59. Without backend stack traces these are not evidence of additional missing Data services. No product/test-data root-cause investigation beyond this separation was performed.

## Evidence and changes
Sanitized evidence /home/slnnk/ai-data/data-services-diagnosis/web-testing-two-2020/summary.json and console-filtered.json. No source, infrastructure, Jenkins jobs, SQL, API test fixtures or CI settings changed. No reruns launched. Parent's central five-target restoration proposal now links this diagnostic; only subcategory-predictor implementation is currently requested.

## Status and risks
Requested bounded log diagnosis complete. Two mock dependencies confirmed; predictor relationship remains hypothesis. Restoring these endpoints alone is not a promise that all59failures will pass. Remaining actions are tracked in the existing central Data-dependency proposal rather than duplicated here.

## Related evidence
[Data dependency inventory](2026-10-21-nomad-test-monolith-data-dependencies.md).
[Subcategory preparation](2026-10-21-nomad-test-subcategory-predictor-vk.md).

## Portable lesson
none
