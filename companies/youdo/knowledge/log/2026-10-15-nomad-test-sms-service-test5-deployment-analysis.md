---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [microservices, postgresql, rabbitmq, gitlab-ci]
---
# SMS service test5 deployment requirements

## Summary

User requested analysis of what is needed to deploy youdo-sms-service while taking ownership of FeatureToggle separately. Target test5 inferred initially, then explicitly approved by user. SMSmaster-191 deployed and accepted after targeted testimagecache recovery and CIpublickey addition on B2BPostgreSQL; no servicerepository edits required. Source is project498, ~/git/youdo-sms-service; existing clean DevOps-689-k8s checkout preserved. Fresh origin/master21060f765af794bbe6bd1447237cf1dbea8f94f4 equals master-190; latest semantic1.0.0 is3e475845faed6c25ce9759f939494701136c0db7(2024-10-10),22commits behind. Prefer currentmaster source for a fresh test build rather than blindly deploying the old semantic release.

## Confirmed requirements

Currentmaster fiveprojects targetnet8.0, images webapp/worker/migrations. Npgsql9.0.3 supports SCRAM, unlike the independently user-owned FeatureToggle incident. Private direct packages ServiceCore1.0.15 and FluentMigratorCore.Consolisator1.8.1 are in prior recovered inventory; full SMS restore graph still requires the actual build. Tests use Docker/Testcontainerspostgres11.5 and mocked HTTP provider clients.

Generic Ansible already supports webEx/webapp,worker,pre/postmigrations and BuildAPI publication. No legacyYandexliteral found in config; noAnsible adaptation provennecessary. CurrentNomad jobyoudo-sms-service-test5 absent(HTTP404), so this is first launch. Monolith already calls http://youdo-sms-service-webapp.test5.vk-test.youdo.local.

PostgreSQL poolb2b: postgres-b2b.service.vk-test.consul resolves10.18.26.44:5432, targetDBtest5_youdo-sms-service. Existing CI POSTGRES_TEST_PASSWORD/youdo authentication verified read-only; no secretvalues retained. CI rootSSH access for database creation not confirmed. LocalSSH host trust failure is not evidence CI SSH is broken; no known_hosts changes made. recreate_db=true means normal first deployment drops/recreates targetDB; no templateDB required.

Worker uses RabbitMQ/vhosttest5, credential from existingCI RABBITMQ_TEST_PASSWORD. No Redisdependency in config, no dedicated Vaulttemplate. FreshDBmigration initializes Primary/SecondaryproviderMock. Staging alone does not disable real providers if DB routing rules are preserved/changed; realSMS sending/adminsend-direct are not required for deployment acceptance and were not attempted. Provider destinations include api.devino.online,sms.intellin.ru,direct.i-dgtl.ru; credentials remain in existing sources/secrets, not recorded here.

## Evidence and limits

Read-only repository/CI/dependency and targeted infrastructure analysis. User's master/latesttag convention retained with explicit distinction between currentmaster tag and oldsemanticrelease. No branchchanges, no merge/release approval requested because no requiredsourceedit identified. Remaining execution tracked centrally in ~/ai/TODO.md.

## Final CI result and user correction

User explicitly corrected: semantic version is not current/relevant for this service. Use fresh origin/master21060f7 only; no new semanticrelease tag required. CI produces master-N, builds webapp/worker/migrations and provides manual normal/keep-db test5 jobs. Existing historicalmasterpipeline137495/IID190 is not a fresh VK-template build. Current full-auto CI also enables automatic production deployment; this effect must be included in any execution decision. Testcontainerspostgres11.5 runnerDocker socket confirmed; registry listing HTTP403 means imageavailability unverified, not absent. No source/DNS/Ansible edits identified as necessary.

## Approved pipeline launch

User explicitly requested launching the fresh master pipeline after deployment requirements and CI effects were explained. Created exactly one pipeline140987/IID191, source21060f765af794bbe6bd1447237cf1dbea8f94f4. Receipt-backed sms-pipeline899.py saves precreate intent and pipeline receipt; source/ref verified by GET. Expectedgeneratedmaster-191; .preprepare-nuget3228602 initiallypending, threecomponentbuilds3228605/6/7 created, unit-tests3228608 created. Fresh test5manualdeploy candidate3228618 not played. No repository/DB/stand changes made.

## Testcontainers image pull blocker

All three SMSmaster-191 images built successfully in pipeline140987 (jobs3228605/6/7). Job3228608 remainedrunning while xUnit fixtures failed to provision PostgreSQL: DockerApiException/InternalServerError, mirror.gcr.io/v2/library/postgres/manifests/11.5 token request timedout awaitingheaders. This is a container image acquisition failure before application test assertions; no claim all application tests pass. User supplied jobURL; read-only diagnosis started for minimal exactimagepreload path. No testsretry/cancel/runnerchange authorized or performed atthischeckpoint.

## Approved test image cache recovery

User approved downloading exactpostgres11.5 locally, docker save/load into onlyrunner172.28.0.171 and retrying tests3228608 after originaljob completes. Localpostgres11.5 and explicitregistry-1.docker.io/library/postgres11.5 both resolveddigestsha256:b3770d9c4ef11eba1ff5893e28049e98e2b70083e519e0b2bce0a20e7aa832fe. First pull finished while bypassattemptstarted; cannot infer bandwidthimprovement fromsecondcachedpull. Saved image transferredviaSSHroot into runnerDockerdaemon; imageIDsha256:5f1485c70c9a5cfb95c4edada198245566e38dd53a06b5876d13194fc0bee3d2/linuxamd64 matched locally/remotely. No registrymirrorconfigs or servicecontainers changed. Testcontainers3.10officialContainerBuilder source defaultPullPolicy.Missing verified; localcache avoids newpull. Originaljob stillrunning with priorfailures; no cancel permission orretry beforeterminal.

Mirroravailability diagnosis: activejobs showed27-50KB/s andtokenrequesttimeouts. CurrentGETtoken200 locally0.37s, fromrunner6.58s; onlypathinstability proven, notglobaloutage. GoogleCloudstatuspage showednobroadsevereincidents. HEADtoken405isexpectedunsupportedmethod, not anavailabilityerror.

## Approved cancellation and exact test retry

Aftercacheloaded, originaltests remainedrunning~15minutes with priorrecordedfailures and stalledoutput (xUnit38.10seconds). User explicitly approved canceling3228608 and retryingonlythatjob immediately. CancelPOST sentonce, terminalcanceledGETconfirmed(duration1027.17seconds), retryPOSTsentonce->new3228653pendingthenrunning on samerunner108/172.28.0.171. Sourcepipeline140987/master21060f7 validatedbeforeandafter. Intent+receipt guards retained. No build retries, runnerconfigurationchanges, manualtest5deploy or otherjobcancellation.

## Approved first deploy and B2B CI SSH alignment

Retrytests3228653SUCCESS37.96seconds,188tests,all3imagesmaster-191successful. User explicitly approved firsttest5deployjob3228618, normalcreation/recreationtest5_youdo-sms-service onB2BPostgreSQL. Jobfailed7.50seconds atCreatepostgresdbifnotexist: SSHroot@postgres-b2b.service.vk-test.consulPermissiondenied, beforeSQL/Nomad writes. User proposed adding key analogouslytoC2C.

ComparedcurrentinheritedGitLabgroupyoudo/PRIVATE_KEY publicidentity in-memory withpreviousC2Cpublicartifact ci-private-key.pub: identicalRSA2048 fingerprintSHA256:QIr7ZqPHi8k/4IPvxu+IkWOCblLwsfeGYwACBJdq5aY. Read-onlyyoudo/sudoinspectionon10.18.26.44foundemptyrootauthorized_keys(mode0600). SSHhostkey enrolledaccept-new locally onfirstconnection; no priorindependentfingerprint verification, no mismatchoverride.

Addedonlythatpublickey to/root/.ssh/authorized_keys; preservedbeforebytes, backup/root/.ssh/authorized_keys.devops-899-sms-before0600, target0600. No privatekey persisted. SeparateCIkeyrootSSHid-u check returned0 usingmemfd andparent/procFD. Firstlocalhelperattemptfailedsyntaxbeforeanyremotechange, corrected; no partialwrite. VerificationinitialselfFD couldn'tsurviveOpenSSHFDclose; parentprocessFDroutepassed. NoSSHdaemon policy/restart orAnsible/repo edits. Artifacts sms-b2b-ci-key899-before/apply/verify.json.

Repeatedsameapprovedtest5deploymentonce: old3228618failed ->new3228662pending, pipeline140987/source21060f7. Receipt+retryintentupdated; BuildAPI expectedCI_JOB_IDnowreadsactive deployreceipt. Runtimeacceptancepending.

## Final test5 acceptance

Deploy3228662 SUCCESS118.89seconds. sms-deploy899.py verify passed metadata_matches/live_matches/html_present/accepted alltrue for master-191, pipeline140987, source21060f765af794bbe6bd1447237cf1dbea8f94f4 andactualdeployjob3228662. Nomadallocation36eeb6f0 running/healthy; webapp andworker running,0restarts,Failedfalse; pre/postmigrationtasks dead/completedwithoutfailure. Consulchecks passing forboth; webapp/_/heartbeatGET200. WorkerconfiguredcheckTCP, acceptedasdeclared; no SMSdelivery attempted. Runtime/BuildAPIacceptance artifacts retained undernext-test5-rollout/.

Test5scopecomplete. Productionchild140988 wascreatedbyapprovedmasterpipelineautomation; no claim here about finalproductionstate. No furthermanualproductionactionperformed.
