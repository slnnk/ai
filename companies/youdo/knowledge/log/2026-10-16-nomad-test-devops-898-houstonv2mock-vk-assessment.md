---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [nomad, vk-cloud, houston, mock]
---
# DevOps-898 HoustonV2Mock VK deployment assessment

## Summary

HoustonV2Mock0.0.35is now deployed in VK through user-played staging3232321/pipeline141077SUCCESS. One shared allocationrunning/healthy,0restarts, Consulpassing; test5Swagger and /experiments HTTP200 (emptylist). Mock is autonomous: no realHub/classifier/MongoDBdependency; experiments in processmemory resetonrestart. Earlier missingdeployment404and CI target-precedence incident below are historical and resolved by explicitVKCLIparameters in MR21/e10c1e2. Build used pipeline-only no-attestation override; persistent compatibility setting remains separate backlog.

## Context and actions

Read-only GitLab project303youdo/mock/houstonv2mock, no projectvariables, master50218a3f5f25747b2ea394bc5fa2e72e167cfc1f/latesttag0.0.33. Fetched origin without checkout mutation; existing clean localmasterd168823preserved. Latest masterpipeline117022/build2264727historicalSUCCESS; tag0.0.33staging2090801MANUAL, tagbuild2090800historicalSUCCESS. Registry repository exists but tagsGETempty. No source edits, branch, build, tag or deployment performed.

## Findings and minimal plan

- One shared Nomad job HoustonV2Mock/count1 serves all stands; wildcard Host rule v2.houston-classifier-mock.{subdomain:.+}.${var.proxy}.youdo.local. Passing dc=vk-test/proxy=vk-test gives requested test5route. No per-stand deploys required.
- Swagger path /api/doc/index.html explicitly documented in readme.md. HTTP404currentlycomesfrom unmatched Traefikroute, not demonstrated app Swagger failure.
- No Hub/MongoDB/model/backenddependency. Experiments are in process memory with hostname testN isolation; restarts lose mockexperiments. Existing Nomad resourcesCPU100/memory200.
- staging.nomad already parameterized dc/proxy/version. Minimum durable repo change is .gitlab-ci.yml staging job: use VK address/deploytoken and dc/proxy=vk-test instead of yandex-test. Preserve public-testjob. GroupyoudoalreadyhascommonVKtoken (credentiallocationonly, neverrecordvalue).
- Registryempty requires image rebuild. After reviewed CIadaptation/newtag (nextcandidate0.0.34), standard tagbuild followed by explicit manual stagingjob; automatic productiondeploynotpresent. Check actual build failures/base images/packages from buildresults before broadening scope.
- Before edits obtain branch/repo/baseapproval under supervised rules; publication/build effects and manual runtimejob require respective approvals. No extra NomadHCL/appcode edits justified by current evidence.

## Knowledge correction and limits

Previous repos.md entry claiming1.0.9/pipeline140997deploymentto14stands was incorrect for project303and is replaced by this verified evidence. Do not use it as runtime acceptance. Current GitLablatestmaster117022and tags0.0.33plus emptyVKruntimeregister are authoritative for this task. Corrected only relevant repositoryrow; other records not attributed speculatively.

## Approved implementation and publication proposal

User requested implementation with “Сделай”, then explicitly approved branch DevOps-898-deploy-mock-on-vk from origin/master50218a3in project303with “Да”. Existing local checkout was clean; branch created without overwriting oldmaster. Only.gitlab-ci.ymlstagingjob changed: Nomad DC/proxyvk-test, NOMAD_ADDRhttp://nomad.service.vk-test.consul:4646 and NOMAD_TOKEN=$NOMAD_TOKEN_VK_TEST, commandnomad job run staging.nomad. Removed hardcoded YandexCLIaddress/token. Public-testandbuildjobs exactly unchanged. HCL/app/Dockerfile untouched.

Checks: git diff --checkPASS; YAMLparsePASS; structured compare confirms all non-stagingjobs unchanged; staging remainsmanual/tagonly. Nomad render version0.0.34gives DCvk-test/count1/expectedwildcardHostRegexp. LocalNomadvalidatePASSwith preexisting deprecatedtasknetworkwarning; serverdrivervalidationskipped. Actual VKjobtraefik2-serviceusestraefik:v2.9.8, matchingHostRegexpv2syntax (initial lookup lowercasejobtraefik404was corrected by jobinventory). GroupyoudoNOMAD_TOKEN_VK_TESTmetadata verified maskedtrue/protectedfalse/scope*, project303sharedrunnersenabled, noprotectedtags. Secret neverprinted/saved. The Data-groupstagingvariables are not used by this separateyoudo-groupmock.

Stage2proposal: commit deploy houston mock staging to vk; MR DevOps-898 deploy houston mock staging to vk, sourceDevOps-898-deploy-mock-on-vk/targetmaster, explicitpath.gitlab-ci.ymlonly, actualdiff5insertions/3deletions. Russianparagraph+tasklinkdescriptionpreparedat ~/ai-data/DevOps-898/classifier-audit/mock-mr-description.md. Publicationapprovalpending. IMPORTANTbranchpushcreatesnopipelinebecauseexistingjobsareonlymaster/tags; mergebuildsmasterimage, protectedtagnotrequiredbycurrentrules, proposednewtag0.0.34buildsreleaseimageandmanualstaging/public-testjobs. Noautomaticdeployment. Runtimejobneedsseparateexplicitapproval. Dockerfilestill.NET3.1SDK/ASPNETfromMCR; investigateactualbuildfailuresbeforeexpandingchanges. No commit/push/MR/merge/tag/deploy for mock yet.

## Publication completed

Stage2userapproval “Да” to the exact commit/push/MRproposal. Reviewed full stageddiff: only.gitlab-ci.ymlstagingchanges,5insertions/3deletions; diff --checkPASS. Committeda735d3eea62d363d41c89c76bda3e5038c33e3e5with deploy houston mock staging to vk; pushedapprovedbranch and created existingtaskMR20 https://gitlab.youdo.sg/youdo/mock/houstonv2mock/-/merge_requests/20 to master. GETreadback verified exactSHA,title,source/target,assigneea.solonenko,squashfalse/source deletiontrue. Workingtreeclean. Pipelines=[]as expected from onlymaster/tagsrules. No merge/tag/build/deploy occurred. Next explicitproposal mergeMR20andtag0.0.34on resultingmaster; tagbuildspublishesimageandcreatesmanualstaging/public-testjobs, noautomaticdeployment. Do not reuse oldtagstagingjob2090801because it retainsoldcompiledYandexconfiguration. Actual0.0.34buildmust succeed beforemanualVKstagingjobcanrun.

## Approved merge and tag

User explicitly approved concrete mergeMR20+tag0.0.34proposal with “Да”, including tagimagebuild/manualdeploymentbehavior. Rechecked openedMRsourcea735d3e,targetmaster,no conflicts, absenceof0.0.34; mergedwithSHAguard,squashfalse,source deletiontrue. Resultmaster403c102f83d499e841f1c57a3e39fb3e7afb16a7. Createdtag0.0.34at exactmergedmaster and verifiedGET. Evidence mock-merge.json/mock-tag.json in auditdirectory. Pipeline141068RUNNING/tagbuild3232212RUNNING; staging3232213/public-test3232214CREATEDthenmanualafterbuild. No manualdeployjobplayed. Read-only monitor-mock-release.py prepared for build/filterederrors. Actualruntime remainsabsentuntil separately approved stagingjobplay.

## Release image publication failed; proposed pipeline-only recovery

Pipeline141068FAILED: build3232212restore/publish compiledsuccessfully, then dockerpushfailed “blob unknown to registry” digestsha256:ce7c01bae66563e8ebd27aa86d187e8b1232c0f4ce31f907ad7468fc3b4c3bae. staging3232213/public-test3232214SKIPPED, so noVKdeployment. Sanitizederrors in mock-release-status.json. No retries/externalrecoveryperformed.

Known analogous registry/Buildxattestationfailure and verified pipeline-only recovery:2026-10-13-gitlab-ci-dynamic-inventory-vk-migration-plan.md, Approvedruntimepreparation section. Existing source/tag unchanged; propose NEWpipeline ref0.0.34 with BUILDX_NO_DEFAULT_ATTESTATIONS=1 only for that pipeline. Workingexplanation is OCIindex/attestationincompatibility; successrequiresactualrebuild. Local reviewed payload prepared mock-rebuild-payload.json. This rebuild would publish0.0.34andexposemanualstagingjob, notdeployautomatically. AwaitexplicitapprovalforpipelinePOSTunderexternalwriterequirement. NoDockerfile/SDK/source/tagchangesjustifiedbythispushfailure.

Traceconfirmed by delegatedread: exports innerimage manifestce7c01, attestationmanifest7c5d6, manifestlistbc988; all9filesystemlayersuploadsuccessfully. Finalblobunknownreferencesinnerimagemanifestce7c01ratherthanmissingfilesystemlayer. This stronglymatchespriorOCIindex/attestationcompatibilitycase; rootregistrybugnotindependentlyproven. No-codepipeline-onlyoverride remainsproposedrecovery.

## Pipeline-only no-attestation rebuild started

Userexplicitlyapprovedsame-tagpipeline-onlyoverridewith “Да” (after a keyboard-layouttypo). Rechecked0.0.34points403c102f83d499e841f1c57a3e39fb3e7afb16a7; POSTcreatedpipeline141070onthatSHA/refwithsoleoverrideBUILDX_NO_DEFAULT_ATTESTATIONS=1; GETpipelinevariablesverifiedoverride. No persistentprojectvariables/source/tagchanged. Newpipelineevidencemock-rebuild-pipeline.json. Buildresultpending; manualstagingnotplayed.

## Rebuild publication succeeded; manual deployment awaiting approval

Pipeline141070SUCCESS/build3232217SUCCESS with approved pipeline-only BUILDX_NO_DEFAULT_ATTESTATIONS=1. ManualVKstaging3232218andpublic-test3232219available. No deploymentsplayed. Registrytag0.0.34metadata/digestGETverified afterbuild; sanitized evidence mock-image-verified.json. This supports registry/attestationcompatibilityworkingexplanation; no persistentCIpatch made. Next concreteexternalaction POST projects/303/jobs/3232218/play deploys exactlyone shared HoustonV2Mockinstance in VK, wildcardroutesallstandsvk-test includingtest5, freshin-memoryexperiments. Public-testuntouched. Awaitexplicitjobplayapproval. FuturedefaultreleasesmayrequirethesameoverrideuntilseparatelyrequestedCIcompatibilitychange.

## Approved staging job started

Userexplicitlyapprovedplayingstaging3232218with “Да”. Beforemutationverifiedmanualstatus,project303/pipeline141070/tag0.0.34/SHA403c102andno-attestationoverride. FirstguardstrictdictcomparisonstoppedbeforewritebecauseGitLabincludesextra raw=falsefield; read-onlycheckconfirmedallintendedfieldsandsoleoverride,guardcorrectedtofieldcomparison. ThenPOST jobs/3232218/play succeededPENDING; subsequentGETRUNNING. No duplicateplayor retry. Public-test3232219remainsMANUAL/untriggered. Evidence mock-staging-play.json. InitialNomad404/Swagger404beforejobregistration, notyetacceptance. Runtimefieldsaddedtoexistingread-onlymonitor script.

## Wrong target caused by CI variable precedence (confirmed)

Staging3232218registeredjobinSelectelNOTVKbecausegroupyoudoNOMAD_ADDR/TOKENoverridejobYAMLvariablesofthesamenames. GroupNOMAD_ADDR=http://nomad.service.selectel.consul:4646andgroupNOMAD_TOKENpresent. Actualstagingtraceevaluation29aa1f05/deployment70e1d969reportednoeligiblenodesfordc=vk-test. VKjobGET404. FreshSelectelGETusingeffectivegroupcredentialsconfirmed newlycreatedHoustonV2MockVersion0/Statuspending/DCvk-test/CreateIndex=ModifyIndex28505172/SubmitTime1792150065878902483andNOallocations. Noexistingjobversionorallocationwasreplaced; donotclaimnoremotewriteoccurred. Sanitizedevidencemock-effective-target.json. No cleanup/retryperformed.

Agentmistake: didnotcheckinheritedgenericNOMAD_ADDR/TOKENconflictbeforepublication. CorrectCIpatternhereismakeendpointselectionexplicitincommand(e.g.nomad job run -address=http://nomad.service.vk-test.consul:4646 -token="$NOMAD_TOKEN_VK_TEST" staging.nomad)orrebindinexecution-shellafterinheritedenvironment,notjobYAMLgenericvariables. Existingdc=vk-testcorrect. Useraskedwhetherdcwrong; answeredcorrectdc/wrongendpointandacknowledgedmistake. Thisisaconfirmedconfigurationbug,notcapacityshortage; donotchangeDCtoselectel,addnodes,orunpauserunners.

Nextcleanupactionrequiringapproval: delete/purgeONLYnewemptySelecteljobHoustonV2MockafterfreshguardVersion0/DCvk-test/noallocations. Laterfollow-upCIbranchproposalDevOps-898-fix-mock-deploy-targetfrommergedmaster403c102; removejobYAMLNOMAD_ADDR/TOKENanduseexplicitCLIaddress/token; localrender/precedencecheck,reviewpublication,newrelease/stagingapprovalsrequired. Thoseactionsnotyetapproved. Job3232218mayremainmonitoringpendingdeploymentuntilcleanup/timeout; no automaticrepeatofmisconfiguredpipeline.

## User cleanup verified; corrective candidate prepared

UserreporteddeletedwrongSelecteljobandinstructedservicefix. FreshGETconfirmedHTTP404forSelectelHoustonV2Mock. Noagentcleanupwrite. Fetchedorigin/master403c102,localcheckoutcleanonpreviousmergedtaskbranch. CorrectivebranchproposalDevOps-898-fix-mock-deploy-targetfromorigin/master403c102awaitsapprovalunderstage1rule.

Beforeapprovalpreparedcandidateoutsidecheckoutin ~/ai-data/DevOps-898/classifier-audit/mock-explicit-target-candidate.yml and reviewedpatchmock-explicit-target.patch. RemovesjobYAMLNOMAD_ADDR/TOKEN,changesstagingcommandto nomad job run -address="http://nomad.service.vk-test.consul:4646" -token="$NOMAD_TOKEN_VK_TEST" staging.nomad. YAMLparsePASS,allotherjobsexactlyunchanged. LocalshellstubwithintentionallywronggenericNOMAD_ADDR/TOKENandplaceholderVKtokenverifiedexplicitCLIargumentsstillselectVK. NoNomadrequestfromtest,nosecretsused. Repositoryfilesunchangedpendingbranchapproval.

Portablelessonwrittenas general/knowledge/gitlab-ci/inherited-deploy-target-variables.md (no companydetails), linkedfromthiscompanylog. No automatic retryofoldcompileddeployjob. PermanentattestationCIsettingremainsseparatebacklog; thisfixscopeonlytargetselection.

## Corrective branch implemented and verified

UserapprovedbranchDevOps-898-fix-mock-deploy-targetfromorigin/master403c102with “Да”. Createdinexistingcleancheckout. Actualrepository.gitlab-ci.ymlonly: removetwoshadowedjobYAMLNOMAD_ADDR/TOKEN,replacebareNomadrunwith explicitVKCLI-addressand-tokenfromexistingNOMAD_TOKEN_VK_TEST. Actualdiff1insertion/3deletions. Nogenericgroupvariableschanged.

ChecksPASS: diff --check; YAMLparse; structuredcompareallotherjobsexactlyunchanged; manual/tagonlypreserved. Shellstubregressionwithintentionallywronggenericaddress/tokenandplaceholderVKtokenverifiedexactintendedCLIargs. ActualNomadCLIrun-outputonsamecorrectedcommandwithplaceholdercredentialsPASS/VKDC/count1withoutcontactingserver. Sanitizedreportmock-explicit-target-verification.json. Candidatewasnotusedtosubmitjob. ActualSelectelcleanupverified404already.

Stage2proposedcommit set explicit vk target for mock deployment; MR DevOps-898 fix houston mock deployment target, approvedbranchto master, explicitpath.gitlab-ci.ymlonly. Bodypreparedmock-target-mr-description.md(singleRussianparagraph+tasklink). GitLabinspectnoexistingopenMR,defaultmaster,squashfalse/source removaltrue/assigneea.solonenko. Awaitpublicationapproval; no commit/push/MRforfollow-upyet. Existingmaster/tagonlyrulesmeanbranchpushhasnopipeline; mergebuildsmaster. Newreleasecandidate0.0.35mustincludeupdatedCI; existing0.0.34compileddeployremainswrongandmustnotberetried. NewbuildshoulduseexistingapprovedpatternBUILDX_NO_DEFAULT_ATTESTATIONS=1aspipeline-onlyoverrideunlessuserseparatelyrequestspermanentCIchange. Merge/tag/newbuild/manualdeployremainexternalactionsrequiringexplicitapproval.

## Corrective publication completed

Stage2userapproval “Да” to exactcorrectivecommit/push/MRproposal. Reviewedfullstageddiffonly.gitlab-ci.yml+1/-3, diff --checkPASS. Committed2c24751ee9c0c62677d313a5e9081e70d1afeb62with set explicit vk target for mock deployment; pushedDevOps-898-fix-mock-deploy-targetandcreatedMR21 https://gitlab.youdo.sg/youdo/mock/houstonv2mock/-/merge_requests/21 tomaster. ReadbackverifiedexactSHA/title/source/target/assigneea.solonenko/squashfalse/removesourcetrue. Localworktreeclean. Pipelines=[]expectedmaster/tagonlyrules. No merge/tag/deployforcorrectivefollow-upyet.

NextproposalexplicitmergeMR21andnewtag0.0.35atresultingmasterwithpipeline-onlyBUILDX_NO_DEFAULT_ATTESTATIONS=1fortagbuild. PreferpassoverrideontagpushusingreviewedGitLabpushoptionratherthanintentionallytriggerknown-failingdefaultbuildthenrebuild; verifymechanismbeforeexecution. No persistentCIsettingchangeimplied. Newmanualstagingwillusecorrectedcompiledcommand; neverretryold0.0.34staging. RuntimeVKmockstillabsentuntilcorrectedrelease/manualdeployment. Awaitmerge/tagauthorization.

## Corrective merge and tag executed

UserexplicitlyapprovedMR21merge/tag0.0.35withno-attestationbuildoverride. Recheckedsource2c24751/no conflicts/mastertarget/tagabsent; mergedMR21withSHAguard,squashfalse,source deletiontrue. Resultmastere10c1e21f4327060d36edbab0e4dfeda89763165. Fetchedwithoutbranchmutation, createdlocaltag0.0.35atexactmergeSHAandpushedtagwithGitLabpushoption ci.variable=BUILDX_NO_DEFAULT_ATTESTATIONS=1. GETverifiedremoteSHAandpipeline141077variable=1; no intentionally failingdefaulttagpipelineorredundantrebuildcreated. Tagpipelinependinginitially. Evidencemock-target-merge.json/mock-target-tag.json. Nomergedeployautoexists; manualcorrectedstagingjobnotplayed. WrongSelecteljobpreviouslyuserdeleted/404verified; noadditionalSelectelchanges.

## Corrected release build verified

Pipeline141077SUCCESS/build3232320SUCCESS. Registry0.0.35metadata/digestverified; exactCIfilefetchedatpublishedtagandYAMLparsedtoassertstagingcommandexplicitVKaddress/tokenandabsenceofshadowedgenericjobvariables. Evidencemock-target-image-verified.json. Manualstaging3232321/public-test3232322ready/unplayed. No VKruntimeyet. NextconcreteruntimeproposalplayONLY3232321whichregistersonecommonmockintheVKclusterwithwildcardstandroutes. GroupNOMAD_ADDR/TOKENcannotredirectthisCLIcommand. Awaitexplicitmanualjobapproval; old0.0.34jobmustnotberetried.

## User deployment accepted; independent mock confirmed

User reported playing deployment personally and asked if realHub/classifier required. FreshGET confirms pipeline141077SUCCESS/staging3232321SUCCESS, public-test3232322MANUAL/unplayed. NomadHoustonV2MockVersion0/DCvk-test, taskmetaVERSION0.0.35, exactly1sharedallocation0150e647-fcc1-0487-8ab8-a50243383779running/healthy/0restarts. Imageexpressionregistry.youdo.sg/youdo/mock/houstonv2mock:${NOMAD_META_VERSION}, memory200MiB. Consulpassing; HostRegexpwildcardmatchesstanddomains. Exactreportedtest5Swagger /api/doc/index.htmlHTTP200/text-html2482bytes; /experimentsHTTP200/application-json2bytes(emptylist). Onlytest5HTTProuteindependentlytested, wildcardconfigurationcoversothers. Acceptanceevidence mock-release-status.json. Deploymentplayattributedtouser, notagent. No furtherexternalwritesperformed.

Architecturefromsource remains: in-memorycache/dictionaries isolatedbytestNhostname; noMongoDB/realHub/classifier/models/upstreamdependency. Restartlosesmockexperiments. RealHub/classifierservices previouslydeployedareindependent ofthismock. Currenttest5routesaddedtoservice-addresses.env; rolloutbacklogclosed. RemainingoptionalCIattestationdefaultcompatibilityitempreserved.

## Existing YouTrack summary updated with mock

User explicitly instructed adding mock to the existing single-service task comment. Located DevOps-898 existing summary74-124675; prepared scoped update preserving all earlier service/LogReader/BuildAPI evidence. Added HoustonV2Mock0.0.35 table row and changed listed single-service count10to11. Added shared VK deployment acceptance, successfulpipeline141077/user-playedjob3232321, test5Swagger/experiments200, runninghealthy/0restarts/Consulpassing, in-memory/autonomous behavior and WebTestSuite seven-experiment setup/testFixTestsVKconfig. Included explicitCLI-targetMR21 and pipeline-onlyno-attestationbuildlimit. Hub/classifier additions were not included beyond explaining mock independence because request specifically concerned mock.

Executed one POST to existing /issues/DevOps-898/comments/74-124675 after fresh concurrent-text guard. ExactGETreadback verified5763characters/hash9ef66f4cb120a049d738e1959260f8b6eae8e3fb8b65a60701a1deaef2a00eda. Original commentID/list preserved; task resolvedtimestamp unchanged. No comment-create or issue-state update. User request was the authorization for this exact existing-comment update. Local reviewedplan/body/receipt/script: mock-comment-update-plan.json, mock-comment-updated.md, mock-comment-update-receipt.json and update-mock-comment.py in auditdirectory. No infrastructure/repository mutation during comment task.

## Backlog classification clarification (2026-10-19)

The optional persistent Buildx attestation compatibility proposal was mistakenly grouped under Content/production S3 in the central TODO. It belongs to Nomad-test service recovery and has been moved there without changing its scope or authorization. It concerns Docker image publication for HoustonV2Mock; no causal or runtime dependency on youdo.content or the production Selectel S3 incident was established. The proposal remains open, with implementation requiring a separate request.
