---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nuget, gitlab, youdo-business]
---
# youdo.business job3219724 fails on missing ServiceCore Metrics version

## Summary

Job3219724 in project423 originally failed with NuGet NU1102: YouDo.ServiceCore.Logging >=1.0.16 and YouDo.ServiceCore.Metrics >=1.0.16 is unavailable from configured Nexus and nuget-private sources; logged nearest version is1.0.15. These requirements occur in the MR build and are outside the restored direct master inventory's 143 pairs. The pinned master inventory required Logging1.0.14 and Metrics1.0.14 for youdo.business; neither package at1.0.16 was in that list.

Both missing1.0.16 packages were subsequently published by the user from CI; fresh public Nexus metadata HTTP200 confirms both present. The user subsequently confirmed that the business build succeeded; follow-up verification backlog is closed.

## Task and context

User asked whether https://gitlab.youdo.sg/youdo/microservices/youdo.business/-/jobs/3219724 is related to NuGet. Read-only investigation only; no package publication, job retry or repository changes were requested or performed.

## Actions and evidence

GET job and trace using existing GitLab access route in current/.env; secrets kept in memory. Compact sanitized evidence: ~/ai-data/nexus-recovery/business-job-3219724.json. Status failed/script_failure, ref refs/merge-requests/3843/head, runner gitlab-runner-docker-1 (172.28.0.171). Internal API image build reports NU1102 through dependent projects and includes eight errors. Delegated full589768-byte trace processed only in memory: exactly two unique NU1102 missing packages (Logging and Metrics1.0.16). Fresh public Nexus metadata HTTP200 confirms neither1.0.16 exists. Compact summary: ~/ai-data/nexus-recovery/business-3219724-nuget-summary.json. Job build-business-internal-api, pipeline140667, sourceSHAa14de776a544ee3b833d5a9f37f22e2d7daee9d0.

## Findings and limits

The two missing package versions are the observed build blocker. Docker image absence in after_script follows the failed build and is not an independent primary cause. Prior143/143claim is scoped to the master inventory, not all MR references or every version of restored libraries. Correct next action is restore the required historical Logging1.0.16 and Metrics1.0.16 packages, then retry the requested failed build under separate explicit external-action approval.

## Changed files

This log and central backlog; no repository or remote-system changes.

## Risks

Only the observed job failure is diagnosed; service-wide restore and exhaustive transitive checks remain outside this read-only request. Live follow-up work is in ~/ai/TODO.md.

## Resolution after user CI publication

User reported publishing the packages from CI. Read-only public version metadata checks confirmed YouDo.ServiceCore.Logging1.0.16 and YouDo.ServiceCore.Metrics1.0.16 both present (HTTP200), without package downloads. Evidence: ~/ai-data/nexus-recovery/business-3219724-ci-published-metadata.json. Central TODO publication item closed; original failed build retry/result verification retained separately. No agent external changes or retry performed.

## Build outcome confirmed by user

After the two CI publications and successful metadata checks, the user reported the business build succeeded. This is user-confirmed evidence; no additional job ID or agent-triggered retry was supplied. Central business build verification item closed.
