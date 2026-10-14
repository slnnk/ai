---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, vk-cloud, gitlab-ci, recovery]
---
# DevOps-898 VK single dynamic implementation and rollout

## Summary

The final user-approved VK launch target is complete: ten single services and LogReader test5 are deployed through GitLab and runtime-verified. Socket per-stand CI was restored through merged MR !82; vks-policy-generator was excluded as unused and MR !18 closed without merge or a new tag. Public-test remains unchanged. Full sixteen-stand LogReader acceptance remains dependent on the other fifteen SQL endpoints; YouTrack closure was not performed.

## Context

11single+2dynamic services; update internal-test shared templates, Socket dynamic CI mode, DebuggingEvents routing/logging SQL and textvalidation logging SQL. Additional runtime prerequisites: Nexus auth/app image builds, RabbitMQ, SQL consumer configs and missing stand SQL readiness. Do not reopen accepted test5MSSQL producer recovery. Do not change unrelated source, production or public-test.

## Actions and commands

Ran ai-sync (no output/reminders). Read plan/context/backlog and existing repo metadata. git status shows four clean checkouts (gitlab-ci-templates, YouDo.Socket, DebuggingEvents, textvalidation); automation-services contains unrelated Jenkins/runner/Terraform changes preserved. Read-only fetch origin master completed for all4repositories after sandbox DNS failure/escalation. Proposed branches await approval: gitlab-ci-templates DevOps-898-deploy-single-dynamic-on-vk; Socket/DebuggingEvents/textvalidation DevOps-898-restore-test-service-on-vk, each from refreshed origin/master.

## Findings and rulings

Ruling: dynamic stand list is in v3/.deploy-test-dynamic.yml, not v3/.main-vars.yml as initial plan said; correct only actual owning file. Two shared files sufficient. Public-test stand list is independent and its active blocks remain byte-identical.

Existing common Nexus Docker-auth patch is already in automation-services local branch DevOps-890-nexus-docker-auth/MR1371, absent current master. Reuse existing reviewed role source rather than duplicate3filechanges or host overrides. Scoped temporary role/playbook outside repo passed syntax and --check on8clients. User explicitly approved Docker auth apply; run.py --apply completed with8hosts changed1each, failed0/unreachable0. Post-apply SSH GET verifies Nexus authenticated HTTP200 on8/8hosts; both registry.youdo.sg and nexus.youdo.com auth entries exist, mode0640. No Nomad restart. Evidence /home/slnnk/ai-data/DevOps-898/auth-runtime/verification.json. Default/password injection route is NEXUS_DOCKER_PASSWORD from current/.env, old registry password from Vault secret/ansible/yandex key nomad_client_docker_pass; no secret literals.

RabbitMQ VK host10.18.26.7 is empty (no nativeunit/containers/images/volumes/Mnesia/additionaldisks). User clarified that RabbitMQ is on the new machine but login must be old: preserve existing Vault credentials, not invent credentials; do not insist on old datastore recovery based on earlier ambiguous wording. Minimal isolated Docker broker bootstrap prepared outside repo at /home/slnnk/ai-data/DevOps-898/rabbitmq-runtime/deploy.yml. Uses official rabbitmq:3.8.34-management, manifestGET200/amd64 available; standalone existing role snapshot without DNScluster/sharedcookie tasks. Existing Vault USER/PASSWORD preserved; expected16testvhosts plus default/. No Kafka, Consul registration or VaultADDR changes bundled. Python/syntaxchecks and --check pass (ok11, changed7simulated, failed0/unreachable0), with no container/handler/vhost execution in checkmode. verify.py prepared for originallogin+17vhosts/perms after start; no secret output. Exact future approval command: ansible-playbook -i /home/slnnk/ai-data/DevOps-898/rabbitmq-runtime/inventory.ini /home/slnnk/ai-data/DevOps-898/rabbitmq-runtime/deploy.yml. Runtime approval pending; no broker mutation yet. Source and target logs preserve decisions/approvals as they arrive.

## Changes and approvals

Approvals: user replied yes to both four named repository task branches and RabbitMQ bootstrap; branches created from refreshedorigin/master. User explicitly approved the separate Docker-auth action via async reply; completed and read-only verified. Runtime bootstrap of RabbitMQ and target Vault address updates remain pending separate approval. User clarified RabbitMQ access data must use the old login/password on the new VM.

Local bookkeeping and fetched refs only; branch proposal pending. User-approved shared-host write was only Docker auth on8clients; no commit/push/MR, RabbitMQ change, service restart or CI trigger performed. Secret values never written to evidence/notes. Live work tracked in ~/ai/TODO.md only.

## Portable lesson

none

## Approved actions and implementation results

User yes approved4branches/localedits and Rabbitbootstrap. Created gitlab-ci-templates DevOps-898-deploy-single-dynamic-on-vk from6d9b695; Socket/Debug/textvalidation DevOps-898-restore-test-service-on-vk frombd5d894/2419b433/9314da1. Exactly5fileschanged:2shareddeployYAMLs,SocketCI,Debug/textvalidationtestHCL. No staged changes/commits/publication yet.

Rabbit bootstrap completed approved playbook withok16changed10failed0/unreachable0; originalVaultloginHTTPtrue,17expectedvhosts present,allpermissions present,version3.8.34. User separately approved Consulregistration byname rabbitmq; agent10.18.26.7 port5672 registeredwithTCPcheck, centralhealth2passing,DNS10.18.26.7. User separately approved VK Vaultupdates: only rabbitmqADDR/postgresADDR/mssqlLOGREADER_CONN_STRING addresses changed; restfieldsbyte-equalverified. ActualLOGREADERconnectioncredentials SELECT1passed againsttest5YouDoLogsExceptions before change. No password/user/database change.

Independentreview found importantSocketpublic-testregression: globaldynamicmode enablednewNomadpublicjob anddisabledoldAnsiblepublicjob. Corrected localSocketrules to preservelegacypublicmanualgates anddisabledynamicpublicjob. FiveapprovedGitLabCIlint/dry-runPOSTs passedvalidtrue/errors0/warnings0; Socketcompiledpublicjobset matchesbaseline. No pipelinescreatedbylint. Sharedpublicblocks byte-identical. LocalNomad1.3.5validate3HCLs passed withdrivercheckunavailable; in-memoryspecoutput VKDC/route checks pass,Socket32groupsfor16stands. Target1.5.3driververificationandappdeployment remain later steps.

Publication bundlepreparedai-data/DevOps-898/publication/manifest.json withexactpaths,filehashes,commit/MRtitles/source/targetandRussianoneparagraph+issuelinkbodies. No secretvaluesstored. Sharedincludesunpinned;13rootCIconsumersverified,globalcode-searchAPIunsupportedsoadditionalconsumerinventorylimitretained. PublicationcanstartMRprepare/buildpipelines; test/proddeployjobsmanual, no merge/deployauthorizedbypublication.

## Publication, merge and build preparation

User explicitly approved4MRpublication(bundlecommits/push/create), then separately approved4merges. Publishedcommits: templates3e748e32/MR88;Socket3b5a2a2b/MR81;Debug6d70daed/MR8;textvalidation4cf19483/MR37. Source/target/SHA verified. Template helper failed only onGETpipelines403 becauseCI unavailable; verified MR88viaMRAPI andresumed withoutduplicatingcommit/push/create. GitLabtrimsfinalnewlinefromdescription; whitespace-onlycomparisoncorrected. No canonicalhelper/repochangesforverificationissue.

Approvedmergescompleted: templatesmastercda625bd(squash36f476c1),Socket8b3912d8,Debug642d8dfa,textvalidation1fa42397. AllMRstatesmerged,allsourceSHAspinned. Fetchedmasterstates andexpected5filehasheschecked; localtaskcheckouts remainclean. No appdeploymentsperformed.

User askedwhetherproposedpreparestartsnewpipeline; clarifiedtargetedretryinexistingpipelinepreservesoldCIYAML,whichisimagebuildonlyandcannotdeployupdatedHCL. Userthenexplicitlyallowedstart. Retried8prepare-nuget+13set-variables,newjobs3226148..3226168,source12releasetags+doclatestmaster,basesunchanged. Selected19buildjobsproduce20components; notstartedbythisprepareaction. Allset-vars success;4NugetrestorescurrentlyfailedHTTP429atNexusfeed(not401). Originnginx/Nexus/upstreamunderread-onlydiagnosis;remainingnugetstatusesmonitored. No blind infrachange or generic retryloop. Evidence release-prepare-results.json/release-prepare-failure-evidence.json.


## First two VK deployments and GitLab delivery preference

The user separately approved direct Nomad submission of doc-generator and DebuggingEvents from pinned current master HCL with selected built release images. Commands used plan_vk_service.py --project-id 527/407 --apply --check-index 0; both returned exit 0. Read-only plans had modify index 0 and no placement failures. At 16:59 UTC, doc-generator allocation/task were running, Consul HTTP check passed and /_/healthcheck returned 200. DebuggingEvents API and Elasticsearch tasks were running, both Consul TCP checks passed, and the Elasticsearch route returned cluster health green with zero unassigned shards. API functionality beyond TCP is not established. Safe evidence: /home/slnnk/ai-data/DevOps-898/pilot-runtime-status.json.

The user then explicitly chose new GitLab pipelines for the remaining services. Further direct Nomad deployments are therefore excluded. Current-master pipeline rules, release image overrides and deployment prerequisites are being checked before preparing the separate pipeline creation approval. Public-test remains excluded.

The user explicitly approved adding VK gateway 10.18.20.3/32 to the existing Nexus nginx whitelist on 10.18.24.233. One line was applied in /etc/nginx/includes/limits.conf, nginx -t passed and nginx reloaded at 16:57:33 UTC. Backup: /etc/nginx/includes/limits.conf.DevOps-898-20261014T165733Z.bak. The exception covers all requests through the VK gateway; Nexus was not restarted.

## Latest verified rollout and scope correction (2026-10-14)

The user selected new GitLab pipelines for subsequent deployment and requested GitLab deployment verification for both initial pilot services. Doc-generator pipeline 140895 built `master-137`; separately authorized production child pipeline 140898 succeeded. Explicitly approved VK deploy job 3226189 succeeded and updated Nomad job `youdo-business-doc-generator` to version 1 with image metadata `master-137`. Its running allocation and Consul checks pass; the configured `/_/healthcheck` returns HTTP 200. DebuggingEvents remains verified from the initial direct deployment: API/Elasticsearch tasks run, TCP checks pass and companion Elasticsearch reports green. Its deployment through a new GitLab pipeline is still pending.

Nine separately approved release pipelines 140901–140909 were created for geocoder, call-service, blec, mailer, LogReader, chat-content, tinkoff, vks-policy-generator and pechkin. The monitored NuGet restores passed after the Nexus whitelist update. Seven services have ready manual VK deploy jobs; chat-content and vks-policy-generator builds remain unresolved. No production deployment is active in these nine pipelines. Socket is absent from this launch manifest. Safe evidence: `new-release-pipelines-status.json`, `new-doc-production-status.json`, `doc-vk-ci-deploy-results.json` and `doc-vk-deploy-health.json` under `/home/slnnk/ai-data/DevOps-898/`.

The user corrected Socket scope: `YouDo.Socket` must deploy separately per stand. Cancel its dynamic-mode change and all newly proposed Socket production rules. The six locally added production-rule lines were removed before the checkout was verified clean. The user approved branch `DevOps-898-restore-per-stand-socket-deploy` from current master `8b3912d8` to reverse MR !81. Its candidate `.gitlab-ci.yml` is byte-identical to original `bd5d8944`: restore `DEPLOY_TEST_PER_STANDS=true` and remove the added public-test overrides. This reverse change has not yet been published or merged; current remote master still contains MR !81. Historical 32-group validation is evidence of the abandoned dynamic candidate, not the accepted Socket delivery model.

The shared-template branch proposal `DevOps-898-enable-manual-master-pipelines` was rejected; no corresponding shared-template changes were made. Textvalidation alone retains the approved local branch `DevOps-898-keep-production-deploys-manual`: twelve added rule lines make four production jobs manual on master. Three CI lint calls passed, including the now-cancelled Socket candidate; review found no remaining issue in textvalidation. Publication approval is pending. No new Socket pipeline is authorized by these changes.

The approved Nexus nginx whitelist addition `10.18.20.3/32` was applied to `/etc/nginx/includes/limits.conf` on `10.18.24.233` at 16:57:33 UTC; configuration test and reload passed. Post-change logs show no HTTP 429, and fresh doc-generator NuGet restore succeeded. Of the earlier seven historical build retries, five succeeded; chat-content hit its one-hour timeout and vks-policy-generator failed on obsolete Debian buster apt URLs. Fix proposals are outside repository checkouts and have not been applied.

RabbitMQ uses the old login/password on the new VM; credentials and other Vault fields were preserved. Public-test remains excluded. Test5 SQL is accepted and working, but the other fifteen stand SQL endpoints still block complete LogReader acceptance. Overall DevOps-898 rollout is in progress, not complete.

## Textvalidation release-tag correction (2026-10-14)

The user pointed out that `DEPLOY_PROD_MODE=manual` should use the standard release-tag workflow rather than run production from master or introduce production-rule overrides. All twelve local textvalidation override lines were cancelled; the checkout was verified clean. No corresponding commit, push, MR or merge occurred, and the earlier publication request is obsolete. The approved local branch name alone did not authorize publication.

The user explicitly requested tag creation: “Ну создай новый тег для этого”. GitLab project 383 tag `1.0.4` was created at merged master `1fa4239704ff4d99e1b5e58a2dbccb3261375036`. Safe receipt: `/home/slnnk/ai-data/DevOps-898/textvalidation-new-tag.json`. Standard manual-mode tag CI is expected to build automatically and expose manual production/VK deploy jobs; pipeline identity and runtime results remain pending verification. This supersedes the prior textvalidation manual-rule/publication-pending paragraph. Socket still has its approved local per-stand reverse branch, with publication and merge pending.

## Verified final launch scope (2026-10-14)

The current user-approved launch target is complete: ten single services plus the explicitly limited LogReader test5 pilot are deployed and runtime-verified in VK Nomad through GitLab. This is a launch result, not a claim that the YouTrack ticket was closed or that all sixteen LogReader stands are accepted. Public-test was not deployed or changed.

| Service | Verified version | Runtime evidence |
|---|---|---|
| doc-generator | master-137 | GitLab deploy, running allocation, passing Consul and configured HTTP 200 |
| DebuggingEvents | 1.0.85 | GitLab deploy, API/Elasticsearch tasks running, Consul passing, HTTP 200; Elasticsearch green |
| geocoder | 1.2.12 | Running allocation, Consul passing, configured health HTTP 200 |
| call-service | 0.0.9 | Web/worker running, Consul passing, web heartbeat 200; pre/post migrations exited 0 |
| chat-content | 1.1.16 | Both uploader/downloader groups running, Consul passing, health HTTP 200 |
| textvalidation | 1.0.4 | Running allocation, Consul passing, configured health HTTP 200 |
| tinkoff | 0.0.10 | Running allocation, Consul passing, configured health HTTP 200 |
| blec | 1.0.2 | Running allocation and Consul registration; root route returns 404, no configured health check |
| pechkin | 2.14.24 | Running allocations, configured health HTTP 200 |
| mailer | 8.1.10 | Running allocations/registrations, API health HTTP 200 |
| LogReader, test5 only | 1.0.39 | Exactly one test5 group, running allocation, Consul passing, HTTP 200 and SQL SELECT 1 |

Safe evidence is in `/home/slnnk/ai-data/DevOps-898/seven-single-runtime-status.json`, `three-ready-runtime-status.json` and `doc-vk-deploy-health.json`. LogReader SQL verification used the same Vault `secret/resources/databases/mssql` USER/PASSWORD fields as the HCL against `YouDoLogsExceptions`. SELECT 1 passed from the operator workstation; TCP was separately verified from the actual allocation node host network, not by container exec. No SQL error classes were observed in its inspected logs. The separately approved Consul CAS update changed only `test_instances/test5/mssql_db` to `sql-test5.service.vk-test.consul,14305`. Other fifteen SQL endpoints remain a backlog dependency for a later full LogReader rollout.

The user excluded vks-policy-generator after its README identified it as unused and explicitly requested closing its MR without deployment. [MR !18](https://gitlab.youdo.sg/youdo/vsk/vks-policy-generator/-/merge_requests/18) is closed, `merged=false`, verified by `vks-mr-closed.json`. No merge and no `0.0.27` tag occurred. The published apt-source fix branch/commit remains unmerged; it is historical publication evidence, not an outstanding launch blocker. The optional chat-content cache fix was never implemented; the new unmodified release build succeeded.

Socket is a per-stand service and excluded from this single/dynamic launch by the user's classification correction. The separately approved reverse publication [MR !82](https://gitlab.youdo.sg/youdo/YouDo.Socket/-/merge_requests/82) was merged after explicit approval into master `7f6d81b38de45961893cc6fa794ce231e5f6cc81`. Its original `DEPLOY_TEST_PER_STANDS=true` CI is restored. Receipt: `socket-revert-publication/merge-results.json`. This supersedes earlier unpublished-reversal and remote-MR !81 state statements. No Socket production-rule overrides were published.
