---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, gitlab-ci, ansible, microservices]
---
# DevOps-899 Monolith microservice rebuild and VK per-stand delivery

## Summary

Completed test5 delivery for all eight selected Monolith-dependent services. Initial30 component builds and four antifraud follow-up builds passed. Eight reviewed MRs are merged. Antifraud23.8.7 now uses direct PostgreSQL5432, healthy without restarts; escrow13.8.12 and the single shared router are healthy after four monolith internal Host-tag corrections. All eight services have matching BuildAPI saved metadata, live Nomad source/image versions and rendered status rows. Config master/preprod was audited; no DNS changes required there. Form was excluded by the user. No PgBouncer configuration or runner DNS settings were changed.

## Scope and approvals

Selected services: Fns, antifraud2, attribution, badgekeeper, bruteforcingdetector, docvalidation, escrow.tinkoff and youdo.userinsurance. User excluded unused youdo.form.

User authorized current master/latest release sources, the two DNS corrections, shared per-stand VK CI mapping, PostgreSQL identity correction, publication and merges, a new escrow tag, rebuilding all selected images, and automatic production deployment. User explicitly skipped runtime preflight for speed. No superpowers skills were used.

Both supervised gates were followed: branch names were confirmed, then actual diffs/checks/commit subjects/MR titles and CI effects were confirmed. User subsequently corrected the task from DevOps-892 to DevOps-899. Publication stopped at a safe boundary, and corrected branch/MR/task-link names were explicitly confirmed. Commit contents/subjects were unchanged. Templates and Ansible had already pushed their old892 branches; those were retained without deletion or history rewriting. Service892 branches remained local.

A later +4/-4 PostgreSQL raw-module correction was separately reviewed and explicitly approved for publication/continuation after an actual CI failure. Merge authorization already covered the task's corrections.

## Repository changes and publication

| Repository | MR | Source commit | Merge commit |
| --- | --- | --- | --- |
| docvalidation | [!137](https://gitlab.youdo.sg/youdo/microservices/docvalidation/-/merge_requests/137) | cfb0642d645848127bc73717e6463dcd891bc96e | b5e247c7b52c6f4b711d875ef01d2c05bc6890c6 |
| escrow.tinkoff | [!50](https://gitlab.youdo.sg/youdo/microservices/escrow.tinkoff/-/merge_requests/50) | c074d78885c1280172b35e18691022bf1ffe14e9 | eaa0d387bb21488f2077968d10def0b9450f0947 |
| gitlab-ci-templates | [!89](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/89) | 9c91d4a058ac440e0f12dabab4d327ca2f0a1a7d | a53eaa729ceaf31786c54254ae7dd78622a6aed7 |
| automation-test-yandex | [!109](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/109) | 3243cc90469700933e86b2a0c4236d436af1b301 | 98e9604253b030005fc5ada2def9da0630f22931 |
| automation-test-yandex follow-up | [!110](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/110) | f1788cff5c1cc75f7547b32c3a8e93305db3ac1b | 9a6a72d74bced71b4b97e6184f1a19f6be92249a |

Branches: DevOps-899-fix-monolith-service-dns in the two service repos; DevOps-899-deploy-per-stand-services-on-vk in templates; DevOps-899-fix-microservice-postgres-auth in Ansible.

Approved commit subjects/MR title suffixes: correct monolith api dns suffix; parameterize escrow router datacenter; switch per-stand service deploys to vk; run microservice postgres tasks as postgres; run microservice postgres commands without remote python. MR titles prefix DevOps-899; descriptions contain one Russian paragraph plus the task link only. Project settings were preserved.

Actual diffs: docvalidation3+/3-, escrow3+/3-, templates3+/4-, initial Ansible8+/0, follow-up Ansible4+/4-. Only explicit task paths were staged and the entire staged diff was inspected. All19 pre-existing MSSQL modified/untracked paths remained unchanged by SHA256.

Checks passed: YAML parsing, exact endpoint replacements and test5/vk-test rendering, structural preservation of CI jobs/public-test, Ansible syntax in a temporary CI directory layout, SQL/conditions/tags/loops preservation for raw conversion, and git diff --check. No target packages or base images were changed. Templates CI is disabled; the publication helper's final pipeline-list403 occurred after successful MR creation and was diagnosed through GET, without retrying creation.

## Release and build results

Escrow latest release13.8.11 was followed by approved13.8.12 at exactly merged mastereaa0d387. No other new tags were created. Shared templates and Ansible were merged before the service merges/new pipelines.

| Service | Source | Pipeline | Component build result |
| --- | --- | --- | --- |
| Fns | master7e819e8 | 140951 | 4/4 success |
| antifraud2 | 23.8.6 | 140952 | 4/4 success |
| attribution | 1.0.22 | 140953 | 3/3 success |
| badgekeeper | 21.13.5 | 140954 | 2/2 success |
| bruteforcingdetector | 1.13.20 | 140955 | 4/4 success |
| docvalidation | masterb5e247c | 140949 | 4/4 success |
| escrow.tinkoff | 13.8.12 | 140950 | 5/5 success, including router |
| youdo.userinsurance | 0.0.68 | 140956 | 4/4 success |

Docvalidation merge and escrow tag pipelines were reused; six other fresh pipelines were created once with receipts. No old compiled pipeline was used to apply the shared CI correction. Automatic production child pipelines for Fns/docvalidation were allowed; their deployment outcome must be recorded separately from image-build success.

## Actual deployment failures and corrections

Badgekeeper first test5 job3227609 passed image checks, found no existing badgekeeper-test5 Nomad job and failed SSH at the first PG task, before SQL. CI entrypoint writes inherited GitLab group youdo PRIVATE_KEY into /root/.ssh/id_rsa. No nearer override was found. A public key was derived through an in-memory descriptor; the private value was never persisted. Public fingerprint SHA256:QIr7ZqPHi8k/4IPvxu+IkWOCblLwsfeGYwACBJdq5aY was missing from PG root authorized_keys.

An explicitly approved SSH action through youdo/sudo on10.18.26.39 appended only that public key to /root/.ssh/authorized_keys, preserving the two existing keys and0600 mode. Backup /root/.ssh/authorized_keys.devops-899-before was created0600. No service restart occurred. Secret source location and public fingerprint are recorded; no private key value was copied to notes/scripts/logs.

Retry3227854 confirmed SSH and sudo-to-postgres work, but failed before SQL with ModuleNotFoundError for ansible.module_utils.six.moves. The CI image pins Ansible2.9.7; read-only host inspection confirmed only Python3.12.3. Reviewed MR110 changes only the four PG shell tasks to raw, retaining SQL, postgres identity, conditions, loops and dropdb tags. This avoids remote Python without upgrading shared tooling. After its merge, retry3227855 was queued in the same pipeline.

## Database mode and in-progress deployment

Test5 deploys use manual-job variable ANSIBLE_SKIP_TAGS=dropdb. Local ansible-config confirms TAGS_SKIP resolves to dropdb. All DROP tasks are tagged; create-if-absent, schema/data migrations and normal Nomad replacement remain active. User was informed that docvalidation template cloning is also skipped: if the target DB is absent, an empty DB is created and migrations run without template seed data. Escrow uses fixed MSSQL databaseTinkoffEscrow; its DROP is skipped while migrations remain active.

Escrow deploy3227465 was launched independently because it does not use delegated PG. Badgekeeper current retry3227855 is pending. Do not infer success from pipeline status manual: test deploy jobs allow_failure and may fail independently.

## BuildAPI acceptance requirement

User explicitly requested verifying service information at http://buildapi.dev.youdo.corp/ after deployment. Check all8 project records in /ms_builds/test5, matching pipeline/job IDs, source SHA/ref and DEPENDS_ON=Monolith. Check live Nomad details through /get_microservices_info/test5, compare image tags with the actual source/pipeline IID, and verify rendered /ms/test5 service rows. Deploy metadata POST has ignore_errors, so green deploy alone is insufficient. No successful metadata acceptance is claimed at this checkpoint.

## Operational artifacts and limits

Sanitized manifests, publication/merge/build/deploy receipts and status files are in /home/slnnk/ai-data/jenkins-recovery/monolith-services-audit/. Helpers: operate.py and verify_buildapi.py. Runtime preflight was intentionally skipped; actual failure diagnosis and post-deploy acceptance remain in scope. Work continues; open status is tracked in ~/ai/TODO.md.

## Portable lesson

None.

## Antifraud direct PostgreSQL follow-up

Read-only runtime comparison confirmed antifraud2 API, service and scheduler use postgres.service.vk-test.consul:5433, while migrations use5432. Six other selected PG services use direct5432; escrow uses MSSQL14305. The same deployed credential succeeds on direct PostgreSQL and fails at PgBouncer. PgBouncer has no youdo auth-file entry and only a grafana_test database mapping; no PgBouncer configuration was changed.

User requested bypassing PgBouncer. Stage1 approved branch DevOps-899-use-direct-postgres from current origin/master2ce9b60 (release23.8.6). Local devops/config.yml changes only three Port=5433 values to5432, +3/-3. YAML parsing, exact semantic-scope assertions and diff-check passed. Proposed commit use direct postgres connections, MR DevOps-899 use direct postgres connections, target master, Russian paragraph plus DevOps-899 link. User explicitly confirmed publication, merge, new23.8.7 release at merged master, rebuild and test5 delivery with database preservation. Commit8256973030aced253c9ae4fa14de015ffa0c89e8 published; MR[!145](https://gitlab.youdo.sg/youdo/microservices/antifraud2/-/merge_requests/145) merged asfb11521ccbfed7dde8fa4bf607d900b95922f8a4. Release23.8.7 created on exactly that current master; pipeline creation is asynchronous. No PgBouncer changes were made.

## Shared router and current escrow blocker

User clarified router is one shared instance for all stands. Existing deploy-test-router job3227478 succeeded with explicit VK environment/address/token/dc/proxy overrides; healthy allocation3f3b4215-fcff-da84-23ec-dcb642013ddb, count1, image/router:13.8.12 confirmed by job metadata. Permanent five-variable CI correction was separately approved and merged via escrow[MR!51](https://gitlab.youdo.sg/youdo/microservices/escrow.tinkoff/-/merge_requests/51), commit137ab6aaab5a3005b6c043089d1a58b230a81124, merge3ceb86f6cce6cc52cb436c5cf68d8236f290108c. Current approved release13.8.12 was retained.

Escrow retry3228022 failed after healthy router: web/api/worker running without restarts, premigrations exit0, but YouDo API healthcheck repeatedly receives HTTP404. Actual URL/path diagnosis is in progress; router readiness alone was insufficient.

## Accepted service delivery checkpoint

Fns3227503, attribution3227574, badgekeeper3227855, bruteforcingdetector3228015, docvalidation3228016 and userinsurance3228017 have matching saved BuildAPI metadata, live Nomad source/image tags and rendered test5 rows. Initial successful jobs for brute/docvalidation/userinsurance were zero-task no-ops because runner DNS intermittently failed to resolve dyninv.vk-test.youdo.local; explicitly approved retries completed actual tasks and metadata checks. No runner DNS configuration was changed.

## Monolith Nomad generation and config repository audit

Live escrow health failure is caused by Host routing: /api/v1/state returns404 through youdo-api.test5.vk-test.youdo.local and200 through the old yandex-test hostname. DNS already points at VK proxies. Ansible group_vars/all.yml traefik_domain is hardcoded yandex-test.youdo.local despite dc=vk-test. app_deploy/tasks/nomad.yml renders nomad.hcl/nomad_web using defaults/main.yml tags. An in-memory candidate using {{ dc }}.youdo.local changes exactly SSR/API/moderation-tickets/moderator-boris Host tags; public hostnames stay unchanged. No HTTP path-prefix rewrite is present; filesystem mounts local/*.json to /app/*.json, registry paths, datacenters and Consul generation are already cloud-independent or dc-based. No repository routing edit or Nomad mutation has been performed.

User specifically requested config master/preprod audit. Repository ~/git/config is clean at2945af7e2924813fae222d0befb154f620e48d5c, matching fresh GitLab master. prepare_configs.yml copies config/preprod and utils, applies generated overrides via patch.sh, then Nomad-specific JSON overlays; config/test5 is not consumed by this pipeline. JSON parsing passed for six preprod and five test5 JSON files; no yandex-test or vk-test literal appears in the base files. Overlay endpoint audit completed: generated SQL connection strings use sql-test5.service.vk-test.consul; PG uses postgres.service.vk-test.consul; app domains use test5.youdo.sg and selected microservice endpoints are dc-based. Existing legacy WCF/testdata and DocValidation.BaseUrl defaults are unrelated to the proven Traefik404. No config repository edits are required for this DNS change.

Antifraud release23.8.7 pipeline140965 is rebuilding four components; unit tests passed. Earlier23.8.6 receipts were preserved as previous-23.8.6-* before selecting the new approved source for test5.

## Monolith routing supervised training follow-up

User explicitly confirmed reuse of automation-test-yandex DevOps-899-fix-microservice-postgres-auth from current origin/master9a6a72d for the one-line traefik_domain change. Existing branch fast-forwarded cleanly; local YAML now uses {{ dc }}.youdo.local. All19 unrelated file hashes preserved. YAML semantic comparison confirms only this variable changed; task-file diff-check passed. User explicitly confirmed publication, merge and the exact CAS-protected runtime routing update. Commit84c4cd76bce27ab4166753082267795fe35d6fcb published through Ansible[MR!111](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/111), merged342b1d544878b594b7f50c66b5c8e92d1bb101fb. Live youdo-test5 changed exactly four Host tags at index8381→8948, evaluation64bf2570-5659-9955-a9c4-176acac1beff completed. Both monolith allocations healthy; VK /api/v1/state nowHTTP200; escrow API/web /hcHTTP200 and Consul API/web/worker checks passing. Old failed escrow deployment status is historical. Retry3228097 was launched with retained skipdropdb to complete normal deployment and BuildAPI metadata writes; migrations still run, DB preserved.

Escrow post-retry BuildAPI acceptance passed: saved project422 release13.8.12/pipeline140950/job3228097/source SHA all match; live Nomad running and rendered /ms/test5 row present. Thus seven selected services are now accepted, antifraud23.8.7 remains pending delivery.

## Antifraud new release build and deploy

Release23.8.7 pipeline140965 completed all four component builds and unit tests successfully. The last API build was slow because an external base-image layer downloaded at approximately25-30KB/s; progress was verified, not a compiler/NuGet failure. Approved deploy3228068 launched for test5 with ANSIBLE_SKIP_TAGS=dropdb, preserving the existing DB while running normal migrations. Runtime port/version and all-service BuildAPI acceptance are pending.

## Final acceptance (2026-10-15)

Antifraud deploy3228068 SUCCESS, release23.8.7/pipeline140965/sourcefb11521ccbfed7dde8fa4bf607d900b95922f8a4. Deployment successful, healthy1/unhealthy0; allocation6a70ea59-fbaf-6812-e3ea-0ca66bb297f2 running. API/service/scheduler/Selenium restart counts0; pre/post migrations exit0; all three runtime PG connections use5432. Previous password-auth/Npgsql/unhandled-exception signatures absent from the inspected scheduler stderr tail.

Escrow deploy3228097 SUCCESS, release13.8.12/pipeline140950. Shared router remains one healthy instance for all stands. Monolith evaluation completed with both allocations healthy; VK API /api/v1/state and escrow API/web /hc return200.

Final verify_buildapi.py exited0 with8/8 accepted: /ms_builds/test5 exact project/pipeline/deploy-job/source/ref/Monolith metadata, /get_microservices_info/test5 live requested release versions and /ms/test5 rendered rows all match. Evidence buildapi-verification-all.json. Fns master-598, antifraud2 23.8.7, attribution1.0.22, badgekeeper21.13.5, bruteforcingdetector1.13.20, docvalidation master-757, escrow.tinkoff13.8.12, userinsurance0.0.68.

All19 pre-existing unrelated Ansible dirty/untracked file hashes remain unchanged. Selected CI job/database behavior was preserved: skipdropdb retains databases, normal migrations run. Runtime preflight was skipped as requested; post-deploy scope covers job health and metadata, not full application business tests. Runner upstream DNS inconsistency was recorded as a separate backlog item on2026-10-15; no additional infrastructure changes were made for it. On2026-10-20 the user confirmed it currently works and explicitly closed the investigation. The central TODO is closed; no new diagnosis, DNS change or root-cause verification was performed for this closure.

## Other stand catalog seeding (2026-10-15)

User explicitly requested analogous BuildAPI service data for test,test1-test7,test10-test15, with per-stand job URLs. Existing test5 was already complete;13other stands had no builds document and no selected service catalog records. Source is the eight accepted test5 releases. Each destination CI_JOB_ID/CI_JOB_URL was resolved from that same service pipeline to exact deploy-yandex-test0/17 for test or N/17 for testN; all104targetjobs were manual. Commit/ref/pipeline/project/DEPENDS_ON fields were preserved.

Prepared plan fingerprint9e7000029c07e70b687b9a5fff4644e892544cee77a3eea1eca82b5893053484. Executed117BuildAPI-only writes:104POST /ms_builds/{stand}/{project_id},13PUT /builds/{stand} containing instance and eight exact service job URL keys (copied fromtest5 fieldnames). No monolith build/date/version metadata was invented. No GitLab jobs or Nomad jobs were triggered by these writes. Every destination was checked unchanged before apply.

Final GET verification passed for all13stands:104catalog records and104joblinks exactly match plan; existing unrelated service data preserved; test5 full source fingerprint unchanged. Targetcatalog entries are deployment sources for future Jenkins recreate_microservices, not evidence of service runtime on these stands. /ms/{stand} continues to show actual Consul/Nomad state independently.

Artifacts seed-stand-buildapi-plan.json, seed-stand-buildapi-receipt.json and seed-stand-buildapi-verification.json; local receipt-backed helper seed-stand-buildapi.py. JSONschema and consumer audit confirmed CI_DEFAULT_BRANCH must be retained because BuildAPI history pruning uses it; builds minimal instance+serviceURL document is supported by Home/GET consumers.

## First-launch Ansible verification (2026-10-15)

User requested checking first start as well as restart. Source inspection confirmed recreate_microservices maps test→0 and testN→N, selects the matching recorded-pipeline deploy job, uses POST/play when statusmanual, POST/retry otherwise, records the returned job ID and polls tosuccess. Existing running service/Nomad job is not required: missing stop is ignored and deploy_microservices creates absent DBs before nomad run.

Executed the actual unmodified recreation playbook (SHA25650070ce87f561bd0c5b8a4e0c17ff4b5c9d9f82d840d8c463ce9da086ae35bdf) with local Ansible core2.15.13 against an isolated localhost GitLab/BuildAPI mock populated from the seeded plan. All13stand hosts passed,104distinct manualjobs received exactlyone/play each,104successpolls,0unexpectedrequests and0failedhosts. No real GitLab mutation or deployment occurred. Helpercheck-first-launch.py and sanitizedreceiptfirst-launch-verification.json. An initial harness counter assertion was corrected; the actual playbook succeeded on both runs and the final entire harness exited0. No repository changes required.

Read-only SELECT checks on10.18.26.39 confirmed DocValidation source database exists and has0activeconnections, allowing clone aspostgres; youdo role hasLOGIN/SUPERUSER and publicschema privileges. Normal Jenkins firstplays do not inject our one-off test5 ANSIBLE_SKIP_TAGS=dropdb: service database recreation remains controlled by each serviceconfig. Existing wait policy is10retries/30seconds beforefallback, so slowdeploys can reachfallback. Exact Jenkinsorchestrator Ansible version was not established; core2.15.13 mock verification is not a claim that all104realdeploys ran. Service GitLab deploy-image Ansible2.9.7 is a separate execution context.
