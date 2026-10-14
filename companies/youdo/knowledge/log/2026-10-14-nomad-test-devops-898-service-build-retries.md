---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, gitlab-ci, nexus, recovery]
---
# DevOps-898 release service build retries

## Summary

Release preparation and builds completed for the final approved launch scope. Ten single services plus LogReader test5 are deployed through GitLab and runtime-verified. A fresh chat-content release build succeeded without the optional cache change. Vks-policy-generator was excluded as unused; its apt-source MR !18 was closed without merge/tag/deployment. Socket per-stand behavior was restored in merged MR !82. Other fifteen SQL stands remain a later LogReader dependency.

## Task and context

Scope11single+2dynamic from [DevOps-898](https://youtrack.youdo.com/youtrack/issue/DevOps-898) and articleDevOps-A-33. Prefer an existing terminal release-tag pipeline; otherwise latest master. Inspect exact commit/ref/job identity and downstream behavior before issuing targeted retries. .NET preparation starts at prepare-nuget; other languages use actual preparation stages. Do not create a pipeline that can auto-deploy production without separate approval.

## Actions

Read current/historical CI and candidate job metadata. Existing retry_library_jobs.py supports exact ref/SHA/job-name validation and targeted retry/play; will reuse or minimally adapt task-local operational helpers. Secret values never stored. Details and sanitized state live in /home/slnnk/ai-data/DevOps-898.

## Findings

Final13release candidates and exact job IDs are recorded in build-candidates-dotnet.json and build-candidates-other.json. Revised sequence: finish reviewed repository/CI/HCL changes and source selection, then rebuild once. Existing retry uses old compiled YAML plus live shared Dockerfile. prepare-nuget is independent; component builds require set-variables dotenv, which is missing for all5non-.NET selected pipelines and expired for4.NET candidates. No prepare-docker prerequisite. Builds overwrite latest and publish chosen tag. Deployment never uses historical old CI jobs to claim new configuration applied.

Pending runtime results are not success claims. Restored GitLab artifact expiry/missing dependencies may require regenerating preparation jobs in the selected pipeline before component builds. Record actual pipeline/job identity and selected version, results and failure reason below when verified.

## Changes and approvals

The user asked whether retries create a new pipeline. We explained that retries use the existing pipeline's compiled CI configuration and that historical deployment jobs will not be used for the VK rollout. The user then approved 21 preparation retries. Their final state is 15 successful and six failed: geocoder, call-service, textvalidation, blec, mailer and LogReader prepare-nuget received HTTP 429. The origin of NuGet throttling remains under investigation; unrelated Nexus REST search throttling alone does not establish the cause.

The user separately approved seven build retries using ready-build-targets.json. Command: `python3 /home/slnnk/ai-data/nexus-recovery/retry_library_jobs.py --targets /home/slnnk/ai-data/DevOps-898/ready-build-targets.json --results /home/slnnk/ai-data/DevOps-898/ready-build-results.json --retry --resume`. GitLab returned new jobs 3226175 through 3226181 for doc-generator, DebuggingEvents, chat-content, tinkoff, vks-policy-generator, pechkin and Socket, respectively. A subsequent GET verified all seven running. They build eight application components; successful image publication has not yet been established.

A hardcoded NuGet credential was encountered in shared v3/.dotnet-nuget.yml:53; its value is not retained in notes. The location-only follow-up is in the central backlog.

The HTTP 429 source was subsequently localized to nginx on Nexus backend 10.18.24.233:80, before Jetty: its inherited global limit is 150 requests/s with burst 150. Public proxy logs show NuGet 429 from that upstream, while Nexus request logs show no NuGet 429. The user approved `python3 /home/slnnk/ai-data/DevOps-898/scripts/retry_nuget_serial.py --apply`: retry six exact failed jobs sequentially, stop on the first failure, and do not change nginx or deploy applications. Geocoder retry 3226182 succeeded; call-service retry 3226183 is running. Further results are recorded in serial-nuget-retry-results.json.

The user suggested adding the new address to the existing nginx whitelist. Read-only paired socket evidence identifies the backend source as VK gateway 10.18.20.3, after SNAT. Neither the runner's public source nor the public proxy's private address is the correct key for this backend limiter. A concrete whitelist patch is being prepared for review; it has not been applied.

Update: the user explicitly approved the one-line gateway whitelist patch, which was applied at 16:57:33 UTC; nginx test and reload passed. Sequential call-service restore 3226183 succeeded. Textvalidation restore 3226184 failed, and the script stopped as designed without retrying blec, mailer or LogReader. Its final failure cause is being checked against the whitelist application time; do not assume it is still throttling.

User-authorized action scope: rebuild application artifacts/images only, including required preparation. No deployment, repository edits, Git publication or branch switching authorized in this request. Public-test remains excluded. Open work is tracked in ~/ai/TODO.md only.

## Portable lesson

none

## Latest build evidence (2026-10-14)

Five of the original seven build retries succeeded; chat-content failed at its one-hour timeout and vks-policy-generator failed fetching obsolete Debian buster apt repositories. No repository fix has been applied. After the approved nginx gateway whitelist update, the nine new release pipelines 140901–140909 passed monitored NuGet restores; seven have ready manual VK deploy jobs. Production jobs are inactive in this launch set. Socket was not included. These facts supersede older running/pending and throttle-diagnosis statements above. [Latest rollout and scope correction](2026-10-14-nomad-test-devops-898-implementation.md#latest-verified-rollout-and-scope-correction-2026-10-14).

## Textvalidation new release source (2026-10-14)

After the user rejected extra production-rule overrides, all twelve local textvalidation rule lines were cancelled. The user explicitly requested a new tag; project 383 tag `1.0.4` now points to merged master `1fa4239704ff4d99e1b5e58a2dbccb3261375036`, including current logging HCL. Pipeline creation/result monitoring is pending; tag creation is not deployment approval.

## Final build and deployment result (2026-10-14)

Ten single services and the explicitly authorized LogReader test5 pilot passed actual runtime checks after GitLab deployment. The earlier chat-content timeout was resolved by the successful fresh release build without a cache-code change. Vks-policy-generator is excluded by user decision; MR !18 was explicitly closed without merge or tag 0.0.27. Socket reverse MR !82 is merged and per-stand CI restored. [Final versions, approvals and limits](2026-10-14-nomad-test-devops-898-implementation.md#verified-final-launch-scope-2026-10-14).
