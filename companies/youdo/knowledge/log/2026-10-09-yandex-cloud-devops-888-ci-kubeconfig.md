---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [kubernetes, ci, credentials, recovery]
---
# DevOps-888: prepare static CI kubeconfig for new a cluster

## Summary
User requested CI kubeconfig matching original contextdefault/clusterkube-test/useradmin-user. Old protected localfile ~/.kube/test-k8s-ci.kubeconfig uses static token, embeddedCA, endpoint10.16.26.3. Tokenidentity inspected in memory confirms kube-system/admin-user, noexpiryclaim. Newcluster endpoint10.16.28.49/CA verified from existing separatecheckconfig; targetadmin-user absent. Prepared3objectmanifest and localcredentialbuilder; actualcreation pendingexplicitapproval.

## Task and context
CI in infra-tf/dev consumes textvariable KUBECONFIG_YANDEX_DEV; plan:dev/apply:dev map it to KUBECONFIG2 and commonsetup writes ~/.kube/config. Kubernetes/Helm providers use kubeconfig_path. Preserve existingcontext/useraliases for compatibility; displayalias kube-test is only localmetadata even though cloudclustername yc-a-k8s-dev.

## Prepared actions
Protectedlocalartifactdirectory ~/ai-data/terraform-recovery/DevOps-888. ci-admin-user.yaml defines ServiceAccountkube-system/admin-user, ClusterRoleBindingadmin-user -> cluster-admin, Secretkube-system/admin-user-token annotatedforSA/typekubernetes.io/service-account-token. SamelegacyCIpattern confirmed in existingKB. kubectlapply --dry-run=client passed for all3objects; noexternalwrites. Existing GETSA returnedabsent. Actualapply to newcluster changesRBAC/Secret and requiresseparateexplicitconfirmation.

build_ci_kubeconfig.py --help passed. Read-onlyhelper fetches existingSecret inmemory, checksSAidentity/endpoint, writes mode0600 newfileyc-a-k8s-dev-ci.kubeconfig with embeddednewCA/staticBearerToken, aliasesdefault/kube-test/admin-user and noexecdependency. Neverprints token; refusesoverwrite. Credentialgeneration/check followsapprovedcreation. NoSecret/tokenvalue written into notes/logs. Oldkubeconfig/defaultcontext untouched.

## Result and pending approval
Concreteapprovalproposal: one kubectlapply -f ci-admin-user.yaml with explicitnewclustercheckkubeconfig/context, creatingall3reviewedobjects in yc-a-k8s-dev. Fullcluster-admin privileges matchexistingCIdeploypattern; staticSecret token hasnoexpiry/rotation automation. Generatedkubeconfig should be placed as TEXT in KUBECONFIG_YANDEX_DEV; changingGitLabvariable itself requiresseparateauthorization. NoGitLabvariableupdate, sourceedit, credentialcreation or repo publication performed. Livefollow-up in ~/ai/TODO.md.

## Sources
[Yandex static kubeconfig guide](https://yandex.cloud/ru/docs/managed-kubernetes/operations/connect/create-static-conf) and [Kubernetes serviceaccount tokenSecret](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/).

## User correction: manage CI identity with cluster Terraform
User requests moving CIaccountcreation into yandex-tf togetherwithcluster. Manualmanifest remainsunapplied; nocredentialscreated. Boundedexistingrootdesign proposed: newtest-k8s/ci-access.tf managing SAkube-system/admin-user, clusterrolebindingadmin-user tocluster-admin, annotatedtokensecretadmin-user-token with wait_for_service_account_token=true; SAdependscluster/nodegroup, outputdependsbinding. Preserve EXACT requestedaliases contextdefault/current-contextdefault/clusterkube-test/useradmin-user, embeddednewCA/endpoint and static token. Do not adoptreviewer's differentnamespace/defaultcontextsuggestions. KeepYCexecbootstrapprovider; no circularselfauth.

Extendoutputs.tf with sensitiveyamlencodedCIkubeconfig, manualrawexport onlyto0600file. Token/kubeconfig persistinConsulstate andsavedplans; sensitiveonlymasksordinarylogs. Remove unredactedterraformshow-json|tf-summarize onlyinplan:test-k8s; nativeplan alreadyprintsredactedreviewableoutput. NoGitLabartifacts configured; don'tintroducekubeconfigartifact. SameSecretproviderpatternexistsinfra-tf/dev/developer-access.tf; Kubernetesprovider2.38supportswaitoption. Repo/ancestorAGENTS absent accordingtoindependentreview.

Proposedstage1: existingcheckout/home/slnnk/git/yandex-tf, branchDevOps-888-k8s-ci-kubeconfig fromorigin/masterce0151f. Threeplannedtaskfiles ci-access.tf,outputs.tf,.gitlab-ci.yml. Needuserapprovalofbranch/design beforecodeedits underglobalGit/MRtraining. Checksplannedfmt,validate,liveplan3create/0otherchangesplus sensitiveoutput and independentreviewofsecretlogging/dependencies. Localnativeplan mustneverprintsecrettoken. Noapply,commit/push/MR orGitLabvariableupdateauthorizedbythisproposal. Usercorrection supersedesmanualprovisioningproposalabove; awaitstage1.
