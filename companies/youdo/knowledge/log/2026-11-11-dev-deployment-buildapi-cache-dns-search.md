---
system: dev-deployment
status: verified
checked: 2026-11-11
tags: [buildapi, redis, dns, kubernetes]
---
# BuildAPI cache clear fails on DNS search expansion

## Task

Diagnose HTTP 500 when clearing cache through BuildAPI. Screenshot response timestamp: 2026-11-11 07:47:52 UTC; affected stand test5.

## Context

Existing checkout /home/slnnk/git/buildapi at 385e974, branch DevOps-898-deploy-buildapi-on-vk-k8s, clean. Cached origin/master is stale at 1b8b8ce6; no fetch performed. Runtime: deployment/buildapi-api in namespace buildapi, VK Kubernetes.

## Actions

Read-only Kubernetes logs, live ConfigMap, pod DNS checks and Redis PING. No FLUSHALL, deployment, repository edits or external mutations performed.

## Findings

The matching POST /cc traceback shows DNS timeout after five seconds, followed by TypeError from int(None) in redis connection initialization. app.py clear_cache passes the result of dns_resolver.get_a_redis_port directly as port; the helper catches DNS exceptions and returns None.

Pod /etc/resolv.conf has ndots:5 and Kubernetes search domains. Configured DNS servers are 10.18.26.34, 10.18.26.38, 10.18.26.37. All answer explicit SRV queries for test5.cache.service.vk-test.consul with port1905 and target 0a121a26.addr.vk-test.consul. System resolver explicit SRV also succeeds. Redis PING to 10.18.26.38:1905 returns True.

The existing helper using resolver.query on the name without a terminal dot reproducibly times out after5.008seconds. The identical helper with absolute name test5.cache.service.vk-test.consul. returns1905 in0.011seconds. This isolates search expansion as the demonstrated trigger. No cache clear was attempted; successful FLUSHALL is unverified.

## Changes

Knowledge log, existing Nomad map and central proposal only. No application changes. Proposed correction: absolute SRV name (or explicitly disable search), bounded Redis connection/read timeouts and explicit dependency-error response rather than passing None.

## Status and risks

Diagnosis complete; fix awaits supervised repository branch/base approval. Suggested new branch fix/buildapi-cache-dns from freshly fetched origin/master in existing checkout. Publication and deployment require separate applicable approvals. Remaining proposal is tracked in central TODO under dev-deployment.

## Portable lesson

none

## DevOps-917 implementation and approval record

The user created DevOps-917 and explicitly confirmed the proposed repository /home/slnnk/git/buildapi, new branch DevOps-917-fix-buildapi-cache-dns and refreshed origin/master base (reply `Да`). Fetch updated master from1b8b8ce6 to9531d9ef; the clean existing checkout was switched to the approved new branch. The earlier generic fix/buildapi-cache-dns proposal is superseded by this approved ticket branch. No existing user changes were present.

Local implementation: dns_resolver.py uses Resolver.resolve with an absolute SRV name and search=False, returns integer SRV port, sets lifetime5 and propagates DNS exceptions. app.py uses an absolute Redis hostname,5second socket connect/read timeouts and a context manager; DNS/Redis failures are logged and return HTTP503. Successful response and FLUSHALL behavior remain unchanged. tests/test_cache.py runs authenticated Flask endpoint tests with mocked external services and startup Mongo discovery.

Validation:5 unittest cases pass, including DNS timeout/NXDOMAIN/NoAnswer, Redis connection/read timeout, successful flush and unauthorized request. Requirements installed in isolated /tmp/buildapi-devops917-venv; Python3.8 local validation with pinned Flask2.0.2/dnspython2.1.0/redis4.6.0. Production image uses Python3.10; no container build or runtime rollout tested here. pip check, git diff --check and kubectl kustomize all passed. No external cache clear occurred.

Publication proposal: commit `fix cache dns resolution`; ready MR `DevOps-917 fix cache dns resolution`; source DevOps-917-fix-buildapi-cache-dns, target master. Description is one Russian paragraph plus task link, saved with proposal/diff/snapshot under /home/slnnk/ai-data/gitlab-workflow/DevOps-917/buildapi. API inspection confirms project77/default master, assignee a.solonenko and no open matching MRs. MR CI runs pylint, kustomize validation and image build/push to project registry; deploy is manual/tags-only. Branch push has no matching jobs. Publication approval pending; no stage/commit/push/MR/tag/merge/deployment performed.

This implementation checkpoint supersedes the earlier diagnosis-only status. Local fix is complete; publication and runtime verification remain tracked centrally.

## DevOps-917 publication completed

User explicitly approved the prepared commit/push/ready-MR proposal with `Да`. Snapshot comparison matched; actual staged diff contained only app.py, dns_resolver.py and tests/test_cache.py. Commit bb23b9520a3eaccef3d6bd84b5b6c273071157a9 exactly matched the reviewed saved patch. Branch push succeeded and MR !41 was created and verified, assigned a.solonenko, squash=false, remove_source_branch=true, draft=false. URL: https://gitlab.youdo.sg/sysadmins/buildapi/-/merge_requests/41. No agent merge, tag or deployment was performed.

Subsequent verification initially encountered sandbox URLError; escalated read-only retry found no open MR. Direct GET by IID confirmed user a.solonenko merged MR !41 at2026-11-11T11:08:01.569+03:00, merge SHA332bcd1dbc16c979e10e95dcf90bf2e01660ccc5. Title/source/target/sourceSHA and exact description match the approved proposal. MR pipeline142720 is canceled; a tag0.5.14 pipeline142721 on the merge SHA is running. This observed release is user initiated; it grants no additional agent runtime permissions. Current CI: https://gitlab.youdo.sg/sysadmins/buildapi/-/pipelines/142721.

Publication complete; local checkout clean and no task shell processes remain. Release CI remains external and running at last observation; inspect/cancel through pipeline142721 UI if needed. Runtime deployment and successful cache clear remain unverified. This checkpoint supersedes publication-pending statements above; remaining action is central TODO.

## User acceptance and YouTrack comment

User reported successful deployment and subsequently confirmed cache clear works (`Работает`). No additional agent runtime check or cache flush was performed. These reports supersede the earlier running-release/runtime-pending checkpoint. Central DevOps-917 follow-up closed based on user acceptance, without claiming independent verification.

User requested a problem/solution comment, then specifically excluded the paragraph about regression tests, version/deployment and user confirmation. This omission applies to this comment, not to global reporting rules. Explicit instruction to add the revised comment authorized the YouTrack write. GET confirmed issue DevOps-917 and no existing comments; POST created comment74-125488; GET verified exact text. Comment includes DNS search-expansion timeout, missing Redis port, absolute DNS-name fix, Redis timeouts, HTTP503 handling and MR41 link only. No issue fields or status were changed.
