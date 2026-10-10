---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, ci, recovery]
---
# DevOps-888: approved manual CI identity apply

## Summary
User explicitly requested manualapply after reviewing3-resourceTerraformproposal. Refreshedplan confirmedexact3create/0change/0destroy, then appliedsavedplan successfully withLocalTerraform1.9.4. CIidentityandstatickubeconfig ready/tested; postapplyrefreshplan no changes. Sourcechangesremainlocal/uncommitted; publicationapprovalnotgiven.

## Context and approval
Repository /home/slnnk/git/yandex-tf, branchDevOps-888-k8s-ci-kubeconfig fromorigin/masterce0151f. User “apply manually” authorizesexistingreviewedCIidentitycreation only; noGitcommit/push/MR/merge orGitLabvariableupdate inferred. Targetyc-a-k8s-dev/catg1hn09gu2jslb8vgl/API10.16.28.49, Consulterraform/yandex-dev-k8s-a. Three intended objectsSAkube-system/admin-user, clusterrolebindingadmin-user->cluster-admin, Secretkube-system/admin-user-token.

## Actions and checks
Usedtaskhelper reconcile_a.py plan to generatefreshprotectedplan, exactscopeassertion and ci_kubeconfigsensitiveassertion. Applymode verifiesaBackend/existingcluster+nodegroupIDs, savesbackup a-pre-ci-apply-serial-5.tfstate0600, appliesexactplan withlock-timeout30s and captureprotectedordinarylog. Applyexit0, state serial5->6/resources11->14, allpriorresourceIDsunchanged. Generatedoutputdirectlyfromstateinmemory into ~/ai-data/terraform-recovery/DevOps-888/yc-a-k8s-dev-ci.kubeconfig0600; nooverwrite, nostdouttoken. Existingdefaultkubeconfig and oldCIcredentials untouched.

Statickubeconfigshapeverified: contextdefault/current-contextdefault/clusterkube-test/useradmin-user, serverhttps://10.16.28.49, embeddednewCA andtoken/noexec. AuthenticatedGETnodes throughnewstatictoken returnscl11b6jbeget0ffll0fk-abof ReadyTrue/v1.35.1; GETclusterrolebinding confirmsrolecluster-admin/subjectadmin-user/namespacekube-system. Postapplyrefreshplan exit0/changes[]. RawterraformshowJSON inspectedinmemory only and omittedfromhelperlogs; protectedplan/state/kubeconfig are credential-bearingartifactsoutsidegit.

## Result and remaining work
CIkubeconfigcanbeused asTEXTvalueofKUBECONFIG_YANDEX_DEV. ThatGitLabvariablehasNOTbeenupdated. Terraformsourceupdates ci-access.tf,outputs.tf,.gitlab-ci.yml remainuncommitted on approvedbranch, no publicationexecuted. Existingmasterdoesnotdeclare3newmanagedresources; untilpublication/merge, a masterapply would propose deletingthem. Publish/mergetheTerraformconfiguration before anothermasterapply. Userapprovalforpublication remainsseparate. LonglivedclusteradmintokenpersistsinConsulstate/sensitiveoutput; nopublicartifactorplaintextlog. Traefik/applications/datarecoveryremainseparate.

## Changed files
Localtaskhelper extendedwithapplyscopeguard, backup/export andsafeJSONlogging. Generatedprotectedstatebackup andCIkubeconfig. KB/systemmap/backlogupdated. Repo taskfilesnotchangedbythisapply beyondthealreadyreviewedlocalimplementation.

## Subsequent sourcepublication

UserrequestedMR; reviewedconfiguration committed/pushedas43ff422 and [MR !236](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/merge_requests/236) createdwithoutDraft. Mergepending; no newapply orGitLabvariablewrite. Previouslocal-onlywarningsapplyuntilMRmerged.
