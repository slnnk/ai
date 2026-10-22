---
system: web-autotests
status: verified
checked: 2026-10-21
tags: [data, dependencies, vk-test]
---
# Static autotest dependencies on price and customer recommendations

## Task
Determine whether youdo.static autotests depend on price-predictor and customer-task-recommendations. Read-only source investigation; no test runs or external application changes.

## Context and actions
Existing clean checkout /home/slnnk/git/youdo.static kept on DevOps-852-disable-autotests d6a8ea3e. Refreshed origin with read-only fetch; inspected master26c7ea0d9fab, testFixTests e7b9963a4ec8 and uitests-actual cb549d8acfd4 without switching branches. Price investigation delegated to a read-only agent. Monolith source inspected in existing /home/slnnk/git/youdo; prior audit revision abc9c7ae1a5. Source findings do not establish deployed browser bundle or effective A/B assignments.

## Findings
- No direct service-host references or dedicated response assertions for either target found in the inspected static autotest code.
- price-predictor: master src/apis/TasksApi.ts:150 defines getRecommendedPrice, but no callers in frontend or tests were found. Monolith TasksController.cs:1392 exposes api/tasks/recommendedprice and calls AiTaskPriceManager at1406. Tests choosing a default budget, e.g. TasksTestSuite.java:78, use ordinary control.budgets/price ranges; these are not prediction output. TaskFormsCreator.cs:137-161 uses price-range manager and RecommendedSbrPriceConstants. No confirmed source path from these autotests to price-predictor.
- customer-task-recommendations: indirect optional browser path exists. src/pages/taskFlexCard/TaskCard.tsx:117-135 requests TasksApi.getRecommendationsForNewTask when task_suggestions_task_page_for_taskers is outside control. TasksApi.ts:225 requests api/tasks/{taskId}/recommendations; monolith TasksController.cs:1595 calls CustomerTaskRecommendationsManager. Its CallWithPoliciesAsync catches failures and returns GetFallbackRecommendationsAsync. No tests explicitly enabling this experiment or asserting this generated recommendation output found. Browser requests may occur in tests depending on experiment assignment, but service failure is not demonstrated as a mandatory test blocker.
- Actual recommendation tests use RecommendationsApi from the youdo-api-testing dependency. AllTasksTestSuite.java:2955-2996 testDisplayRecommendedTask seeds recommendations with createUserRecommendation and asserts the executor list. Both current master and testFixTests selenium.conf:533,560 point youdo.recommendations.host to recommendations-mock.vk-test.youdo.local. This is separate from customer-task-recommendations. Prior Jenkins2020 evidence directly demonstrated missing mock /save errors; see linked log.

## Changes
Knowledge log, existing nomad-test map and repository catalog only. No source, CI, services, A/B assignments, fixture APIs or Git publication changed.

## Status and risks
Requested investigation complete. No new execution action required or added to TODO. Existing proposal for restoring missing monolith services remains open; this investigation does not establish that either real Data service is required for passing current UI suites. No outage experiment or full runtime trace performed; transitive dependency implementation in the separately versioned youdo-api-testing library was not audited.

## Related evidence
[Monolith audit](2026-10-21-nomad-test-monolith-data-dependencies.md).
[Jenkins2020 mock failures](2026-10-21-nomad-test-web-testing-two-2020-data-errors.md).

## Portable lesson
none
