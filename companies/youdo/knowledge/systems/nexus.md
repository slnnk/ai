---
system: nexus
status: verified
checked: 2026-10-13
tags: [nexus, recovery, ansible]
---
# Nexus server and recovery state

## Summary

Fresh Nexus3.96.4 deployed on `10.18.24.233` after explicit approval using existing automation-services roles and separate `/data`. Docker, Maven and NuGet repositories and compatible service identities are restored; public HTTPS reads were verified. NuGet recovery now confirms all 143 required package/version pairs across 52 package IDs through public metadataHTTP200, using historical CI retries and separately approved exact-source fallback uploads. Service restore and exhaustive transitive checks are deferred. Temporary anonymous access remains enabled by user request; disabling it and remaining npm/other recovery work are tracked in `~/ai/TODO.md`. Evidence: [deployment](../log/2026-10-11-nexus-fresh-recovery-plan.md), [NuGet publication recovery](../log/2026-10-12-nexus-next-library-recovery.md).

## LDAP authentication and authorization enabled (2026-10-13)

Nexus uses `FreeIPA` at `ipa6.youdo.corp:636` with LDAPS and the explicitly approved FreeIPA CA in its built-in truststore. Bind credentials are accessed only through `SELECTEL_PROD_LDAP_NEXUS_USER` / `SELECTEL_PROD_LDAP_NEXUS_PASSWORD` in `~/ai/current/.env`. Directory base `dc=youdo,dc=corp`; users `cn=users,cn=accounts`, `inetOrgPerson`, uid/cn/mail; static groups `cn=groups,cn=accounts`, `groupOfNames`, cn/member, full user-DN member format. Direct group membership verified; no nested groups observed.

Mappings use local role IDs matching FreeIPA groups: `nexus-users` grants wildcard repository browse/read/add/edit only; `nexus-admins` inherits `nx-admin`. Current/future repositories are covered. Active realms exactly `NexusAuthenticatingRealm`, `DockerToken`, `NpmToken`, `LdapRealm`. Existing local roles, active local admin/CI identities and temporary anonymous settings were preserved. LDAP connection and mapping tests passed; user confirmed administrator LDAP login. Final GET verification passed11checks; LDAP artifact publication was not tested. See [applied configuration, approvals and rollback](../log/2026-10-13-nexus-ldap-enabled.md). User-requested LDAP update added to existing DevOps-890 comment 74-124640; exact text GET-verified.

## PyPI recovery stage 1 applied (2026-10-13)

After explicit user approval "Сделай 1", Nexus File stores `pypi-hosted`/`pypi-cache`, hosted `pypi-private` (`ALLOW_ONCE`, strict validation), proxy `pypi-proxy` (upstream `https://pypi.org/`, `/simple`) and group `pypi` (private before proxy) were created. CI user `pypi` is active with sole role `nx-pypi`: PyPI browse/read and hosted add/edit. Existing protected group `data` CI `PYPI_USERNAME=pypi` has no subgroup/publisher overrides; the matching existing `PYPI_PASSWORD` was used in runtime memory only.

Independent read-only verification confirms exact settings and valid CI index authenticationHTTP200; invalid credentials401. Previously existing repositories, blob configurations, users/roles, realms and anonymous settings were preserved. Only dynamic blob `availableSpaceInBytes` is excluded from preservation comparison. Evidence: `~/ai-data/nexus-pypi-recovery/pypi-create-verification.json` and before snapshot; apply/verify helper `restore_pypi.py`.

The user changed DNS: authoritative `dig @172.28.0.9` at17:29MSK returns `pypi.youdo.local` → `10.18.24.233`, TTL3600. Initial workstation resolution to former Nexus10.16.24.23 and timeouts are historical; independent DNS query confirms the new address, while workstation default resolver127.0.0.53 still returns10.16.24.23 and ordinary HTTP times out. Forced new-IP requests with Host:pypi.youdo.local verified private/group simple indexes200 and /simple/301 to the group index; existing nginx GET routes need no change. POST publication mapping, resolver propagation, exact missing artifact paths and runner-side access remain to verify. No library publication or CI retry was run. Preserve exact frozen lock URLs/hashes; original wheels may be needed.

Group data audit covers all62projects including subgroups/archive:9PyPI publishers and32canonical consumed versions. Publishers are basis, aio-service-client, eventum, basis-fastapi, toster, metronom, basis-aiohttp, iss under data/python-libraries, plus data/castle. CI uses PYPI_REPOSITORY/PYPI_USERNAME/PYPI_PASSWORD and Make aliases YOUDO_PYPI_*. Extraform retry3222248 blocks on locked youdo-basis10.0.2; deployed Nomad refs require separate inventory. See [plan, applied stage and data library inventory](../log/2026-10-13-nexus-pypi-recovery-plan.md).

## Basis PyPI library restored (2026-10-13)

`youdo-basis==10.0.2` wheel and sdist were rebuilt from unchanged original tag with historical hatchling1.27.0/uv-dynamic-versioning0.5.0, published after approval and verified through Nexus component metadata: both SHA256 exactly match frozen consumers. CI retry3222818 stayed pending after approved project207 instance-runner enablement and was canceled for approved local fallback; scheduling cause remains undetermined. Runner171/172 host DNS resolves new10.18.24.233 and legacy index reads200. First extraform archive-source local build completed frozen dependency install then failed on missing Git metadata; approved existing-checkout build of extraform0.31.17 SHA3c04a38b succeeded with unchanged Dockerfile/lock; original branch restored clean. Local image smoke checks Python3.12.15/basis10.0.2/Luigi3.6.0; runtime-required registry tag0-31-17 published after approval; independent manifest digest9795ee9a5049/config digestbc896c9f matched the local image. No latest/dotted aliases, deployment or cron execution. That was the first-library checkpoint; subsequent batch and live inventory status follow below. See [basis recovery execution](../log/2026-10-13-nexus-pypi-basis-recovery.md).

## PyPI library batch and Nomad periodic inventory (2026-10-13)

Task ownership corrected per user2026-10-14: Python library/PyPI recovery is [DevOps-890](https://youtrack.youdo.com/issue/DevOps-890), cron workload images [DevOps-895](https://youtrack.youdo.com/issue/DevOps-895), and data/dockers/base images [DevOps-891](https://youtrack.youdo.com/issue/DevOps-891). Comments890/74-124640 and891/74-124638 updated,895/74-124666 created; exact final text GET-verified. Historical approved DevOps-891 Git names remain unchanged. See [publication receipts](../log/2026-10-14-nexus-recovery-task-comment-reconciliation.md).
DevOps-895 was reported closed by the user on2026-10-14: eight-reference cron image restoration is accepted complete. Runtime identity/history caveats remain documented; they do not reopen the task or prove all23jobs executed new bytes. No tracker mutation was performed by the agent;890/891 scopes remain unaffected.

Runtime audit2026-10-14: four non-cleaner periodic parents show post-restoration starts; cashflow/cashflow-openai exit0 and force_pull+Downloading image give strong new-image evidence, but actual worker image IDs are unverified (SSH auth denied172.24.0.221). Ab/recommended run states are verified, refs alone do not prove IDs. Eighteen others lack retained detailed child/alloc records, not proof of never running. Cleaner actual cached image differs from registry and exits1; user explicitly excludes it due known bad Nexus credentials. No job trigger or infrastructure mutation. See [runtime audit and limits](../log/2026-10-14-nexus-nomad-cron-runtime-audit.md).

32of32 canonical required versions are published and Nexus checksum metadata-verified:5modern wheel+sdist exact-hash,11older Poetry wheel-only exact-hash,10setuptools exact-source sdists for requirements-only consumers without retained hashes, and six rebuilt versions with seven separately approved new-hash assets. The final six require consumer lock repairs; their old hashes do not match. Eventum1.0.1 exact wheel is published and Nexus GET metadata-verified. Live read-only Nomad inventory covers160jobs/23periodic parents/eightuniqueimages; extraform's four tasks use its restored image. Four more images for15periodic tasks built/pushed after approval with exit0 and independent remote config matching local IDs. Final approved runtime publications and GET-only verification confirm8of8images available for23periodic tasks. Seven current configs match recovery publications; cashflow:master was externally replaced by later successful CI3223227/pipeline140792/source20e641529 and current config7b3e6157 is trace-verified, not overwritten. No allocation/app/default-CMD/deployment/periodic run was performed. Five master-based repair branches with ten verified hash-only replacements passed original-Dockerfile/safe package metadata checks; user approved stage-two publication including automatic latest effects, and five commits/MRs are now GET-verified (initial historical CI snapshot before approved follow-up: ab140778/rowers140779 full success; task-quality3223110 oldDinD19.03.12 first-RUN cgroup launch failure before pip (host cgroupv2 unverified), recommended3223107 successful-build image-push finalization timeout (14of15layers pushed), and daily3223113 base-pull finalization timeout (8downloads complete/3pulls complete) were separate infrastructure failures subsequently superseded by successful retries/Docker29.9.0 corrections/master CI; specific original network causes are unproven; exact hash-only commits and clean local checkouts verified). CI on all five feature branches automatically publishes branch images and latest before tests. Feature branches do not deploy to Nomad. Workstation default pypi.youdo.local DNS resolves10.18.24.233 and ordinary simple-index routing returns200 without forced address. Recovery-host cloud provider remains unconfirmed; corporate hostname alone is not VK scope evidence. User-approved original rowers0.19.3/recommended1.16.24 archive copies with only five reviewed lock hash changes built successfully and their exact runtime tags were separately approved/published/config-verified. Recommended hash MR78 was explicitly approved and merged to master1fa2457d; post-merge master pipeline140796 succeeded. Task-quality MR57 was separately approved/merged to mastera51285b3 after successful Docker29.9.0 pipeline140795; post-merge master pipeline140797/build/tests succeeded. Daily MR8 includes separately approved Docker29.9.0 build-only overrides and pipeline140798 succeeded; no automated test job is present. Daily MR8 was separately approved/merged to master39b7fd86 after successful140798; master140799/build3223285 succeeded (build-only/no automated tests). All three earlier infrastructure-failing consumers now have successful master CI. Ab MR50 and rowers MR79 were explicitly approved/merged to master7a430478/f754bce4; ab master140800 succeeded including tests/lints and user subsequently executed productiondeploy3223291 successfully (GET verified00:25:53MSK, no allocation/application health check); rowers master140801/build/test/lint also succeeded, digest7dbf90e3. All five consumer MRs are merged and all five master CIs succeeded; the agent executed no manual runtime job or deployment. The user-executed ab production deploy succeeded in CI only; actual allocation/cron/application health remains unverified. Publication itself does not change existing allocations or run jobs. See [batch execution and artifact-type limits](../log/2026-10-13-nexus-pypi-library-batch-recovery.md).

## Host, access and storage

Root SSH available with `-F /dev/null`, ECDSA host algorithm and local MSS1100 ProxyCommand relay for larger transfers. Relay path `/home/slnnk/ai-data/nexus-recovery/ssh_mss_proxy.py`; VPN packet-size mechanism remains a hypothesis. Ubuntu22.04.5, RAM15Gi. `/dev/vdb` ext4, UUID `4685cc2f-9753-4196-a9bf-68038195577c`, already persistently mounted at `/data`; no formatting or fstab changes. Docker root `/data/docker`, containerd link `/data/containerd`, compose `/data/nexus/docker-compose.yml`, Nexus data `/data/nexus/nexus-data`, UID200. Root2.3G used/7.3G free; data1.1G used/157G free.

## Deployment and verification

External wrapper/vars/inventory `/home/slnnk/ai-data/nexus-recovery/` reuse unchanged docker-compose, nexus and nginx roles; no base Linux or monitoring role added. Approved apply recap `ok53 changed36 unreachable0 failed0 skipped27`, exit0. Docker29.9.0, Composev2.27.1, Docker/Nginx active.

Container `nexus-nexus-1`, image `sonatype/nexus3:3.96.4`, digest `sha256:5f48f9085096e96f4111ec07d79d57ca5a4a1da5a2003a3028a0b60c62bea7d1`, matching verified latest; restart0, memory4.25GiB/15.61GiB. `/data/nexus/nexus-data:/nexus-data` bind mount. Existing template JVMheap6Gi/direct6Gi retained.

Local8081 REST status and writable endpoints HTTP200; Nginx UI HTTP200; external `http://msk3-nexus.youdo.corp/service/rest/v1/status` HTTP200. Nginx routes Docker group pull to3000 and hosted push to3003. Initially absent connectors caused `/v2/` HTTP502; approved hosted/group initialization subsequently completed. Approved Docker group/hosted, Docker Bearer Token realm and CI-user initialization completed; Docker Hub proxy explicitly excluded. Initial admin credential location `/data/nexus/nexus-data/admin.password`; value unread and not recorded.

## Historical context

Previous host also served `msk3-nexus.youdo.corp`, internal10.16.24.23, image3.70.4-java11-ubi with data on ext4 `/dev/vdb`; former details are in [June diagnostics](../log/2026-06-17-nexus-nomad-pull-latency.md). Current instance intentionally starts without backup data. GitLab base-image job3217901 failed at Nexus login after restored bootstrap images became available; no CI retry triggered by this deployment.

## Onboarding authentication finding

After user changed admin password through UI (HTTP204), subsequent EULA GETs returned HTTP403 as unauthenticated user `-`. Nexus process/status remained healthy. Reload/login with the user's newly set password is the next browser action; no credentials were read and no server fix/EULA acceptance was attempted. A separate Go client for user cleaner hits authentication rate limits HTTP429; review that client under existing CI-credential initialization work. Details and timestamps: [audit](../log/2026-10-11-nexus-fresh-recovery-plan.md).

## Browser large-request transport finding

User polling POST Content-Length5310 aborts with `NS_BINDING_ABORTED` and no HTTP status. Controlled6000-byte diagnostic HTTP request fails at default MSS and succeeds at MSS1100; small-request45KiB responses work either way. Thus size-dependent client-to-server request transport failure is verified; the exact VPN dropping component is unidentified. Proposed temporary HTTP80 TCPMSS1100 rule is prepared in `/home/slnnk/ai-data/nexus-recovery/fix-http-mss.yml`, syntax-checked and pending explicit approval, not applied. No service restart/SSH/8081 or reboot-persistence changes proposed. Details: [audit](../log/2026-10-11-nexus-fresh-recovery-plan.md).

## Diagnostic direction: VPN capture first

The user preferred inspecting traffic on the VPN server before applying the proposed HTTP MSS rule. No MSS firewall rule was applied; its permission request is deferred. Read-only topology research finds an August3 corporate OpenVPN record for `ipsec-vm`10.16.20.3, tunnel172.30.62.1, config `/etc/openvpn/server.conf`; this is not proof of the recovered current endpoint. On 2026-10-13, the user confirmed `10.16.20.3` is the old OpenVPN server; live SSH verified current OpenVPN on `sc-gateway2.youdo.corp` / `172.28.0.200`, using `/etc/openvpn/server.conf` ([verification](../log/2026-10-13-corporate-network-openvpn-n-velikanets-routes.md)). Current local route uses tun1 MTU1500, source172.30.63.8 and gateway172.30.63.1; Nexus sees browser source10.18.20.3. Current VPN host/interface identification and header-only traffic inspection are the next diagnostic steps. No packet capture or VPN configuration change was performed by delegated KB research.

## Current gateway and capture localization

Recovered gateway `ipsec-vm`10.18.20.3 accessible as youdo with passwordless sudo; root SSH rejected. New key was accepted into local known_hosts via TOFU; no remote access changes. Paired35s header-focused captures report zero kernel drops. Default-MSS test first5192 request bytes are absent already at gre_selectel ingress; only tail911 reaches gateway and Nexus, which ACKs the initial missing sequence. MSS1100 comparison delivers complete6103 bytes. Loss is localized upstream of gateway GRE ingress; precise upstream drop remains unverified. No temporary MSS firewall rule applied. See [audit](../log/2026-10-11-nexus-fresh-recovery-plan.md) for exact sequences and artifacts.

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

## Current public LB route and DHCP delivery (2026-10-12)

Read-only recheck supersedes the earlier missing-route finding: sc-lb-pub01172.28.0.141 routes10.18.24.233 via172.28.0.1 deveth0, with destination10.18.24.0/24 installed. Latest DHCP lease from172.28.0.3 includes this route via RFC3442 option121. eth0 uses DHCP/ifupdown; no local manual persistence found in inspected configuration. Direct Nexus REST status returns200; public unauthenticated cached Maven POM now returns401 rather than timeout, while public status still404. Authenticated public download remains unverified. No remote changes made; earlier temporary /32 proposal is unnecessary for current connectivity.

User corrected the earlier statement:172.24.0.0/24 is current for physical production servers; lb pub uses172.28.0.0/24. Hardware inventory172.24.0.22/.23 is not obsolete. Verified hardware Netplan route via172.24.0.1 is specific to that network and must not be copied to lb pub. No repository route management found for either group. Prefer the existing DHCP route; if local enforcement is requested, propose a separate ifupdown hook using the current private gateway rather than changing cloud-init-generated interfaces or introducing Netplan. [Evidence and proposal](../log/2026-10-12-nexus-public-lb-route-verification.md).

Public nginx Maven routing verified with `nginx -T`: `/etc/nginx/conf.d/nexus.youdo.com.conf` has HTTPS prefix location `/repository/maven` forwarding unchanged URI to `http://msk3-nexus.youdo.corp`; this covers public/releases/snapshots repositories. No location-level nginx authentication or access restriction found. The vhost does not proxy `/service/rest/`, explaining public status404 independently of Maven connectivity.

## Authenticated public Maven verification

Read-only `/home/slnnk/ai-data/nexus-recovery/verify_public_maven.py` exited0. Existing GitLab group34 Maven credentials were used in memory only, with normal HTTPS certificate validation and no redirects followed. Public `https://nexus.youdo.com/repository/maven-public/` returned200 for Jivo2.6.0 POM (8839 bytes,0.14s), Jivo2.6.0 AAR (2187102 bytes,1.11s), and Google AGP8.13.2 POM (11773 bytes,0.10s). Both POMs parsed as XML project documents; AAR ZIP integrity and AndroidManifest.xml verified. Anonymous Jivo POM returns401 as expected. Selected public artifacts verified; full Gradle build/transitive dependencies and Cyberity remain unverified. No credential values printed or persisted.

## Local explicit-backend proposal withdrawn

User explicitly requested reverting the two prepared Nexus backend edits. Restored only `inventories/prod_selectel/group_vars/balancers_public` and `roles/nginx/templates/vhost/nexus.youdo.com.j2` to HEAD after verifying their exact diffs consisted solely of the known Nexus proposal. Scoped `git diff` is empty. Unrelated runner/Terraform local edits remain. No state-changing git commands or remote changes executed. Public nginx continues using `msk3-nexus.youdo.corp`; authenticated public Maven reads already passed with that configuration. Earlier statements that these two edits remain pending are superseded.

## Temporary anonymous access enabled (2026-10-12)

User explicitly requested enabling anonymous to prioritize recovery. Anonymous GET/PUT verification confirms enabled=true, userId=anonymous, realmName=NexusAuthorizingRealm. Existing nx-anonymous role unchanged: wildcard repository read/browse plus search/healthcheck read; no write privileges. Anonymous public Maven reads for Jivo2.6.0 and AGP8.13.2 POM both return200 and valid XML. This supersedes earlier anonymous-disabled/unapproved statements. Disable after recovery and consumer credentials setup; tracked in ~/ai/TODO.md. [Authorization, execution and scope](../log/2026-10-12-nexus-temporary-anonymous-access.md).

## NuGet recovery inspection and plan (2026-10-12)

Live master NuGet.Config in youdo.business and youdo/youdo requires legacy public nuget/nuget-private feeds and username nuget; password present in private source files, values not recorded. Nexus lacks that user and repository names: only three verified-empty defaults exist on default blob store. Public static indexes200 point to group nuget paths currently404. Prepared plan separates nuget-hosted/nuget-cache storage, restores hosted nuget-private + proxy nuget.org-proxy + group nuget, and creates one nx-nuget role/user with existing credentials. Private packages require separate recovery and youdo/youdo also references BaGet. No mutations performed. [Inspection and proposed steps](../log/2026-10-12-nexus-nuget-recovery-plan.md).

## NuGet recovery steps 1-4 completed (2026-10-12)

User approved steps1-4. Created separate nuget-hosted/nuget-cache File stores; replaced three rechecked-empty defaults with hosted nuget-private, NuGet.org V3 proxy nuget.org-proxy, group nuget (private then proxy). GET-verified settings. Created active user nuget with existing matching consumer password and sole nx-nuget role: wildcard NuGet browse/read plus add/edit only nuget-private. No admin/delete.

Public indexes, versions and registration metadata HTTP200; Newtonsoft.Json13.0.3 package2441966 bytes downloaded and ZIP/nuspec verified. Request log confirms nuget principal for authenticated metadata GET. No nginx changes needed for current read endpoints; both existing static aliases resolve via group nuget. API-key publishing not verified or changed. Anonymous remains enabled; private hosted contents and full service restores remain to recover/check. [Execution and evidence](../log/2026-10-12-nexus-nuget-recovery-applied.md).

## NuGet master-wide recovery inventory (2026-10-12)

Scanned157live master snapshots among164unique ~/git repos;62NuGet consumers,3198references,387IDs/1131version expressions.52private/custom library IDs143requested versions absent from nuget.org/current Nexus. CSV lists consumers and source candidates from30-project youdo/Lib catalog plus service-owned library projects; two historical mappings are hypotheses. BaGet timeout and missing committed lock/assets files prevent complete transitive availability claims. Three public version gaps are separate from private restore. No packages restored or repositories modified. [Full list, methodology and limits](../log/2026-10-12-nexus-nuget-master-inventory.md).

## Library publication retry-first recovery (2026-10-12)

User requested publish retries before dependency checks. Coworking1.0.7/1.3.3 retries fail unavailable SDK2.1 image;1.3.4 fails missingRabbitHole. User explicitly approved adding nx-nuget to publisher gitlab (preserved nx-docker), after RabbitHole1.4.2 retry failed403. Repeated RabbitHole1.4.2 publication job3218670 succeeded; public .nupkg78097bytes downloaded and ZIP/nuspec verified. RabbitHole1.4.1 retry3218622 pending completion;1.4.3 retry3218623 fails emptyNuGetVersion, currenttag absent. No repo/tag/CI variable changes performed. [Approvals, jobs and evidence](../log/2026-10-12-nexus-library-publish-retries.md).

## RabbitHole and Coworking restored; fast verification convention (2026-10-12)

RabbitHole1.4.1/1.4.2/1.4.3 and Coworking1.0.7/1.3.3/1.3.4 now present in Nexus. CI restoredRabbitHole1.4.2(job3218670),1.4.3(pipeline140646/job3218762),Coworking1.3.4(job3218902). Explicitly approved local historical-source rebuild/uploads on SDK6 recovered RabbitHole1.4.1 and Coworking1.0.7/1.3.3. Explicitly approved stalled RabbitHole1.4.1 job cancellation. Publication uses Basic credentials and works without NuGetApiKey realm. Publishergitlab now has nx-docker+nx-nuget after explicit approval; dedicatednuget used for manual uploads.

User recovery preference: retry requested library publish jobs first; investigate actual failures rather than pre-audit all dependencies. Post-publication verification should only confirm package/version metadata in Nexus, without downloading the nupkg. Applied after user correction; local artifacts can be validated before explicit upload approval. Original master inventory52IDs143pairs remains evidence; two libraryIDs/sixpairs completed,50IDs137pairs pending. [Approvals, outcomes and provenance](../log/2026-10-12-nexus-library-publish-retries.md).

## npm recovery inventory and plan (2026-10-12)

Read-only npm inspection finds no npm repositories, npm stores or npm service user on the recovered instance. All-client audit covers164local checkouts and identifies legacy group `npm`, hosted publication `npm-private`, public/internal endpoints, and four private library packages from `youdo-core-frontend-tools`. Business origin/master locks require UI0.39.0/eslint2.1.0/prettier0.0.1/cursor-extension0.0.3; Business landings needs UI0.17.5/eslint1.2.5. Extra local Business refs require UI0.30.1/0.34.0. Proposed separation: npm-hosted/npm-cache File stores, npm-private hosted, npmjs-proxy public proxy, npm group. Live GitLab master verifies Business/landings requested versions and four library npmjs metadata404s; producer master is newer (UI0.40.1/cursor1.0.0), so historical source/original tarball recovery is necessary. Existing NPM_TOKEN auth identity still needs verification; no npm writes or publication performed. Details: [npm recovery plan](../log/2026-10-12-nexus-npm-recovery-plan.md).

## npm steps1-3 applied (2026-10-12)

User-approved npm-hosted/npm-cache File stores, npm-private hosted, npmjs-proxy and npm group created; nx-npm/active npm user created, NpmToken enabled alongside existing realms. New token internal whoami200 identifies npm; internal lodash metadata200, no tarball download. Actual publisher uses _authToken; old project496 NPM_TOKEN401 requires replacement. Public npm404 is explained by absent /repository/npm location in live production LB vhost. GitLab/LB writes and libraries/CI retries remain unperformed. [Applied evidence](../log/2026-10-12-nexus-npm-recovery-applied.md).

## npm producer CI credential updated (2026-10-12)

After explicit user approval, project496 youdo-core-frontend-tools NPM_TOKEN was replaced with the verified npm Bearer credential. PUT200 and GET value/unchanged-metadata checks passed. No CI retry or library publication. Public npm nginx location still pending. [Evidence](../log/2026-10-12-nexus-npm-recovery-applied.md).

## SORM Docker runner authentication diagnosis (2026-10-12)

Public Docker manifest for SORM migrations0.0.22 returns200 with current CI gitlab credentials,401 BASIC anonymously. Both Docker repositories have forceBasicAuth=true despite global anonymous enabled. Runner105 on172.28.0.171 config.toml DOCKER_AUTH_CONFIG contains only registry.youdo.sg user technical; no Nexus entry or Docker config.json in inspected root/runner locations. Job3219124 fails before scripts with no basic auth credentials. No new Nexus user required; no runtime changes performed. [Evidence and limits](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

## npm library CI restoration proposal (2026-10-12)

Existing deploy lib jobs mapped to exact source versions: manual2640279 for UI0.17.5/eslint1.2.5; retry2775626 for cursor0.0.3; retry3197313 for UI0.39/eslint2.1/prettier0.0.1. publish job is Storybook S3 and excluded. Selected jobs publish sibling workspace versions; old auth/duplicate ALLOW_ONCE handling needs actual failure review. No retry/play performed. [Concrete proposal](../log/2026-10-12-nexus-npm-library-retry-plan.md).

## Runner Nexus pull credentials applied (2026-10-12)

After explicit user request, added nexus.youdo.com/gitlab to existing DOCKER_AUTH_CONFIG in /etc/gitlab-runner/config.toml on172.28.0.171 (four runner entries) and172.28.0.172 (three). registry.youdo.sg/technical preserved. Both services active and automatically reloaded config; read-back and unchanged second preflight verified, mode0600 preserved. No CI retry. Runtime-only change; configuration-management persistence remains separate. [Approval and checks](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

User subsequently retried the affected SORM job and reported success after adding runner Nexus credentials; retry ID not supplied. [Result](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

## npm approved job execution results (2026-10-12)

All3approved launches completed:2640279 failedENEEDAUTH after successful build; retries3219284/3219285 succeeded and restored UI0.23.3/0.39.0 metadata. Correction: historical deploy lib runs publish from packages/ui, so only UI is published; earlier whole-workspace assumption was incorrect. Other5requested pairs remain absent. No package downloads. [Results and diagnosis](../log/2026-10-12-nexus-npm-library-retry-plan.md).

Nomad follow-up:172.24.0.12/msk3-nomad02 Docker plugin in /etc/nomad.d/client.hcl uses /root/.docker/config.json, containing only registry.youdo.sg user nomad; Nexus entry absent. Read-only inspection only; task-level auth uninspected. [Evidence](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

## NuGet recovery continuation 2026-10-12

Historical publication retries and separately approved exact-source fallback uploads completed for all 143 required NuGet pairs, public metadataHTTP200 verified. All requested Fluent versions, DocXToPdfConverter1.1.0-youdo, Kaiena1.0.8 and Serilog exceptional sink versions are metadata-verified. Existing runner/SDK/BaGet failures are diagnosed only after retry; CQRS archived project retry403 uses a separately approved local fallback. Current evidence and limits: [recovery log](../log/2026-10-12-nexus-next-library-recovery.md). No package download verification or repository/CI configuration edits.

## Dedicated Docker pull user created (2026-10-12)

After explicit user request, active docker now has sole role nx-docker-read (ID/name), four direct browse/read privileges for docker group and docker-hosted, no write rights. Password location current/.env NEXUS_DOCKER_PASSWORD. GET verification and public authenticated /v2/ plus SORM service0.0.22 manifest HEAD200 passed. Existing gitlab/nx-docker unchanged; no client config/job changes. [Authorization and checks](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

## Current Docker role after user correction (2026-10-12)

User docker now has sole nx-docker, superseding earlier read-only assignment. Existing nx-docker has eight direct privileges: docker group browse/read/delete and docker-hosted browse/read/add/edit/delete. gitlab retains nx-nuget+nx-docker and also gains Docker deletion rights. nx-docker-full created during the earlier approach was unused and removed; nx-docker-read remains unused. Exact GET configuration and unchanged-password manifest HEAD200 verified. User preference is to modify/reuse nx-docker rather than create a separate full-access role. [Correction and checks](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

## Nomad172.24.0.12 Nexus credentials applied (2026-10-12)

User-authorized change added nexus.youdo.com/docker to /root/.docker/config.json on172.24.0.12/msk3-nomad02. Existing registry.youdo.sg/nomad and mode0640 preserved; Docker plugin already references that file. Node-side authenticated SORM service0.0.22 manifest HEAD200 with saved credentials verified. No service/allocation/job restart, image pull or other-node changes. Runtime-only; configuration-management persistence separate. [Approval and verification](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

After explicit user request, the same Nexus Docker auth applied to172.24.0.11/msk3-nomad01 and172.24.0.13/msk3-nomad03. All requested clients11/12/13 use nexus.youdo.com/docker in /root/.docker/config.json, preserve registry.youdo.sg/nomad and mode0640; saved-credential node-side service0.0.22 manifest HEAD200 verified on each. Runtime-only, no restarts. [Checks](../log/2026-10-12-nexus-sorm-runner-image-auth.md).

## All requested npm library versions published (2026-10-12)

CI UI17.5/ESLint2.1/Prettier0.0.1 and local ESLint1.2.5/cursor0.0.3 publications completed; UI39 already restored. Hosted metadata confirms all6pairs. Four pairs differ from old lock integrity; ESLint2.1/Prettier match. UI latest is17.5; tag API and npmCLI400. Exact-byte39republish with temporary ALLOW policy prepared but requires separate approval, not executed. Public npmLB route still pending. [Publication evidence and limitations](../log/2026-10-12-nexus-npm-library-restoration.md).

## npm UI latest restored (2026-10-12)

After explicit approval, temporary npm-private ALLOW and identical-byte UI0.39 republish restored latest0.39.0. ALLOW_ONCE returned and GET-verified; UI39integrity unchanged and all prior UI versions preserved. No other repository policy change. [Evidence](../log/2026-10-12-nexus-npm-library-restoration.md).

Final NuGet recovery cleanup: all143/143required pairs were independently metadata-verified (HTTP200), central publication backlog closed, and26 redundant own retries canceled after explicit approval; fresh job GETs confirm26canceled. Service restore/transitive checks remain deferred; Mailer prerelease Contract>=1.9.3 resolves1.9.4. See the [recovery log](../log/2026-10-12-nexus-next-library-recovery.md).

## Local Ansible persistence prepared (2026-10-12)

Approved local automation-services changes add optional Nexus entry plus nonempty secret guard/no_log and host_vars for Nomad11/12/13, excluding14. Password env lookup NEXUS_DOCKER_PASSWORD requires controller export; no value in git. Inventory/render/guard/syntax/scoped whitespace and read-only review passed; Molecule unavailable locally. No commit/push/apply. Source branch/localHEAD absent on current GitLab; old MR1368 now a different MR and fetch blocked by changed SSH key. Future publication requires source/base re-evaluation. [Design, approval, checks and limitation](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

## Ansible publication and scope correction (2026-10-12)

Initial three-client change published as2c251767 onDevOps-890-nexus-docker-auth, [MR1371](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1371), pipeline140662skipped. User subsequently requested common Docker auth for all consumers of Nomad role. Local correction moves Nexus identity/envpassword into role defaults, removes three host_vars and aligns guard with config-writing condition. Target diff nowthree role files; render/guard/actual skipped-role/syntax/review checks passed. Corrected commit/push/MR metadata pending approval; subsequentpush will run molecule-nomad. Runtime clients11/12/13 unchanged; no others deployed. [Training and validation](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).


## Business autotest Maven dependency cycle (2026-10-12)

Project480 `youdo-business-tests` build3219500 and verify-modules3219502 fail resolving TKB/Sber snapshots. TKB project536 build3219485 and Sber project578 build3219490 require the missing main suite snapshot, forming a circular bootstrap dependency. `verify-modules` compiles/builds API/UI modules with `-x test`; it neither runs tests nor publishes libraries. Main-suite `publish-maven` is master-only, and master retains the cycle. Diagnosis used GET requests only; no retries or edits. [Evidence](../log/2026-10-12-nexus-youdo-business-tests-maven-recovery-diagnosis.md).

## Common Nomad auth correction published (2026-10-12)

User approved corrective publication. Commit5c623f52 onDevOps-890-nexus-docker-auth published in [MR1371](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1371), title updated for Nomad hosts. Final MR has only three role files; Nexus config now common to all consumers writing Docker auth, envpassword required. Push pipeline140665/molecule-nomad3219595 running at initialcheck; MRpipeline140666skipped/manualtest. No merge/deploy. [Approvals/checks](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

Final CI result for common Nomad auth correction: push pipeline140665/job3219595 failed before tests because registry.youdo.sg/sysadmins/ansible-molecule-toolset:latest manifest missing in restored registry. Local checks pass; Molecule unexecuted, image recovery remains separate. [Failure evidence](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

Image recovery investigation confirms project437 build3219476 fails at archived Debian Buster APT Release404. Approved correction redirects APT sources in both Dockerfile stages and removes redundant forced Galaxy installation, preserving original packages and versions. Local build passed;81f3a8e published in [MR1](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/merge_requests/1). [Master pipeline140669](https://gitlab.youdo.sg/sysadmins/ansible-molecule-toolset/-/pipelines/140669) on aad593fd succeeded with build3219854/latest3219855, confirming master/latest publication. Requested DevOps-891 comment74-124638 update GET-verified. Automation-services Molecule retry remains pending. [Approvals and validation](../log/2026-10-12-gitlab-ansible-molecule-toolset-recovery.md).

Verified GitLab dependency history dates the TKB cycle to2024-09-30 (main-suite MR!193) and Sber cycle to2026-02-12 (MR!238); both dependency directions include `implementation` and `testImplementation`. These predate recovery/DevOps-832. See the diagnosis log above for exact commits; cached artifacts masking bootstrap failure remains an inference.

Local bootstrap preparation now passed:11 common Java sources from main-suite0da09367 produce13 class files; TKB71ead24 and Sbercaab397 main-only `:jar` validations passed using the isolated bootstrap dependency. No Nexus upload or CI retry performed; external publication approval remains pending. The partial snapshot is recovery-only. See the diagnosis log for checksum, provenance and reviewed command.

## CI-discovered NuGet requirements after master inventory

Job3219724 (youdo.business MR3843, sourceSHAa14de776a544ee3b833d5a9f37f22e2d7daee9d0) fails NU1102 on YouDo.ServiceCore.Logging1.0.16 and YouDo.ServiceCore.Metrics1.0.16. Fresh Nexus version metadata HTTP200 confirms both absent (nearest1.0.15). Neither version was in the restored143 direct master inventory pairs; pinned business master referenced1.0.14. The user subsequently published both extra1.0.16 versions from CI; fresh public metadataHTTP200 confirms both present. Publication backlog closed; the user subsequently confirmed the business build succeeded, so its follow-up verification backlog is also closed. No agent publication or retry performed. [Evidence](../log/2026-10-12-nexus-business-job-3219724-nuget.md).

Bootstrap publication was explicitly approved and succeeded (Gradle8s). GET metadata through hosted/group confirms main-suite snapshot1.0.0-20261012.151934-1; incomplete bootstrap is live, full replacement pending. TKB remote6ae621a has the same tree as validated71ead24. No TKB/Sber CI retry has been authorized or performed; approval is separate. Earlier pending-bootstrap-publication statements are superseded.

First TKB/Sber publications were separately approved and succeeded (3219856/3219857); hosted/public metadata confirms TKB1.0.0-20261012.152716-1 and Sber1.0-20261012.152806-1. Separately conditionally approved full main-suite publication is pending in3219858. Bootstrap stays live until that succeeds; recovery TODO remains open. Additional publications/builds still need approval.

Full main-suite publication3219858 succeeded; hosted/public metadata confirms1.0.0-20261012.153418-2, replacing the incomplete bootstrap as latest. Separately approved second TKB/Sber publications3219859/3219860 and builds3219861/3219862 are running. Final business build/publication are conditionally approved but not performed. Overall verification remains open; this is one bounded final pass.

## Business/TKB/Sber Maven recovery completed (2026-10-12)

All three master pipelines137380/139740/133551 are green; final publication/build jobs and explicitly approved latest updates succeeded. Current full snapshots: business1.0.0-20261012.154307-3, TKB1.0.0-20261012.153739-2, Sber1.0-20261012.153623-2. Hosted/group metadata agrees; registry latest digests equal fresh pipeline tags master-2686/master-98/master-18. Read-only final verification passed without package/image downloads. Source cycles remain; no deployment or tests run. Earlier pending statuses above are superseded. [Evidence](../log/2026-10-12-nexus-youdo-business-tests-maven-recovery-diagnosis.md).

User rebuilt the missing Molecule toolset image; latest tag metadata HTTP200/digest verified. Job3219595 remains failed until separately authorized retry. [Verification](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

Approved retry3219868 successfully pulled restored toolset but failed before Molecule: client Docker API1.39 below daemon minimum1.40. Toolset uses docker.io from Debian Buster; CI uses floating docker:dind. Image missing block resolved; compatibility fix remains separate. [Retry result](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

## Raw mobile repository recovery prepared (2026-10-12)

Live Nexus lacks raw/raw-private, raw-hosted store and raw identity. Four live GitLab projects79/65/69/154 use matching NEXUS_CREDS username raw. Android publishes to raw-private and Appium reads via raw; iOS fixed ZIP/version paths require overwrite and iOS Appium currently uses an anonymous internal raw-private URL. Prepared OpenAPI-validated File blob raw-hosted, raw-private hosted ALLOW, raw group over raw-private, nx-raw read/browse+hosted add/edit and raw user reusing credentials. Existing public nginx routes need no change. Read-only dry run passed; external creates await approval. Application artifacts not restored. [Plan, checks and scope](../log/2026-10-12-nexus-raw-recovery-plan.md).

## Raw mobile configuration restored (2026-10-12)

After explicit approval all five creates completed: File blob raw-hosted, raw-private hosted with ALLOW and ATTACHMENT, raw group with raw-private member, nx-raw role (read/browse all raw, add/edit raw-private), active raw user with the existing matching four-project credential. GET settings and raw authentication verified (asset list200, invalid password401). Missing-object404 verified at internal/public/iOS Appium hosts with authenticated and anonymous requests. Actual APK/ZIP downloads remain unverified because repositories are empty; no CI or publication triggered. Existing nginx and anonymous policy preserved. [Approval, execution corrections and verification](../log/2026-10-12-nexus-raw-recovery-plan.md).

## Molecule compatibility fix prepared in same MR

User requested minimal DinD pin in MR1371. Local .gitlab-ci.yml now pins docker:28.5.2-dind for allthree Moleculejobs; official API range1.24-1.51 covers client1.39, publictag verified, CI syntaxvalid. Commit/push/MRmetadata approval pending. New manualjob with compiledupdatedconfig needed afterward; old retry retains floatingservice. [Checks and scope](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

## Recovery status communicated (2026-10-12)

User-requested DevOps-890 comment74-124640 published and exact text GET-verified. Fresh inventory19repos/10File stores/8active users, completed work and explicit limitations included. [Publication record](../log/2026-10-12-nexus-recovery-status-comment.md).

## DinD pin publication completed (2026-10-12)

Approved commitf4018c2b pins docker:28.5.2-dind for allthree Moleculejobs in MR1371, title updated to cover common Nomad Nexus auth and DinD. Final MRfourfiles verified. New pipelines140672/140673skipped by rules, molecule-nomad manualjobs3219872/3219873; full validation pending separate manualstart authorization. No merge/deploy. [Publication](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

User declined manualMoleculejob3219872 start after DinD pin publication; it was not played. Latest common-auth/DinD MR1371 remains published with static validation only, fullMolecule not run. [Decision](../log/2026-10-12-nexus-automation-services-nomad-docker-auth.md).

## MassTransit1.8.1 assembly repair (2026-10-15)

User-authorized historical rebuild replaced only YouDo.Extensions.MessageBus.MassTransit1.8.1, retaining PackageVersion and removing fallback Version override. DLL/reference identity1.0.0.0; offline .NET6 probe with release-selected MessageBus191/Net181 passed21types. Nexus asset SHA2569f557ada75b1032044635dc2ba0169b2d049e8cadc2e21cb643a778c154aad9f metadata verified after publication via internal PackagePublish endpoint. Subsequent monolith fresh restore/rebuild verified corrected package hash and direct test5 Nomad deployment succeeded; no source or policy change. See [repair](../log/2026-10-15-nexus-messagebus-181-assembly-repair.md).

## UI 0.26.0 and 0.25.4 CI recovery inspection (2026-10-15)

After failed CI retries3228457/3228458 (npm implicit-latest guard), user-authorized local builds from pinned historical sources published UI0.25.4 then0.26.0 with explicit recovery tag. Original build commands passed in node24.13.0/npm11.6.2, both archives516files; only scratch lockfiles changed. Independent metadata GET confirms both versions present, latest0.40.1 preserved and recovery0.26.0; SHA512matches local archives and existing dist metadata retained. No repo edit, policy change or verification download. Original consumer lock integrity remains unverified. [Source identities, builds, publication and limits](../log/2026-10-15-nexus-ui-0260-0254-ci-recovery-inspection.md).
