---
system: jenkins
status: verified
checked: 2026-10-15
tags: [recovery, buildapi]
---
# Jenkins BuildAPI publication correction and test5 metadata restoration

## Summary

User requested fixing the missing BuildAPI test5 row. Updated only dynamic_deploy Update buildsinfo: four old base URLs replaced with buildapi.dev.youdo.corp, four curl commands gain --fail --show-error, shell gains set -e. Exact updated script hash and approval independently verified. Restored current test5 metadata and one historical record from successful5826; authenticated API and rendered home HTML verified. No deployment/build rerun.

## Task and approvals

User: «Исправь» after the [root-cause diagnosis](2026-10-15-jenkins-buildapi-test5-missing-row.md). Concrete network command approvals covered Pipeline save/approval and separately PUT current metadata plus POST history. No Git, repository, infrastructure rollout, credential rotation or message publication was performed. Superpowers skills were not used.

## Changes and key commands

Local operational helpers, containing no stored credentials or full Pipeline source:

- /home/slnnk/ai-data/jenkins-recovery/fix-buildsinfo.py plan|apply
- /home/slnnk/ai-data/jenkins-recovery/backfill-buildsinfo5826.py [--apply]

Pipeline source and credentials were processed only in memory. Plan asserts four old URLs/four curl commands in Update buildsinfo, preserving other script bytes. Bash -n passed before mutation. Jenkins Script Console sets the exact guarded CpsFlowDefinition and approves only the matching script; no build is triggered.

Before SHA256 fe0c3a782d18b6d02b889f5b9be27699512134b5fb9fec1b996670c7ebc6482d; after185031f56de3696377922b5a45221ab839f1df6a5e67d1621883990329bc85e4.

The first helper applied and approved the script, then stopped on strict XML byte-equivalence after Jenkins reserialization. No retry mutation was attempted. Independent GET confirmed exact expected script hash; a read-only Script Console check confirmed ScriptApproval.using succeeds. Full job XML byte equivalence was not established; CpsFlowDefinition assignment/save was the only job mutation. This limitation is retained in buildsinfo-fix-receipt.json rather than claiming a full XML-diff check passed.

## Metadata restoration and verification

GET inspected5826 SUCCESS and parameters before writing; duplicate guards checked current row and history. Restored only test5, monolith139914, static139593, buildid5826, date2026-10-15_10:43:49 from Jenkins BUILD_TIMESTAMP, original initiating user, original Restore/Rabbit/Elastic selections and empty optional fields. User attribution was used only for the required record, not printed in operational output. Blank BUILD was replaced with the known originating build number5826 for traceability. Existing BuildAPI credentials remain in their original source only.

PUT /builds/test5 and POST /builds completed. Fresh GET confirmed every restored field, exactly one matching history record, and authenticated home HTML contains test5 and both pipeline IDs. Receipt buildsinfo-backfill5826-receipt.json confirms current/history/home verification and deploy_rerun=false.

## Limits and bookkeeping

Future Jenkins publication has not yet been exercised in a new build; saved script syntax/hash and approval were checked. No service addresses were newly discovered or changed. TODO and Jenkins map updated. Earlier user instruction to accept the locally successful Rabbit path for Jenkins is reflected by closing that acceptance item; no Jenkins Rabbit rerun is claimed. Optional nginx empty-input cleanup remains a separate proposal.

## Portable lesson

None.
