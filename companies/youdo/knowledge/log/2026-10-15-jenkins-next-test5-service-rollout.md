---
system: jenkins
status: verified
checked: 2026-10-20
tags: [recovery, gitlab-ci, ansible, deploy]
---
# Next test5 rollout excluding Cerberus2

## Summary

User authorized executing the next iteration except Cerberus2. Seven Nomad targets remain: broadcast, featuretoggle, youdo.content, youdo.landings, youdo.trackingpixel, YouDo.Socket, youdo.help; separate moderation build/S3 publication is tracked explicitly. Cerberus excluded from build/deploy sources. Seven selected Nomad services are deployed to test5 with expected source/version confirmed via BuildAPI; moderation S3 publication also completed. Content2.5.13 fixes missing CI credential aliases; trackingpixel historical packages restored without source changes; Broadcast integrations passed after targeted local PostgreSQL image publication. Historical UI limitations were observed for Landings (no healthcheck/HTML row) and Socket (version cell alias). The user closed the Socket UI mapping follow-up as unnecessary on 2026-10-20; no fix or new live verification was performed.

## Approvals and scope

User explicitly confirmed Content branch DevOps-899-deploy-content-on-vk from current origin/master02abe198. Then approved actual one-file +23/-9 diff, commit deploy content on vk test stands, MR DevOps-899 deploy content on vk test stands, source→master, merge, release2.5.12 at resulting master, rebuild and test5 deploy. Other six fresh builds/deploys were authorized by the user's all-except-Cerberus instruction. Existing user instruction accepts normal database creation/recreation for first deployments; no one-off skipdropdb variables will be injected. MiniSape, WalletOne, Form and B2B remain excluded.

Moderation publication replaces the entire youdo-static-test/test5 S3 prefix and updates shared fonts plus manifest/Consul; exact destructive effects require the final reviewed publishing approval before playing that job. Only its build pipeline is launched at this checkpoint.

## Content implementation and training

Only .gitlab-ci.yml changed, +23/-9: custom Nomad/DC/domain/Consul/BuildAPI target VK; use child DEPLOY_NOMAD_ADDRESS/TOKEN and existing group CONSUL_TOKEN_VK_TEST. Keep Levant/Vault/libvips template unchanged, preserve public-test flow, production rules and allow_failure. Existing versionPUT uses APP_IMAGE_TAG in VK; new job URL/catalog POSTs provide Jenkins metadata. No new secret variables created and no secret values recorded. Complete staged diff inspected and only agent taskpath committed.

YAML, extracted Bash syntax, diff-check passed. GitLab CI Lint releasecontext validtrue, errors/warningsnone,31jobs. Commitd348955ac77af3c4823fed45543688aa35c11c83 pushed to approved branch. MR body is one short Russian paragraph about VK deployment/BuildAPI plus DevOps-899 link, matching approved convention. MR[!63](https://gitlab.youdo.sg/youdo/microservices/youdo.content/-/merge_requests/63) created with project squash=true preserved, then merged as9714ed52108b206eb94866038b44db8301e2f407 (squash94709a1781d501aed70c09e8a18d0d55b13bf98b). Approved tag2.5.12 created at exactly that current master; automatic pipeline140980 reused, no duplicate pipeline POST.

## Rebuild sources and pipeline receipts

| Service | Release | Pipeline |
| --- | --- | --- |
| broadcast | 1.2.11 | 140972 |
| featuretoggle | 1.0.11 | 140973 |
| youdo.landings | 1.3.35 | 140974 |
| youdo.trackingpixel | 1.0.5 | 140975 |
| YouDo.Socket | 1.2.9 | 140976 |
| youdo.help | 1.0.14 | 140977 |
| youdo.moderation (S3 assets) | 1.0.45 | 140978 |

Each ref's exact SHA was checked against live GitLab before pipeline creation; mutation intents and pipeline receipts are saved. Normal production jobs remain manual. Content release build will also update its latest image as reviewed.

## Artifacts and limits

/home/slnnk/ai-data/jenkins-recovery/next-test5-rollout/ contains sources.json, receipt-backed rollout.py, build-intent/build/status/watch files and Content MR body. Source analysis and CI-lint receipts remain in monolith-services-audit/. Live next steps tracked in ~/ai/TODO.md. No unrelated checkout edits were changed; all19existing Ansible dirty/untracked paths remain outside this task.

## Runner queue investigation

All eight eligible docker/dind slots across runners105/106 are occupied by pre-existing unrelated deployment jobs, mostly test4. Six verified jobs (Fns, docvalidation, attribution, bruteforcingdetector, antifraud2, userinsurance) currently end at PostgreSQL Recreatingdb task for docker:test4. Fresh test5 pipelines have .pre pending with no runner assigned; no build failures have occurred yet. No unrelated jobs were cancelled or runner capacities altered. Read-only PG wait investigation is underway.

Moderation S3 inspection refined ownership: direct collision with monolith static is not proven (SSR uses youdo-ssr-test), but publication still recursively replaces its test5prefix and writes global fonts. Anonymous S3 listing denied403, no data copied. Exact publishing-effects approval remains pending until build ready.

## PostgreSQL pager root cause and approved fix

Read-only process inspection on10.18.26.39 proved all seven stalled test4 chains sshd→sudo→psql→pager, 13-16minutes, with psql waiting for pager and no active SQL. The raw/become path allocates TTY and enables the interactive pager. Current dynamicinventory test4_postgres/test5_postgres both resolve to10.18.26.39.

User explicitly approved cancellation of test4jobs223/3227430,320/3227573,300/3227681,244/3227502,359/3227608,340/3227644,384/3228067. Root sent exactly those cancel requests; initially canceling. Separate B2Bmonitoring423/3227851 was untouched. Slots freed and new builds began. No direct remote processes/PGbackends were killed.

User approved reuse AnsiblebranchDevOps-899-fix-microservice-postgres-auth fromcurrentmaster342b1d5, then actual +4/-4 diff/publication/merge. Only five psql invocations in four raw tasks gained -P pager=off; SQL, flags, loops and tags unchanged. YAML/exactsemanticcomparison/diffcheck passed; real SSH TTY read-only SELECT of200rows completedrc0 in1.27s. All19pre-existing foreignfile hashes preserved.

Commitcfb5aacec2c324554592b0bef3e477b45aa356d9, Ansible[MR!112](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/112), merged620607f1a75b47a32660462532e906b8ce53516a. Commit/MRsubject disable postgres pager in microservice deploys; shortRussianparagraph+DevOps-899link only, projectsettingspreserved. New service jobs clone this currentmaster. Reusable diagnosis: [psql pager under raw/become](../../../../general/knowledge/ansible/psql-pager-with-raw-become.md).

## First execution checkpoint

Socket build succeeded; approved first test5 deploy3228384 played. Trackingpixel prepare-nuget3228339 failed and is being diagnosed. Other builds continue; Content140980 still queued at lastsnapshot. No deployment acceptance claimed yet.

## Socket acceptance and dependency recovery steering

Socket deploy3228384 SUCCESS; two expected socketChat-test5 allocations healthy with0restarts and Consul passing. BuildAPI saved metadata matches pipeline140976/release1.2.9/source/deployjob; live VersionCompatible1.2.9 confirmed (custom template has VERSION but no IMAGE_TAG). HTML socketchat row exists. Existing BuildAPI UI cannot map project nameYouDo.Socket to consul name socketchat, so its rendered version cell stays blank despite correct live API; an optional UI mapping follow-up was recorded rather than changing unrelated application metadata. On 2026-10-20, the user closed this follow-up as unnecessary. The central TODO is closed without implementation; the historical finding is retained, with no new live verification.

Trackingpixel prepare-nuget3228339 failed NU1605: direct DI.Abstractions6.0.0 in net6 migration project versus resolved Common0.5.0 requiring8.0.1. Initial one-line8.0.1 bump was proposed but NOT approved; user asked what was wrong with existing version. Root corrected diagnosis: historical Common0.4.1 and Common/Logging/Metrics/Tracing0.3.1 are missing from restored Nexus, causing NuGet fallback to0.5.0. Existing6.0.0 is valid for the intended historical graph. User then asked whether internal Common0.4.1 can be rebuilt; root proceeds with local historical package reconstruction, preserving application source and version pin. No trackingpixel branch was created and no source edits made.

Internal source project487 youdo/Lib/youdo.servicecore, existing proven historical sources031 at5f3dadb3e58deb866d0bd520811a8fb6782d9db4 and041 at776173d5c407cd4533fb70e776c8448d83503ad8 under ai-data/nexus-recovery/servicecore-031-build/source and corresponding041. Prior recovery published Application/Configuration only, leaving these transitive dependencies missing. Existing SDK6cached and recoveryhelpers support local pack; exact five-package publication awaits prepared artifact review/approval.

Landings/Help/moderation still downloading base Node images with no npm execution; DockerHub download/network investigation is read-only. No retries/restarts or registry proxy changes were applied.

## Approved historical NuGet publication and rollout progress

User explicitly approved publishing five reconstructed packages and retrying failed trackingpixel prepare-nuget, preserving DI6.0.0 and application sources. Existing publish_library_batch.py validated reviewed manifest servicecore-missing-five-ready.json and published Common0.3.1/0.4.1, Logging/Metrics/Tracing0.3.1. All five public Nexus metadata endpoints HTTP200; publisher rc0. No package downloads used for verification. Exact project516/job3228339 retry created3228514 after pipeline140975/sourceSHA validation; receipt prevents duplicate writes. Historical source and dependencies retained; no application repository edit or release tag needed.

Featuretoggle deploy3228290 SUCCESS; BuildAPI saved metadata/live source/version1.0.11/HTML row all match. Help image build succeeded and approved deploy3228412 started. Content unit tests and all pre-jobs succeeded, build-api3228487 running. Broadcast integration test3228248 failed; gating/root cause is under read-only investigation.

Runner image diagnosis: host Docker and DinD use mirror.gcr.io; active layer files grew at27-36KB/s, one completed normally. No429, timeout or download-retry errors found; DNS/TLS work. Slow download through Google mirror is observed, underlying bottleneck unknown. Help advanced to successful Next.js image build. Do not restart active jobs or alter mirrors on this evidence.

## Broadcast PostgreSQL image recovery

Broadcast integrationjob3228248 failed before tests with runner_system_failure: registry.youdo.sg/youdo/devdocker/postgres:latest manifest unknown; allow_failure=false gates deploy3228256. All three Broadcast component images subsequently built successfully. Exact producer is devdocker project63, master8c8dde3e, postgres/Dockerfile based on postgres:10 with ru_RU.UTF-8 locale. User independently restarted master_build3228515; observed running. This job publishes six devdocker images; agent did not restart it or change source. Read-only monitoring requested; separate explicit approval requested before retrying failed Broadcast integration job after PostgreSQL image publication.

Help deploy3228412 SUCCESS and BuildAPI metadata/live/HTML verified for1.0.14. Trackingpixel restored all4projects with NU1603=0/NU1605=0, unit tests passed, three image builds continue.

## Latest deployment outcomes

User approved conditional retry Broadcast integrationjob3228248 after PostgreSQL image publication. User explicitly approved Moderation job3228437 S3 prefix replacement/shared fonts/manifest effects; root played it once, currently running.

Landings deploy3228320 SUCCESS; BuildAPI metadata/live1.3.35 match. HTML row absent: existing webEx_check=false omits health checks; BuildAPI HTML enumerates Consul checks rather than all services. No source change made.

Content image2.5.12 built; approved deploy3228496 failed at Nomad job submission with403 Permission denied before BuildAPI publication. Read-only ACL/token diagnosis ongoing; no retry yet. Trackingpixel worker/webapp built, migrations still building.

## Devdocker internal CI images (approved implementation)

User requested devdocker use base-images to reduce external downloads. Approved branch DevOps-899-use-internal-docker-images from fresh origin/master8c8dde3. Actual .gitlab-ci.yml +3/-2 only: docker:latest -> registry.youdo.sg/youdo/base-images/docker:git; service docker:dind -> registry.youdo.sg/youdo/base-images/docker:dind with explicit alias docker. Both client/server20.10.17, registry manifestsHTTP200. Runtime Dockerfiles unchanged, especially PostgreSQL10/ru_RU locale (base-images PostgreSQL16 is incompatible as a direct replacement).

YAML semantic comparison preserved all scripts/rules, diff-check and GitLab CI Lint(master simulation) passed valid=true/noerrors/nowarnings. Actual staged diff inspected, sole path.gitlab-ci.yml. User approved publication/merge and automatic rebuild/push of six existing latest images. Commit3c231dfc17d7a9008c66e25aede5c8506f2004c7, MR[!55](https://gitlab.youdo.sg/youdo/devdocker/-/merge_requests/55), merge1f0c0d5eda479a0e05d9d3fc9653d81dff252c33. Project default_off squash preserved; short Russian MR paragraph plus DevOps-899 link. Old user-started job3228515 unchanged. New automatic master pipeline to be adopted by exact mergeSHA, not created again.

Content2line correction approved for publication/merge/release/deploy: commit0e13307, MR[!64](https://gitlab.youdo.sg/youdo/microservices/youdo.content/-/merge_requests/64), merged344f69e5f9957ebb49dc14ca4c25a79e9613a7a4. Tag2.5.13 at mergedmaster, automatic pipeline140983 adopted. Prior2.5.12 receipts archived, active sources updated. No missing intermediate DEPLOY_NOMAD variables remain in custom Content deployment.

Moderation job3228437 SUCCESS. S3 manifestHTTP200, one referenced assetHEAD200(length425447), Consul markerHTTP200/version3228437. Trackingpixel all three images+tests successful, approved deploy3228352 launched.

## Local PostgreSQL image recovery and Content acceptance

User explicitly requested local build and registry push of missing devdocker PostgreSQL image to unblock Broadcast. Existing clean checkout postgres/Dockerfile unchanged (blobbe15955ee7babf4853d7367d5545f3ccf7ca6e08): FROMpostgres:10 and ru_RU.UTF-8 localedef. Local Docker buildlinux/amd64 completed~15seconds; PG_VERSION10.21-1.pgdg90+1, LANGru_RU.utf8. Push succeeded for registry.youdo.sg/youdo/devdocker/postgres:latest, digestsha256:8b9bcb6701e75ce1b0d8d9b935d7c90e0d44df59b3abf7cdddd74c9cd5dc90f1. Credentials used in-memory via Docker API, not saved. Receiptlocal-postgres-push899.json. Remote metadata verification and already-approved Broadcast integration retry delegated.

Content2.5.13 deploy3228570 SUCCESS77.6seconds; BuildAPI metadata/live/HTML all accepted, correctpipeline140983/SHA344f69e5. Nomadyoudo-content-test5 running, healthy1/unhealthy0, APIrestarts0. Original403resolved. Trackingpixel1.0.5 deploy3228352SUCCESS101seconds, BuildAPI metadata/live/HTML accepted. Only Broadcast remains for this iteration.

## Broadcast final deployment

Remote PostgreSQL registry digest matched the locally pushed image. User-approved exact integration retry3228248 ->3228590 completedSUCCESS79.7seconds,8tests passed,0failed. Root played already-approved first test5deploy3228256 (pipeline140972, release1.2.11, SHA04291f24e8452c99ab7bedb15f346ea081e3fa36). BuildAPI final metadata/liveNomad/HTML allmatch/accepted=true; deploy3228256 SUCCESS86.31seconds. Nomad allocationb5215346 running/healthy, API+scheduler running0restarts, migrations completedwithoutfailure, Consul checks passing. Entire selected iteration accepted; artifactsbroadcast-runtime-acceptance899.json andbroadcast-deploy899-status.json.
