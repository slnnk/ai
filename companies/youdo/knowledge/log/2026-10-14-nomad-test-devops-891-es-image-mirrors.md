---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [base-images, DevOps-891, DevOps-894]
---
# DevOps-891 Elasticsearch image mirrors for Nomad test stands

## Summary
User approved base-images branch DevOps-891-mirror-elasticsearch-images from origin/master. Two minimal digest-pinned Dockerfiles and internal registry references in the existing DevOps-894 Nomad templates are prepared locally; no builds, image publication, tags or redeployments performed.

## Task
Mirror Elasticsearch6.8.23 and tobias74/elasticsearch-head in the company registry to reduce external registry dependency after the test3startup deadline miss. Base-image work belongs to DevOps-891 per canonical user classification; Nomad integration remains DevOps-894.

## Context
base-images tag-driven CI extends .build_tag_single_baseimage_docker from gitlab-ci-templates; only tags trigger image builds, target linux/amd64. User explicitly approved the proposed branch. Fetched origin/master, now8759867; clean existing checkout switched to the approved branch without touching earlier DevOps-891 history. automation-test-yandex remains on its approved DevOps-894-deploy-elasticsearch-on-vk branch with unrelated MSSQL changes preserved.

## Actions
Read public Docker Hub manifests. Elasticsearch6.8.23 source manifest-list digestdeda76957c8cacc5dbf0d535fd14fe365f37d839813099bc32f26390a5e232dc advertises linux/amd64. elasticsearch-head current source manifest digest1a888b9281359313004c8fee4d74bc8fe9b32da69667be6cc72be304b8f22dca pinned; no invented upstream version. Added one-line FROM Dockerfiles inheriting existing images without changing configuration. Changed only image strings in thin/thick/public-test templates for this mirror adaptation. Local template validation passed for all three variants, Ansible syntax passed, git diff --check passed in both repositories. Read-only review confirmed Dockerfile/tag/registry/template consistency with no blockers.

## Findings
Release tags elasticsearch/6.8.23 and elasticsearch-head/sha-1a888b928135 map to registry.youdo.sg/youdo/base-images/elasticsearch:6.8.23 and registry.youdo.sg/youdo/base-images/elasticsearch-head:sha-1a888b928135. Tag builds would publish images; MR/branch publication alone does not build them. Cold pulls still occur on a Nomad node; internal registry hosting does not prove that all starts will fit the existing healthy deadline. Current upstream head digest was pinned; cached older latest bytes on existing nodes were not compared. No runtime change until images exist and deployment is separately authorized.

## Changes
base-images: elasticsearch/6.8.23/Dockerfile and elasticsearch-head/sha-1a888b928135/Dockerfile (two new lines total). automation-test-yandex: es_thin.j2, es_thick.j2 and es_public-test.j2 image references. Local ai-data template check updated to expect internal images and parse public-test too. No source configs, CI definitions or unrelated files changed.

## Publication proposal
Pending approval: commit `mirror elasticsearch images`; MR `DevOps-891 mirror Elasticsearch images`; source DevOps-891-mirror-elasticsearch-images, target master, only the two Dockerfiles included. Description:
```text
Добавлены базовые образы Elasticsearch6.8.23 и elasticsearch-head для публикации во внутреннем registry; исходные образы зафиксированы по digest.

https://youtrack.youdo.com/issue/DevOps-891
```

No merge, tags, build or redeployment is authorized by MR publication approval. Existing DevOps-894 automation changes require their own reviewed publication scope.

## Open items
Publication, release-tag build and deployment actions remain tracked in ~/ai/TODO.md.

## Portable lesson
none

## Approved publication completed
User explicitly approved the presented commit/push/MR action. Staged diff verified exactly two Dockerfiles, two insertions and no pre-staged/unrelated changes. Committed2e19eb0f906ef7f842876e42e91903682a4824aa with approved message `mirror elasticsearch images`, pushed approved branch and created [MR40](https://gitlab.youdo.sg/youdo/base-images/-/merge_requests/40), title DevOps-891 mirror Elasticsearch images, source DevOps-891-mirror-elasticsearch-images→master. Russian description plus task link preserved. API verification confirms exact remote source SHA, assigneea.solonenko, squashfalse and remove-source-branchtrue; no pipelines, consistent with tag-only CI. Local base-images checkout clean. No merge, release tags, image builds or deployment performed. This supersedes pending-publication statements above. Automation template changes remain local on the separate approved DevOps-894 branch.

## Approved merge, release tags and successful builds
User explicitly authorized merging MR40 and creating both release tags so the images build. Preflight GET showed mergeable MR, exact approved source2e19eb0f906ef7f842876e42e91903682a4824aa and no conflicting tags. API PUT merged MR40; merge commitc522f0f653ccf64c4d56a1996ffb315a930e6b66. API POST created elasticsearch/6.8.23 and elasticsearch-head/sha-1a888b928135 at that exact merge commit. No +latest tags requested or created.

Elasticsearch [pipeline140808](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140808), build job3223683: success. Head [pipeline140809](https://gitlab.youdo.sg/youdo/base-images/-/pipelines/140809), build job3223684: success. Authenticated docker manifest inspect --verbose verifies linux/amd64 manifests available for registry.youdo.sg/youdo/base-images/elasticsearch:6.8.23 (platform manifestsha256:74d18607336d7954c115613a3ae1f0660458597e8b3f28f76f4874b842e9fc10) and registry.youdo.sg/youdo/base-images/elasticsearch-head:sha-1a888b928135 (platform manifestsha256:f7cdc818c5f3e1c25a5fd143d7fe22700098e84a7b6458dd81cb138bb3358074). Evidence ai-data/devops-894-playbooks/es-mirror-manifests.json; no layers downloaded.

Merge/build/image availability are completed, superseding earlier pending statements. Existing stands still use previous images; local DevOps-894 template references are ready but their Git publication and runtime rollout are not authorized by this merge/tag request.

## Approved runtime rollout completed
User later explicitly authorized simultaneous full redeployment of test1–test7/test10–test15. All13finalNomad deployments succeeded with internal image refs verified via job GET. Two healthy-deadline misses recovered by simultaneous stop/run retries; setup-to-container-start was under0.4s, suggesting image loading was not the cause in these failures. [Rollout evidence](2026-10-14-nomad-test-devops-894-es-unlimited-redeploy.md). This supersedes the earlier pending-runtime-rollout condition; automation Git publication remains outstanding.
