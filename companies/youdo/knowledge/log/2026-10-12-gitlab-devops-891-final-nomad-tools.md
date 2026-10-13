---
system: gitlab
status: verified
checked: 2026-10-12
tags: [registry, base-images, recovery]
---
# DevOps-891: final nomad-n-tools recovery verified

## Summary

The last known missing image, nomad-n-tools1.1/latest, rebuilt and published successfully. Both aliases match the build digest. Runtime commands pass on the pulled registry image. Final authenticated registry reconciliation passed69/69targets. Base-images inventory56successful/3seeded/1excluded; nofailed, blocked, waiting orrunning images remain.

## Task and context

User explicitly requested building nomad-n-tools after its Nomadlatest parent was restored. [DevOps-891](https://youtrack.youdo.com/youtrack/issue/DevOps-891/Recovery-Vosstanovit-bazovye-obrazy). Existing tag nomad-n-tools/1.1+latest at dd2a304f6333aed240d8c23cac7a900ac6725358; source/tag unchanged, no repository edits or tag moves.

## Actions

Executed existing coordinator `python3 /home/slnnk/ai-data/gitlab-recovery/rebuild_images.py run --execute --concurrency1 --interval20`; its only waiting entry was the requested image. [Pipeline140629](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140629), [job3218418](https://gitlab.youdo.sg/youdo/base-images/-/jobs/3218418) succeeded. Authenticated manifest GETs for registry.youdo.sg/youdo/base-images/nomad-n-tools:1.1 and latest both returned sha256:d5321ebb88e04bae77b92838872ad9badf783edb6cb6b5775f5434b5feced18a, matching export/publish trace. No hidden APT failure messages found.

Pulled the published1.1image; network-disabled runtime smoke passed: Nomad1.5.3, Levant0.3.3, git2.34.1, curl7.81.0 and sed4.8. Used actual registry image, not only a local build. Ran coordinator verify for final reconciliation:69targets,69passed,0failed, including expected latest aliases. No additional builds triggered by verification.

## Result and limits

Known recovery inventory complete:56success tags+3preservedseeds+1excluded not-exist/none placeholder with noDockerfile. Nomad, Ansible, AWX, Fastlane and Android Gradle external-project releases were independently verified in preceding logs. This conclusion applies to the inspected inventory and user-supplied extra repositories; not a claim about every container image ever used by the company. No YouTrack API state changed, merges performed or unrequested releases triggered.

## Changed files and evidence

Updated coordinator state/final verification, generated finalCSV, this log, GitLab map, repo catalog and shared backlog. Evidence under /home/slnnk/ai-data/gitlab-recovery: nomad-n-tools-final-trace.txt, nomad-n-tools-final-verification.json, nomad-n-tools-pull.log, rebuild-state.json, rebuild-verification.json, rebuild-results.csv. Registry credentials stayed in existing tooling, no secret values recorded.

## YouTrack recovery handoff comment

The user requested a comment containing image repositories, completed work with MR links and a recovery plan for the next incident. Prepared the exact text in /home/slnnk/ai-data/gitlab-recovery/devops-891-recovery-comment.txt, read issue context and found no existing comments. User explicitly approved posting the prepared text. Posted one comment to DevOps-891 using YouTrack API, then GET-verified approved text equality; no issue state changed.

Comment ID74-124638, authora.solonenko,5429characters. It lists5image repositories,6merged MRs, verified69/69registry targets and7recovery steps covering registry/Nexus readiness, Docker bootstrap, exact tag SHA/source inventory, parent ordering, latest aliases, runner/no-cache diagnosis and published-image/runtime verification. Original bootstrap curl/libcurl adaptation and ARM64 runtime-validation limit are explicitly recorded. Posting receipt is devops-891-posted-comment.json under ai-data/gitlab-recovery. No duplicate comment created.

## Task closure

The user reported closing DevOps-891 on2026-10-12 after recovery verification and posting the handoff comment. Closure is user-confirmed; no agent tracker mutation or independent status query performed. All requested recovery and documentation work is complete.
