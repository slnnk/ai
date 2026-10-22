---
system: nomad-test
status: verified
checked: 2026-10-21
tags: [kafka, zookeeper, kafka-rest, vk, ci]
---
# Full isolated Kafka job migration to VK

## Summary
MR3 merged with explicit user approval as 627242c9. Master pipeline141395 and staging3242525 succeeded; Nomad deployment9053c9ff successful, all three groups healthy, four tasks running with zero restarts. REST GET/brokers returns200 and broker1001; all four new Consul services passing. Existing KafkaVM10.18.26.5 remains passing and separate. Production3242526 remains manual. Predictor readiness remains a separate proposal.

## Task and authorization
User requested minimal changes to run full jobkafka in VK. Asked to resolve topology ambiguity because existing Kafka broker10.18.26.5 is healthy; user explicitly selected wholejob with separatebroker over REST-only reuse. User subsequently instructed `Не нужно проверять, пушь изменения и запускай через ci`, then required a different Nomadjobname to avoid an existingKafka conflict. This authorizes the scoped publication/CIwork and waives further local runtime checks for this Kafka task; global supervision/external merge restrictions remain unchanged. Do not generalize the waiver to other service tasks.

## Context and findings
Repository /home/slnnk/git/kafka, data/event-streaming/kafka project181, base/currentmaster0934474f2491df184c57c5ef4ee878dec6371142. Existing staleMR1 Deploy to yandex-test belongs to a different sourcebranch and was preserved. No task conflicts/unrelated local changes.

Project had sharedrunnersdisabled/noassignedrunners. No projectNomadvariable overrides; Data-group NOMAD_STAGE_ADDR/TOKEN match reviewedVKendpoint and existing .env VK_TEST_NOMAD_TOKEN. Project has deployment-only CI, no ownimagebuild/registry needed (registryAPI403 was irrelevant). Master-only jobs originally auto-staging thenauto-production. Four existing publicimages all available/linuxamd64/Dockermanifestv2: cp-zookeeper/cp-kafka/cp-kafka-rest5.2.1 and sheepkiller/kafka-managerlatest. No image versions/resources/storage policy changed.

## Changes
Published commitf175adc5fb6097461ef7ec06dc19c266ee6412a3 on DevOps-898-deploy-kafka-vk from0934474f. Only staging.nomad and .gitlab-ci.yml,7insertions/6deletions:
- Nomadjob kafka -> kafka-vk-test, datacenteryandex-test -> vk-test.
- New broker Consulname kafka-nomad, RESTbootstrap kafka-nomad.service.vk-test.consul:9092. Existing servicekafka onVM10.18.26.5 unchanged; new cluster deliberately separate/empty per user's topology choice.
- Kafka-manager route updated to currentTraefik rule and kafka-manager.vk-test.youdo.local.
- Staging command passes NOMAD_STAGE_ADDR/TOKEN explicitly as CLIflags, avoiding generic inherited Nomadtarget overrides.
- Productionjob manual, bounding requested automaticrun to VK; production.nomad and productioncredentials unchanged.

User explicitly requested pushing after scope discussion and waived checks. Prepared concrete proposal/body/snapshot, inspected full workingdiff, verifiedsnapshot beforestaging, inspected complete stageddiff and actualresultingcommit; clean worktree. Pushed sourcebranch. No application validation/CI lint added after waiver; publication review/readbacks are not runtime success claims.

## Local test attempt and cancellation
Before waiver, attempted isolated fullstack with originalmemorylimits in random localComposeproject codex-kafka-vk-0b20c423/internalnetwork; images pulled, command failed at RESTpublishedport lookup beforefunctionalchecks. No capturederrorlines, so no inferred rootcause/success. Scriptalreadyfinished when stoprequested; finallycleanup exit0 removed task-createdcontainers/network/anonymousvolumes. No further localtesting after explicitwaiver. Retainedlogs/receipts in /home/slnnk/ai-data/data-services-diagnosis/kafka-vk-local/. No VK cluster writes during this attempt.

## Publication and CI readiness
Created readyMR3 https://gitlab.youdo.sg/data/event-streaming/kafka/-/merge_requests/3, title DevOps-898 deploy isolated kafka job to vk, targetmaster. ExactRussianbody/DevOps898link, assigneea.solonenko, squashfalse, source-remove-on-mergefalse. Helper independently GETverified source/target/SHA/title/body/settings. Featurebranch has no matchingjobs under existingmaster-only rules, pipelinesemptyexpected. Publication bundle /home/slnnk/ai-data/gitlab-workflow/kafka-vk/kafka/.

To enable requested CIexecution, set project181shared_runners_enabled=true; independentGETverified, no otherprojectsettings changed. Receipt kafka-shared-runners-receipt.json. No sourcepipeline run attempted because existingrules requiremaster; do not manufacture a branch deploymentpath or push targetbranch.

Fresh mergepreflight: MR3opened/ready/mergeable/discussionsresolved, sourcef175adc5, targetmaster0934474f, source-removalfalse. Merge would trigger existingautomaticstaging to VKfulljob; production staysmanual. Separate explicit merge approval requested before merging. No merge, tag, pipelinePOST, remoteNomadjobrun or productionoperation performed. User's request to runCI is not treated as permission to bypass explicit merge gate.

## Status and risks
Deployment complete through CI after explicit user merge/deployment approval. No further local tests after waiver. Observed Nomad and Consul health plus REST broker metadata; no event production or application prediction requests performed. Predictor telemetry recovery has not been independently confirmed; its earlier contract readiness failure is separate and remains a proposal in central TODO.

## Related evidence
[Predictor dependency diagnosis](2026-10-21-nomad-test-subcategory-readiness-kafka-rest.md).

## Portable lesson
none

## Approved merge and deployment outcome
User answered yes to the concrete merge/MR3 and automaticVKdeployment proposal. Merge PUT pinned sourceSHAf175adc5; independent GET verified merged, mergecommit627242c9be004fe876f20aa32b0992500e0c1ca6, at2026-10-21T18:45:16+03:00. Receipt kafka-mr3-merge-receipt.json. Masterpipeline141395 SUCCESS, staging3242525 SUCCESS, production3242526 MANUAL (not played). Nomaddeployment9053c9ff-35d2-c04e-64b7-30c9dca4f562 SUCCESS: all three groups HealthyAllocs1/DesiredTotal1. Allocations3a58660b REST,57509204 manager,a3a65769 broker/ZK all running, all four tasks restart0. Consul kafka-nomad10.18.26.21:9092, zookeeper10.18.26.21:2181, kafka-rest10.18.26.34:8082, kafka-manager10.18.26.30:20134 all checks passing. REST GET/brokers HTTP200 with brokers[1001]. Existing kafka remains10.18.26.5:9092 passing. Snapshots kafka-ci-status.json and kafka-vk-services.json under ai-data/data-services-diagnosis. No production operation, topic/event write or predictor retry.
