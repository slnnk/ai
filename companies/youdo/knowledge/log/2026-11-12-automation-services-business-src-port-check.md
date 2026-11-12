---
system: automation-services
status: verified
checked: 2026-11-12
tags: [nginx, headers, DevOps-913]
---
# business.youdo.com source-port forwarding check

## Task
Check whether X-Src-Port is forwarded for business.youdo.com, following the completed DevOps-913 work. Investigation only; no configuration changes authorized or made.

## Context
Existing checkout `/home/slnnk/git/automation-services`, clean branch `sync`, HEAD `b6ae6699b85c2ada474088d1cc4a0d86a196c91e`; no fetch or repository mutations. Read live vhosts on both hardware balancers, sc-balancer-redirect and sc-lb-pub01. Prior task: [DevOps-913](2026-11-10-automation-services-devops-913-client-headers.md).

## Actions
Read nginx vhosts and shared nginx.conf/includes. Ran bounded 20-second tcpdump captures selecting only the marked request headers; no remote files written. Public HTTPS GET `/robots.txt` with a unique query marker and no injected headers returned HTTP200. Scripts are under `~/ai-data/gitlab-workflow/DevOps-913/automation-services/`: capture_business.py, check_business_external.py, check_business_selectel.py.

## Findings
Public DNS resolved to92.53.80.147, which is directly assigned to eth1 on sc-lb-pub01.youdo.corp (internal172.28.0.141). The marked request was captured leaving this nginx toward proxy.service.consul over HTTP80. Host was business.youdo.com; X-Real-IP was present; X-Src-Port was absent. No marked request was observed on either hardware balancer or sc-balancer-redirect. The forwarding checks exited1 because the header assertion correctly detected absence; this is an observed missing header, not a passing test.

Live sc-lb-pub01 vhost location / sets X-Real-IP from $remote_addr, but does not generate X-Src-Port. No proxy_pass_request_headers or X-Src-Port overrides were found in nginx.conf/shared includes. The local business.youdo.com template has the same behavior. This confirms absence for the tested direct public path, without claiming anything about other DNS views or final application processing. The earlier conclusion that Servicepipe was absent was unsupported: a public address assigned to nginx does not exclude routed/L3-L4 protection. Whether Servicepipe participates in this path remains unverified. The capture establishes header absence only.

## Changes
Knowledge bookkeeping only. No nginx files, services, repository branches or external trackers changed.

## Status and risks
Requested check complete. All four bounded captures were terminated/reaped; all SSH processes exited. No background operations remain. Adding a header is outside this read-only request and requires the repository and external-change approvals if requested. The completed DevOps-913 TODO remains closed; no new implementation task was agreed.

## Portable lesson
none

## Follow-up clarification (2026-11-12)

The user questioned the claim that sc-lb-pub01 operates without Servicepipe. Local nginx configuration includes shared qrator_servicepipe real-IP trust handling, which supports possible proxy use but does not establish the actual request path. Public DNS and interface assignment alone cannot establish absence of Servicepipe network protection. Corrected the unsupported topology conclusion; X-Src-Port absence on the captured request remains verified. No additional remote operations started.

## Implementation proposal (2026-11-12, awaiting agreement)

The user requested proposed changes to add X-Src-Port for business.youdo.com. Proposed repository sysadmins/automation-services, new branch DevOps-913-business-src-port from freshly fetched origin/master (cached SHA a8b70e0177d581f77f72aa5e1312dabae2899ef3 at proposal time). Add proxy_set_header X-Src-Port $remote_port in location / of business.youdo.com.j2 only when balancers_public is in group_names. This targets the currently single sc-lb-pub01 and preserves incoming ports on hardware/other balancers. The shared server block also serves business-api.youdo.com, so the proposal explicitly includes that alias. Questionnaire special location remains outside this proposed generic-location change. Suggested validation: render public and hardware inventory variants, verify supplied header is overwritten on the public variant and preserved on the other variant, then separately approved live nginx syntax/reload and marked request capture on sc-lb-pub01. No implementation, branch switch, publication or rollout is authorized by a proposal request.

## Approved implementation and manual application (2026-11-12)

The user rejected the proposed inventory-group condition and approved the unconditional header after clarification that business-api.youdo.com shares the server block. The user then requested manual application and Ansible preparation, accepting the proposed branch/base. This supersedes the earlier conditional proposal and investigation-only status. No durable cross-task preference was inferred from the task-specific rejection of if conditions.

Fetched origin/master and created DevOps-913-business-src-port from457cf622c6ce4ebf2fe97eff501b4998d3363a2b in the clean existing checkout. Added exactly one unconditional line after X-Real-IP in roles/nginx/templates/vhost/business.youdo.com.j2: `proxy_set_header X-Src-Port $remote_port;`. Final git diff --check passed; status contains only that modified template; nothing staged, committed or pushed. First repository gate was satisfied by the implementation request after the explicit repo/branch/base proposal. Proposed eventual commit subject: `forward source port for business`; MR title: `DevOps-913 forward source port for business`. Publication was not requested or performed.

The user explicitly answered `Да, применить` to the concrete remote transaction: back up sc-lb-pub01 /etc/nginx/conf.d/business.youdo.com.conf, insert the source-port directive, nginx -t, systemctl reload nginx, restore file on failure. Executed the prepared apply_business.py over SSH to172.28.0.141. Backup: /var/backups/nginx/business.youdo.com.conf.DevOps-913.20261112T081043328621Z. Syntax passed, reload succeeded, service active. nginx warned about variables_hash sizing; no tuning was performed. No other balancer was changed.

Validation: strict Jinja production/test render and extracted-location nginx1.18 syntax plus HTTP echo test passed; caller-supplied X-Src-Port51000 was replaced by the connection port. Harness initially needed whitespace assertion adaptation; final checks passed. Local nginx emitted its default startup error-log permission alert but syntax/runtime assertions passed. Full vhost syntax was validated by live nginx before reload, not by local nginx1.18. Temporary local servers stopped.

Post-reload public GET /robots.txt with unique marker returned HTTP200. Bounded selected-header capture on sc-lb-pub01 observed Host business.youdo.com, X-Real-IP present and X-Src-Port28028. sc-balancer-redirect did not observe the marked request. Port corresponds to nginx client connection; no claim that it equals pre-NAT source port. Both captures and SSH commands exited0 with cleanup; no background operations remain. The reused check script prints a generic hardware-nginx success label, but the structured capture identifies sc-lb-pub01.

Requested manual application and local Ansible preparation are complete. Broader Ansible rollout/publication remains unperformed and requires a separate request/approval; no such task is pending in this session. Original DevOps-913 closure remains historical.

Applicable learning outcomes: discussion-before-implementation followed (waited for implementation request); existing checkout preserved without worktree; remote change waited for exact transaction approval. No unrelated checkout changes existed to exercise mixed-change preservation. Final patch is the user's corrected unconditional scope.

## MR publication preparation (2026-11-12)

The user requested MR preparation. Prepared ready MR proposal and immutable snapshot under ~/ai-data/gitlab-workflow/DevOps-913/automation-services/business/. Actual net diff remains exactly the one unconditional template line; empty index and no other changes; git diff --check passed. Proposed source DevOps-913-business-src-port, target master, commit `forward source port for business`, title `DevOps-913 forward source port for business`. Exact Russian body is in body.txt: one paragraph explaining the shared business/business-api header and the DevOps-913 link. Read-only GitLab inspection found no existing open MR; default master, squash default_off, assignee a.solonenko, recent remove_source_branch true. CI declares only Molecule tests, first branch push excluded by zero before-SHA, branch-dependent rules do not match MR pipelines; Nomad fallback is manual. No release/deploy jobs or external includes. Reused successful task checks without unnecessary reruns. Waiting for the second supervised approval of the concrete publication proposal; no stage/commit/push/MR write performed. Inspection process exited0; no background operations remain.

## Approved publication result (2026-11-12)

The user explicitly approved the complete second-stage proposal with `Да`. Snapshot check matched before staging; inspected the entire staged diff: exactly one added source-port directive in the one agreed template, no other staged work. Committed `b16b69d562effb27c236ea41d99e65c243871806`, subject `forward source port for business`; resulting commit matched the reviewed patch. Push of DevOps-913-business-src-port succeeded after a sandbox DNS failure was retried with escalation (the failed sandbox attempt could not resolve GitLab). No force or target push.

Created ready [MR !1397](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1397), title `DevOps-913 forward source port for business`, source DevOps-913-business-src-port, target master, assignee a.solonenko, squash false, remove_source_branch true. Creation helper and separate verify both confirmed branch/MR SHA, title, exact description and source/target. Pipeline142851 is skipped, not a test pass. No merge, broader rollout, tracker write or manual CI execution performed.

Original/final names and body were accepted unchanged at this publication stage; earlier scope correction rejecting conditions remains retained above. Repo status is clean and final commit diff --check passed. Publication task complete; no agreed session actions remain. All push/API commands exited0 and no background operations remain. Previous uncommitted/unpublished statements describe the earlier preparation stage and are superseded by this publication.

## Simplicity proposal review (2026-11-12)

In a subsequent global-rule discussion, the user cited this task as an example of
unnecessary complexity and requested proposed simplicity wording before adoption.
The recorded original proposal conditioned the directive on inventory membership;
the final accepted implementation was one unconditional directive. The initial
condition attempted to preserve behavior on other balancers, but that restriction
was not a requested requirement. The source shows a rejected conditional proposal,
not a conditional directive deployed to production.

Proposed general lesson: each added condition, exception, configuration option or
abstraction needs a concrete requirement or verified system constraint; hypothetical
future needs do not justify complexity. This is a candidate global rule awaiting
review, not a blanket prohibition on conditions or operational safeguards. No code,
live service or existing approval boundaries changed in this discussion.
