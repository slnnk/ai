---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [featuretoggle, postgresql, frontend, diagnosis]
---
# Test5 social login buttons: FeatureToggle data API failure, handed to user

## Summary

User reported no social login buttons on test5, then identified FeatureToggle and explicitly took ownership. Agent stopped read-only diagnosis immediately and made no infrastructure/configuration/data changes. SSR GET /api/features/GetFeatureSet returned success with FeatureSetId0 and empty Features; FeatureToggle GET for all nine social provider keys returned500. API logs showed Npgsql Authentication method not supported (Received:10), consistent with an old client unable to negotiate PostgreSQL SASL/SCRAM. Exact transitive Npgsql version not verified; source references linq2db.PostgreSQL2.6.4.

## Evidence and limits

Live publictest5 homepageHTTP200 uses NextSSR staticpipeline139593. Legacyassetconsumer maps static.test5.youdo.sg/assets/manifest.json to youdo-static-test/test5/manifest.json; Moderation indeed owns legacylogin assets, so its publication alone is not corruption evidence. NewSSR has a differentassetpipeline. No socialasset404 cause was proven. Earlier working assumption that icons were inline applies onlytolegacyModeration; no validbrowsernetwork reproduction obtained. Chromium anonymousheadless navigation failedERR_ABORTED and was stopped; it cannot support a claim about the actual rendered popup.

All nine FeatureToggle socialGET500 beforedataread; do not infer empty persistedflags or DBwipe. Service config recreate_db=false. SSRobservedFeatures{} and components gate socialbuttons by flags. User said 'Проблема с featuretoggle, занимаюсь'; no further diagnosis/fix afterhandoff.

## Artifacts and changed files

~/ai-data/jenkins-recovery/login-static-diagnosis/ contains failedbrowserattemptmetadata and launchlog; next-test5-rollout/diagnose-login-static899.py is localread-onlybrowserhelper, not a source change. VKservice-addresses records observedendpoints/status without credentials. No issuecommentpublication or servicechanges.

## User-confirmed resolution after flag recovery

User restored FeatureToggle, then initially still saw no socialbuttons. Read-only follow-up: FeatureToggleSOCIAL_VK_ENABLED andSETTINGS_FOR_SOCIAL_NETWORKS GET200/enabledtrue; monolithGetFeatureSet200success/id1066/35features, socialVK/OK/Google/Mail/MBM/Huawei true/Facebookfalse. Fresh SSRHTMLbuild139593 includedactualReduxfeatureSet1067/36features withVK/OK/Mail/Tinkoff enabled. All14homepageNextJS/CSSHEADsHTTP200 withcorrectMIME. useFeature reads ReduxSSRstate and doesnotautomaticallyrefreshalreadyopenedtab; socialbuttonsorder is populated byclientuseEffect.

Asked whether fullreload/newprivatetab hadbeen tried. User explicitly confirmed: 'После полной перезагрузки появились'. Remaining UI symptom was stalefeaturestate in the open tab after user-fixed FeatureToggle, not missingstaticassets. No staticredeploy,featurewrites,cacheclear,restartorrepofixneeded/performed byagent. Browserheadlessattempts remainedERR_ABORTED and provide no renderedUI evidence; finalresolution rests onuserconfirmation plusserverdata proof.
