---
system: youdo
status: verified
checked: 2026-11-25
tags: [graphify, code-navigation]
---
# YouDo: Graphify C# navigation pilot

## Task

Run the requested local Graphify pilot on the YouDo monolith. Compare
candidate source discovery with agentgrep and rg, then check actual call paths
against the C# source.

## Context

`~/git/youdo`, local commit `abc9c7ae1a5cc65509065be344abf20cb74a6810`,
branch `DevOps-904-cache-monolith-npm`. The checkout was clean before and after
the pilot. No remote refresh. Scope was the 7,950 tracked C# files. The
Graphify defaults excluded vendored `util/node/node_modules/node-gyp/lib/Find-VS2017.cs`.
Two source files had partial parse errors. Eleven produced no symbol nodes.
The pilot used the local AST update, with no semantic model or integration.

## Actions

Copied tracked C# files to a private temporary directory using
`git ls-files -z '*.cs'` and tar. Installed Graphify 0.9.119 in an isolated
Python 3.12 venv and ran `graphify update ./src`. An auxiliary 370-file copy
tested graph generation while the full graph ran. Its output was excluded from
the comparison.

Preselected six questions with manually verified expected source files. The
baseline interleaved `agentgrep find --paths-only --max-files 5 <anchor>`
with `rg -l -w -F <anchor>` results, sorted with exact file stems first.
The graph arm used `graphify query "<question>" --seed <anchor> --depth 2
--budget 2000`. Its ranking was the first five distinct file paths in the
returned NODE lines. The combined arm kept the first two ordinary results and
interleaved graph and remaining ordinary candidates up to five files. The
criterion was presence of every required source file in the first five.
This grades single-pass candidate retrieval. Iterative source reading
confirmed all six scenarios. No timed agent or token-consumption comparison
was performed.

## Findings

| Scenario | Query anchor | Required files in first five, baseline | Graphify | Combined |
| --- | --- | ---: | ---: | ---: |
| Redis readiness registration | RedisHealthCheck | 2/2 | 2/2 | 2/2 |
| Daily subscription HTTP client | DailyCompilationsService | 1/2 | 2/2 | 2/2 |
| Escrow offer version check | RegisterDeal | 0/2 | 0/2 | 0/2 |
| User verification to storage | UserVerificationInfoController | 1/3 | 1/3 | 1/3 |
| Recommended executors to AI manager | RecommendedExecutorsController | 1/3 | 1/3 | 1/3 |
| Payment notification publisher and consumer | YandexKassaNotification | 3/3 | 3/3 | 3/3 |
| Complete scenarios | | 2/6 | 3/6 | 3/6 |
| Matched files | | 8/15 | 9/15 | 9/15 |

Full build took 138.88 s and peaked at 1,031,020 KiB RSS. The 115,890,877-byte
JSON contains 68,900 nodes and 180,491 edges. Median CLI time, including
startup, was 0.0965 s for the two ordinary commands and 8.8785 s for
Graphify query. Five graph answers reported truncation or went over the
requested output budget. The escrow seed was ambiguous.

### Source evidence and targeted paths

Paths below are relative to `~/git/youdo` at the recorded commit.

- Redis: `YouDo.AspNetCore.HealthChecks/HealthCheckExtensions.cs:31`
  registers the class from `YouDo.AspNetCore.HealthChecks/RedisHealthCheck.cs:9`.
- Daily subscriptions: `YouDo.Managers/Ai/Recommendations/DailyCompilationsService.cs:69`
  calls the Refit interface method from
  `YouDo.Managers/Ai/Recommendations/IHttpDailyCompilationsClient.cs:13`.
- Escrow: a directed `graphify path` with the API file qualified via
  `path::symbol` found the edge from `RegisterDeal()` in
  `YouDo.Web.Api/Controllers/Escrow/EscrowAuthorController.cs:122` to
  `SbrTaskManager.CreateDealWithCheckVersionAsync()`. The version guard and
  subsequent creation call are in `YouDo.Managers/Escrow/SbrTaskManager.cs:393`.
- Verification: a directed path from `UserVerificationInfoController.GetByUserIdAsync()`
  to `VerificationInfoRepository.GetUserVerificationInfoAsync()` returned three
  edges through the interface and its implementation. Verified in
  `API/YouDo.API/Controllers/Users/UserVerificationInfoController.cs:41`,
  `YouDo.Managers/IocModule.cs:655`,
  `YouDo.Managers/Users/VerificationLightweightManager.cs:66`, and
  `YouDo.DAL/Repositories/Verification/VerificationInfoRepository.cs:58`.
- Recommendations: a directed path from `RecommendedExecutorsController.Recommended()`
  to `ExecutorAiRecommendationsManager.GetAsync()` returned two call edges via
  `ExecutorRecommendationsManager.GetRecommendedWithoutOfferedAsync()`.
  Verified in `YouDo.Web.Api/Controllers/RecommendedExecutorsController.cs:130`,
  `YouDo.Managers/ExecutorRecommendationsManager.cs:53`, and
  `YouDo.Managers/Ai/Recommendations/ExecutorAiRecommendationsManager.cs:59`.
- Payment notification: `YouDo.Web.Kassa/Controllers/PaymentsController.cs:28`
  publishes the message from
  `YouDo.Entities/Finances/YandexKassa/YandexKassaNotification.cs:8`.
  `YouDo.Finance.Service/Processors/YandexKassaNotifications/YandexKassaNotificationsProcessor.cs:11`
  declares the consumer.

All three targeted paths were inferred edges. The source checks above
established the links for these inputs. The exact endpoint names were available
for these diagnostic path tests. Their results are outside the top-five score.

## Changes

The repository stayed clean at the same commit. The pilot did not install
hooks or configure any agent. Temporary inputs, graphs and venv were removed.
A private replay archive with the comparison scripts and scenario definitions
is stored at `~/ai-data/graphify-pilot/2026-11-25-youdo-csharp-replay.tar.gz`.
It contains no copied source files or graph. Retain it for a repeat comparison
against another Graphify version. It can be removed if that comparison is dropped.

## Status and risks

Pilot complete. Keep agentgrep and rg for everyday navigation and consider
Graphify on demand for call paths with known endpoints. The observed single-pass
gain was one scenario, with a slower CLI and a two-minute initial build.
There is no rollout or outstanding action. No pilot process remains.

## On-demand adoption, 2026-11-25

The user selected `graphify path` for complex call chains with two known
endpoints in checkouts under `~/git`. Normal searches continue to use
agentgrep and rg. Installed Graphify 0.9.119 in a local Python 3.12 venv and
created the private output root `~/ai-data/graphify/`.

A disposable two-file C# fixture verified that the CLI builds to an absolute
output path outside the source directory, returns the expected directed edge,
and resolves the renamed endpoint after a subsequent update. No checkout graph
was built during setup. The CLI is invoked directly by the agent's shell.

## Portable lesson

none

## Task metrics: youdo-graphify-code-pilot-2026-11-25

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "youdo-graphify-code-pilot-2026-11-25",
  "created": "2026-11-25T01:35:55.327641+03:00",
  "first_result": "pass",
  "final_result": "pass",
  "state": "closed",
  "kind": "investigation",
  "model": "unknown",
  "session_id": "unknown",
  "corrections": null,
  "unnecessary_actions": null,
  "critical_events": null,
  "tokens": null,
  "active_seconds": null,
  "evidence": "Full C# graph built, six paired queries graded, and three targeted paths verified in source",
  "updated": "2026-11-25T01:35:55.327689+03:00"
}
```
