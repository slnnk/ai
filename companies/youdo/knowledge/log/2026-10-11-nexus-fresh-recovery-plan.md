---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, recovery, ansible]
---
# Fresh Nexus deployment plan on recovery host

## Task

Prepare a fresh Nexus deployment without backups on `10.18.24.233` using existing automation-services roles and a separate data disk. The user explicitly approved runtime apply and requested the latest version. Approved service deployment completed; fresh Docker repository and CI-user initialization remain separate follow-up work.

## Context and findings

- Root SSH works with `-F /dev/null` and ECDSA host-key algorithm. Ubuntu22.04.5, RAM15Gi, root10G; `/dev/vdb`170G ext4 already persistently mounted at `/data`, UUID `4685cc2f-9753-4196-a9bf-68038195577c`. No Docker installed at inspection.
- GitLab base-image [job3217901](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3217901) passed the restored Docker bootstrap image stage and now fails at Nexus login with connection refused. Nexus availability is the next blocker.
- Existing `nexus.yml` uses base Linux, Nginx, docker-compose, Nexus and monitoring. Minimal external wrapper reuses only docker-compose, nexus and nginx; repository remains on `DevOps-890-update-jenkins-images` with unrelated Terraform/runner changes preserved.
- Nexus role binds `/data/nexus/nexus-data`, UID200, ports8081/3000/3003; Original proposal used former `sonatype/nexus3:3.70.4-java11-ubi`; after user correction external vars select latest verified `sonatype/nexus3:3.96.4`. JVM heap6Gi/direct6Gi on RAM15Gi follows prior configuration. Blank instance needs separate repositories/users bootstrap; role only installs service.

## Prepared files and checks

External `/home/slnnk/ai-data/nexus-recovery/deploy.yml`, `vars.yml`, `inventory.ini`: exact single root host; existing filesystem UUID/type/mount assertion; asserts old Docker/containerd paths absent or already matching expected symlinks; creates `/data/docker` and `/data/containerd` with safe links before package installation. No formatting or fstab/mount changes. Docker role's unsafe legacy `docker_symlink` variable is explicitly required to remain undefined.

Vars now use explicit latest Nexus tag3.96.4, compose directories, default Nexus Nginx proxy, package nginx, empty vhost/upstream/blocked-IP lists. Resolver comes from current host resolv.conf. Nginx unblock script is excluded with `--skip-tags nginx_unblock_ip`. Existing roles install Docker CE and Composev2.27.1, service and HTTP reverse proxy. Docker mirror is public mirror.gcr.io; old Nexus insecure-registry entries are not pull mirrors.

Syntax-check passed and list-hosts selected exactly one host. No remote check-mode was executed. After explicit approval, root agent started apply, initial session51374 stalled during SSH transport before installation; current session63486 proceeds with the bounded-MSS relay, final apply exited0, see completed verification below. No repository files, secrets or Git state changed during preparation. Approved apply may now change the specified host runtime. Command prepared for review:

```bash
ANSIBLE_ROLES_PATH=/home/slnnk/git/automation-services/roles ansible-playbook -i /home/slnnk/ai-data/nexus-recovery/inventory.ini /home/slnnk/ai-data/nexus-recovery/deploy.yml --skip-tags nginx_unblock_ip
```

## Risks and limits

Fresh-host check-mode can fail on not-yet-installed tools or directories. Full Nginx role copies existing static credential file `roles/nginx/files/.htpasswd`; values were not read or printed, and default Nexus HTTP vhost does not use it. No Vault credential is required by the selected roles. Deployment does not initialize Docker group/hosted repositories or the CI user. Follow-ups are tracked only in `~/ai/TODO.md`.

## Approved latest-version apply

The user approved deployment and requested the latest version. Sonatype release notes identify3.96.4; Docker Hub latest and3.96.4 resolve to matching digest `sha256:5f48f9085096e96f4111ec07d79d57ca5a4a1da5a2003a3028a0b60c62bea7d1`. Root updated external vars, syntax-check passed, and initial apply session51374 stalled during SSH transport. Current apply session63486 uses the locally prepared MSS1100 relay; final runtime verification passed for service/UI; Docker repository endpoint remains uninitialized.

Current Docker image contract remains UID200 with writable `/nexus-data`; template uses supported `INSTALL4J_ADD_VM_PARAMS` and persistent Java prefs. Fresh data avoids old database migration requirements. Sources: [official Docker image](https://github.com/sonatype/docker-nexus3), [runtime configuration](https://help.sonatype.com/en/configuring-the-runtime-environment.html), [installation](https://help.sonatype.com/en/install-nexus-repository.html), [3.96.x release notes](https://help.sonatype.com/en/sonatype-nexus-repository-3-96-0-release-notes.html).

## Transport workaround and apply progress

Ansible setup stalled on this VPN path despite successful short raw commands; initial attempts were interrupted before installation. Local `/home/slnnk/ai-data/nexus-recovery/ssh_mss_proxy.py` sets TCP_MAXSEG1100 before connect and relays standard input/output without changing SSH authentication or host-key checks. A read-only 64KiB transfer returned exactly65536 bytes. Current approved apply session63486 completed Gathering Facts and the exact existing data-disk UUID assertion, created `/data/docker` and `/data/containerd` and the `/var/lib` symlinks, then reached system-package installation. This records progress, not completed deployment. No filesystem formatting, mount or fstab changes occurred. Only the root agent executed the approved runtime apply.

## Completed approved deployment

Apply session63486 exited0: `ok=53 changed=36 unreachable=0 failed=0 skipped=27`. Repository remained unchanged. Docker29.9.0 and Nginx are active; Docker root `/data/docker`, containerd `/var/lib/containerd` links to `/data/containerd`.

Container `nexus-nexus-1` runs `sonatype/nexus3:3.96.4`, repository digest `sha256:5f48f9085096e96f4111ec07d79d57ca5a4a1da5a2003a3028a0b60c62bea7d1`, matching verified Docker Hub latest. Bind mount `/data/nexus/nexus-data:/nexus-data`, restart count0, memory4.25GiB of15.61GiB. Local8081 REST status and writable checks HTTP200; Nginx UI HTTP200; external `http://msk3-nexus.youdo.corp/service/rest/v1/status` HTTP200. Root filesystem2.3G used/7.3G free; data1.1G used/157G free.

`/v2/` returns HTTP502 because this fresh instance has no Docker repositories/connectors yet. This is an uninitialized dependency, not failed Nexus process startup. Initial admin password exists only at `/data/nexus/nexus-data/admin.password`; value was not read or recorded. Docker repositories/connectors, Docker Bearer Token realm and CI-user credentials require a new explicit initialization approval; no such initialization or CI retry was performed.

## Onboarding EULA permission diagnosis

User reported wizard step3 EULA permission error and disconnected UI. Read-only logs show Firefox admin session, then `PUT /service/rest/internal/ui/onboarding/change-admin-password` at19:51:22 returned HTTP204 as admin. Following `GET /service/rest/v1/system/eula` at19:51:26 and19:51:33 returned HTTP403 with user `-` (unauthenticated); UI static files remained HTTP200. Nexus stayed running, restart0, OOMfalse and REST status HTTP200.

Conclusion: browser authentication was lost after the password change, consistent with EULA endpoint requiring administrator access. Recommended reload and sign in as admin with the new password the user just set, then resume wizard. No server changes, password reads, session-cookie copying or API EULA acceptance occurred. [Official EULA API](https://help.sonatype.com/en/eula-rest-api.html) requires `nexus:*` administrative privilege for GET/POST; this diagnosis does not accept the agreement on the user's behalf.

Separately, Go HTTP client searches against docker-hosted returned HTTP429 approximately every7 seconds; Nexus rate-limit key identifies `user::cleaner`. This is a separate client's authentication/rate-limit issue, not the admin wizard error. Cleaner credential review is covered by the existing fresh-instance CI-user/credential initialization action in `~/ai/TODO.md`; no duplicate task added.

## Browser disconnect: request-size-dependent path failure

Installed public JavaScript `NX.controller.State` shows the disconnect dialog after four consecutive polling XHR transport errors (except HTTP402), resetting the counter on success. The user's F12 evidence identifies the failing polling request as POST with Content-Length5310, `NS_BINDING_ABORTED` and no HTTP status; successful unrelated ExtDirect calls do not disprove this transport failure.

Read-only controlled HTTP test sent a large request with6000-byte `X-Diagnostic-Padding`: default TCP MSS timed out after7.11s with0 bytes received; MSS1100 completed in0.23s with HTTP200 and591 header bytes. Earlier45KiB response with a small request completed using either MSS. These comparisons verify a size-dependent outgoing-client-request transport failure; they do not identify the precise packet-dropping VPN/gateway component. This disconnect is separate from the previously corrected post-password-change authorization issue.

Local `/home/slnnk/ai-data/nexus-recovery/fix-http-mss.yml` passed syntax-check and awaits explicit user permission. Proposed bounded temporary rule checks for the exact existing iptables rule before adding OUTPUT TCP source-port80 SYN (masked SYN,RST) TCPMSS set1100. It changes only HTTP80 connection MSS advertisement; no SSH/8081 changes or service restarts. Rule is not reboot-persistent and has NOT been applied at this update. Optional telemetry `appt.*` cookie warnings do not appear in the installed polling/disconnect decision logic.

## Diagnostic direction: VPN capture first

The user preferred inspecting traffic on the VPN server before applying the proposed HTTP MSS rule. No MSS firewall rule was applied; its permission request is deferred. Read-only topology research finds an August3 corporate OpenVPN record for `ipsec-vm`10.16.20.3, tunnel172.30.62.1, config `/etc/openvpn/server.conf`; this is not proof of the recovered current endpoint. Current local route uses tun1 MTU1500, source172.30.63.8 and gateway172.30.63.1; Nexus sees browser source10.18.20.3. Current VPN host/interface identification and header-only traffic inspection are the next diagnostic steps. No packet capture or VPN configuration change was performed by delegated KB research.

## Recovered VPN access and paired header capture

User confirmed VPN/gateway recovery at `10.18.20.3`. Root SSH rejected authentication; `youdo` login and `sudo -n` work, hostname `ipsec-vm`, StrongSwan running with GRE interfaces. First connection accepted the new host key via TOFU into local known_hosts; no remote SSH/root configuration changed. Prior10.16.20.3 map is historical.

Root ran simultaneous35-second text captures, header-focused `tcpdump -s96 -v -S` without ASCII/hex output or pcap file: `/home/slnnk/ai-data/nexus-recovery/vpn-tcp-headers.txt` (any) and `nexus-tcp-headers.txt` (ens3). VPN148 packets, Nexus72 packets, both report0 kernel drops. Delegated analysis read only those local text artifacts. No firewall MSS rule applied.

Failed controlled flow50428: client172.28.0.200 SYN MSS1358 enters gre_selectel, gateway NAT source10.18.20.3 forwards SYN with MSS1310; server1460 SYNACK is clamped to1310 on GRE egress. Request starts at expected seq4267804146, but capture first receives only final911 bytes seq4267809338:4267810249. Missing first5192 bytes are already absent at GRE ingress and also absent at Nexus; Nexus repeatedly ACKs4267804146 until client FIN about7 seconds later. Gateway forwards the observed tail correctly. Thus loss occurs before the captured gateway GRE ingress, not between its ens3 and Nexus.

Successful comparison flow49224 advertises MSS1100, unchanged through gateway. Complete6103 request bytes seq4265393284:4265399387 arrive and are acknowledged; Nexus sends591 response bytes. SYNACK on return GRE still advertises1310, consistent with client-side outgoing segmentation making this comparison work. Capture packet lengths2176/1751 may reflect GRO/GSO coalescing and must not be treated as wire segment sizes. No IP fragment records observed. Exact upstream dropping device remains unidentified; additional upstream/GRE-path evidence is needed. Browser traffic from172.24.0.12 also traverses gre_selectel and receives MSS clamp1310.

## Local nested TrustTunnel routing finding

The user confirmed Nexus UI works without local TrustTunnel. Actual corporate OpenVPN profiles specify UDP `msk-vpn.youdo.sg:1194`, resolving45.159.210.228. Before local edit, route lookup selected TrustTunnel tun1/table880/source172.16.219.2, directly proving nested corporate-VPN transport. User authorized adding only endpoint `/32` to local TrustTunnel excluded_routes; parse/exact diff checks passed. User restarted TrustTunnel;45.159.210.228 now routes directly viaWiFi192.168.192.1, confirming active exclusion. Corporate VPN is currently disconnected:10.18.24.233 also selects WiFi rather than the corporate tunnel; reconnect before UI verification. No gateway/Nexus MSS rule or remote configuration changed. Personal-layer details: [client routing log](../../../../personal/knowledge/log/2026-10-11-trusttunnel-client-corporate-vpn-exclusion.md).

## Final nested-VPN transport verification

After user reconnected corporate VPN, simultaneous route checks show public corporate endpoint45.159.210.228 directly viaWiFi192.168.192.1; Nexus10.18.24.233 via172.30.63.1 devtun1 source172.30.63.6; public1.1.1.1 viaTrustTunnel tun0/table880 source172.16.219.2. Interface names changed with reconnect; roles are identified by routes, not names.

Identical6000-byte-header HTTP test now passes with default MSS: HTTP200,591 bytes,0.06s (previously7s timeout/0 bytes). MSS1100 comparison also HTTP200/0.05s. Nexus UI GET `http://10.18.24.233/` returns HTTP200. Local endpoint exclusion fixes the reproduced transport failure with both VPNs active; no firewall/MSS or remote-network changes were applied. User should refresh the browser and confirm its UI symptom is gone; browser-session behavior itself is not yet independently verified. Nexus repository/realm/CI-user initialization remains separate pending work.

## Prepared repository and CI-user API plan

User confirmed browser UI works after the local TrustTunnel exclusion. Existing admin authentication succeeds using `NEXUS_ADMIN_PASSWORD` stored only in `~/ai/current/.env`; no value recorded. Read-only resource GETs show seven fresh default Maven/NuGet repositories, default blob store with40 blobs, active realm `NexusAuthenticatingRealm`, and no gitlab user. GitLab group8 variables identify CI username `gitlab`, existing password present, internal host `msk3-nexus.youdo.corp` and public `nexus.youdo.com`; values remain private runtime inputs.

Local `/home/slnnk/ai-data/nexus-recovery/api-plan.json` references eight separate JSON payload files. Payloads recursively checked against downloaded OpenAPI3 schema for required fields, known property names, types/enums and nested objects. Proposal, not applied: create File blob stores docker-hosted/docker-cache with relative paths under existing `/nexus-data/blobs`; Docker hosted docker-hosted onHTTP3003/writePolicyALLOW; Docker Hub proxy docker-hub/indexHUB with remote registry-1.docker.io; group docker onHTTP3000 with hosted+hub members; preserve existing authentication realm and add DockerToken; create ci-docker role; create gitlab user with existing CI password injected at runtime.

Role privileges are browse/read for all three Docker repositories plus add/edit only hosted; no admin or delete. User service email `ci@youdo.com` is a required-field placeholder identifier, no message is sent. Proxy supplies required storage, Docker, dockerProxy, proxy/cache and HTTP client structures. Docker v1 disabled and forceBasicAuth true. Actual privilege IDs must be confirmed through live GET after repositories exist; realm list must be reread before PUT if state changes. Eight external operations remain pending explicit user approval; no repository/user/realm/blob mutations were performed by plan preparation.

## Approved repository and user initialization completed

User approved the prepared plan with Docker Hub proxy excluded. Applied and GET-verified File blob stores docker-hosted/docker-cache; hosted docker-hosted onHTTP3003 with writePolicyALLOW; group docker onHTTP3000 with ONLY docker-hosted member. No docker-hub proxy created. DockerToken realm enabled while preserving NexusAuthenticatingRealm. Role nx-docker (renamed from historical ci-docker) has six privileges: browse/read on two repositories, add/edit only hosted. User gitlab is active with password matching the existing GitLab CI variable; values were not printed or recorded.

Initial apply stopped when privilege discovery expected field id but the API uses name. Corrected local execution logic resumed with checks of existing configurations and exited0. This is verified configuration/user initialization, not yet successful Docker login: external `/v2/` challenge currently presents Basic rather than Bearer and authentication checks continue. No CI job retry or image push was performed by this initialization.

## Final internal CI authentication verification

Local `verify_ci_login.py` checked Docker `/v2/` headers and authenticated GET with the existing GitLab CI credentials: internal `msk3-nexus.youdo.corp` returns HTTP200. Unauthenticated challenge is Basic; active DockerToken realm was independently verified. Basic challenge does not prevent successful current internal credential authentication. This is endpoint/credential verification, not a claim that Docker CLI login or a CI job was executed.

Public `nexus.youdo.com` redirects to HTTPS and then hits a15-second read timeout from the workstation. No external DNS/TLS changes were made. Public availability remains a separate limitation; internal CI endpoint is verified and does not depend on this public check. No CI retry or image publish occurred.

## CI role renamed after explicit user approval

User explicitly requested role ID and name `nx-docker`, analogous to built-in role names. Root executed `rename_ci_role.py`: created `nx-docker` with the same six privileges, updated active user `gitlab` to role `nx-docker`, verified the user assignment and exact privileges with GET, deleted historical `ci-docker`, and verified its absence. Initial user PUT returned HTTP400 because required `source` was missing; the corrected request included source and reused the already verified new role. Final execution exited0. No additional privilege, password, repository or realm changes were made.

## Maven blob-store separation proposal (not applied)

Read-only API inspection verified all four existing Maven repositories have no assets: each asset response had `items: []` and `continuationToken: null`. They currently use blob store `default`. Local proposal `/home/slnnk/ai-data/nexus-recovery/maven-plan.json` preserves existing repository names, policies, remote URLs and group members while separating storage: File blob store `maven-hosted` for release/snapshot hosted repositories, and `maven-cache` for Maven Central proxy and public group. The existing `default` blob store and NuGet repositories remain unchanged. Root checked the filtered POST payloads against required schema fields. Deleting/recreating the four Maven repositories and creating the two blob stores is a prepared proposal only: user approval is pending and no external mutation has been performed for this plan.

## Android Maven proxy proposal supersedes Central-only plan (not applied)

The initial Central-only Maven proposal is superseded. Read-only local checkout `android-youdo4` is clean on `DevOps-833-fix-hotfix`, HEAD `227f7518c3` dated2026-08-13. Root independently checked live GitLab `develop`: root `build.gradle.kts` repository declarations at lines3 (buildscript) and35 (allprojects), plus `buildSrc/build.gradle.kts` line16, all use `https://nexus.youdo.com/repository/maven-public/`. Live dependency differences include Mindbox2.15.4, Tinkoff `ru.tinkoff.core.tinkoffauth:tid:1.3.1`, removal of Facebook login and addition of `me.saket.telephoto:zoomable-image-coil3:0.19.0`. No Gradle task, build or repository edit was performed.

Updated local `/home/slnnk/ai-data/nexus-recovery/maven-plan.json` proposes File blob stores `maven-hosted` and `maven-cache`: retain releases/snapshots hosted repositories and six proxies (existing Central plus google/huawei/rustore/jitpack/cyberity); `maven-public` has eight members (two hosted, six proxy). All proxies use `maven-cache`; hosted repositories use `maven-hosted`. Previous repository names, policies and applicable URLs are preserved; new proxy names are proposed names, not recovered historical names. The existing default blob store and NuGet repositories stay unchanged. User approval is pending; no Maven API mutation was performed.

| Needed artifacts | Proposed upstream | Evidence |
|---|---|---|
| AGP8.13.2, AndroidX, Google/Firebase | `https://dl.google.com/dl/android/maven2/` | [Android documentation](https://developer.android.com/build/remote-repositories); exact AGP8.13.2 POM GET200 XML |
| AGConnect1.9.5.301 and Huawei plugins/HMS | `https://developer.huawei.com/repo/` | [Huawei documentation](https://developer.huawei.com/consumer/en/codelab/HMSPreparation/index.html); exact agcp1.9.5.301 POM GET200 XML |
| RuStore review0.1.6 | `https://nexus-external.rustore.ru/repository/maven-rustore-exposed/` | [Current official installation](https://www.rustore.ru/help/en/sdk/reviews-ratings/kotlin-java/10-0-0); exact POM200 XML, AAR200 ZIP, metadata200 lists0.1.6 |
| PhotoView2.3.0 | `https://jitpack.io/` | [PhotoView README](https://github.com/Baseflow/PhotoView#dependency); exact POM200 XML |
| Cyberity mobile SDK1.31.2 | `https://maven.cyberity.ru/repository/maven-public/` | [Vendor installation](https://developers.cyberity.ru/android-sdk/android-sdk/); workstation connection timeout20s and Nexus-host connection timeout12s/HTTP000; upstream connectivity unresolved from both locations |

The old RuStore `https://artifactory-external.vkpartner.ru/artifactory/maven` URL returns404 HTML for POM and metadata; current primary documentation identifies the migrated upstream above. No SDK version change is needed for review0.1.6. Exact Central POM GETs returned200 XML for Tinkoff1.3.1, Mindbox2.15.4, Jivo2.6.0 and OK2.1.8. AppMetrica and Mindbox official installation documentation uses Central, so separate vendor proxies are unnecessary. This confirms selected artifact availability, not full transitive resolution or a successful Android build.

Read-only proposal validation: root finalized `maven-plan.json` with two blob stores, two hosted repositories, six proxies and one group. Recursive OpenAPI validation passed; optional null fields from GET responses were omitted from POST payloads. Cyberity remains an unresolved upstream connectivity limitation from both workstation and Nexus host. No Maven state changes were performed.

## Approved Maven configuration applied; authentication proposal pending

After explicit user approval, root ran `apply_maven.py` successfully (exit0): created File blob stores `maven-hosted`/`maven-cache`; deleted/recreated the four verified-empty Maven repositories preserving policies; created google/huawei/rustore/jitpack/cyberity proxies. Public group contains eight members (two hosted, six proxies including Central). GET verified each repository's exact storage, Maven, proxy and group configuration. Authenticated real POM GETs through public group returned200 XML for Central Jivo2.6.0, Google AGP8.13.2, Huawei agcp1.9.5.301, RuStore review0.1.6 and JitPack PhotoView2.3.0. Cyberity upstream connectivity remains unresolved; public `nexus.youdo.com` HTTPS availability is a separate limitation. No Android/Gradle build or CI retry was executed. Earlier proposal-only sections describe chronology; the Maven repository configuration above is now applied.

Live GitLab project411 `master` matches inspected autotest-core checkout configuration; project79 `develop` matches inspected Android repository URL declarations. Both dependency repository blocks have no credentials. Autotest-core dependency block additionally uses Maven Central and `https://repo.jenkins-ci.org/releases/`; its publishing block uses internal `maven-snapshots` with project properties `nexusUser`/`nexusPassword`. CI supplies `NEXUS_MAVEN_USER=maven` and `NEXUS_MAVEN_PASS` inherited from group34 `team-youdo-testers`; only variable names/location and nonsecret username are recorded. Android `NEXUS_CREDS` uploads APK/version into raw-private and is separate from Maven downloads.

Current anonymous configuration is disabled (`enabled:false`, userId `anonymous`, realmName `NexusAuthorizingRealm`); the default anonymous user has `readOnly:false` and role `nx-anonymous`. Unauthenticated Maven GET returns401; user `maven` does not yet exist. Local `maven-auth-plan.json` is a prepared, unapplied proposal: create `nx-maven-read` with Maven wildcard browse/read; create `nx-maven` extending read plus snapshot add/edit; create active user `maven` using the existing group34 CI password at runtime; replace existing anonymous user's roles with the Maven read role and enable anonymous access. This authentication change requires user approval and has not been applied.

## Maven CI user and roles applied; anonymous access unchanged

User explicitly authorized creation of Maven user and roles only. Root executed `create_maven_user.py` (exit0): role ID/name `nx-maven-read` grants `nx-repository-view-maven2-*-browse` and `nx-repository-view-maven2-*-read`; role ID/name `nx-maven` inherits `nx-maven-read` and adds `maven-snapshots` add/edit privileges. Active user `maven` has role `nx-maven` and uses the existing GitLab group34 `NEXUS_MAVEN_PASS` at runtime in memory only. GET verified user and both exact role configurations; authenticated Jivo2.6.0 POM GET through public group using these CI credentials returned200 XML. GitLab variables were unchanged. Anonymous access remains disabled: enabling anonymous was neither approved nor applied. Android and autotest-core dependency blocks still specify no credentials, so their dependency authentication mechanism remains a separate decision; authenticated publishing identity is now initialized. No repository edits or CI/build execution occurred.

## Current Maven role consolidated after user clarification

User clarified that no read-only consumers need a separate Maven read role. Root ran `consolidate_maven_role.py` (exit0), first verifying that only `nx-maven` inherited `nx-maven-read` and no other users or roles directly depended on the read role. Current role ID/name `nx-maven` now has four direct privileges: Maven wildcard browse/read and maven-snapshots add/edit, with `roles: []`. GET verified exact permissions; historical `nx-maven-read` was deleted and verified absent; user `maven` remains assigned `nx-maven`. Effective permissions did not change. Anonymous remains disabled and no anonymous change was authorized. Earlier two-role sections record historical steps, not the current role model. Company Nexus preference: use the minimal role model and introduce separate read roles only when an actual consumer needs one.

## Pending dependency-auth implementation and public endpoint limits

Read-only autotest-core CI inspection confirms `.gitlab-ci.yml` runs `gradle :jar` first without `-PnexusUser`/`-PnexusPassword`; only the second publishing command receives those properties. A future authorized credential-based Maven download change must cover both the dependency repository credentials (same project properties as publishing) and credentials available to the first jar command, or supply appropriate external Gradle properties. Merely adding a credentials block would not make CI work. No repository edits were authorized or made.

Latest public endpoint checks: HTTPS `nexus.youdo.com/service/rest/v1/status` quickly returned404; the exact previously cached Jivo2.6.0 POM URL timed out after10s/HTTP000. Internal authenticated Maven reads returned200 earlier. Public availability remains unresolved; the404 alone does not establish that artifact downloads work or that the service is down.

## Public LB route preflight (2026-10-12; deployment pending)

User approved reuse of automation-services branch `DevOps-890-update-jenkins-images` and the Nexus backend change. Root edited only the shared Nexus vhost template and public-balancer inventory variable to target `10.18.24.233`; these local edits are not yet deployed or published. User independently reloaded nginx. Live public LB `root@172.28.0.141` / `sc-lb-pub01.youdo.corp` / public92.53.80.147 previously logged old upstream10.16.24.23 although current hostname lookup resolves10.18.24.233. After user reload, route to10.18.24.233 still selects public gateway92.53.80.145 viaeth1 with source92.53.80.147; TCP80/8081/3000 and public POM timeout remain unresolved. No route/firewall change was performed.

Read-only VPN inspection at `youdo@10.18.20.3` confirms gre_selectel address10.0.30.2/32, underlay local10.18.20.3, remote5.188.184.67, peer route10.0.30.1; routes for172.28.0/24,172.24/24,172.29/24 and172.31/16 use the tunnel. Older team topology docs identify peer5.188.184.67 as FortiGate ne1260 with LAN172.24.0.1; historical GRE10.0.24 endpoints are not current. They show sc-gateway2(172.28.0.200) reaching FortiGate via172.28.0.4→172.24.0.203→172.24.0.1, and identify its own GRE as KZ-only. No evidence establishes172.28.0.1 as the same FortiGate device. Route next-hop and persistence must follow verified LB private-network topology; blindly routing via sc-gateway2 is not justified.

## Verified private gateway and temporary host-route proposal (2026-10-12)

Root read-only verification on `root@172.28.0.200` / sc-gateway2 shows Nexus10.18.24.233 routed via172.28.0.1 deveth0 with source172.28.0.200. TCP80 connects and REST status GET returns200. Live gateway GRE is `gre_gcp`, local10.0.34.1, peer10.0.34.2, remote34.179.163.161; no Selectel GRE is present there. Repository gateway configuration remains historically different, so it is not an authoritative live-tunnel map.

Local `/home/slnnk/ai-data/nexus-recovery/public-lb-route-plan.json` proposes one temporary host route on public LB172.28.0.141: `10.18.24.233/32 via172.28.0.1 deveth0`. Not applied; persistent configuration remains to be selected after verifying the existing LB network manager and successful reachability. Two approved automation-services backend edits are local only: public-balancer variable targets10.18.24.233 and shared template renders all six proxy destinations with preserved hostname fallback for other groups. Render and `git diff --check` passed. No deployment, commit or publication has occurred.

Daily ai-sync retry for2026-10-12 failed at pull/rebase because KB changes are unstaged; root informed the user. No manual git mutation, stash or commit was used to bypass it.
