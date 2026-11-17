---
system: nomad-test
status: verified
checked: 2026-11-17
tags: [vk-cloud, inventory, shared-services]
---
# DevOps-884 shared application inventory from VK recovery

## Task
Prepare an initial historical list of shared applications restored in VK Cloud for DevOps-884. Investigation only; no implementation or external writes requested.

## Context
Fresh authenticated YouTrack GET on November17 confirmed DevOps-884 title `[Dynamic env] Деплой общих сервисов`, description examples pechkin/mailer/geocoder, and no comments. Interpret single as one shared deployment across stands, not necessarily one container or allocation. Recovery evidence below is dated October14–21; no current runtime audit performed.

## Findings
Initial ten shared services, accepted October14:

1. geocoder
2. youdo-call-service
3. youdo-business-doc-generator (doc-generator)
4. chat-content
5. textvalidation
6. tinkoff-e2c-sign-service
7. DebuggingEvents (including companion Elasticsearch)
8. BlackListedEmailChecker (blec)
9. pechkin
10. mailer

Source: [final launch table](2026-10-14-nomad-test-devops-898-implementation.md#verified-final-launch-scope-2026-10-14).

Subsequently restored shared applications:

11. HoustonV2Mock, October16, version0.0.35.
12. houston-hub v2, October16, version2.7.7.
13. houston-classifier v2, October16, version2.6.10.
14. daily-compilations, October21, version0.5.15.
15. subcategory-predictor, October21, version1.0.8 (VK one healthy instance; production replicas are separate).
16. youdo_recommendations_mock (recommendations-mock), October21, version0.0.16.

Sources: [Houston acceptance](../systems/nomad-test.md#hub-mongodb-memory-and-final-shared-rollout-2026-10-16), [Houston mock](2026-10-16-nomad-test-devops-898-houstonv2mock-vk-assessment.md), [daily-compilations](2026-10-21-nomad-test-daily-compilations-missing.md), [subcategory-predictor](2026-10-21-nomad-test-subcategory-predictor-vk.md), [recommendations mock](2026-10-21-nomad-test-recommendations-mock-vk.md).

Exclude Socket and LogReader: per-stand deployment, even though LogReader initially had only test5. Exclude vks-policy-generator: unused and explicitly not deployed. Price-predictor, customer-task-recommendations and taskqualitycontrolfortest lack accepted restoration in the inspected October21 evidence; do not claim them restored. Infrastructure and deployment tooling are outside this application list.

## Changes
Historical inventory bookkeeping only. No source, infrastructure, Git or YouTrack mutation.

## Status and risks
Requested initial list complete:16 shared applications supported by recovery records. Shared topology does not establish replica count1. No new implementation proposal or follow-up action was introduced; DevOps-884 overall design/implementation is not complete or authorized by this inventory. Existing recovery backlog remains unchanged. No task background operations remain.

## Portable lesson
none

## Task metrics: DevOps-884-shared-inventory

```agent-task-metrics-json
{
  "version": 1,
  "task_id": "DevOps-884-shared-inventory",
  "created": "2026-11-17T21:47:43.295708+03:00",
  "first_result": "unknown",
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
  "evidence": "Live Nomad GET snapshot 2026-11-17T18:49:53UTC:14of16matched,2absent,4additional shared application jobs; allocation counts match desired.",
  "updated": "2026-11-17T21:50:49.945746+03:00"
}
```

## Live Nomad comparison (November17, 18:49:53 UTC)

User requested a live comparison. Read-only authenticated Nomad API GETs covered all visible namespaces (`default` only),328jobs, current allocation stubs and each job specification. Sanitized snapshots: `/home/slnnk/ai-data/devops-884/nomad-inventory.json` and `comparison.json`. No job templates, environment values or credentials were persisted. These observations supersede the historical-only scope for the current comparison, while October recovery evidence above remains historical.

14of16 listed applications have running jobs and desired running allocation counts. No houston-hub or houston-classifier job exists in the returned inventory, and no corresponding task/group names were found under other jobs. HoustonV2Mock is present and running; do not equate it with the two real applications.

Name mappings: textvalidation -> textvalidation-master; tinkoff-e2c-sign-service -> tinkoffe2csignservice; DebuggingEvents -> debuggingevents-master; BlackListedEmailChecker -> blec-staging; youdo_recommendations_mock -> recommendations-mock.

Four additional shared application jobs are running, each with1desired/1running allocation: escrow-tinkoff-router, moderation-bert, taskqualitycontrol and userinsurance-gotenberg. Thus18shared application jobs are observed under this scope (14matching+4additional), rather than the historical16. This excludes infrastructure/tooling: dynamic-inventory, Kafka components, Redis, Traefik, Consul exporter and Alloy; system jobs are also excluded. A per-stand application having only one currently deployed stand is not classified as shared on that basis.

Running allocation counts for matched applications: mailer21(API1+scheduler10+dispatcher10), pechkin3, chat-content2(uploader1+downloader1), daily-compilations2(API1+PostgreSQL1); each other matched application1. All match desired group counts in the snapshot. Count refers to allocations, not containers, health checks or unique service consumers. Application HTTP/Consul health and functional tests were not exercised. Cause/date of Houston job disappearance is unknown; no restoration requested.

Comparison complete; no external mutations or remaining background operations. No new follow-up proposal or task was introduced, and existing backlog remains unchanged.

## Houston replacement clarification (November17)

User asked whether HoustonV2Mock replaces real Hub/classifier. Confirmed by fresh read-only Nomad job GETs for all12currentlyrunning monolith stands: test,test1–test7,test11–test14. Both `HoustonClassifierV2BaseUrl` and `HoustonHubV2Baseurl` target `http://v2.houston-classifier-mock.<stand>.vk-test.youdo.local` on every inspected stand. Sanitized allowlisted field evidence: `/home/slnnk/ai-data/devops-884/houston-consumer-endpoints.json`. No whole job/template/environment persisted.

Thus HoustonV2Mock replaces both real services for these test consumers, without a real Hub/classifier dependency. Prior comparison correctly reported missing real jobs but omitted their functional replacement and could misleadingly suggest missing test functionality. For DevOps-884 current shared test-application inventory, retain HoustonV2Mock and exclude the real Hub/classifier as unused by these consumers; preserve their historical recovery above.18currentlyobserved shared application jobs remain; there is no demonstrated Houston restoration gap. Mock is not full real-service parity: experiments are stored in memory, isolated by stand hostname and lost on restart; manual/API or autotest setup supplies them. Sources: [documented mock behavior](2026-10-16-nomad-test-houston-mock-experiment-setup.md) and [original dependency audit](2026-10-21-nomad-test-monolith-data-dependencies.md).

Factual clarification recorded in this task and existing system map; no new global policy, external action or backlog task. Verification complete; no background operations remain.

## Target dev Kubernetes inventory (user decision, November17)

User clarified that this list is the desired application inventory for the dev Kubernetes cluster under DevOps-884, rather than merely a historical/current Nomad inventory. User accepted the four additional shared applications and requested adding ai-qa. Real Houston Hub/classifier remain excluded because HoustonV2Mock supplies both test interfaces. The target is19services:

1. geocoder
2. youdo-call-service
3. youdo-business-doc-generator
4. chat-content
5. textvalidation
6. tinkoff-e2c-sign-service
7. DebuggingEvents
8. BlackListedEmailChecker (blec)
9. pechkin
10. mailer
11. HoustonV2Mock
12. daily-compilations
13. subcategory-predictor
14. youdo_recommendations_mock (recommendations-mock)
15. escrow-tinkoff-router
16. moderation-bert
17. taskqualitycontrol
18. userinsurance-gotenberg
19. ai-qa

This is task-scoped target selection, not evidence that all19services currently run in dev Kubernetes and not authorization for deployment, repository edits or external changes. ai-qa is included by explicit user request; no additional runtime check performed. Historical/live Nomad findings above remain dated evidence. Inventory update complete, no background operations; no additional implementation task proposed or started.

## YouTrack description updated (November17)

User explicitly requested adding the target list to the issue description, not a comment. Prepared `/home/slnnk/ai-data/devops-884/description-update-proposal.json`, preserving the original description and appending the19service dev Kubernetes target inventory plus Houston replacement clarification. Presented exact local proposal and operation scope; user replied `Да` to authorize this update.

Fresh GET verified issue DevOps-884/id71-138332 and original description unchanged. One POST updated only `description`. Independent GET verified exact full approved text, including all19services, original paragraph and Houston clarification. Receipt `/home/slnnk/ai-data/devops-884/description-update-receipt.json`, updated1794942017088. No comment created, status changed, deployment or additional external operation. Requested description update complete; no remaining session action items or background operations. Existing unrelated backlog unchanged.

## First ten service repository assessment requested (November17)

User selected the first ten services for read-only repository analysis. All target services must use permanent namespace dev and support deployment from MR and master pipelines, like ai-qa. This supersedes any earlier namespace selection for the DevOps-884 target; current runtime ai-qa still uses dev-ai-qa and was not moved. [Completed assessment and verified constraints](2026-11-17-dev-deployment-devops-884-first-ten-assessment.md). No implementation, issue-description update or deployment was requested in this turn.

## Existing CI modes retained (user correction, November17)

User selected retaining existing service deployment modes. Dev Helm job must be available in MR and existing release pipelines: semver tag for manual-mode services, master for auto mode. This supersedes the prior all-services-master target interpretation for DevOps-884. Existing .rules-prod-manual already supports the selected behavior. [Canonical decision](2026-11-17-dev-deployment-devops-884-first-ten-assessment.md#ci-mode-decision-user-correction-november17). Namespace dev remains selected; no implementation authorized.

## Target namespace changed to dev-single (November17)

User selected permanent namespace `dev-single` for DevOps-884 common services, superseding the prior `dev` target. The accepted19service inventory is unchanged. Existing Vault namespace pattern `dev-*` includes `dev-single`, so a role binding expansion for literal dev is no longer required. Existing CI modes remain selected. [Decision](2026-11-17-dev-deployment-devops-884-first-ten-assessment.md#namespace-decision-dev-single-user-correction-november17). No deployment or repository implementation requested/performed.
