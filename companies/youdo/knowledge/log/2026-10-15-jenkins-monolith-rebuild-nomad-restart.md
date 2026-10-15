---
system: jenkins
status: verified
checked: 2026-10-15
tags: [jenkins, gitlab, nomad, nexus, monolith]
---
# Monolith release rebuild and direct test5 Nomad restart

## Summary

User explicitly authorized rebuilding monolith and then restarting the Nomad job with rebuilt images, bypassing Jenkins deployment. Both artifact and Docker builds succeeded; all20image digests changed. Direct Nomad deployment9ee77925 completed successfully: both groups healthy,19service tasks running with zero restarts; pre/post migration lifecycle tasks completed. Representative finance/seocms logs have no MessageBus exception. Monolith source changes remain forbidden. No Restore/DB reset/other Jenkins stages authorized in this continuation.

## Preparation and authorization

Exact selected release pipeline139914, sourceSHAf89090ed12073eacceef6d05530cf2df53b764e5, project18. Existing build_release3225571/build_docker_release3226107 successful; no other running project pipelines. Snapshotted registry metadata for20numeric tags139914 and test5 Nomad baseline version2/jobmodifyindex7185. Job isdead/Stopfalse; datacentervk-test/default namespace. Full Nomad job spec kept only in memory, not written to notes or receipts.

## Actions

- Original release build caches ./nuget-packages under fixednuget key. Scoped GraphQL runnerCacheClear gid://gitlab/Project/18 invalidated this project cache to avoid restored old MassTransit bytes. Exact mutation/schema checked against this GitLab instance and official API reference. No runner/global cache or source edit. Cake restore additionally uses NoCache=true.
- Retried build_release3225571 as [job3226699](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3226699) in same139914 pipeline. FinalSUCCESS933.122377s, artifact1546296587bytes. Exact corrected MassTransit1.8.1 SHA512 verified in Installed trace before Docker retry; runner reported no extracted cache for newnuget-3-non_protected key. No MSB3277 conflicts observed.
- Helper monolith-nomad-rebuild.py and receipt monolith-nomad-rebuild-receipt.json under ~/ai-data/jenkins-recovery protect duplicate mutations and exactSHA/target. Planned follow-up uses build_docker_release only after successful build/contenthash verification, registry metadata verification, then test5 job registration with images pinned to fresh digests and EnforceIndex. Existing fields/lifecycle retained; no Jenkins trigger.

## Findings and limits

Docker release job normally pushes20images under numeric139914 and release MR-title aliases; it does not run production deployment jobs. New digest references avoid reusing stale local Docker images under unchanged numeric tags. Representative finance/seocms digest changes required. Work completed as recorded below: successful images and direct Nomad rollout; application business flows were not exercised. Original job pre/post migration lifecycle remains part of starting the monolith job; this is not a Restore DB reset.

## Related work

[MassTransit correction](2026-10-15-nexus-messagebus-181-assembly-repair.md) and [runtime diagnosis](2026-10-15-jenkins-monolith-messagebus-assembly-mismatch.md).

## Docker build follow-up

Retried build_docker_release3226107 as [job3226700](https://gitlab.youdo.sg/youdo/youdo/-/jobs/3226700), same139914pipeline. Initialrunning; onlybuildjobsretried. Registry verification and direct Nomad restart pending successful publication.

## Images and direct Nomad registration

Docker job3226700 SUCCESS791.3s, trace confirms artifact3226699 used and40pushes complete (numeric andreleasealiases). Registry metadata verified all20numeric139914images have changed digests versus prebuild snapshot. User-authorized Nomad registration accepted newjobVersion3/JobModifyIndex7265, evaluation7cf5e401-46a8-adcf-cc6d-388db10cfa4a, deployment9ee77925-032d-a7c2-acc4-4867ed265714. Changed only21task image references to20verifieddigestrefs; retained other job fields/lifecycle, Stopfalse, EnforceIndex. No Jenkins/Restore launched. Newsvc allocationeedf8a47-96f1-b31e-070c-5e6c2d7dda2e andwebfe77a222-e010-377d-0350-f782bfd120a5; firstcheckpoint prestartmigrationrunning, other tasksawaitingstart. Final deploymentSUCCESSFUL, both groups HealthyAllocs1/UnhealthyAllocs0. Svc8running+2completedlifecycle tasks; web11running. All current tasks have failedfalse/restarts0.

## Final runtime verification

Nomad jobyoudo-test5 version3 running; deployment9ee77925-032d-a7c2-acc4-4867ed265714 successful. Both groups healthy with1allocation each. Existing old failed deployment remains historical, not current rollout. Last8KBstdout/stderr of finance/seocms inspected read-only: previous MessageBusbindingerror absent and no exception classes in sampled output. No Jenkins trigger, Restore, DB reset, source edit or unrelated job change. Probe demonstrates corrected startup and Nomad health, not comprehensive application testing.
