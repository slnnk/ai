---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, gitlab-ci, inventory]
---
# Next per-stand service recovery scope from DevOps-A-33

## Summary

User requested the next iteration list based on DevOps-A-33 per-stand services, excluding B2B and already deployed services. User subsequently explicitly excluded MiniSape. Eight Nomad candidates remain, plus the article's separate-CI/S3 youdo-moderation frontend. This is scope research only; no repository edits, publications, builds or deployments were performed.

## Source and filtering

Fresh authenticated GET of [DevOps-A-33](https://youtrack.youdo.com/youtrack/articles/DevOps-A-33/Shablony-GitLab-CI#Spisok-servisov), article242-6005, supplied the service table. Already accepted eight Monolith-dependent services, monolith/static and prior single/dynamic releases were excluded. B2B is determined by the article Team column, not only repository name. Form remains excluded as unused. MiniSape is excluded by the user's explicit correction regardless of its technical classification.

Socket is included according to the user's prior explicit per-stand correction and merged MR82/master7f6d81b3. The article's dynamic Socket label is outdated. LogReader remains dynamic and already deployed on test5, outside this scope.

## Nomad candidates

| Service | GitLab repository |
| --- | --- |
| broadcast | [youdo/microservices/broadcast](https://gitlab.youdo.sg/youdo/microservices/broadcast) |
| cerberus2 | [youdo/cerberus2](https://gitlab.youdo.sg/youdo/cerberus2) |
| escrow.walletone | [youdo/microservices/escrow.walletone](https://gitlab.youdo.sg/youdo/microservices/escrow.walletone) |
| featuretoggle | [youdo/microservices/featuretoggle](https://gitlab.youdo.sg/youdo/microservices/featuretoggle) |
| youdo.content | [youdo/microservices/youdo.content](https://gitlab.youdo.sg/youdo/microservices/youdo.content) |
| youdo.landings | [youdo/youdo.landings](https://gitlab.youdo.sg/youdo/youdo.landings) |
| youdo.trackingpixel | [youdo/SEO/youdo.trackingpixel](https://gitlab.youdo.sg/youdo/SEO/youdo.trackingpixel) |
| YouDo.Socket | [youdo/YouDo.Socket](https://gitlab.youdo.sg/youdo/YouDo.Socket) |

## Separate frontend entry

The article also lists youdo-moderation as C2C/per stand with its own CI and S3 publishing. Keep it visible as a separate delivery path; do not conflate it with the monolith backend web-moderation task or assume the shared Nomad microservice playbook deploys it. No repository URL is supplied for this row in the article.

## Findings and limits

Local master/origin CI inspection confirms the eight article candidates originally considered use DEPLOY_TEST_PER_STANDS=true; MiniSape was then removed by user instruction. Socket remains per-stand by the accepted newer correction. Cerberus2 and Socket have custom Ansible deploy overrides; youdo.content has custom Levant/Nomad delivery warranting VK migration review: NOMAD_DC=yandex-test and NOMAD_YANDEX_TEST_ADDR remain in its CI. Content and landings existing local feature checkouts were preserved; audit used origin/master content without switching branches. No claims of fresh remote-master fetch for all candidate repositories.

Read-only VK Nomad jobs snapshot found no candidate deployment; current monolith test5 task names do not contain these candidates. Existing monolith/static and accepted releases remain complete. No new health preflight, database checks or image builds were needed to compose this list.

## Evidence and changed files

Sanitized candidate manifest next-iteration-candidates.json, fresh source article article-DevOps-A-33.json and live job summary next-iteration-live-jobs.json are under /home/slnnk/ai-data/jenkins-recovery/monolith-services-audit/. Knowledge bookkeeping only; repository and remote state unchanged. Live future work belongs in ~/ai/TODO.md.

## User scope corrections and deployment analysis

User subsequently added youdo.help and explicitly excluded escrow.walletone. Active eight-service Nomad list and current-master test5 preparation findings are recorded in [deployment analysis](2026-10-15-jenkins-next-test5-service-deployment-analysis.md); earlier table is the original proposal, not current execution scope.
