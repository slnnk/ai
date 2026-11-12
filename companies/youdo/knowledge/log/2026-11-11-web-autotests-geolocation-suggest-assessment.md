---
system: web-autotests
status: verified
checked: 2026-11-11
tags: [selenium, geolocation, assessment]
---
# Web autotests: geolocation suggest failure assessment

## Summary

- Initial Chrome152 site-options geolocation failed at5s; NetLog localized about9s of DNS search delay.
- Negative mcs.local queries fail upstream with EDNS DO while ordinary/EDNS-no-DO queries work.
- Gateway BIND forwards mcs.local to10.18.20.65 and packet capture confirmed it sends the failing DO form.
- User approved the proposed per-upstream workaround and fresh-session verification with `Сделай`.
- On2026-11-11, added server10.18.20.65 edns no on gateway10.18.20.3; syntax/reconfig/service checks passed.
- Afterward kube-dns returns the negative answer in7–8ms and existing private/public names still resolve.
- Fresh Chrome acquisition now469ms with timeout5s; repeat calls7ms/8ms, all successful.
- Position accuracy remains about2796km; complete task-creation UI was not reproduced.
- DevOps-920 Ansible persistence published as commit1cbb9476 / MR1394; exact remote state verified, CI skipped.
- User reported DevOps-920 closed on2026-11-11; accepted complete and central follow-up closed. No background work remains.

## Task and evidence

Assess https://youdo.loop.ru/youdo/pl/ugx1hwywwp8i7mzm85d1n9ty6y . Read the root and two replies through authenticated GET. The reporter confirms web testing. Chrome and ChromeDriver both report 152.0.7977.82. Final XPath expects the original address input `яку `; this proves the expected value was captured before address replacement, not that geolocation never completed.

## Local code findings

Inspected existing clean youdo.static checkout d6a8ea3e437c522c78de75e3de000d4df00eb899 and cached origin/master 26c7ea0d9f (October21; no fetch). Both versions of testGeolocationInSuggestOnTaskPage click geolocation, then immediately capture getAddressFromInputByNum(1). The click helper calls waitPreloaderHidden: sleep1 followed by generic preloader disappearance; getter only reads getValue. There is no explicit wait for an address change. A timing race is plausible, not reproduced or established as root cause. BasePage has setFakeGeolocationMoscow, unused by this test.

Local infra-tf values pin Chrome node image 4.48.0-20260909; cached history last changed scaling on October1. This is not proof of current cluster configuration or absence of recent deployment. Local base-images Dockerfile extends the matching upstream image and adds trusted certificates; no geolocation policy is declared there.

## Status and limits

Initial assessment used only source inspection; the subsequent user-requested Selenium check is recorded below. No repository edits or implementation/follow-up task was assigned; existing closed Selenium scaling investigations remain closed. Central backlog unchanged.


## Authorized live Selenium probe

User requested verification through Selenium; the execution approval covered one temporary Chrome session, opening https://test.youdo.sg, geolocation permission and coordinate overrides within that session, and closing it. Probe: /home/slnnk/ai-data/selenium-geolocation/probe.py; result: /home/slnnk/ai-data/selenium-geolocation/result.json.

Remote Chrome152.0.7977.82 on selenium-node-chrome-85c5d99c9f-qb5sc matches the reported browser version. The test origin was secure, the API available, and default geolocation permission already granted. Real geolocation succeeded in9119ms with reported accuracy2795716.633836537metres (about2796km). After explicit permission grant, another call succeeded in1ms with the same accuracy; this does not establish a fresh external provider request. Fixed test coordinates succeeded in1ms with10m accuracy. The initial9.1s delay supports the timing hypothesis: the reported failing run advanced about3.2s after the click. This is a separate run and does not prove the historical cause.

Session DELETE succeeded; process exited0. No browser session or background process remains from the probe. No task/account creation, product writes, repository changes or infrastructure configuration changes. The exact reporter stand/options, image update history, reverse geocoding and complete UI scenario remain unverified; no claim of end-to-end reproduction or repair.


## Browser acquisition versus address lookup

Follow-up source inspection distinguishes the measured9.1s navigator.geolocation callback from application reverse geocoding; the probe itself did not invoke the application geocoder. Local src/libs/geolocation/GeolocationHelper.ts defaults to enableHighAccuracy=true, timeout=5000, maximumAge=0; the probe used enableHighAccuracy=false and timeout=12000. Thus the probe was not an exact reproduction of application options. A geolocation acquisition timeout is another plausible failure, and simply waiting longer in the test is not a demonstrated fix. Deployed source/options and exact failing UI path remain unverified.

In the inspected local geolocation controller, success passes coordinates to MapsApi.geocode. js/Libs/YouDo/Maps/MapsApi.js selects YandexMapsApi, whose geocode wraps ymaps.geocode. This inspected path uses the Yandex browser maps API; the internal geocoder service must not be blamed for the separately measured browser coordinate acquisition. Chromium has a network location provider, but the actual provider endpoint, network timing, startup delay and cause of poor accuracy were not captured. No new remote operations or background work were started. These are diagnostic limits, not assigned implementation tasks; TODO unchanged.


## Detailed probe: reproduced timeout and DNS localization

User requested continued investigation. A separately approved temporary Chrome session on selenium-node-chrome-85c5d99c9f-4pqnd used Chrome152.0.7977.82 with NetLog enabled only for that process. Exact local helper options (high accuracy, timeout5000, maximumAge0) produced code3 / `Timeout expired` after5005ms despite granted permission. Immediate repeat succeeded after4960ms, with accuracy2795716.633836537m. Extended15s call then returned in5ms. The root page had no ymaps object, so reverse geocoding was not exercised.

Detailed probe script/result and sanitized NetLog event summary reside under /home/slnnk/ai-data/selenium-geolocation/. Initial browser extraction capped at6MB and was incomplete. After successful session deletion, read-only kubectl exec retrieved the full Chrome NetLog from the existing pod. Both raw NetLogs are mode0600 and must not be pasted into chat because URLs can contain credentials. No secrets copied to KB.

NetLog identifies https://www.googleapis.com/geolocation/v1/geolocate. The first browser DNS resolution starts at108105444ms. Chrome queries search expansions selenium.svc.cluster.local, svc.cluster.local and cluster.local, all quickly returning NXDOMAIN; next it queries www.googleapis.com.mcs.local. Built-in DNS times out at+3038ms (ERR_DNS_TIMED_OUT / -803), then system resolution completes at+9050ms. The first geolocation request had already ended at+4995ms. A subsequent geolocation request starts at+9998ms, uses DNS cache and gets HTTP200 at+10063ms. Thus the main delay in this probe is DNS resolution, not Google HTTP processing or the internal geocoder service.

Read-only /etc/resolv.conf from the same pod: nameserver10.254.0.10, search selenium.svc.cluster.local svc.cluster.local cluster.local mcs.local, options ndots:5. Kubernetes lists10.254.0.10 as kube-system/kube-dns. No ConfigMap named coredns exists in kube-system; no alternate DNS configuration or upstream owner was established.

Independent six-query UDP probe from the same pod confirmed: absolute www.googleapis.com A returns NOERROR/eight answers in3ms; HTTPS/type65 NOERROR/no answers in63ms. www.googleapis.com.mcs.local A and HTTPS both time out after2s. www.googleapis.com.cluster.local A and HTTPS return NXDOMAIN in1ms. The final mcs.local search suffix is the reproducible problematic DNS branch; the upstream reason it fails remains unknown.

No DNS/Helm/infrastructure configuration changed. All command processes exited; the temporary browser session was successfully deleted. Complete task-creation UI remains untested. The earlier timing-only hypothesis is superseded by a reproduced5s acquisition timeout with DNS evidence; the test's missing address wait is still independently observable. Proposed DNS remediation and repeat verification are tracked in central TODO; historical closed scaling tasks remain closed.


## Correlation with BuildAPI DevOps-917

User pointed to today's analogous BuildAPI issue. Reviewed [the existing BuildAPI record](2026-11-11-dev-deployment-buildapi-cache-dns-search.md), including its latest user-accepted closure. BuildAPI's relative Redis SRV query reproducibly took5.008s and timed out; the identical absolute query returned port1905 in0.011s. The published application fix (MR41, accepted release0.5.14) makes names absolute/disables search and adds error/timeouts handling. It bypasses the search-expansion problem for that application; no shared-cluster DNS repair is recorded there.

Both investigations demonstrate DNS search expansion delaying unrelated applications in VK Kubernetes. Selenium additionally localizes an unresponsive expansion to mcs.local. The BuildAPI record does not identify the exact stalled search suffix/upstream, so a shared mcs.local root cause is plausible but not established. Existing BuildAPI closure remains intact. The separate Selenium DNS proposal is unchanged; no authorization to modify cluster DNS is inferred from this correlation. No remote operations were started for this comparison.


## DNS forwarding and DO-flag investigation

The user authorized checking the mcs.local route. Read-only Kubernetes service/EndpointSlice inspection shows kube-system/kube-dns10.254.0.10:53 maps UDP/TCP to10.18.26.6:8153. No k8s-app=kube-dns pods and no DNS-named ConfigMaps were visible across namespaces. Managed endpoint metrics identify CoreDNS1.14.6 and forward destination10.252.0.10:53. Its further forwarding chain was not exposed. Local infra-tf/dev/coredns.tf concerns a stale coredns-user customization and is not proof of the managed runtime configuration.

The original Chrome pod had been removed by autoscaling, so subsequent read-only DNS probes ran from existing deployment/buildapi-api, without creating a new pod/session. UDP and TCP both show absolute www.googleapis.com and existing vk-ms1-jenkins-test.mcs.local resolving in milliseconds via kube-dns, the managed endpoint and IPsec/BIND10.18.20.3. The nonexistent www.googleapis.com.mcs.local name times out at all three in2s. Direct cloud DNS10.18.20.65 is unreachable from that pod; this is source-specific and not evidence of global cloud-DNS failure.

Read-only SSH to youdo@10.18.20.3 confirms the running BIND configuration has zone mcs.local, type forward, forward only, upstream10.18.20.65. From the gateway, direct cloud-DNS ordinary queries succeed: existing private name3–7ms, negative search-expanded name NXDOMAIN2–8ms. The local BIND negative query times out even with a6s budget. Checking-disabled flags do not resolve it; running BIND has dnssec-validation no.

A controlled matrix separates EDNS from DNSSEC OK/DO. For the negative name, plain DNS and EDNS without DO return NXDOMAIN in2–9ms over UDP/TCP. EDNS with DO times out over UDP; TCP sometimes times out and sometimes closes before the response-length header. The current parser records the latter as an error, not a valid DNS response. For the existing private name, all modes including DO return NOERROR in4–9ms. A6s bounded packet capture on ens3 confirms BIND repeatedly sends the negative query to10.18.20.65 with EDNS DO and COOKIE, with no matching reply observed. Controlled plain/EDNS-no-DO queries and their NXDOMAIN replies appear in the same capture. This isolates a DO-dependent failure for negative names on the gateway-to-cloud-resolver path; cloud DNS internals versus an intervening network filter cannot be distinguished here.

Generated scripts/results are under /home/slnnk/ai-data/selenium-geolocation/: inspect_dns.py, dns_route_probe.py, dns-route-result.txt, gateway_dns_probe.py, gateway-dns-result.txt, bind_detail_probe.py, bind-detail-result.txt, edns_probe.py, edns-result.txt, edns_verbose_probe.py, edns-verbose-result.txt. Captures were bounded read-only subprocesses, automatically ended by timeout, with relevant text held in memory and returned to local files. All task shell commands exited. No configuration, service state or application data changed.

Candidate mitigation for review: disable EDNS specifically for server10.18.20.65 in BIND, then verify private positive and negative names, kube-dns behavior and fresh Chrome acquisition. BIND's per-server edns setting is documented at https://bind9.readthedocs.io/en/stable/reference.html . This is an untested proposal, not an implemented fix. Because managed CoreDNS's route beyond10.252.0.10 is unverified, changing gateway BIND alone must not be promised to fix all cluster DNS. Provider diagnosis of negative DO responses is another applicable route; no provider ticket was sent.


## DevOps-920 runtime workaround and local persistence

User approved the concrete runtime plan with `Сделай`: back up named.conf.local, add edns no for10.18.20.65 only, named-checkconf, rndc reconfig, DNS and fresh Chrome verification. Preflight found no existing upstream server block and recorded config SHA1e1743dce7070b82eac5b9f030e436e98018f3fddef6efcbea41420f05af41cd. The approved script /home/slnnk/ai-data/selenium-geolocation/apply_bind_edns.py copied the original to /var/backups/named.conf.local.pre-edns-20261111T151755Z, appended the server block and preserved file ownership/mode. Syntax passed, rndc reconfig exited0 and bind9 remained active. Result SHA2877e3ec4dbba96ade6ff01daece84546809028f8d2a7d134c79accf04ed75e8. Canonical named-checkconf output normalizes the address to10.18.20.65/32; verified effective edns no. Initial display regex missed the /32 form, not an application failure.

Read-only post-change DNS matrix from BuildAPI: negative www.googleapis.com.mcs.local returns NXDOMAIN via BIND2ms, kube-dns7–8ms and managed backend3–4ms, over both UDP/TCP. Existing private hostname and absolute Google names remain NOERROR,1–8ms. Fresh temporary Chrome152 session on selenium-node-chrome-85c5d99c9f-vbqrx returned real coordinates469ms on the initial call using high accuracy/timeout5000/maximumAge0, then7ms/8ms on repeats. Permission granted; secure test.youdo.sg origin. Session deletion succeeded and probe exited0. Accuracy remains2795716.633836537m. This verifies the DNS and browser-acquisition workaround, not complete task-creation UI or geocoder behavior. Results: dns-route-after.txt and after-result.json under the existing generated-data directory.

Rollback reference (requires separate user approval if needed): restore the backup to /etc/bind/named.conf.local, run named-checkconf and rndc reconfig. No rollback was performed.

For persistence, asked for the task ID against the explicit proposed sysadmins/automation-services branch <ID>-fix-private-dns-edns and fresh origin/master base. User supplied `DevOps-920`; resolved approved branch is DevOps-920-fix-private-dns-edns. Fetch refreshed origin/master to4385a463f7d7c0eeb938af2a99142fc9c70886ba. Before switching, verified the base changes do not overlap unrelated work. Created the approved branch in the existing checkout, preserving hashes of all unrelated tracked/untracked contents; no stash/reset/worktree. Existing unrelated23dirty paths and empty index preserved.

Task changes: roles/bind/templates/named.conf.local.j2 renders optional bind_no_edns_servers with per-server edns no; inventories/vkcloud/group_vars/ipsec sets that list from existing vkcloud_dns_servers. No hardcoded upstream in the shared role; other inventories default to no override. Local Ansible render succeeded3tasks; output without override is byte-identical to the baseline. Ansible role syntax-check passed. Rendered VK configuration passes gateway named-checkconf via stdin without installing it. Task-scoped git diff --check passed; broad check finds pre-existing trailing whitespace in unrelated cron-docker-clean.j2, intentionally preserved.

Publication proposal saved at /home/slnnk/ai-data/gitlab-workflow/DevOps-920/automation-services/ with proposal.json, actual task.diff, literal body.txt and snapshot.json. Commit `fix private dns edns`; ready MR `DevOps-920 fix private dns edns`; source DevOps-920-fix-private-dns-edns, target master. Project216 inspected, default master, current assignee a.solonenko, no matching open MR. CI has only three Molecule jobs: first branch push excluded; task paths do not match automatic Molecule changes rules; optional manual Nomad fallback exists, no deployment jobs/includes. Snapshot matches; user publication approval pending. No staging, commit, push or MR creation yet. Repository-local instruction review requires two reviewers before integration; no merge is proposed/authorized.

Runtime repair verified; Ansible persistence prepared and pending second supervised approval. Central DevOps-920 entry supersedes the earlier diagnosis-only/no-runtime-authorization proposal. Historical BuildAPI acceptance and DevOps-897 closure remain intact. No task processes/sessions remain.


## DevOps-920 publication completed

User explicitly approved the prepared task-only commit/push/ready-MR proposal with `Да`. Pre-stage snapshot check matched, initial index was empty. Staged only the two agreed files and verified the entire staged diff byte-for-byte against task.diff. Commit1cbb94766001742cd29cadb89abef119019e1377 (`fix private dns edns`) contains exactly that patch:2files,7insertions. Post-commit comparison matched; unrelated tracked/untracked content hashes remain unchanged and index empty.

Approved source branch DevOps-920-fix-private-dns-edns pushed successfully. Created ready [MR1394](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1394), title `DevOps-920 fix private dns edns`, target master, assignee a.solonenko, squash=false, remove_source_branch=true. Creation and separate GET-only verification both confirm exact expected SHA, title, source/target and literal body.txt description. [Pipeline142790](https://gitlab.youdo.sg/sysadmins/automation-services/-/pipelines/142790) is skipped, matching the first-push CI exclusion. No merge, release, extra deployment or manual pipeline job was performed.

Publication is complete. Runtime workaround and prior DNS/Chrome verification remain unchanged; source persistence is awaiting review/merge in the central proposed follow-up. All publication shell processes exited0. No task sessions/background commands remain. The earlier publication-pending checkpoints above are superseded by this section.


## DevOps-920 issue comment

User requested the prepared problem/solution comment, with the final MR-status sentence replaced by the MR URL alone, and explicitly instructed posting it. This wording preference is scoped to this comment, not a global reporting rule. GET confirmed DevOps-920 (71-139249) and no existing comments. POST created comment74-125509; separate GET verified its text exactly matches /home/slnnk/ai-data/gitlab-workflow/DevOps-920/automation-services/comment.txt. The comment states the DNS/DO cause, scoped gateway workaround and measured DNS/Chrome results, followed only by the MR1394 URL. No issue fields/status were changed. No new backlog action; existing proposed MR review/merge remains unchanged. All task commands exited and no background operations remain.


## User closeout

On2026-11-11 the user reported DevOps-920 closed (`Задачу закрыл`). Treat the task and its central follow-up as accepted complete; no further work requested. The runtime workaround was independently applied/verified and Ansible persistence published as1cbb9476/MR1394. The MR merge state was not independently checked in this closeout; do not infer a user/agent merge from issue closure. No external writes, new infrastructure checks or background operations were performed. This acceptance supersedes earlier live review/merge follow-up directions while preserving the publication evidence and UI/accuracy verification limits.
