---
system: jenkins
status: verified
checked: 2026-10-16
tags: [jenkins, recovery, vkcloud]
---

# Jenkins infrastructure and recovery state

## Summary

User acceptance2026-10-20: deployment works correctly and BuildAPI updates. The test2/test3/test7 follow-up for historical Jenkins5828/5829/5830 failures is closed; no new fixes or independent runtime checks in this closure. Earlier attempt outcomes remain historical. [Closure](../log/2026-10-16-nomad-test-recovery-comment-completeness-recheck.md#jenkins-deployment-follow-up-closed-by-user--2026-10-20).

Jenkins controller and AutoTest agent restored on VK hosts on 2026-10-13 under [DevOps-892](https://youtrack.youdo.com/youtrack/issue/DevOps-892). Controller is accessible internally at http://10.18.26.8/. Authorized checkout-only test-git build4 succeeded on the controller; quiet mode was restored after explicit user approval and API confirmed quietingDown=true. Persistent controller image Git correction was merged, published and verified after approved recreation; stored-credential branch lookup returns205/master. AutoTest actual checkout and downstream workflows remain untested. Later that day the user supplied replacement balancer 10.18.20.97: its existing Nginx route to the VK controller returned HTTPS 200 with normal certificate validation using a forced address. Public HTTPS at138.16.201.238 is verified through corporate OpenVPN. After the local TrustTunnel exclusion was prepared, the user supplied a screenshot confirming the authenticated Jenkins UI opens at https://build.youdo.sg; the screenshot does not independently establish the active client route. WebSocket forwarding remains unverified. Historical Jenkins notes incorrectly use DevOps-890, which is the Nexus task; do not carry their completion status into DevOps-892.

Latest acceptance: dynamic_deploy5826 completed SUCCESS on test5 on2026-10-15 with Restore, Elasticsearch, monolith/static, buildsinfo and Suggestions reindex enabled. B2B Elasticsearch/microservices were disabled. Four ignored Ansible failures including HTTP401 remain; successful status does not verify Rabbit cleanup. See [5826 reconciliation](../log/2026-10-15-jenkins-build5826-plan-reconciliation.md). Earlier quiet-mode and failed-build checkpoints below are historical.

## Microservice version selection

Verified2026-10-16: dynamic_deploy5847/5848 on test reapplied badgekeeper21.13.5 from BuildAPI /ms_builds/test despite successful MR36 deployment3232612. BuildAPI delete_stale_ms_build removes feature-ref records whenever a default-branch/semver release record exists;3232612 publication returned insert1/deleted1. Jenkins retries the saved pipeline deploy job even if already successful. Badgekeeper fallback was skipped in5848. User clarification2026-10-20: this version-selection behavior is correct and requires no fix. The earlier proposal to retain the latest feature deployment is cancelled; no implementation performed. [Investigation](../log/2026-10-16-jenkins-badgekeeper-5848-version-selection.md).

## Controller timezone

Since 2026-10-16 the controller's default display timezone is `Europe/Moscow`. The active Compose service sets `TZ=Europe/Moscow` and `JAVA_OPTS` includes `-Dorg.apache.commons.jelly.tags.fmt.timeZone=Europe/Moscow`; Jenkins `System Information` confirmed both `user.timezone` and the formatter property after container recreation. This is the default for users without a personal timezone preference. The host OS timezone/clock was not changed. [Change log](../log/2026-10-16-jenkins-controller-timezone-moscow.md).

## Hosts and access

| Component | Host / address | Verified state |
| --- | --- | --- |
| Controller | vk-ms1-jenkins-test / 10.18.26.8 | Root SSH; Jenkins 2.555.1; 11 jobs; 116 active plugins; authenticated API works; quietingDown=true after approved restoration; queue empty at smoke completion; test-git4 SUCCESS |
| Agent | vk-ms1-jenkins-agent-test-01 / 10.18.26.26 | Root SSH; AutoTest online via WebSocket, 5 executors |

Bootstrap access is youdo with passwordless sudo. User authorized adding .ssh/id_ed25519.pub for root; completed and independently verified on both hosts. No key values retained here. Browser access requires network reachability to 10.18.26.8, such as the corporate VPN. Accounts and credentials come from the October 7 backup.

## Storage and runtime

Both hosts have Docker 29.9.0 and Compose installed through existing docker-compose -> docker Ansible roles. Docker and containerd data reside on the verified /data filesystems via guarded symlinks. Controller /dev/vdb is 150 GB, UUID 937fca4e-18b8-4bc1-a1a2-5b4d1e5931f4, approximately 131 GB free after deployment. Agent /dev/vdb is 10 GB, UUID b1457393-253d-4960-9278-b9b6ad40161a, approximately 7.8 GB free after image deployment. User approved current agent disk; cold-build workspace/cache growth remains untested.

Controller host JENKINS_HOME is /data/jenkins/data/jenkins. Recovery quiet hook was removed from init.groovy.d on2026-10-15 at the user's explicit request. Original file retained at /data/jenkins-recovery/disabled-hooks/devops-892-recovery-quiet.groovy, mode0600/root; independent read confirms startup path absent and API quietingDown=false. No restart performed. Earlier hook-presence statements below are historical. No restored queue items, timers/SCM triggers, unfinished build.xml records, home startup hooks or image reference startup hooks were found before first startup.

## Images and credentials

Image work is tracked in DevOps-891. Current controller image registry.youdo.sg/sysadmins/devops-tools/jenkins master/latest digest sha256:458ac695b4114f0f3f837a3c99294c1a82e629ab2b53b1be2ea35c97a9425e71, master pipeline140773/build3222952/latest3222953 SUCCESS, deployed by approved recreation. Previous controller2-555-1-2 digest75671f1c… remains historical/rollback. Agent3355.v388858a_47b_33.6/latest digest sha256:2bd47b51f2e63488631a2de675870424d4a62066d33ebd4880751693318c9731, pipeline140739 succeeded and host digest verified.

Vault endpoint explicitly supplied by user: http://vault.service.vk-test.consul:8200; tooling token location ~/ai/current/.env, variable VK_VAULT_TOKEN. secret/ansible/yandex and common are readable, vkcloud document returns 404. Jenkins service account nomad uses key jenkins_client_docker_pass in secret/ansible/yandex on this VK Vault; pull access verified. The document name is historical and does not imply a live Yandex dependency. Remote Docker auth is protected 0600; agent secret retrieved in memory via authenticated Jenkins API and supplied to protected compose with no_log.

Persistent controller Git correction completed: MR17/source3419ae2d merged96a754a6, .dockerignore excludes .git. New image layer scan finds no root Git metadata/startup hooks. After recreation, /.git and credential.interactive are absent without manual correction; stored-credential branch lookup205/master present. Protected /data/jenkins/compose-devops-891-image.yml pins the verified digest and is0600. Canonical Ansible/base compose still use2-555-1-2; future base-only apply could restore the defective image, so approved deployment-source alignment remains separate follow-up. [Final execution](../log/2026-10-13-jenkins-devops-891-fixed-image-recreation.md).

## Backup and public route

Restored /data/backup/jenkins-test/jenkins_20261007.tar.gz from msk3-backup02.youdo.corp / 172.24.0.18. Archive is 1532460486 bytes, SHA256 699f78d187419d4f1b401d2c8da2c0144eba4082877b882f49551d00e84041dd; source and destination checksum/gzip verified. Retained controller archive /data/jenkins-recovery/jenkins_20261007.tar.gz, mode 0600. Changes after October 7 are outside this restore point.

Replacement balancer 10.18.20.97 (balancer-test01), supplied by the user on October13, is reachable over SSH as youdo; root login was denied. Nginx1.30.1 is active/enabled. Existing /etc/nginx/conf.d/build.youdo.sg.conf redirects HTTP to HTTPS and proxies to http://vk-ms1-jenkins-test.mcs.local/, resolving to10.18.26.8. Certificate location is /etc/nginx/ssl/wildcard.youdo.sg.crt and private key location is /etc/nginx/ssl/wildcard.youdo.sg.key; private key contents were not read. sudo -n nginx -t passed with server_names_hash sizing warnings. A forced-address HTTPS request to /login returned200 and X-Jenkins2.555.1 with normal TLS validation. The proxy uses HTTP1.1 and forwarding headers but sets Connection empty and has no explicit Upgrade directive; WebSocket forwarding is not verified. Balancer-local getent resolved build.youdo.sg to138.16.201.238; this supersedes the earlier local observation of178.154.207.53 but is not a global DNS or public end-to-end verification. No remote changes or reload occurred. See [balancer inspection](../log/2026-10-13-jenkins-devops-892-vk-balancer-check.md).

Subsequent workstation checks resolve build.youdo.sg to138.16.201.238 (default DNS and172.28.0.9, no AAAA); public/floating-IP assignment to the replacement balancer remains unverified. HTTPS to this address and forced10.18.20.97 both timed out after5seconds. Workstation route to10.18.20.97 is via172.30.63.1/tun0 with source172.30.63.11. Nginx listens on0.0.0.0:80/:443 and local forced127.0.0.1 HTTPS returns200. Confirmed iptables INPUT DROP/source allowlist omits172.30.63.0/24 (includes172.30.62.0/24 and historical10.16 networks) with no universal80/443 accept. Packet capture on ens3 confirmed SYN172.28.0.200:37610 ->10.18.20.97:443 during the timed-out forced request: the VPN path translates workstation source172.30.63.11 to172.28.0.200. This actual source and172.28.0.0 subnet are absent from the allowlist, confirming the VPN-path firewall block. Adding only172.30.63.0/24 would not match it. Subsequently the user authorized allowing only this actual source to TCP80/443 on ens3. The idempotently added runtime ACCEPT rule was verified, and forced-address workstation HTTPS returned200 with valid TLS. Ordinary DNS-path HTTPS still times out. The temporary rule was subsequently removed at explicit user request; its absence was verified and public HTTPS through corporate OpenVPN still returned200 from138.16.201.238. No persistence is needed for the removed rule. Enabled restore-iptables.service restores /etc/iptables-rules via /usr/sbin/iptables-restore --wait=5; that file was not changed. See [approved runtime firewall change](../log/2026-10-13-jenkins-devops-892-vpn-firewall-allow.md). See [VPN firewall diagnosis](../log/2026-10-13-jenkins-devops-892-vpn-firewall-diagnosis.md).

Jobs targeting unavailable Yandex infrastructure cannot be accepted as functional until their dependencies return. Airflow schedule still targets the obsolete Yandex DNS name; Oct11-13 runs failed. New source, backup SSH trust/authorization and /data/backup preparation remain pending. User explicitly deferred monitoring installation and Git publication; Loki is currently unreachable. Open work is tracked only in ~/ai/TODO.md.

## Sources

Recovery results, next restoration sequence, remaining work and automation proposals were posted to DevOps-892 as comment74-124647 on October13 and exact-text verified. Controller image source correction is locally implemented under DevOps-891 and context checks pass; source published in MR17, source pipeline140771 SUCCESS; MR17 merged SHA96a754a6 and master pipeline140773SUCCESS. Approved controller recreation and fresh runtime Git/API verification passed. See [source correction plan and approval ledger](../log/2026-10-13-jenkins-devops-891-exclude-git-metadata-plan.md).

[Current execution log](../log/2026-10-13-jenkins-devops-892-vk-recovery-execution.md), [approved recovery plan](../log/2026-10-13-jenkins-devops-892-vk-recovery-plan.md), [historical recovery audit](../log/2026-10-10-jenkins-devops-890-recovery-audit.md). Historical audit is useful for technical facts but has an incorrect ticket identifier.

## Public route verification after VPN diagnosis

Normal DNS/TLS curl --interface tun0 to https://build.youdo.sg/login returnedHTTP200 from138.16.201.238. Simultaneous ens3 capture on10.18.20.97 showed source45.159.210.228 to443, confirming the correct public route and corporate OpenVPN external source already allowed by the firewall. This supersedes earlier unverified public-IP/path statements. Ordinary requests still use personal TrustTunnel tun1/table880/source172.16.219.2 and time out. Main route already uses172.30.63.1/tun0, but policy30801 lookup880 precedes main. Local config now excludes138.16.201.238/32; parsing/unique-route checks passed, but client restart is pending and active routing is unchanged. No new remote firewall rule, persistence save or restart was authorized/executed. See [public route diagnosis](../log/2026-10-13-jenkins-devops-892-public-vpn-route.md).

## Browser confirmation (2026-10-13)

The user supplied a screenshot showing the authenticated Jenkins UI at https://build.youdo.sg. This supersedes the earlier browser-blocked observation. The recovery quiet-mode banner remains visible; no quiet-mode release, hook removal or functional build was authorized by this screenshot. Active TrustTunnel route/restart status was not independently checked.

## Actual job launch and controller GitLab acceptance

User approved temporary cancelQuietDown («Да»); API returned200. Authorized test-git build4 completed SUCCESS in1130ms, builtOn empty(controller), checkout revision a240575a6a360a908005fb3f1814fca13ee6e065. No Git authentication/network failure was found. Final API shows quietingDown=false, queue0 and116active plugins; AutoTest remains online with5executors, actual checkout untested. Recovery hook remains and will re-enable quiet mode on restart. The user subsequently approved restoring quiet mode («Да»); POST /quietDown returned200 and a fresh API read confirmed quietingDown=true. See [smoke execution](../log/2026-10-13-jenkins-devops-892-git-smoke.md) and [build4](https://build.youdo.sg/job/test-git/4/).

## Historical controller image merge and recreation checkpoint (superseded by final result below)

User approved merge and controller recreation for verification. MR17 merged with SHA96a754a6abe44c4049b61cee287ab07d1c46ef15; source noop CI140771 succeeded after slow preparation. Master image pipeline140773 build3222952 runs, latest3222953 is created; fixed-image publication/recreation not yet complete. Controller preflight quiet=true/queue0/active executor tasks0, jobs11; nodes online, data131GBfree, expected UUID/mounts/hook retained. Stored-credential GET parameter lookup confirms205branches/master before recreation. Exact provenance/digest guards and rollout helper prepared; fresh image and post-recreation acceptance remain pending.

## Current controller after fixed-image recreation

New containercc6f744294ff77471b765d30e543883ea738dc3108e0abb2b23734dc8a7758c4 uses digest458ac695…; all mount signatures, /data UUID and recovery-hook hash/mode preserved. API quiet=true, queue0,11jobs/116plugins, controller10executors and AutoTest5online. Public HTTPS200 verified through corporate OpenVPN. Earlier in-progress checkpoint sections above are historical; fixed-image recreation acceptance is complete.

## Tracker result synchronization

DevOps-891 existing recovery comment74-124638 was updated after explicit user request with the merged source fix, successful fixed-image pipeline/digest and recreation acceptance. Exact text was GET-verified after POST, updated1791910089885. The comment retains other recovery results and states the pending Ansible pin synchronization.

## Recovery comment reconciliation (2026-10-14)

The existing DevOps-892 comment `74-124647` omits late October 13 acceptance results and contains obsolete pending items. The reconciled replacement was published after explicit user approval and exact text was verified via GET. See [reconciliation log](../log/2026-10-14-jenkins-devops-892-comment-reconciliation.md).

## dynamic_deploy Restore review (2026-10-14)

User clarified Restore means the job stage. Live GET confirmed playbooks and inventory selectors. User narrowed scope to old yandex-test addresses and minimal deployment changes. Normal test5 Restore has no newly found address-edit requirement; live inventory targets are VK. Thick test/test1/test6 still have old SQL names in origin/master, with local unpublished VK replacements. General hardening is outside current scope; special autotest inventories remain old. No reset/clear task executed or repository changed. See [review](../log/2026-10-14-jenkins-restore-playbooks-review.md).

## test5 monolith deployment attempt (2026-10-14/15)

User-authorized dynamic_deploy5819 used latest-release pipeline139914 after all20 numeric image tags were verified published. All Restore enabled except B2B elastic; suggestions enabled; static/microservices disabled. Build failed on PG SSH host-key trust and balancer root SSH access; Rabbit purge also returned401 but was ignored. Deploy monolith and Post update were skipped. No retry performed. See [execution](../log/2026-10-14-jenkins-test5-release-deploy.md).

## test5 SSH credential alignment (2026-10-15)

User-requested public key of credential ssh installed for root on PostgreSQL10.18.26.39 and balancer10.18.20.97; existing keys preserved. Controller-origin SSH using that exact credential verified rootLogin/status0 on both. Restore PG DB now explicitly uses credentialsId ssh and hostKeyChecking false matching Nginx, exact script approved. No job retry or sshd setting change. Rabbit401 remains unresolved. See [access change](../log/2026-10-15-jenkins-ssh-credential-vk-access.md).

## PostgreSQL host-key flag correction after build5820

Repeated authorized build5820 failed on PG host-key verification despite applying credential ssh. Legacy hostKeyChecking=false is a no-op in installed Ansible plugin635.v34b_48e979c86. PostgreSQL now uses disableHostKeyChecking=true, exact updated script approved; no subsequent build yet. Nginx already sets env.ANSIBLE_HOST_KEY_CHECKING=False and reached cleanup successfully. Rabbit401 remains. See [repeat and correction](../log/2026-10-15-jenkins-test5-deploy-retry.md).

## test5 PG peer-authentication checkpoint

Third authorized build5821 passed PG SSH and failed local psql peer authentication because the reset task ran as root with -U postgres. Active PG16 pg_hba local rule118 requires peer; read-only command as Unix postgres succeeds. SQL-user execution adaptation remains pending branch approval; pg_hba unchanged. Monolith/suggestions have still not deployed. See [attempts and verification](../log/2026-10-15-jenkins-test5-deploy-retry.md).

## youdo.static VK migration audit

Jenkins Deploy static launches GitLab deploy_yandex_test stand job, which invokes SSR/Nomad and S3 delivery. SSR INTERNAL_URL/BuildAPI settings and inherited group8 Nomad endpoint still point to yandex-test; minimal adaptations needed before enabling WEB_STATIC. Current build5822 leaves WEB_STATIC false. See [static audit](../log/2026-10-15-jenkins-static-vk-deploy-audit.md).

## Build5822 final cause and static MR publication

Build5822 passed PG resets but failed monolith config upload at old buildapi.yandex-test.youdo.local/upload HTTP404; rescue notify timeout secondary. Monolith Nomad rollout/Post update/suggestions skipped. Static address commitf424127 published in [MR108](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/108) after explicit approval; shared BuildAPI correction covers observed stale URL. MR108 subsequently merged asf916ad19; project278 VK_TEST_NOMAD_TOKEN configured; build5823 passed BuildAPI upload and reached Nomad rollout, where service startup is blocked by mixed MessageBus assembly identities. See [logs](../log/2026-10-15-jenkins-test5-deploy-retry.md) and [static changes](../log/2026-10-15-jenkins-static-vk-deploy-audit.md).

## Monolith release assembly compatibility

Pipeline139914 selects MessageBus1.9.1 (DLL assembly1.0.0.0) with MassTransit1.8.1 (reference1.8.1.0). Exact consumed package hashes verified from build3225571. Build success does not establish runtime binding compatibility. Matching1.9.1 packages have consistent assembly references; no package/source changes authorized yet. See [diagnosis](../log/2026-10-15-jenkins-monolith-messagebus-assembly-mismatch.md).

## Static rollout and library correction (2026-10-15)

Static release139593 build chain succeeded; image master-2.917.139593 registry metadata verified. User-authorized test5 static deploy job3226694 succeeded157.5s. Monolith5823 endedFAILURE940155ms on DLL startup; corrected historical MassTransit1.8.1 package subsequently replaced in Nexus with binding probe/checksum verification. Monolith subsequently rebuilt through jobs3226699/3226700 with corrected package hash verified; direct test5 Nomad version3 deployment successful, both groups healthy and19service tasks running without restarts. No Jenkins deployment/Restore rerun; source changes forbidden. See [publication](../log/2026-10-15-nexus-messagebus-181-assembly-repair.md).

## Direct monolith startup accepted (2026-10-15)

User-authorized fresh release139914 rebuild cleared onlyproject18runnercache, artifact3226699success andDocker3226700success. All20numericimage digests changed. Direct Nomadjobyoudo-test5 version3 uses20verifieddigestrefs across21tasks; deployment9ee77925 successful, web/svc healthy1each,19service tasks running/restarts0. Representative MessageBus startup error absent. See [execution](../log/2026-10-15-jenkins-monolith-rebuild-nomad-restart.md).

## Full Jenkins deployment started (2026-10-15)

User-authorized dynamic_deploy5824 running with rebuiltmonolith139914/static139593, WEB_STATICtrue, priorRestoreselections retained, B2B/MICROSERVICESfalse andsuggestionstrue. Parametersmatch GETverified. Numericimagecache absent onall8eligibleclients, no cache mutation needed. FinalFAILURE onPostupdateAuthandgetcookies timeout to test5.youdo.sg/api/users/signin/; monolithNomadversion6 andstaticGitLab3226701/NomadSSR deployed successfully with healthytasks/restarts0. See [launch](../log/2026-10-15-jenkins-test5-full-deploy-with-static.md).

## Build5826 ignored errors and quiet-hook removal (2026-10-15)

Three Rabbit cleanup errors: queue listing401, list-construction type error, undefined queues_name at purge. Queue cleanup did not complete. Fourth ignored failure is nginx cache grep with no operands for xargs rm (rc123), not PostgreSQL. Recovery quiet hook moved outside startup with preserved hash/mode; quietingDown=false. See [diagnosis and execution](../log/2026-10-15-jenkins-build5826-errors-and-disable-quiet-hook.md).

Local Rabbit follow-up: user-authorized test5 clear.yml run using current local group_vars/all.yml succeeded with ok3/failed0/ignored0 and no401; queue listing and purge completed. Jenkins was not rerun, so Jenkins-specific effective variables remain unverified. See the diagnosis/execution log above.

## BuildAPI metadata gap after build5826 (2026-10-15)

Update buildsinfo still uses hardcoded buildapi.yandex-test.youdo.local URLs;404 is masked by curl without --fail. New BuildAPI /builds is empty and test5 missing. Ansible upload/static success does not create a current builds row. Build5826 SUCCESS therefore confirms deployment, not result publication. See [diagnosis](../log/2026-10-15-jenkins-buildapi-test5-missing-row.md).

## BuildAPI publication corrected (2026-10-15)

Update buildsinfo four base URLs now point to buildapi.dev.youdo.corp, curl has --fail --show-error and shell set -e. Exact script hash185031f5… and approval independently verified. Restored test5 current/history metadata from5826; GET and authenticated home HTML confirm test5/139914/139593. No build/deploy rerun. Full job XML byte equivalence after Jenkins serialization was not established; script equality was verified. See [execution](../log/2026-10-15-jenkins-buildapi-publication-fix.md). Earlier stale-URL findings are historical.

## Monolith-dependent microservices VK audit (2026-10-15)

Nine local/remote-master Monolith services inventoried; user excluded unused youdo.form, leaving8selected services. Required: docvalidation DNS typo, escrow router dc interpolation, shared v3 per-stand CI VK mapping and peer-compatible PG delegated tasks. Legacy Form CI/selector changes are outside scope. Fresh BuildAPI microservice catalog has only static; bootstrap via new service GitLab deployments before Jenkins recreate. Existing global VK Nomad Jenkins binding is present. Research only; no rebuild/deploy approved or performed. See [audit and inventory](../log/2026-10-15-jenkins-monolith-microservices-vk-audit.md).

## DevOps-899 implementation and rebuild checkpoint (2026-10-15)

User assigned per-stand microservice delivery to DevOps-899, approved all four branch/publication proposals (including corrected task names), merges, escrow release, fresh builds and automatic production deployments. Runtime preflight explicitly skipped. Initial30component builds succeeded. All eight services accepted through saved BuildAPI metadata, live Nomad source/image tags and rendered test5 rows. Follow-up Ansible110 fixes oldAnsible/remotePython compatibility; escrow51 permanently moves the shared router CI job toVK. Shared router13.8.12 runs healthy count1. Antifraud145 changes three runtime PG ports5433→5432; approved release23.8.7 at merged masterfb11521 completed pipeline140965 builds/tests and deploy3228068 successfully. Escrow13.8.12 recovered through Ansible111 routing-domain correction and four live monolith Host tags; deploy3228097 succeeded. Config master/preprod audited without DNS edits. No PgBouncer configuration or runner DNS settings were changed. See [execution and approvals](../log/2026-10-15-jenkins-devops-899-monolith-microservice-recovery.md).

## Per-stand microservice catalog seeded (2026-10-15)

DevOps-899: accepted eight-service test5 releases copied into BuildAPI deployment catalogs for test,test1-test7,test10-test15. Thirteen other stands received104CI records plus104links to their exact manual deploy jobs from the same source pipelines; source test5 unchanged. BuildAPI GET verification passed. These are prepared sources for future Jenkins recreate_microservices; seeding does not start deployments or populate live Nomad/Consul state. See [seeding evidence](../log/2026-10-15-jenkins-devops-899-monolith-microservice-recovery.md#other-stand-catalog-seeding-2026-10-15).

First-launch check for this seeded catalog: actual recreate_microservices playbook passed a local Ansible2.15.13 mock execution for all104manual jobs/13stands using /play, with no /retry/unexpected mutation. Absent Nomad jobs are tolerated; absent DBs are created. PG DocValidation clone source exists and had0activeconnections. Normal firstplays follow service DB recreation flags (no one-off skipdropdb variable). Real104deployments were not started by the check; exact Jenkins Ansible version remains unverified.

## Next per-stand iteration scope (2026-10-15)

From DevOps-A-33 excluding B2B/completed deployments and user-excluded MiniSape/Form: broadcast, cerberus2, escrow.walletone, featuretoggle, youdo.content, youdo.landings, youdo.trackingpixel and YouDo.Socket. Socket's accepted per-stand MR82 supersedes the article dynamic label. Separate frontend entry youdo-moderation uses its own CI/S3. Scope only; no implementation/deployment authorized by this list. See [candidate evidence](../log/2026-10-15-jenkins-next-per-stand-service-iteration.md).

Next-iteration scope corrected by user: add youdo.help, exclude escrow.walletone (alongside MiniSape/Form/B2B). Fresh current-master analysis identifies mandatory Content custom VK CI migration and Cerberus custom PG/absent-template blocker; six other service repos need no confirmed adaptations. See [test5 analysis](../log/2026-10-15-jenkins-next-test5-service-deployment-analysis.md). No builds/deploys triggered.

Next rollout execution: Content MR63 merged9714ed5/release2.5.12/pipeline140980; six unchanged releases plus moderation build pipelines140972-140978 launched. Cerberus excluded by user. Seven unrelated test4jobs blocked runners due psql pager under raw/become; exact cancellations approved and completed requests, then Ansible MR112 merged620607f disables pager in five invocations. Newtest5firstdeploys follow normal DB creation/recreation. See [rollout evidence](../log/2026-10-15-jenkins-next-test5-service-rollout.md).

## DevOps-899 next test5 iteration accepted (2026-10-15)

Seven selected Nomad services deployed: broadcast1.2.11, featuretoggle1.0.11, Content2.5.13, Landings1.3.35, trackingpixel1.0.5, Socket1.2.9, Help1.0.14. Moderation1.0.45 assets published to S3 with explicit prefix replacement approval. Current BuildAPI source/version metadata verified; Landings HTML absent by existing webEx_check=false design, Socket version-cell mapping absent, APIs correct. Broadcast finaldeploy3228256 healthy after localdevdocker/postgres:latest recovery; ContentMR64fixedcredentialaliases. Cerberus/MiniSape/WalletOne/Form/B2B excluded. See [execution log](../log/2026-10-15-jenkins-next-test5-service-rollout.md).

Recovery task comments updated and exact-GET verified on2026-10-15: Jenkins892/ES894 and per-stand899 reflect5826/5827 and acceptedtest5services. See [comment publication record](../log/2026-10-15-recovery-task-comment-updates.md). Issue states were not changed.

### Four additional stand deployments (2026-10-15)

User-authorized full dynamic_deploy builds test2 #5828, test3 #5829, test7 #5830, test8 #5831 launched with #5827 parameters; all observed running and parameters verified. Completion not yet established. [Launch evidence](../log/2026-10-15-jenkins-four-stand-full-deploy.md).

### Obsolete test8 removed (2026-10-15)

After5831, user cancelled test8: four stand-specific Nomad jobs and dedicated5GiBESvolume deleted; no matching jobs/activeallocations remain. Subsequent cleanup explicitly limited to BuildAPI: exact test8 documents removed from builds/allbuilds/ms_builds; shared resources and remaining data retained. [Evidence](../log/2026-10-15-jenkins-test8-cleanup.md).

Jenkins dynamic_deploy5832 FAILURE2026-10-15 for test/RESTOREtrue: master381391de5d8c21b58ea73f928b5b52c6a63d68b3 still uses old thick MSSQL endpoint, causing controller TCP1433 timeout to sql-test.ru-central1.internal in restartMSSQLSERVER; snapshot Restore never invoked. Controller DNS/TCP1433 succeeds for all3VK names/addresses. User-approved three-variable endpoint publication completed as cdb11b5522ec6c30fae9cd5086898ff70f2cd2ba / [MR113](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/113), source DevOps-897-point-large-mssql-to-vk to master; effective inventory and syntax/YAML/diff checks passed, pipelines[]. User explicitly authorized MR113 merge; fresh GET confirms merged cf88e42259787a8c6350771d17726bd4fcff3e30 and master SQL fields point at VK for all3stands. User subsequently reported successful playbook execution after the endpoint merge; endpoint fix accepted on that report, no independent new build/log verification. No local Git merge/switch; full workflow publication remains separate/pending. [Diagnosis and separate errors](../log/2026-10-15-jenkins-build5832-mssql-old-endpoint.md).

## DNS on controller and AutoTest (2026-10-16)

Controller host uses dnsmasq10.18.26.8 →10.18.20.3; controller container uses Docker127.0.0.11 with cached external127.0.0.53. Both resolve buildsinfo.vk-test.youdo.local → CNAMEbuildapi.dev.youdo.corp →10.18.26.60. AutoTest now uses dnsmasq on10.18.26.26 →10.18.20.3, with searchyoudo.local and Consul forwarding matching the controller. systemd-resolved is disabled. Host getent, dig through127.0.0.53, and agent-container getent resolve buildsinfo.vk-test.youdo.local to10.18.26.60. Applied existing dnsmasq role on2026-10-16; [live evidence](../log/2026-10-16-jenkins-autotest-buildsinfo-local-dns.md).


## VK Selenium and diagnostic access

BuildAPI VK operational kubeconfig also provides read access to Selenium: `/home/slnnk/ai-data/buildapi-vk/kubeconfig-ci.yaml` (mode0600, context `default/vk-ms1-k8s-test`), matched to project77 file variable `KUBECONFIG_DEV` (scope `kube-test`). Local exec auth plugin is `/home/slnnk/ai-data/buildapi-vk/bin/client-keystone-auth`; prepend that directory to PATH for `kubectl --kubeconfig ...`. Do not copy kubeconfig contents into notes. Selenium endpoint ingress is `selenium.dev.youdo.corp` →10.18.26.60, namespace `selenium`. Build3362 on2026-10-16 correlated its session-start EOF with KEDA scale-from-zero, registry DNS timeout and Chrome pods unschedulable on two workers; details and evidence: [Selenium incident](../log/2026-10-16-jenkins-selenium-vk-grid-session-eof.md).

## DevOps-903 nginx cache cleanup (2026-10-20)

Local one-line xargs `-r` fix validated for empty/matching/repeated search on the approved task branch from bf91d5b9; unrelated MSSQL edits preserved. Published as d26e37e/[MR122](https://gitlab.youdo.sg/sysadmins/automation-test-yandex/-/merge_requests/122), user-merged as master d9ee37a and fetched source verified; no live cleanup or rollout. See [task record](../log/2026-10-20-jenkins-devops-903-empty-nginx-cache-cleanup.md).
