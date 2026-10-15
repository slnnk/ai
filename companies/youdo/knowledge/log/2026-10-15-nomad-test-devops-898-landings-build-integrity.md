---
system: nomad-test
status: verified
checked: 2026-10-15
tags: [gitlab, landings, npm, node, devops-898]
---
# DevOps-898 Landings package integrity and internal Node image

## Summary

Prepared local fixes for the failed Landings build: refreshed stale integrity entries for two unchanged private npm package versions and selected the existing internal Node24 image. User explicitly approved publication after completed validation. CI Lint and the parent agent's isolated full Docker build both passed.

## Task and approvals

Task [DevOps-898](https://youtrack.youdo.com/issue/DevOps-898). User supplied failed [build-web3229694](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/jobs/3229694) in pipeline141007 and approved branch `DevOps-898-refresh-landings-ui-integrity` from master2f6e82ec9b18b9d41eeb9a556d1c005f7a7281b1 plus the checksum fix. User subsequently explicitly requested fixing the image and preparing its base in base-images. After the actual diff, checks and proposed names were presented, user explicitly replied "Подтверждаю публикацию". This authorized staging the two reviewed paths, commit, branch push and MR creation as one publication action. Deployment/merge are not authorized.

## Evidence and findings

- The actual build failure was npm EINTEGRITY during npm install for @youdo/ui0.17.5. Node16 engine messages were warnings, not the fatal cause. API build3229695 succeeded; deployment and production jobs were skipped after the failed web build.
- Anonymous read-only Nexus metadata and artifact GETs independently confirmed consistent current SHA512/SHA1 for @youdo/ui0.17.5. The lockfile held an older checksum. A later local install exposed the same mismatch for @youdo/eslint-config1.2.5; its current metadata and artifact also agree. The reason the contents of the same published versions changed is unverified.
- Sanitized evidence: `/home/slnnk/ai-data/DevOps-898/landings-build/ui-integrity.json` and `eslint-integrity.json`. No package archives, credentials or raw response headers were persisted by this diagnosis.
- Existing base-images recipe/tag node/24 is already published: Node24.13.0/npm11.6.2, successful pipeline140561, registry digest `sha256:1eddbf968846faf466c9dc7fdc285254ad670b7d6ac38f68bd5dfa59f373f73f`. Manifest HTTP200/linux-amd64 confirmed. Evidence `/home/slnnk/ai-data/DevOps-898/node24-manifest-preflight.json` and `node24-tag-pipelines.json`. No base-images repository edit or release is required.

## Local changes and review

Checkout `/home/slnnk/git/youdo.business.landings`, approved branch `DevOps-898-refresh-landings-ui-integrity`.

- `.gitlab-ci.yml`: NODEJS_IMAGE becomes registry.youdo.sg/youdo/base-images/node; NODEJS_IMAGE_TAG becomes24, as explicitly requested.
- `package-lock.json`: four integrity fields only, covering both lockfile-v2 representations of @youdo/ui0.17.5 and @youdo/eslint-config1.2.5. All dependency versions, resolved URLs and other JSON values remain unchanged.
- Independent deep JSON diff confirms precisely those four paths; each checksum matches the saved metadata/artifact evidence. `git diff --check` passes. No source or runtime deployment configuration changes.

## Validation and publication state

CI Lint passed according to the parent verification. Isolated build uses the actual internal Node24 base pulled by digest; parent session93713, log `/home/slnnk/ai-data/DevOps-898/landings-build/local-build.log`. The build completed with exit0: Node24.13.0/npm11.6.2, npm install and npm run build passed, including final nginx image `sha256:abce3cedf21e4c0d225ffd554a012a73ea94931475f0a4416c7ee7b6846b3bc1`. Existing ESLint engine-range and Vite chunk-size warnings were nonblocking. An earlier cached-base attempt was cancelled after the base digest mismatch was detected; its result is not acceptance evidence.

Proposed commit: `refresh landings package integrity and node image`.
Proposed MR: `DevOps-898 refresh landings package integrity and node image`.
Source/target: DevOps-898-refresh-landings-ui-integrity → master. Publication approval received: "Подтверждаю публикацию". Actual staged diff reviewed; only `.gitlab-ci.yml` and `package-lock.json` were staged. Commit `ee64ce015fce4b59a921e078019c30c596bbae85` created with the proposed message and branch push succeeded. [MR18](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/merge_requests/18) created successfully against master; assignee a.solonenko, squash false, remove source true preserved. [MR pipeline141016](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/pipelines/141016) created; its successful completion is not yet asserted. Working tree clean. No merge or deployment executed.

Fresh master pipelines include automatic production canary/update and release; merge/deployment are not authorized by branch or publication approval. Stand acceptance remains GitLab and Nomad statuses only, per user direction.

## Risks and limits

The checksum corrections trust the current internally published metadata and independently matching tarballs without changing versions. Full local build passed; no deployment or successful new pipeline is claimed. Existing Node24 base is reused without modifying base-images.

## User-approved merge and pipeline cancellation

User explicitly requested merging Landings and stopping its MR pipeline. Canceled MR pipeline141016; subsequent GET confirmed `canceled`. Merged MR18 into master using expected source SHA `ee64ce015fce4b59a921e078019c30c596bbae85`, preserving MR/project settings. GitLab confirmed `merged`, merge commit `39c1e5fe4977e500b414549e5d27057930b4fca4`, no squash and no merge error. Master pipeline [141017](https://gitlab.youdo.sg/youdo/microservices/youdo.business.landings/-/pipelines/141017) created automatically on that merge commit; last GET `pending`. Existing automatic production CI effects were disclosed before publication approval and again before merge. No stand deploy jobs played. Helper `/home/slnnk/ai-data/DevOps-898/landings-build/merge_landings.py cancel|merge|status`; API writes authorized only for the requested cancellation and merge.
