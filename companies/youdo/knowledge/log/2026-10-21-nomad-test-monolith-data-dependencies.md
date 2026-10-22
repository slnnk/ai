---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [data, monolith, dependency-audit]
---
# Monolith Data dependencies on VK test stands

## Task
Identify additional dependencies of test-stand monoliths on Data services after restoring daily-compilations. Investigation only; no restoration or deployment requested.

## Context
Inspected existing local monolith abc9c7ae1a5 and automation-test-yandex d26e37e without switching/fetching/editing, together with fresh GitLab Data group project inventory and live VK Nomad/Consul GETs. Source examples can lag remote master; deployed Nomad environment templates are the current configuration evidence. Enumerated11running monolith jobs: test,test1,test2,test3,test4,test5,test6,test7,test11,test12,test13. Other stands were not running monolith jobs in this snapshot and are not covered by the current-runtime claim. Read one environment template per monolith, without exporting full secret-bearing templates.

## Findings
All11examined monoliths have identical shared endpoint addresses for the following dependencies. Code config fields have registered clients and concrete call sites, so these are functional dependencies for relevant scenarios; no claim that every dependency is required for startup or that every feature is enabled.

| Dependency | Monolith usage / configured target | Current VK observation |
| --- | --- | --- |
| data/price-predictor | AiServices.SuggestedTaskPriceApiEndpointUrl, v1.price-predictor.vk-test.youdo.local/prediction; AiTaskPriceHttpClient | No matching job/catalog service; GET /health404 |
| data/subcategory-predictor | AiServices.TasksCategorizerServiceUrl, v1.subcategory-predictor.vk-test.youdo.local; IAiTasksCategorizerClient POST /prediction | No matching job/catalog service; GET /health404 |
| data/customer-task-recommendations | CustomerTaskRecommendations.Endpoint, customer-task-recommendations.vk-test.youdo.local; CustomerTaskRecommendationsManager uses typed client | No matching job/catalog service; GET /v1/healthz404 |
| Task quality control | AiServices.TaskQualityControlApiEndpointUrl, taskqualitycontrol.vk-test.youdo.local; TaskQualityControlModule client | No matching job/catalog service; root GET404; test target intended sysadmins/taskqualitycontrolfortest rather than real data/task-quality-control |
| Task/executor recommendations and similar tasks | RecommendedTasksApiEndpointUrl, RecommendedTasksV2ApiEndpointUrl, RecommendedExecutorsApiEndpointUrlV2, SimilarTasksApiEndpointUrl all target recommendations-mock.vk-test.youdo.local with different paths | No matching job/catalog service; root GET404. Expected sysadmins/youdo_recommendations_mock supplies test responses instead of real recommendation services/generators. Default source config also names data/recommended-tasks and rowers-ranker; runtime explicitly overrides them to mock |
| Houston A/B hub/classifier | HoustonClassifierV2BaseUrl and HoustonHubV2Baseurl point to v2.houston-classifier-mock.<stand>.vk-test.youdo.local | Shared HoustonV2Mock job/catalog entry present; test5 GET /experiments200. Swagger/index and root404 are wrong-route probes, not service failure |
| data/daily-compilations | DailyCompilationsEndpointUrl, v1.daily-compilations.vk-test.youdo.local | Restored0.5.15, GET /health200; detailed rollout evidence in prior note |
| data/eventum | Eventum.Endpoint v1.eventum.vk-test.youdo.local; EventumManager sends events only when Enabled | Effective deployed Enabled is string false on all11stands. GET /health404, but this integration is currently disabled. nomad_environment.json.j2 overrides earlier environment template/default settings |

Checked Data group membership rather than treating all adjacent services as Data. BLEC is youdo/BlackListedEmailChecker, subcat-recomm-abtest is youdo/microservices/subcategoriesrecommendationabtest, recommendations/task-quality mocks are sysadmins projects. Those are adjacent test dependencies, not additional real Data services. Existing monolith antifraud2/attribution are not equated with the separate data/antifraud project.

Source anchors: YouDo.Configuration/Environment/Services/AiServicesConfig.cs; YouDo.Managers/IocModule.cs around800,830,1154,1189; TaskQualityControlModule.cs; Ai/Recommendations/AiRecommendationsService.cs and AiTaskPriceHttpClient.cs; Tasks/CustomerTaskRecommendationsManager.cs; Eventum/EventumManager.cs. Nomad staging specs define /health for price/subcategory and /v1/healthz for customer-task-recommendations. Mock app root exists in source, so missing root404 plus absent registration supports unavailable route conclusion. No prediction/classification POST or application mutation executed.

## Actions and evidence
Generated sanitized inventories /home/slnnk/ai-data/data-services-diagnosis/data-dependencies.json and data-dependency-health.json. HTTP checks performed from the workstation via corporate access, not within monolith containers. Exact application payloads and feature behavior were not exercised; response404 and inventory absence establish missing configured routes, not model/data readiness. Services could have additional indirect database/queue dependencies outside this HTTP inventory.

During template inspection an inline Consul token field was exposed from automation-test-yandex/playbooks/deploy/app/roles/app_deploy/templates/nomad_environment.json.j2, Services.Consul.Token. No value retained here; validity/scope unverified. Separate review proposal recorded under Security.

## Changes
KB note, existing system map/repository catalog and central TODO proposals only. No source edits, external settings changes, CI/deployment, prediction/event writes or SQL writes.

## Status and risks
Inventory complete for11currentlyrunning monolith stands. Five missing configured targets identified: three real Data API projects plus recommendation and task-quality mocks. A shared instance per configured address is the apparent existing topology; no per-stand replication proposed. Optional restoration remains a proposal in central TODO, not permission to execute. Healthy Houston mock and disabled Eventum do not require replacement by real Data services for current test configuration. Generators are separate background producers, not these synchronous API dependencies.

## Related evidence
[Daily-compilations restoration](2026-10-21-nomad-test-daily-compilations-missing.md).

## Portable lesson
none

## Subsequent restoration status
By the later2026-10-21 snapshot, daily-compilations and recommendations-mock restored/accepted; subcategory-predictor VK healthy and retrycontract3242527/load3242528 SUCCESS in pipeline141391. Full isolatedKafka job deployed successfully via pipeline141395. Remaining three configured missing targets from the original audit: price-predictor, customer-task-recommendations and taskqualitycontrol (sysadmins/taskqualitycontrolfortest). These have not been re-probed in this status-answer turn. Taskqualitycontrol is directly demonstrated by8Jenkins2020failures; other two are configuration dependencies without direct error evidence in that build.
