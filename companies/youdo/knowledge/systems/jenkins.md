---
system: jenkins
status: verified
checked: 2026-10-13
tags: [jenkins, recovery, vkcloud]
---

# Jenkins infrastructure and recovery state

## Summary

Jenkins controller and AutoTest agent restored on VK hosts on 2026-10-13 under [DevOps-892](https://youtrack.youdo.com/youtrack/issue/DevOps-892). Controller is accessible internally at http://10.18.26.8/. Authorized checkout-only test-git build4 succeeded on the controller; quiet mode was restored after explicit user approval and API confirmed quietingDown=true. Persistent controller image Git correction was merged, published and verified after approved recreation; stored-credential branch lookup returns205/master. AutoTest actual checkout and downstream workflows remain untested. Later that day the user supplied replacement balancer 10.18.20.97: its existing Nginx route to the VK controller returned HTTPS 200 with normal certificate validation using a forced address. Public HTTPS at138.16.201.238 is verified through corporate OpenVPN. After the local TrustTunnel exclusion was prepared, the user supplied a screenshot confirming the authenticated Jenkins UI opens at https://build.youdo.sg; the screenshot does not independently establish the active client route. WebSocket forwarding remains unverified. Historical Jenkins notes incorrectly use DevOps-890, which is the Nexus task; do not carry their completion status into DevOps-892.

## Hosts and access

| Component | Host / address | Verified state |
| --- | --- | --- |
| Controller | vk-ms1-jenkins-test / 10.18.26.8 | Root SSH; Jenkins 2.555.1; 11 jobs; 116 active plugins; authenticated API works; quietingDown=true after approved restoration; queue empty at smoke completion; test-git4 SUCCESS |
| Agent | vk-ms1-jenkins-agent-test-01 / 10.18.26.26 | Root SSH; AutoTest online via WebSocket, 5 executors |

Bootstrap access is youdo with passwordless sudo. User authorized adding .ssh/id_ed25519.pub for root; completed and independently verified on both hosts. No key values retained here. Browser access requires network reachability to 10.18.26.8, such as the corporate VPN. Accounts and credentials come from the October 7 backup.

## Storage and runtime

Both hosts have Docker 29.9.0 and Compose installed through existing docker-compose -> docker Ansible roles. Docker and containerd data reside on the verified /data filesystems via guarded symlinks. Controller /dev/vdb is 150 GB, UUID 937fca4e-18b8-4bc1-a1a2-5b4d1e5931f4, approximately 131 GB free after deployment. Agent /dev/vdb is 10 GB, UUID b1457393-253d-4960-9278-b9b6ad40161a, approximately 7.8 GB free after image deployment. User approved current agent disk; cold-build workspace/cache growth remains untested.

Controller host JENKINS_HOME is /data/jenkins/data/jenkins. Recovery quiet hook is /data/jenkins/data/jenkins/init.groovy.d/devops-892-recovery-quiet.groovy, mode 0600; it will reapply quiet mode after a restart until explicitly removed. No restored queue items, timers/SCM triggers, unfinished build.xml records, home startup hooks or image reference startup hooks were found before first startup.

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
