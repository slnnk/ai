---
system: yandex-cloud
status: verified
checked: 2026-10-09
tags: [terraform, kubernetes, ci, recovery]
---
# DevOps-888: inspect CI plan 3217580 secret drift

## Summary
Job3217580 plan:test-k8s and MRpipeline140512 succeeded. CIplan0add1change0destroy for CISecret in-place; diffshowsnochangedattribute/output. Independentlocalrefreshplan repeatsnochanges withsameprovider versions butTerraform1.9.4 vsCI1.7.5. Exactcauseunverified; no tokenrotation claim orapply performed.

## Context
[Job3217580](https://gitlab.youdo.sg/sysadmins/yandex/yandex-tf/-/jobs/3217580), MR!236 refrefs/merge-requests/236/head, SHA43ff422c101542bbc69ae6fff4fa5d659503fd11, pipeline140512success. Runner106/gitlab-runner-docker-2(172.28.0.172). MRverificationalso showsbranchpipeline140511canceled. Sourcecheckoutclean, no newrepo/clusterstatewrites.

## Evidence
Delegatedlongtraceinspectionfilteredonlysafestatus/error/version/attributeindicators; neverprinted rawsecret/token/kubeconfig. CI Terraform1.7.5,Kubernetesprovider2.38.0,Yandex0.169.0. Resourcekubernetes_secret_v1.ci_admin_token plannedin-placeupdate. Safe tracecontext: unchangedid,4unchangedattributeshidden,1unchangedblockhidden; nochangedfield, sensitivevaluediffline or ci_kubeconfigoutputchange. Noerrors. Tracecannotestablish tokenrotation/precisechangedattribute.

Localread-onlyrefreshplan withTerraform1.9.4/samecachedproviders exit0/changes[]. Protectedhelper JSONoutputcapturedinmemory; logsstorevalues-free summary. Sensitiveoutput/tokenstate/artifactsnotprinted. Therefore discrepancyreproducedonlybetween CI and localplanenvironment. Terraformversiondifference is observed, itscausalrole ishypothesisnotverified. Furtherdiagnosis shouldcompareplansusingexactCI1.7.5 beforechangingcredentials/config orclaimingrootcause.

## Actions and limits
Read-onlyGitLabjob/MRverification andlocalTerraformplan; no jobretry/apply, secretrotation, providerupgrade, repoedit orGitLabvariablewrite. MRCIchecks pass, but CIplanisnotstrictlyno-op. ExistingCIcredentials remainvalid basedonpreviousauthenticatedGET; nofreshcredentialhealthclaimfromthisCIplan. Worklog/backlogupdated; furthermatchingversioninvestigationpending.
