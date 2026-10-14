---
system: nomad-test
status: verified
checked: 2026-10-14
tags: [nomad, elasticsearch, vk-cloud, ansible, awx, DevOps-894]
---
# DevOps-894 fixed snapshot names and original AWX order

## Summary

Per explicit user correction, ES snapshot preparation now matches the original two-stage pattern: delete_image first, create_image second, using permanent thin/thick snapshot names. Removed snapshot versioning, retention, publication metadata and fallback snapshot UUIDs from inventory. Local syntax and create/delete/full-order fixtures pass. User-approved one-time rename completed; both permanent names are available.

## Task

DevOps-894: simplify preparation and deployment to fixed snapshot names instead of tracking the latest version/UUID.

## Context

User rejected the additional version retention and create-before-delete ordering, then explicitly requested always addressing snapshots by name. This overrides earlier design choices and supersedes those descriptions in the October13 notes. Local edits remain on the approved DevOps-894-deploy-elasticsearch-on-vk branch; unrelated MSSQL work preserved. No new Git publication or remote mutation authorized/performed in this turn.

## Actions

Reordered refresh tasks to delete then create. Cleanup lists and deletes only snapshots with the exact configured thin/thick names, waits for deletion, and performs no retention. Creation uses those names, waits available and restores seed mounts; no timestamp or metadata is added. Deployment resolves the named available snapshot's UUID internally for the CSI API. No operator-maintained snapshot IDs remain in inventory.

## Findings

Permanent names: vk-ms1-share-base-thin and vk-ms1-share-base-thick. Source seed Cinder volume IDs remain stable configuration, distinct from recreated snapshot IDs. Both entrypoint syntax checks and git diff --check pass. Local fixtures cover create_image, delete_image and combined run; combined run proves both old snapshots are removed before new ones are created, unrelated snapshots preserved, no Nomad calls and no metadata publication.

Already-prepared cloud snapshots retain their old versioned names: thin0d38e5f9-3c42-4923-9e29-4c50bb1de70c and thickef5fb5f1-c828-4605-9f1c-81022edd988b. To immediately use them with the fixed-name configuration, a one-time rename is needed. Prepared local helper ~/ai-data/devops-894-playbooks/rename_prepared_snapshots.py defaults to plan only, --apply checks target name collision/provenance then PUTs name for those two IDs. User explicitly approved the remote rename with "yes"; --apply completed exit0 and GET verified both permanent names/status available. No redundant snapshot creation required.

## Changes

Changed es_vk_refresh.yml, es_vk_cleanup_snapshots.yml, es_vk_publish_variant.yml, es_vk_select_snapshot.yml, scoped VK inventory and README. Removed es_snapshot_prefix, es_snapshot_keep and es_base_snapshot_ids. Snapshot UUIDs are resolved at execution rather than persisted in inventory. Fixture tooling remains outside the repository.

## Limits

Only the approved snapshot name changes were applied; no AWX configuration, stand deployment, commit or push. One-time rename is complete; the next normal AWX run follows delete_image then create_image. Backlog lives in ~/ai/TODO.md. ai-sync reminder forwarded to user: compare personal/usage/*.txt (--kb block) with September30 data.

## Portable lesson

none


## Approved rename completed

User confirmed the concrete two-snapshot rename. Executed `python3 ~/ai-data/devops-894-playbooks/rename_prepared_snapshots.py --apply`, exit0. Both name collisions/provenance checked before mutation, each PUT followed by GET verification. Thin0d38e5f9-3c42-4923-9e29-4c50bb1de70c is now vk-ms1-share-base-thin; thickef5fb5f1-c828-4605-9f1c-81022edd988b is now vk-ms1-share-base-thick; both available. UUIDs/data unchanged. Fixed-name deployment lookup can use these already-prepared snapshots. No new snapshots or other resources created/deleted.
