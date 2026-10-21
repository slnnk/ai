---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [youtrack, recovery, audit]
---

# Closed recovery comment completeness recheck

## Summary

The user questioned the completeness of the brief comment-update plan. A fresh read-only YouTrack snapshot and three independent evidence reviews covered all11closed recovery tasks found in the70most recently updated resolved DevOps issues. No comments changed since the initial snapshot. The previous plan omitted substantial supporting work, especially PostgreSQL/PgBouncer, FeatureToggle data, shared CI changes, .NET2.1mirrors and full-fleet Elasticsearch deployment. The revised plan covers7task comments: DevOps-899,898,894,892,891,896 and a historical-only addition for889. Existing890,893,895,897comments already cover the material completed recovery results and should be preserved without duplicate additions.

## Task and context

Scope: reconcile completed work and verification limits into existing closed YouTrack comments; no external writes are authorized by this review request. Source attribution: per-stand C2C/B2B delivery and its database prerequisites belong899; shared single/dynamic services, LogReader and BuildAPI platform recovery belong898; base-images/devdocker/data-dockers belong891; packages/PyPI belong890; production periodic runtime images belong895. Historical branch/MR/artifact IDs remain unchanged. Jenkins publication fixes stay primarily892 with links from899, avoiding duplicate task accounting.

## Actions and evidence

- Ran ai-sync.sh with no output/reminders. Reused the established YouTrack GET client and company environment loader.
- Saved full current task/comment baseline at `/home/slnnk/ai-data/youtrack-comment-reconciliation/closed-issues-recheck.json`; all11recovery comment texts match the initial baseline. Tokens stayed in the company .env and process memory.
- Delegated independent read-only reviews for Jenkins/SQL/ES, service/database recovery and recovery dependencies. Reports: `audit-jenkins-sql.txt`, `audit-service-work.txt`, `audit-recovery-dependencies.txt` in the same artifact directory. The service report contains41evidence rows, including already-published results; these are not41new completed tasks.
- Fresh GET Jenkins dynamic_deploy5828–5832 saved sanitized results in `jenkins-builds-recheck.json`:5828test2FAILURE,5829test3FAILURE,5830test7FAILURE,5831test8SUCCESS,5832testFAILURE; all finished. No build was retried.
- Read Jenkins5828–5830console logs only into memory and saved task/stage hints plus broad error-class markers in `jenkins-failure-contexts.json`. Parallel-stage interleaving and ignored failures prevent treating these hints as established final root causes. Raw logs, request credentials and personal data were not persisted.

## Revised comment changes

### DevOps-899 — per-stand services and recovery prerequisites

Retain already-published initial test5/test4 results and their existing technical fixes. Add the later exact coverage rather than claiming every service on every stand:

- Seven C2C services expanded to8stands: Broadcast1.2.11, FeatureToggle1.0.11, Landings1.3.35, Socket1.2.9, Help1.0.14, Content2.5.13, SMSmaster-191; Moderation1.0.45 assets published to the same8stands. SMS/Fns/DocValidation have14stand coverage across C2C+B2B. Antifraud23.8.8 is confirmed on5stands only; TrackingPixel1.0.5 remains test5-only evidence.
- Completed B2B catalog on test10–test15:12per-stand services plus reused shared doc-generator from898. Include main Business21509, auth168, billing707, B2B Landings109, MobileID58, TKB267, Tochka1767, Kitcut103, Notifications190, SMS191, DocValidation757 and Fns598; deployment acceptance was mostly GitLab/Nomad status checks, not full business-functional testing.
- FeatureToggle data recovery:149seedfeatures plus49missing production-CSV keys,198total;13other stand database clones with hash/sequence checks and main-template refresh. MD5 compatibility narrowed to the existing youdo role while defaults/other roles retain SCRAM. Prepared14stand databases do not establish14runtime FeatureToggle deployments; runtime coverage is8C2C.
- PostgreSQL/PgBouncer: C2C PG final max_connections1000; C2C PgBouncer final clientcap3000/usercap250/softFD4096, Cerberus14DBpools capped10each and Antifraud14transaction routes capped2each, Grafana session pool preserved. B2B PG/PgBouncer capacity1000; TKB6explicit routes and existing SCRAM verifier, Tochka12routes; direct/pooled SQL checks passed. Retain password/auth scope and final effective settings rather than listing superseded intermediate limits as current.
- Cerberus1.0.9 all14active stands via ordinary GitLab jobs, normal database recreation,42worker startup markers and clean current membership. Include source/playbook fixes114/115/117 and runtime PgBouncer routing; do not describe abandoned DB-preservation or manual membership-repair proposals as the accepted solution.
- Supporting CI/source fixes: merged shared per-stand VK templateMR89 and keep-db inheritanceMR91 (18child overrides removed); keep-db jobs were statically checked but not runtime-tested by this recovery. Landings lockfile integrity/internal Node24/nginx80 repairs. Business final6literal VK addresses, postgres raw/become tasks and pager-off fixesMR118/119/120. Preserve historical898names for these899results. Include SMS CI SSH-key/runner-image preparation where useful.

Sources: [service evidence table](/home/slnnk/ai-data/youtrack-comment-reconciliation/audit-service-work.txt), [FeatureToggle seed](2026-10-15-nomad-test-featuretoggle-test5-seed.md), [FeatureToggle clones](2026-10-15-nomad-test-featuretoggle-stand-clones.md), [B2B pool capacity](2026-10-15-postgresql-b2b-connection-limits-1000.md), [Business final rollout](2026-10-16-nomad-test-devops-898-business-rollout.md), [Cerberus final standard rollout](2026-10-16-nomad-test-cerberus-standard-gitlab-rollout.md).

### DevOps-898 — shared services and completed LogReader

Replace obsolete test5-only/other15SQLblocker text with LogReader1.0.39 on all14active stands, pipeline141021/deploy3230221,13Consul SQL-address corrections and persistent project stand list. SQLSELECT1all14; all14Nomadhealthy/Consulpassing/HTTP200/zero restarts;28log streams inspected without matched error classes. test8/test9excluded. Keep10single services and BuildAPI0.5.13recovery already published, with per-stand B2B cross-reference899. Shared doc-generator is reused, not6new instances.

Source: [LogReader approval and acceptance](2026-10-16-nomad-test-logreader-all-active-stands.md).

### DevOps-894 — complete Elasticsearch fleet lifecycle

Add omitted full parallel14stand Ansible lifecycle run:14/14exit0, no retries,121.790seconds, healthy_deadline2m/progress_deadline3m, internal images. Thick test/test1/test6=40GiB, other11thin=5GiB. Earlier13stand batch was superseded by this result. Existing individual Jenkins checks/5826/5827 are already described. Do not claim fresh ES HTTP/index checks on all14from this batch.

Source: [all14ES lifecycle](2026-10-14-nomad-test-devops-894-es-all-stands-deadlines.md).

### DevOps-892 — Jenkins delivery prerequisites and final attempt outcomes

Add performed SSH access/plugin-option repair for PostgreSQL/balancer, static release139593rebuild (prepare-npm/build_ssr/Docker; image master-2.917.139593), project278canonical VK token variable and direct static test5deploy3226694. Refine the existing BuildAPI publication bullet with4URLfixes, curl fail-on-HTTP and shell error propagation; metadata repair was already described, not a separate wholly new outcome.

Record final attempts accurately:5828/test2,5829/test3,5830/test7failed;5831/test8succeeded and then test8was retired by user request (4Nomad jobs, dedicated5GiBESdisk and BuildAPI records removed). Link5832/MSSQL endpoint fix to897without claiming a later independently verified successful Jenkins thick run. Existing5826/5827success,quiet-hook removal and local RabbitMQ purge acceptance remain as-is. AutoTest/backup/canonical configuration gaps remain unfinished.

Sources: [static rebuild](2026-10-15-jenkins-static-release-rebuild.md), [SSH prerequisites](2026-10-15-jenkins-ssh-credential-vk-access.md), [BuildAPI publication](2026-10-15-jenkins-buildapi-publication-fix.md), [test8retirement](2026-10-15-jenkins-test8-cleanup.md), fresh sanitized Jenkins status artifact.

### DevOps-891 — omitted base images and corrected devdocker outcome

Add completed .NET2.1SDK/ASP.NET mirrors from base-imagesMR42, merged release tags on master, local checks SDK2.1.818/runtime2.1.30 and verified image publication. Both images were published; SDK pipeline140998job3229538was canceled after the approved direct push, runtime pipeline140999job3229539succeeded. Do not claim two successful pipelines or consumer cutover: consumer image-reference changes were deferred.

Update devdocker aggregate pipeline140984from pending/unconfirmed to observed failed master_build3228589 (test3228588success). Its MR55/internal Docker and independently successful PostgreSQL10ru_RUpublication/Broadcast8of8already appear in the comment; retain them, avoiding duplicate new-result accounting. Full6image recovery is not established.

Source: [.NET2.1mirror publication](2026-10-15-base-images-dotnet21-mirrors.md); previous live GET recorded in [main plan](2026-10-16-nomad-test-youtrack-comment-reconciliation-plan.md).

### DevOps-896 — specific consumer cutover correction

Replace stale claim that test_inventory.sh needs the VKURL: the actual Jenkins consumer already queries dyninv.vk-test.youdo.local, confirmed October14and15. Do not generalize to all consumers or remove historical liveSQL/repeated-refresh limits. Closed accepted state remains unchanged.

Sources: [Restore address review](2026-10-14-jenkins-restore-playbooks-review.md), [VK audit](2026-10-15-jenkins-monolith-microservices-vk-audit.md).

### DevOps-889 — historical completed work before Yandex route cancellation

Add a short dated historical paragraph: yc-a-sql-base copy reached READY, minimal local recovery adaptation checked, HDD/quota constraints diagnosed. Then preserve explicit cancellation of the Yandex direction and cross-reference the completed VK recovery under897. No full Yandex recovery, quota request or publication occurred. This preserves real performed work without reopening an obsolete path.

Source: [Yandex recovery history](2026-10-09-yandex-cloud-devops-889-mssql-recovery-plan.md), [HDD selection](2026-10-10-yandex-cloud-devops-889-mssql-hdd-disk-selection.md).

## Already complete comments and limits

-890already includes UI0.25.4/0.26.0, MassTransit1.8.1repair,5further ServiceCore versions,32PyPIversions and earlier NuGet/Maven/npm recovery.
-893already contains Terraform/Nomad/CSI/SSD/CIapply results; later application PostgreSQL work is not evidence of Terraform changes.
-895already contains8restored periodic runtime refs; no fresh proof of all23parents running new image bytes, and excluded nexus-cleaner repair remains excluded.
-897already includes all7thick steps,11thin jobs,MR106/1374,MR113and user-reported successful playbook after5832. Do not count these again as missing.

Do not claim universal zero restarts: Cerberustest11, Antifraudtest7 and DocValidationB2Btest12/test14had recovered restarts in their recorded acceptance. Do not infer104actual deployments from104manual links. Preserve service-specific scope, status-only test limits, excluded services and Git history. No YouTrack/state changes were made.

## Changed files and risks

Created this audit log and sanitized snapshots/reports; expanded the existing comment plan to7tasks; updated the existing system map and central backlog/index/sync bookkeeping. Final exact text still needs preparation and review, with a fresh GET baseline check before each approved external update. Jenkins failure root causes were not diagnosed by this audit; stale pending entries were replaced with observed final statuses without rerunning builds.

## Subsequent publication (2026-10-16)

The user approved updating existing comments; all7proposed tasks now have their original summary comments updated in place, verified with no new comments or state changes. [Publication and exact IDs](2026-10-16-nomad-test-recovery-existing-comments-updated.md).


## Jenkins deployment follow-up closed by user — 2026-10-20

The user confirmed that deployment now works correctly and BuildAPI updates. Closed the test2/test3/test7 deployment and metadata-consistency follow-up in the [central backlog](../../../../TODO.md), moving its closed record from the unrelated FeatureToggle section to Jenkins recovery. Earlier build failures and diagnostic limits remain historical evidence, not a current open investigation. No new fixes, Jenkins reruns or independent runtime checks were performed in this closure. This acceptance does not close unrelated Jenkins backup, monitoring or recovery proposals.
