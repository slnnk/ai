---
system: gitlab-ci
status: verified
checked: 2026-10-15
tags: [recovery, gitlab-ci, kubectl, monitoring]
---
# Deploy monitoring uses internal kubectl image

## Summary

User requested replacing external kubectl image used by SMS monitoringjob3228652. Updated shared gitlab-ci-templates/v3/.monitoring.yml deploy-monitoring image from bitnami/kubectl:latest to registry.youdo.sg/youdo/base-images/kubectl:1.35.6. One-line replacement published and merged as MR90; master image verified via GET. Newconsumerpipelines adopt it; oldcompiledjob keepsoldimage onretry. No newSMS pipeline or monitoringcluster write executed as partofthischange.

## Training approvals and implementation

User explicitly confirmed branch DevOps-899-use-internal-kubectl-for-monitoring from fresh origin/mastera53eaa7, then approved actual+1/-1diff/publication/merge, commit use internal kubectl image for monitoring, MRtitle DevOps-899 use internal kubectl image for monitoring, source→master. Explicit scope states no newSMS pipeline yet; applies tonewpipelinesofallsharedtemplateconsumers. Existingcheckoutclean, noAGENTSfound, no worktree used.

Onlyv3/.monitoring.yml staged and actualstageddiff checked; rules/scripts/dependencies/entrypoint unchanged. Imagecontainskubectl andjq requiredbycommands. YAMLparse/exactimageonlycomparison/diffcheck/peerreviewpassed. EquivalentSMScontextoverride passed GitLabCILint52jobs/errorsnone/warningsnone; not a realclusterexecution. Artifactmonitoring-kubectl899-ci-lint.json.

## Publication and verification

Commit1701f36ff75308f48adc173877611c7e2d5b059a, MR[!90](https://gitlab.youdo.sg/sysadmins/devops-tools/gitlab-ci-templates/-/merge_requests/90), targetmaster7bd157809882e31066e0cddae276c90ac822f3ce. Project squash=true preserved; squash37128a838b145d876b490d8ffc59681f9f068ba8. MRdescriptiononeRussianparagraph+DevOps-899link only; exactGETchecked.

PublicationhelpercreatedMRsuccessfully thenfailed optionalpipelinesGET403 because project428 builds_access_level=disabled; read-onlyinspection recoveredexistingMR90, no duplicatecreation. MergeexactsourceSHAguarded, mastercommitandbase64fileGETverifiednewimage/absenceofoldBitnami. Receiptmonitoring-kubectl899-publication.json andmergeintent under~/ai-data/jenkins-recovery/next-test5-rollout/.

## Changed files and limits

Repository solepathv3/.monitoring.yml+1/-1. LocaltaskartifactsMRbody/lintcandidate/results, KBlog/repos/systemmap/index/syncnotes updated. ExistingSMS140987/job3228652 cannot adoptnewimageviaretry; no newerconsumerpipeline was requested/started inthisscope. No runtime monitoringacceptance claimed, no KUBECONFIGDATA value read orchanged.
