---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, elasticsearch, vk-cloud, ansible, DevOps-894]
---
# DevOps-894 VK ES playbook adaptation

## Summary

Local ES deployment and base-publication playbooks now support VK Cloud/vk-csi through a scoped inventory. Deployment clones validated Cinder snapshots; weekly publication creates and validates candidates before durable metadata publication. Syntax, template parsing and 11 local HTTP-fixture scenarios passed. No adapted playbook was applied to infrastructure, and nothing was committed/pushed.

## Task

DevOps-894: adapt the Elasticsearch playbooks in automation-test-yandex after successful live thin/thick snapshot restoration verification.

## Context

Proposed branch DevOps-894-deploy-elasticsearch-on-vk, repository ~/git/automation-test-yandex, base origin/master (a240575). User explicitly approved creating the branch and task-local edits with "Да". `git switch -c DevOps-894-deploy-elasticsearch-on-vk origin/master` succeeded. Existing unrelated MSSQL changes and untracked mssql_inventory.ini were preserved; no staging, commits or other publication actions performed.

The user requested playbook adaptation only in this step. AWX restoration/configuration, Airflow DAG edits and production/stand execution remain outside this local operation. Proposed publication names, not approved: commit `adapt elasticsearch deployment to vk cloud`; MR `DevOps-894 Deploy Elasticsearch on VK Cloud`; source DevOps-894-deploy-elasticsearch-on-vk, target master. Relevant CI effects must be reviewed before any publication approval.

## Actions

Added a backend-gated VK task path to the existing deploy/base-publication entrypoints. Initial implementation retained Yandex behavior; this was superseded by the explicit VK-only correction below. Public-test remains on its separate bind-mount path. Parameterized thin/thick volume identities, namespace and service domain; fixed the touched legacy malformed Jinja expression and put backend guards before skipped YC result accesses.

Deploy preflights plugin and exact source snapshot before teardown, waits for allocations/claims/cloud detach, checks disk ownership and refuses seed deletion, deletes through CSI before losing registration, verifies cloud/Nomad disappearance, restores via top-level SnapshotID and validates actual disk type/size/provenance. run_es loads the existing volume independently and checks ES primary-shard readiness. No forced deregistration/detach or swallowed authentication failures in the VK path.

Publication retains AWX tags create_image/delete_image. It verifies the exact seed disk attachment/filesystem/no active users, temporarily unmounts while snapshotting, remounts in always, validates an isolated disposable clone against metadata from the source ES APIs and deletes the clone. Only successful candidates receive Cinder snapshot metadata es_validated=true. Deployment discovers the latest available validated snapshot of its exact thin/thick seed; known tested bootstrap UUIDs remain fallback. Retention preserves bootstrap snapshots and at least two newer validated publications per variant; failed candidates remain unpublished for inspection. Durable cloud metadata allows separate AWX job pods; no publication state relies on /tmp.

## Findings

Verification evidence:

- Both entrypoints pass ansible-playbook --syntax-check; scoped --list-hosts selects only the logical vk_es target.
- Offline thin/thick job render and Nomad JSON parse pass with correct VK volume identity, DC/namespace/domain. CSI payloads use SnapshotID and exact 5/40 GiB capacities. Both isolated validation job variants parse without service registrations. Initial Yandex fallback rendering passed before the VK-only correction. Current checks require VK variables and verify the YC template is removed; public-test template remains byte-identical to HEAD and renders.
- Actual deploy playbook against local Nomad/Cinder HTTP fixtures: first deployment, reset, standalone run_es, busy claims, invalid snapshot, ACL denial, and existing-volume create refusal all pass. Busy/invalid/denied/existing cases perform no destructive mutations.
- Actual AWX publication entrypoint against local fixtures/mount stubs: create_image success for both variants, metadata mismatch cleanup/no publication, lost clone-create response reconciliation/cleanup/no publication, delete_image retention all pass.
- Fresh code review found skipped YC guard ordering and ambiguous clone-create cleanup issues; both fixed and rechecked. No material new issues reported for the fix pass.
- git diff --check passes. KB lint has zero errors and six pre-existing warnings.

Fixture tests use fake credentials and 127.0.0.1 only; publication filesystem commands/SSH/sudo are stubbed in a temporary copy. They verify orchestration and failure paths, not an actual AWX environment or new live application deployment. Previous live clone validation establishes vk-csi/ES compatibility, but the adapted playbooks still need an explicitly approved pilot run.

## Changes

Task paths:

- playbooks/deploy/docker/deploy_es_nomad.yml and recreate_es_base_image.yml.
- playbooks/deploy/docker/files/nomad_es/es_thin.j2, es_thick.j2, es_validation.j2, vk-csi-es-volume.json.j2.
- playbooks/deploy/docker/tasks/es_vk_auth.yml, es_vk_select_snapshot.yml, es_vk_deploy.yml, es_vk_refresh.yml, es_vk_publish_variant.yml, es_vk_validate_publication.yml, es_vk_cleanup_snapshots.yml.
- inventories/vk_es/hosts, group_vars/all.yml and README.md.

Local fixture artifacts outside the repository: ~/ai-data/devops-894-playbooks/test_templates.py, test_lifecycle.py and test_publication.py. No credential values stored in task files or notes. Required AWX environment names are documented; Keystone credentials are kept in memory with no_log. Stand Consul token is explicitly scoped; validation jobs clear inherited Consul/Vault credentials.

## Limits

The unavailable Yandex AWX workflow has not been recreated or rescheduled. DBA_Clean still targets the Yandex share in its repository; changing its destination to the VK seed mounts requires separately approved dba branch edits. AWX must reach the backup ES metadata APIs and provide the share SSH credential. Coordinate producer copy/publication/cleanup/deployment runs so selection and deletion do not overlap; source metadata must match the delivered cold copy. Bootstrap snapshots are intentionally retained. If a CSI failure creates an unregistered cloud disk, do not blindly recreate it; inspect provenance and request explicit cleanup. Live application testing and Git publication are not authorized by the local branch approval. Backlog is in ~/ai/TODO.md.

## Portable lesson

none


## User correction: VK only

The user explicitly requested removing all Yandex-specific ES code and cloud-selection checks. The existing approved task branch was reused; no additional Git operation or publication approval was needed for these local corrections. This supersedes all earlier dual-backend descriptions for the ES adaptation.

Replaced deploy_es_nomad.yml and recreate_es_base_image.yml with VK-only entrypoints, removed es_cloud configuration and all backend conditions, deleted the unused yc-csi-es-volume.hcl.j2, and removed YC volume/domain fallbacks from thin/thick templates. Public-test keeps its original bind-mount template but its entrypoint uses the configured VK Nomad API. README now describes VK-only behavior. No unrelated Yandex/MSSQL repository code was removed.

Required API/authentication, disk provenance and detach checks remain because they guard actual VK operations; no provider-selection checks remain. Search across touched ES playbooks/tasks/templates/inventory found no yandex, yc-csi or es_cloud references. Both syntax checks, template parsing, seven deployment HTTP-fixture scenarios and four publication/retention scenarios passed after correction. Reviewer confirmed no material issues and correct retained AWX tag propagation. No remote changes, staging, commits, push or deployment.


## User correction: fast deployment, Nomad result only

The user requested fast stand startup and explicitly accepted successful Nomad deployment as the sufficient deployment result. Simplified es_vk_deploy.yml to select a snapshot, stop the job, delete/recreate its CSI volume, render the existing template and run `nomad job run` without `-detach`. Removed plugin checks, allocation/claim/Cinder polling, backing-disk provenance checks, existing-volume preflight, post-creation verification and Elasticsearch health/metadata checks from the deployment path. CSI delete retries only its operation errors while detach completes; there are no fixed sleeps or independent detach checks. run_es uses no cloud authentication or snapshot lookups. Public-test also uses the blocking Nomad command. Snapshot selection retains the durable validated-publication metadata lookup but no longer verifies the selected snapshot through extra GET/assert tasks.

The separate base snapshot publication playbook remains unchanged: data validation occurs there rather than on every stand deployment. This supersedes earlier descriptions of extensive deployment preflight and readiness checks. README updated accordingly. This is scoped to the user's requested fast deployment, not a broader permission to skip all other task verification.

Checks after simplification: syntax check and template parse pass, git diff --check passes. Two focused local fixtures verify run_es performs only Nomad submission, uses no -detach flag, succeeds on the command's exit0 and fails on exit1. The older seven-case deployment fixture describes the previous stricter implementation and is no longer the current deployment acceptance suite. Publication fixtures were not rerun because its code did not change. No live deployment, Git staging, commit or push. HashiCorp job run documentation confirms default deployment monitoring and failure exit status: https://developer.hashicorp.com/nomad/commands/job/run .


## User correction: no clone validation during preparation

After the actual create_image stage successfully prepared two snapshots, the user explicitly requested removing the added clone/ES/index verification to speed preparation. Historical Yandex image publication had no such verification. This supersedes the earlier separation that retained full validation in weekly publication. Future create_image performs seed unmount, Cinder snapshot creation/availability wait, remount and direct publication (es_published=true), with no Nomad clone jobs or source ES metadata APIs. The unused validation task/template and variables were removed. Snapshot selection/retention now use the publication marker; fallback UUIDs point to the snapshots from the completed run. See [actual execution and changes](2026-10-13-nomad-test-devops-894-awx-create-image-run.md). No redundant live rerun or extra validation after that instruction.
