---
system: nomad-test
status: verified
checked: 2026-10-16
tags: [nomad, vk-cloud, houston, mongodb]
---
# DevOps-898 Hub MongoDB memory increase and release

## Summary

User requested increasing Hub staging MongoDB memory to256MiB and a new release after the initial2.7.6startupOOM. Explicit branch approval received. Local one-line change and checks complete; publication approval pending. Current runtime remains2.7.6with100MiB; new proposed release2.7.7not created.

## Context and actions

Existing release2.7.6was deployed through GitLab141056/3231955from masterb28b07a. App/Mongo recovered automatically after MongoOOM137once and Hub2worker restarts. Read-only logs later confirmed app Settings.mongo.servers=None during Mongo discovery before recovery. User now explicitly requests changing Mongo memory, so this is authorized task scope, not optional hardening. No app startup-race changes included. Classifier MR20is green and still unmerged; the memory request does not authorize classifier merge/tag.

Fetched Hub origin; clean initial checkout. Stage1 proposal branch DevOps-898-increase-hub-mongodb-memory in data/houston/hub from origin/masterb28b07ac3f91909c88442473e23139a65184e106; user reply “Да” explicitly approved. Created branch in existing checkout; only deployments/staging.nomad changed memory100to256in Mongo task resources. Prior task branches preserved; no unrelated changes.

## Verification

- git diff --check PASS, actual diff1insertion/1deletion.
- Nomad1.3.5local job validate with version2.7.7and existing staging DC/domain values PASS, zero warnings; server driver validation intentionally skipped.
- nomad job run -output structured comparison against HEAD confirms ONLY mongo.Resources.MemoryMB100to256changed. No deployment/API write from these checks.
- Read-only GitLab inspect: project163defaultmaster, no existing open MR for new branch, squashdefault_off/recentfalse, source deletiontrue, assigneea.solonenko.

## Publication proposal and approvals

Stage2pending. Proposed commit increase staging mongodb memory to 256 mib. Proposed MR DevOps-898 increase hub staging mongodb memory, branch DevOps-898-increase-hub-mongodb-memory to master, explicit path deployments/staging.nomad only. Russian description prepared at ~/ai-data/DevOps-898/classifier-audit/hub-memory-mr-description.md: one paragraph explaining100to256afterOOM plus task link. Branch publication starts ordinary CIbuild/test/validation, pushes branch image and latest, no automatic deployment on branch. Later proposed tag2.7.7on resulting master starts release+automatic VKstagingdeployment; productionmanual. Publication approval does not by itself authorize merge. No commit/push/MR/merge/tag/deploy for this follow-up performed yet.

## Changed files and risks

Repository: hub/deployments/staging.nomad only. KB log/system/backlog and local MRdescription prepared. Memory applies only to staging Mongo task, app/production unchanged. No volume/data or Mongo version changes. Runtime limit increase and new release remain unverified until publication/merge/tag/deploy.

## Publication completed

Stage2 user approval: explicit “Да” to reviewed commit/push/MR proposal. Full staged diff inspected, deployments/staging.nomad only100to256, diff --check PASS. Committed2efc5181f787e66f8e0909bf972a028430f7a6e0 with increase staging mongodb memory to 256 mib; pushed approved branch; created MR25 https://gitlab.youdo.sg/data/houston/hub/-/merge_requests/25 to master. GETreadback verified expected SHA/title/source/target, assigneea.solonenko, squashfalse, source deletiontrue. Local worktreeclean. Pipeline141059 initiallyPENDING, build3232090pending, tests3232091–3232093created. No merge/tag/deploy for this follow-up; existing runtime2.7.6/100MiB unchanged. Next proposal after successfulCI: merge MR25 and tag2.7.7on resulting master, which automatically deploys VKstaging; production remainsmanual. Merge requires explicit approval beyond publication gate.

Latest GET: pipeline141059SUCCESS at exact2efc518; build3232090,ruff3232091,mypy3232107,Nomad lint3232108allSUCCESS. Shared runners enabled and105/106online/unpaused confirmed during initial queue. Agent performed no job retries. Ready for explicit mergeMR25+tag2.7.7approval; automatic staging deployment effect stated. Runtime remains2.7.6/100MiB until release.

## User completed both merges/tags; runtime verification

User reported “Я уже все смержил и добавил теги на оба сервиса”. Fresh GET verified HubMR25merged, merge/masterfda0ef4fdac865d3e12036937a7886bcea984790 and tag2.7.7exactlythere; classifierMR20merged, merge/master3d511c3f9c6da8f5848ec0b90f6a449d2c29ae41 and tag2.6.10exactlythere. These merges/tags were performed by user, not agent.

Hub pipeline141063SUCCESS/staging3232118SUCCESS; production3232119MANUAL. Nomad jobversion1, app image2.7.7, one app + one Mongo allocationrunning/healthy; Mongo MemoryMB256/MemoryMaxMB0 (no separate max, memory acts as task limit). Mongo new allocation122106e1-c105-d0d5-eede-d4703c5f20cd has0restarts; appfbdd500f-87b6-115a-8848-8e2621d7180a has1restart and currentlyhealthy. Consulpassing, /health200, /experiments200total0. Requested memory applied. Long-term memory stability not established by immediate check.

Classifier pipeline141061SUCCESS/staging3232105SUCCESS; production3232106MANUAL. Version2.6.10, one app + one Redisgroup (Redis/exporter)running/healthy, Consulpassing, /health200. Appad6a4468-e049-7e33-eb26-e48cdbbaefe7has1restart; Redisgroupc5b05ae5-3484-43b8-5597-8676cdcd40bd tasks0restarts. Sanitized snapshots hub-release-status.json/classifier-release-status.json in audit directory. All requested shared Hub/classifier rollout and Mongo256MiB tasks verified complete. No experiment import performed.
