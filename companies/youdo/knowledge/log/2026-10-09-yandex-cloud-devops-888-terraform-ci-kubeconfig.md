---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, ci, recovery]
---
# DevOps-888: manage CI kubeconfig with cluster Terraform

## Summary
User requested Terraform-managed CIidentity with cluster in yandex-tf, then explicitly requested the proposed branch. Created DevOps-888-k8s-ci-kubeconfig from fetched origin/masterce0151f in existingcheckout, preserving clean unrelatedstate. Local three-fileimplementation ready; fmt/validate/YAMLchecks/diffcheck and independentreview passed. Liveplan3create/0change/0destroy, onlySA/RBAC/Secret, ci_kubeconfigsensitiveconfirmed. Noapply or publication.

## Task and context
Original CIformat contextdefault/current-contextdefault/clusterkube-test/useradmin-user, targetAPIhttps://10.16.28.49, targetcloudcluster yc-a-k8s-dev/catg1hn09gu2jslb8vgl, Consulterraform/yandex-dev-k8s-a. Originalstaticaccount kube-system/admin-user clusteradmin. User moved provisioning from manualmanifest intoTerraform; manualmanifest remains unapplied and newCIidentitynotcreated. Defaultuserkubeconfig/oldcredentials unchanged.

## Actions and changed files
Added test-k8s/ci-access.tf45lines with kubernetes_service_account_v1.ci_admin in kube-system, automountfalse and cluster/nodegroupdependencies; kubernetes_cluster_role_binding_v1.ci_admin grants existingcluster-admin; kubernetes_secret_v1.ci_admin_token admin-user-token annotatedtoSA/typekubernetes.io/service-account-token/wait_for_service_account_tokentrue. ExistingYCexecbootstrapprovider retained; no selfauthcycle.

Extended test-k8s/outputs.tf34lines with yamlencoded sensitiveci_kubeconfig output, exactrequestedaliases, newprivateendpoint/CAencodedonce, tokenread decodedfromSecretdata, outputdependsRBAC. .gitlab-ci.yml plan:test-k8s now ordinaryterraformplan, no unusedsavedtfplan/no plaintextJSONsummary; apply remainsmanualmasteronly. Otherjobs unchanged. Final3files80additions/2deletions includinguntrackednewfile. No secretsinrepo.

## Verification
terraformfmt -check -diff exit0; terraformvalidate -no-color exit0 using isolated a-plan-data/cachedKubernetes2.38.0/Yandex0.169.0; YAMLparse/jobassertionspassed and gitdiff --check exit0. Independentreviewconfirmed CA/tokenencoding, exactaliases/kube-systemnamespace, create/destroydependencies, bootstrapauth, narrowCIeffects and sensitivemasking. Followupreviewapproved removing unusedtfplan.

Refresh-enabledliveplan exit0: create kubernetes_service_account_v1.ci_admin,kubernetes_cluster_role_binding_v1.ci_admin,kubernetes_secret_v1.ci_admin_token; all existingresourcesunchanged. JSONassert ci_kubeconfig after_sensitive=true. Protectedlocalplan/log/show/summary under ~/ai-data/terraform-recovery/DevOps-888/a-post-import.* nowcontainthisthree-resourceproposal, overridingearlierverificationplan; noapply. LocalTerraform1.9.4 vsCI1.7.5 meansCIgeneratesitsownplan. NativeAPIrequestsauthenticatedthroughsamebootstrapYCprofile.

## Risks and use
LonglivedCItoken grantscluster-adminasbefore. Token+kubeconfigwillpersistinConsulstate andprotectedplans; sensitiveonlyredactsordinaryTerraformlogs. CIremovesplaintextJSONsummary andsaveddiskplan; no kubeconfigartifacts/upload/newGitLabvariablesadded. Afterapprovedapply exportterraformoutput -rawci_kubeconfig directlyto0600file; neverprint/log. Existinginfra-tf/dev consumesTEXTvariableKUBECONFIG_YANDEX_DEV. UpdatingthatGitLabvariable requiresseparateapproval. Futurestaticcredentialrotation/revocation is managedviaSecret/SA. Clusterreadinessalreadyverified; thischangeaddsCIaccessonly, notTraefik/workloads.

## Publication proposal and approval record
Stage1 approved by user “create the branch” after concretebranch/designproposal. BranchDevOps-888-k8s-ci-kubeconfig, repo/home/slnnk/git/yandex-tf, baseorigin/masterce0151f, targetmaster. Proposedcommit manage kubernetes ci credentials with terraform; MRtitle DevOps-888 manage CI kubeconfig with Terraform withoutDraft. MRbodyoneshortRussianparagraph+tasklink. CIvalidate/planrunonpublication, manualapplymasteronlyretained; newclusterbootstraprequiresprivateAPIreachabilitybeforeKubernetesresources. Stage2publicationpending; nostaging/commit/push/MR/merge/deployment orGitLabvariablewrite.

## Subsequent authorized manualapply

User authorizedmanualapply instead of publication. Refreshed3-resourceplan applied successfully, state serial6/14managedresources, statickubeconfig0600generatedandGETtested, postapplyplan no changes. Sourcechanges remainlocal; noGitpublicationapproval. Publish/mergeconfiguration beforeanothermasterapply toavoidplanningdeletionofnewCIresources. See [manualapplyresult](2026-10-09-yandex-cloud-devops-888-ci-manual-apply.md).

## Stage2 publication approved and completed
After reviewingexact3filediff/checks/commit/MR/source-target/CIeffects, userrequested “prepare MR”. Thisexplicitpublicationrequest authorizedpreviouslyproposedcommit/push/MR action. Stagedexact .gitlab-ci.yml,test-k8s/ci-access.tf,test-k8s/outputs.tf; inspectedactualstageddiffincludingnewfile, gitdiffcachedcheckpassed. Commit43ff422c101542bbc69ae6fff4fa5d659503fd11 manage kubernetes ci credentials with terraform,3files80add2delete. PushedDevOps-888-k8s-ci-kubeconfig withupstream. Created [MR !236](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/merge_requests/236), titleDevOps-888 manage CI kubeconfig with Terraform, sourceDevOps-888-k8s-ci-kubeconfig->master, noDraft; assigneea.solonenko,squashfalse,sourceremovalaftermerge. Pipeline140511 runningatpublicationcheck. Existingmanualapply alreadycompleted; agentdidnotmerge/runnewapply/changeGitLabvariables. CIcredentialsfileoutsidegit; workingcheckoutclean. User/authorizedmerge stillneeded beforemasterapplyincludesnewresources.

## MR CI result

Pipeline140512 succeeded, job3217580 plan shows0add1CISecretin-placechange0destroy withnochangedfields/outputshown; localrefreshplan repeatsnochanges,sameproviders, differingTerraformversion. Noapply/tokenrotationperformed. Exactcauseunverified; see [inspection](2026-10-09-yandex-cloud-devops-888-job-3217580.md).
