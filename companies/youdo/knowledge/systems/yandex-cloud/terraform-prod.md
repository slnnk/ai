---
system: yandex-cloud
status: verified
checked: 2026-09-17
tags: [terraform, yandex-tf, prod, awx, sentry, hashi-master, base-image]
---
# Yandex Terraform: prod

Last verified: 2026-09-17.

## Scope and access

- Repository: `/home/slnnk/git/yandex-tf`.
- Safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`.
- Terraform root: `/home/slnnk/git/yandex-tf/prod`.
- Remote state: Consul at `consul.service.selectel.consul:8500`, datacenter `selectel`, path `terraform/yandex-prod`.
- The Yandex provider expects `prod/key.json`, which is ignored by Git. GitLab `plan:prod` and `apply:prod` copy this key from project Secure Files before running Terraform. Never record the key contents in notes.

## AWX retirement (2026-09-15)

- Removed `prod/compute-awx-prod.tf`. It declared the Ubuntu image data source, `yandex_compute_disk.boot_awx_prod`, `yandex_compute_instance.awx-prod-01`, and output `awx-prod-01`.
- Removed `ansible_host.awx-prod` from `prod/ansible-hosts.tf`.
- No AWX data disk was declared; the only managed disk is the 30 GB boot disk.
- Live Consul state before apply contains `ansible_host.awx-prod`, `yandex_compute_disk.boot_awx_prod`, and `yandex_compute_instance.awx-prod-01` plus the image data source. Expected cloud/resource destruction is exactly 3 managed objects; the data source and output only disappear from configuration/state.
- Local full `terraform validate`/plan requires `prod/key.json`; the provider reports `Invalid SA Key` when the ignored file is absent. For a one-time check on 2026-09-15, `test-infra/key.json` was copied temporarily to `prod/key.json` with mode `0600`, used for validation and planning, then the copy was deleted. The source key was not changed.
- Verified prod result: `terraform validate` succeeded and the live plan is clean: `0 to add, 0 to change, 3 to destroy`. The three deletes are only `ansible_host.awx-prod`, `yandex_compute_instance.awx-prod-01`, and `yandex_compute_disk.boot_awx_prod`; output `awx-prod-01` disappears. Saved local plan: `/tmp/yandex-tf-prod-awx-removal.tfplan` (ephemeral, do not use as a long-term artifact).
- No apply was performed during the repository edit.

## Branch synchronization (2026-09-17)

- Branch `DevOps-859-delete-old-vms` was synchronized with `origin/master` at `5825e8a` by merge commit `99cca47`.
- `master` had changed `ansible_host.awx-prod` into a commented block; the merge conflict in `prod/ansible-hosts.tf` was deliberately resolved in favor of the feature branch's full deletion.
- After the merge, `prod/compute-awx-prod.tf` remains deleted and no `awx-prod` or `awx-01` references remain under `prod/`.
- Follow-up commit `3ca0a26` removes the commented `ansible_host.sentry-prod` block from `prod/ansible-hosts.tf`. This initially preserved the VM definition; commit `bca68d9` subsequently removed the Sentry VM resources as part of the full retirement described below.
- No Terraform apply or remote-state mutation was performed. The branch remains local/ahead of its remote until explicitly pushed.
- `terraform fmt -check` still reports pre-existing alignment differences in `prod/ansible-hosts.tf` and `test-infra/ansible-hosts.tf`; these were not reformatted during conflict resolution to avoid unrelated changes.

## Sentry and Hashi Master retirement (2026-09-17)

- Commit `bca68d9` directly deletes `prod/compute-sentry-prod.tf` and `prod/compute-hashi-master.tf`; no `.tf.off` replacements were created.
- Deleted Sentry objects: image data source, boot and data disks, `yandex_compute_instance.sentry-prod01`, and its output.
- Deleted Hashi Master objects: image data source, three boot disks, three `yandex_compute_instance.hashi-master-prod` instances, and their output.
- Removed the commented `ansible_host.hashi-master-prod` block. The Sentry inventory block was already removed by `3ca0a26`.
- Removed `boot_sentry_prod` and `data_sentry_prod` from both `yandex_compute_snapshot_schedule.vm_snap_daily` and `.vm_snap_weekly`; all other scheduled disks remain unchanged. Hashi Master disks were not present in these schedules.
- GitLab MR `yandex-tf!225` (`devops-860-delete-sentry-hashi-master`) was used read-only as the scope reference. Its rename-to-`.tf.off` approach was deliberately not copied, fetched, merged, or cherry-picked into the working branch; the resources were deleted directly instead.
- Validation initially succeeded only on a temporary complete copy with the valid ignored key from `test-infra/key.json`. On 2026-09-17 the user replaced the ignored placeholder `prod/key.json` with a working key, so direct validation in `prod/` now succeeds.

## Shared Ubuntu 22.04 base-image overwrite mitigation (2026-09-17)

- The user replaced the ignored placeholder `prod/key.json` with a working service-account key; the key remains gitignored and its contents were not recorded.
- Updated the four active prod workloads that use the shared Ubuntu 22.04 base image: GitLab, Nexus, YouTrack, and FreeIPA. Their `yandex_compute_image` data sources now resolve `name = "yc-base-image-ubuntu-22-04"` in `var.folder_id` rather than hard-coding old image ID `fd8tpn447q9l6en2gqvi`.
- Added `ignore_changes = [image_id, snapshot_id]` to the four corresponding standalone boot disks. Existing disks remain attached when the stable image name is rebuilt with a new ID, while a newly created disk uses the current named image.
- Deliberately did not change the separate Ubuntu 20.04 image used by 1C or either Windows image used by SQL Report.
- Direct `terraform validate` in `prod` succeeds with the working ignored key.
- Read-only verification command: `terraform plan -refresh=false -lock=false -detailed-exitcode -no-color`. All four named image lookups resolved current ID `fd8ot9ko30559cfp1p0o`; no boot-disk or VM replacement was planned for GitLab, Nexus, YouTrack, or FreeIPA.
- Current unrelated plan baseline is `0 to add, 2 to change, 11 to destroy`: removals are the already configured AWX, Sentry, and three Hashi Master retirements; the two in-place changes remove the retired Sentry disks from daily and weekly snapshot schedules. Review that destructive scope separately before apply.
- Operational caveat: the lifecycle ignore intentionally prevents automatic migration of existing machines to later base-image builds. Re-imaging an existing prod host requires a separately reviewed controlled recreation or temporary removal of the ignore rule.
- No Terraform apply was run. Before apply, inspect a fresh plan carefully to confirm the intended instance/disk destruction and snapshot-schedule updates.

## Related recipes

- [Rebuilt cloud image with the same name makes Terraform plan mass disk and VM replacements](../../../../../general/knowledge/terraform/image-rebuild-forces-disk-replacement.md)
