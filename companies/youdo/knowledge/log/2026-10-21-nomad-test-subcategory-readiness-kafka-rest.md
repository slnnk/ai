---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [subcategory-predictor, kafka-rest, eventum, readiness]
---
# Subcategory rollout readiness race and missing Kafka REST

## Task
User reported errors and still-running deployment in VK Nomad predictor, then suggested data/event-streaming/kafka/staging.nomad as a missing dependency. Continue read-only diagnosis of release1.0.8/pipeline141391; no new deployment/source change requested by the hypothesis alone.

## Context
MR22 user-merged11909b42/release1.0.8. Build/test/lints/release and staging3242500 SUCCESS. Current final pipeline141391 FAILED because contract3242501FAILED; load3242502SUCCESS by exitcode but with non-success HTTP responses; production3242503SKIPPED. Predictor task is running on agent06 with0restarts; HTTPhealth200 and Consulpassing verified. Logs were filtered to infrastructure errors and model-init timestamps, without request/user payload fields.

## Findings
Three distinct observations must not be conflated:

1. Missing telemetry dependency: stderr repeats DNS `Domain name not found` / aiohttp ClientConnectorError to kafka-rest.service.consul:8082, invoked by eventum producer. In sampled64KB tail,20connector error traces. No processrestart or modelstartupfailure observed. Predictor starts Eventum producer only after loading models; telemetry delivery remains broken without REST proxy.
2. Premature contract test: Dredd3242501 sent2POST/prediction requests at15:06:11UTC and received proxy404text/plain, expected200/400JSON. Service startup log15:05:33.928, preprocessor loading15:05:33.929, root/category models still loading15:06:16–15:06:26, Eventum producer start15:06:27.269. Therefore contract test ran before app/model initialization finished. Correct configured host v1.subcategory-predictor.vk-test.youdo.local is in actual Dreddcommand; source route POST/prediction exists. Add a bounded HTTPhealth-ready barrier before postdeploytests as a proposal; do not skip tests or infer these404are caused by Kafka.
3. Nomad rollout progress was expected health gating: actual MinHealthyTime300000000000ns(5min), firsttaskstarted15:05:32.918UTC, initialdeployment5668cfca healthycount0 while running. Later freshGET confirms successful/HealthyAllocs1/DesiredTotal1/Unhealthy0; no promotion needed, DesiredCanaries0 for initialdeployment. User's UI-running observation was real at that time, now superseded by successful Nomad rollout. A successful CIstagingjob had returned earlier and did not provide sufficient HTTPreadiness barrier.

Load3242502 ran120requests/30.01s,104non2xx/3xx; wrk jobexit0 is not a passing API outcome. Later prediction requests reached app and triggered Eventum DNS errors. Precise time distribution of those104responses was not reconstructed; this supports a readiness concern without treating loadjobSUCCESS as functional acceptance.

## Kafka file and existing broker
Read-only clone /home/slnnk/git/kafka from data/event-streaming/kafka currentmaster0934474f2491df184c57c5ef4ee878dec6371142. User-linked staging.nomad indeed includes kafka-rest group (confluentinc/cp-kafka-rest5.2.1,static8082), plus ZooKeeper+Kafka and kafka-manager. File targets old yandex-test; CI master automatically stages thenproduction. No files edited and no jobs played.

Fresh VKinventory: Consul already has service kafka at nodevk-ms1-kafka-test01/10.18.26.5:9092, serf/alive checksPASS and workstation TCPconnectPASS. No kafka-rest registration. No ZooKeeper registration in filteredcatalog. Nomad contains kafka-schema-registry job; broker itself is not a job namedkafka in this cluster, consistent with existing dedicated VM. Thus missing component is REST proxy rather than evidence that an entire new broker stack is required. Do not redeploy full legacy staging job blindly: it would add another Kafka/ZooKeeper/manager and targets the wrong DC. Broker version/protocol compatibility and exact REST-only delivery plan remain to be established before proposing execution.

Existing Kafka addressbook entry already matches10.18.26.5 and kafka.service.vk-test.consul:9092; no new address added or changed. User instruction to investigate this file does not authorize infra mutation, pipeline run, topic writes or storage recreation.

## Evidence
- /home/slnnk/ai-data/data-services-diagnosis/subcategory-runtime-log-summary.json
- subcategory-vk-acceptance.json, subcategory-release-status.json
- vk-kafka-existing-service.json
- GitLab contract3242501 and load3242502 traces inspected in memory, filtered results above.

## Changes and status
KB bookkeeping and repository clone/catalog only. Predictor rollout is running/healthy and Nomad deployment successful, but end-to-end release acceptance remains incomplete due to missing telemetry REST dependency and prematurely run contract tests. Production was not deployed by this failed pipeline. Next proposed work is prepare RESTproxy reuse of existing broker and bounded postdeployment readiness; source/deploy approvals remain required. Central TODO tracks remaining actions; other three missing Data targets remain proposals.

## Related evidence
[Subcategory CI recovery](2026-10-21-nomad-test-subcategory-predictor-vk.md).

## Portable lesson
none

## User chose full separate Kafka job (2026-10-21)

After REST-only reuse was recommended, user explicitly selected the full existingjob with a separatebroker. The REST-only reuse recommendation above is superseded as execution scope. FullVKjob kafka-vk-test with brokerConsulnamekafka-nomad is published in [KafkaMR3preparation](2026-10-21-nomad-test-kafka-vk-full-job.md); oldVMbroker remainsseparate. Userwaived further localKafka checks/requestedpush andCI. ActualCIexecutionawaits separateMRmergeapproval. PredictorCIreadinessproposal remains open and was not implemented in this Kafka change.

## Subsequent dependency restoration
User approved full isolatedKafka MR3 merge,627242c9/masterpipeline141395, staging3242525SUCCESS. Nomadkafka-vk-test successful/allgroupshealthy/zero taskrestarts; Consulkafka-restpassing at10.18.26.34:8082 and GET/brokers200[1001]. Separate kafka-nomad broker10.18.26.21:9092, existing kafkaVM10.18.26.5 unchanged/passing. This supersedes the earlier missingREST observation; predictor telemetry recovery not independently verified and earlier contract readinessrace remains a separateproposal. No predictor retry or productionoperation. [Kafka outcome](2026-10-21-nomad-test-kafka-vk-full-job.md).

## Later test retry outcome
User reported successful tests; fresh GitLab GET confirms test:contract3242527 SUCCESS and test:load3242528 SUCCESS in releasepipeline141391. Pipeline is running because production deploy:service3242503 started automatically after tests. No agent retry or production mutation. Earlier failed attempts remain historical evidence; a readiness barrier is an optional improvement, not a current blocker. Remaining unrestored monolith dependencies from the audit: data/price-predictor, data/customer-task-recommendations, sysadmins/taskqualitycontrolfortest. Only taskqualitycontrol has direct missing-route evidence in Jenkins2020 among these three (8 final failedtests).
