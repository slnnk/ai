---
system: automation-services
status: verified
checked: 2026-11-10
tags: [nginx, gitlab, DevOps-913]
---
# DevOps-913: forward client headers for b2bautomation and jarvis

## Task
Prepare the requested client-header changes and MR in sysadmins/automation-services.

## Context
Existing checkout: `/home/slnnk/git/automation-services`. Base: `origin/master`, SHA `6d467c2e196f347bfe500bb96f0af0ce4e03f111` after fetch. Existing unrelated Jenkins, runner and inventory edits are preserved. The staging area was empty before work.

## Actions
The initial proposal set both headers for both domains. The user supplied Servicepipe's statement that X-Src-Port forwarding was configured in August. The final proposal preserves the incoming jarvis port and sets the b2bautomation port from the connection.

First gate: proposed repository automation-services, new branch `DevOps-913-forward-client-ip-port`, base `origin/master`, b2bautomation two headers and jarvis IP only. The user explicitly approved with `Да` on 2026-11-10. Created that branch and added exactly three lines across two templates.

Second gate: prepared local diff and publication snapshot; the user explicitly approved the complete publication proposal with `Да` on 2026-11-10. Commit and MR names: `forward client headers for b2bautomation and jarvis` and `DevOps-913 forward client headers for b2bautomation and jarvis`. Target: `master`. Proposal artifacts: `~/ai-data/gitlab-workflow/DevOps-913/automation-services/`.

## Findings
DNS observed: jarvis.youdo.com -> 91.206.127.88 (RIPE RU-SERVICEPIPE); b2bautomation.youdo.com -> 92.53.80.150 (RIPE SELECTEL-NET). DNS alone does not establish the complete origin path. Servicepipe forwarding is user-reported; live header contents were not captured. The shared realip include restores the client IP from trusted X-Forwarded-For.

Validation: strict Jinja rendering for prod/test names passed. Extracted location blocks passed local nginx 1.18 syntax checks and HTTP echo verification: b2bautomation overwrites a supplied IP/port with connection values, jarvis overwrites IP and preserves supplied port 51000. Harness uses a temporary backend and representative add_custom_header include. All temporary servers exited. Nginx emitted an initial default error-log permission alert but both checks and HTTP assertions succeeded. Full vhost syntax was not checked because local nginx 1.18 lacks the existing http2 directive; Molecule was not run.

Task-scoped git diff --check passed. Global diff --check reports existing trailing whitespace in unrelated roles/gitlab-runner/templates/cron-docker-clean.j2; preserved.

CI inspection: only Molecule tests are declared. The first branch push is excluded by zero before-SHA; later nginx branch updates may run molecule-nginx. MR rules require CI_COMMIT_BRANCH and do not match MR pipelines. Nomad fallback job is manual. No deployment/release jobs are declared.

## Changes
- roles/nginx/templates/vhost/b2bautomation.youdo.com.j2: X-Real-IP from $remote_addr and X-Src-Port from $remote_port.
- roles/nginx/templates/vhost/jarvis.youdo.com.j2: X-Real-IP from $remote_addr; incoming X-Src-Port remains unmodified.

## Status and risks
Local implementation, scoped checks and publication are complete. Commit `03dfaef36fdc822ecde8c4f6c75b70fd3beaabb8` contains exactly the two reviewed templates and three added lines; staged diff was inspected before commit and the resulting commit matched. Push succeeded. [MR !1391](https://gitlab.youdo.sg/sysadmins/automation-services/-/merge_requests/1391) is ready, assigned to a.solonenko, source `DevOps-913-forward-client-ip-port`, target `master`, squash false, source deletion on merge true. GitLab helper verified SHA/title/body/source/target; pipeline142626 is skipped. Initial sandbox API call failed with URLError; read-only inspection confirmed no MR before the approved retry created it. Publication task is closed in [central TODO](../../../../TODO.md). No merge, broader rollout or manual CI execution authorized. The separately approved manual b2bautomation application on balancer-internal is recorded below. Shared templates affect all environments using them after a separately authorized rollout. The local HTTPS-to-upstream path for b2bautomation was subsequently verified below. The jarvis browser path through Servicepipe was subsequently verified on balancer02 below; final application handling and the balancer03 real-request path were not captured.

## Portable lesson
none

## Manual b2bautomation application on balancer-internal
On 2026-11-10 the user requested manual application to balancer-internal, then explicitly approved the concrete SSH transaction with `Да`: backup, add both headers, nginx syntax check, reload, restore file on failure. Local application script: `~/ai-data/gitlab-workflow/DevOps-913/automation-services/apply_b2bautomation.py`.

Applied only `/etc/nginx/conf.d/b2bautomation.youdo.com.conf` on `sc-balancer-internal.youdo.corp` / `172.28.0.145`. Backup: `/var/backups/nginx/b2bautomation.youdo.com.conf.DevOps-913.20261110T145050721580Z`. Added `proxy_set_header X-Real-IP $remote_addr;` and `proxy_set_header X-Src-Port $remote_port;` inside the existing proxy location. nginx1.30.1 syntax check passed, systemctl reload succeeded at17:50:50MSK and service remained active. A separate read-only SSH check confirmed both lines, ExecReload status0 and systemd's successful reload log. A subsequent bounded live capture verified the nginx-to-upstream headers; see the verification below. Jarvis and other hosts were not changed. All task commands exited; no background operations remain.

## Live b2bautomation header verification
On 2026-11-10 the user requested header forwarding verification. A bounded tcpdump capture on balancer-internal observed only the marked request's selected headers in the reported output; no remote files were written. A local HTTPS GET to b2bautomation.youdo.com/robots.txt with a unique query marker returned HTTP200. curl used source port8880 and deliberately supplied X-Real-IP192.0.2.12 and X-Src-Port1. The outgoing HTTP request to the Consul proxy carried Host b2bautomation.youdo.com, X-Real-IP127.0.0.1 and X-Src-Port8880. Thus nginx overwrites both input headers with the actual connection IP/port and forwards them to the next upstream. This verifies the local balancer HTTPS path, not Servicepipe or final application handling. The capture process was terminated and reaped in the verification script's finally block. SSH exited0; no background operations remain.

## Manual jarvis application on hardware balancers
On 2026-11-10 the user requested manual jarvis application on both hardware balancers. After read-only inspection, the user explicitly approved both concrete SSH transactions with `Да`: backup the jarvis vhost, add X-Real-IP only, nginx syntax check and reload, preserve incoming X-Src-Port. Applied sequentially to msk3-balancer02.youdo.corp /172.24.0.22 and msk3-balancer03.youdo.corp /172.24.0.23 using the local script `~/ai-data/gitlab-workflow/DevOps-913/automation-services/apply_jarvis.py`.

Both `/etc/nginx/conf.d/jarvis.youdo.com.conf` files now contain `proxy_set_header X-Real-IP $remote_addr;` after the existing Host directive. X-Src-Port is not overwritten. Backups: `/var/backups/nginx/jarvis.youdo.com.conf.DevOps-913.20261110T145528286240Z` on172.24.0.22 and `/var/backups/nginx/jarvis.youdo.com.conf.DevOps-913.20261110T145548776559Z` on172.24.0.23. nginx1.30.1 syntax checks passed on both; pre-existing server_names_hash sizing warnings remained. Reload succeeded at17:55:29MSK and17:55:54MSK respectively. Separate read-only checks confirmed both config lines, active nginx, ExecReload status0 and successful reload journal messages. A subsequent browser request verified the Servicepipe-to-nginx-to-upstream headers on balancer02; see below. No other vhost or hash tuning was changed. All SSH commands exited; no background operations remain.

## Real browser request through Servicepipe
On 2026-11-10 two CLI HTTPS requests received HTTP403 at Servicepipe's public address91.206.127.88 and no corresponding marked upstream request appeared on either hardware balancer. The user offered to open Jarvis in their browser. A bounded capture of selected headers on both balancers then observed the uniquely marked browser GET on msk3-balancer02. Outgoing Host was youdo-business-tickets-web.proxy.youdo.local; X-Real-IP equaled X-Forwarded-For (the browser client's public IP, omitted here); X-Src-Port39761 was present. This verifies that the real Servicepipe path delivers a source-port header which the changed nginx location preserves, while nginx supplies the real client IP. It does not independently measure the browser's post-NAT port or final application handling. The corresponding request was not observed on balancer03 at the time of the first capture result.

Both bounded remote captures subsequently exited and their SSH processes returned0. Final result: marked request captured on balancer02 only; no background operations remain.

## YouTrack completion comment
On2026-11-10 the user explicitly requested publishing the final edited comment to DevOps-913. Read-only inspection confirmed the issue and no matching/related comment. Created comment74-125443 with the agreed concise text and MR1391 link; a separate GET verified the exact text. No task status change was requested or performed. All commands completed.

## User-confirmed closure
On2026-11-10 the user reported merging MR1391 and closing DevOps-913. Treat this task as complete. Merge and issue closure are user-reported and were not independently queried in this turn; earlier no-merge statements describe the prior publication/application stages. No further rollout or diagnostics are pending for the agreed scope.
