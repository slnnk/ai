---
system: yandex-cloud
status: verified
checked: 2026-09-17
tags: [terraform, yandex-tf, test-infra, nomad-test, base-image, instance-group]
---
# Yandex Terraform: test-infra

Last verified: 2026-09-17.

## Scope and access

- Repository: `/home/slnnk/git/yandex-tf`.
- Safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`.
- Terraform root: `/home/slnnk/git/yandex-tf/test-infra`.
- Yandex Cloud folder is resolved by name as `test-folder`; resources are on the private test subnet, primarily in `ru-central1-b`.
- Remote state: Consul at `consul.service.selectel.consul:8500`, datacenter `selectel`, path `terraform/yandex-test-infra`.
- Local access requires the cloud service-account key at `test-infra/key.json` and `CONSUL_HTTP_TOKEN`; record only their locations, never their values.

## CI/CD path

- GitLab jobs are in `.gitlab-ci.yml`.
- A change below `test-infra/**` triggers `validate:test-infra` (`tflint`) and `plan:test-infra`.
- On `master`, `apply:test-infra` is manual. It runs an unpersisted fresh `terraform apply -auto-approve` twice; the second run is an inventory workaround. Therefore the apply job does not consume the reviewed `tfplan`, and its fresh plan must be checked carefully at execution time.
- `ansible:test-infra` is a separate manual job depending on the apply job and runs `automation-services/cluster_docker.yml` using Terraform-backed inventory.

## AWX and Sentry retirement assessment (2026-09-15)

Task: determine the safe removal procedure for the test AWX and Sentry VMs. No resources or repository files were changed during the assessment.

Verified in live Consul state:

- AWX: `ansible_host.awx_test01`, `yandex_compute_instance.awx-test01`, `yandex_compute_disk.boot-awx-test`.
- Sentry: `ansible_host.sentry-test`, `yandex_compute_instance.sentry-test`, `yandex_compute_disk.boot-sentry-test`, `yandex_compute_disk.data_new_disk_sentry-test`.
- The Sentry data disk is a separately managed 186 GB `network-ssd-io-m3` disk. Its `secondary_disk.auto_delete = false` only prevents deletion as a side effect of VM deletion; removing its own Terraform resource from configuration still plans destruction of the disk.
- No `prevent_destroy` lifecycle rules exist on these resources. Disk lifecycle only ignores changes to `snapshot_id`.
- Repository-wide references to the test hosts are confined to `test-infra/compute-awx-test.tf`, `test-infra/compute-sentry-test.tf`, and the two matching blocks in `test-infra/ansible-hosts.tf`.

Recommended retirement workflow:

1. Confirm service owners have stopped traffic/jobs and decide whether the Sentry data disk needs retention.
2. If data must be retained, create and verify a snapshot/backup before apply and keep the `data_new_disk_sentry-test` resource in a separate Terraform file so it remains managed. If it must remain in Yandex Cloud but cease Terraform management, use an auditable Terraform `removed` block with `destroy = false` (supported by the CI Terraform 1.7.5); avoid an uncoordinated manual `terraform state rm`, because the still-present configuration can then plan a replacement disk.
3. Delete both compute files and remove both `ansible_host` blocks in the same merge request.
4. Review `plan:test-infra`; expected managed-object destruction is exactly 7 objects if the Sentry data disk is deleted: 2 hosts, 2 instances, and 3 disks. Outputs and image data sources disappear from configuration/state but are not cloud objects to destroy. Any unrelated change is a stop condition.
5. Merge, then manually run `apply:test-infra` on `master`. Verify both applies and then verify absence in Terraform state and Yandex Cloud. Run `ansible:test-infra` only if reconfiguration of the remaining hosts is intended.

Rollback: restore configuration through Git and recreate from Terraform. VM-local data is recoverable only from a verified snapshot/backup; recreated boot disks are initialized from the configured Ubuntu image.

## AWX and Sentry repository removal (2026-09-15)

- Deleted `test-infra/compute-awx-test.tf` and `test-infra/compute-sentry-test.tf`; the Sentry 186 GB data disk is intentionally not retained.
- Removed `ansible_host.sentry-test` and `ansible_host.awx_test01` from `test-infra/ansible-hosts.tf`.
- `terraform validate` succeeded outside the filesystem sandbox. The sandbox itself prevents Terraform provider child processes from starting, so provider-based validation must run outside it or in CI.
- Live read-only plan result: `0 to add, 17 to change, 7 to destroy`. The seven destroys are exactly the two Ansible hosts, two VMs, two boot disks, and the Sentry data disk expected above.
- Important apply risk: the same plan contains 17 unrelated in-place updates caused by `user-data`/SSH-key representation drift. They affect ordinary VMs plus both Nomad instance groups. Do not treat the current apply as an isolated retirement until this drift is reviewed in the CI plan; applying the instance-group changes can trigger rollout behavior.
- Restart impact verified 2026-09-15: the 15 standalone `yandex_compute_instance` updates have no replacement paths and update only VM metadata. Yandex Cloud documents that standalone VM metadata updates do not require stopping or restarting the VM. The two instance-group template metadata changes do require VM restart: all 7 Nomad agents and all 3 Nomad/Consul masters are subject to sequential restart. Both groups have `max_unavailable = 1` and `max_expansion = 0`; the master group additionally has `max_deleting = 1` and `startup_duration = 30`.
- Repository diff at verification: only the two deleted compute files and the two removed inventory blocks; `git diff --check` passed and no AWX/Sentry references remained under `test-infra`.

## Unexpected mass replacements in MR !224 plan (2026-09-17)

- GitLab job `3150822` (`plan:test-infra`, pipeline `138877`, commit `bca68d9`) reported `30 to add, 15 to change, 37 to destroy`. Do not apply this plan.
- The intended retirement accounts for exactly 7 standalone destroys: two Ansible hosts, two VMs, AWX boot disk, Sentry boot disk, and Sentry data disk.
- The extra actions are replacements of 15 unrelated boot disks and their 15 dependent VMs. Every disk replacement is driven by `image_id = fd8tpn447q9l6en2gqvi -> null`; instance replacement then follows from the changed boot-disk ID. The image data sources still resolve the expected image ID, so the image itself is not missing.
- Baseline job `3145820` for the same MR on 2026-09-16 00:00-00:01 MSK produced the expected `0 add, 17 change, 7 destroy`. By job `3148467` at 15:30-15:31 MSK the mass replacements were already present (`34 add, 17 change, 34 destroy`). Therefore the change appeared between those jobs without a matching repository diff.
- No successful GitLab `apply:test-infra` job exists in the inspected interval. The only master apply job (`3145068`) remained manual and was not started.
- Read-only Consul state inspection on 2026-09-17: state format `4`, serial `694`, writer `terraform_version = 1.9.4`, lineage `822e477f-4c5f-190f-0071-2d7daca04375`, Consul `ModifyIndex = 175842428`. GitLab runs Terraform `1.7.5` with Yandex provider `0.127.0`.
- A plain Terraform plan refreshes state only in memory and does not persist it. The `terraform_version = 1.9.4` marker therefore indicates an apply-like state write outside the inspected GitLab jobs: most likely a manual `terraform apply`, `terraform apply -refresh-only`, deprecated `terraform refresh`, or an explicit state write from Terraform 1.9.4. Consul state alone does not record the operator or exact command.
- Reproduced read-only with both normal plan and `plan -refresh=false -lock=false`: the same 15 disk plus 15 VM replacements remain. This localizes the problem to the persisted state/config/provider interaction rather than current cloud refresh or the AWX/Sentry deletion diff.
- Safe next step: identify the operator/command and provider version used during the state write, then obtain the pre-write Consul state backup from before 2026-09-16 15:30 MSK. Compare its serial/resources before considering a controlled state restore. Do not add broad `ignore_changes = [image_id]` or apply the current plan as a shortcut; either action can hide real drift or destroy unrelated VMs.

## Shared base-image overwrite: confirmed cause and mitigation (2026-09-17)

- Confirmed cause: an employee overwrote the shared Yandex Cloud image used to initialize all `test-infra` boot disks. The old image ID recorded in state/configuration was `fd8tpn447q9l6en2gqvi`; the rebuilt image with the stable name `yc-base-image-ubuntu-22-04` currently resolves to `fd8ot9ko30559cfp1p0o`.
- Updated all 15 active Ubuntu image data sources under `test-infra`: lookup now uses `name = "yc-base-image-ubuntu-22-04"` and `folder_id`, rather than a hard-coded image ID. The disabled `compute-elk-test.tf.disabled` file was intentionally left unchanged because Terraform does not load it.
- Added `ignore_changes = [image_id, snapshot_id]` to the 13 managed standalone boot disks. Existing `snapshot_id` protection was preserved.
- Added a narrow lifecycle ignore for `instance_template[0].boot_disk[0].initialize_params[0].image_id` to both Nomad instance groups. This prevents replacement/rollout of existing group VMs solely because the stable image name points to a newly built image ID; newly created instances still use the currently resolved image.
- `terraform validate` succeeds with Yandex provider `0.127.0`, confirming the nested lifecycle paths are valid.
- Read-only verification used `terraform plan -refresh=false -lock=false -detailed-exitcode -no-color`. Result: `0 to add, 17 to change, 7 to destroy`; the previous 15 boot-disk plus 15 VM replacements are gone. The seven remaining destroys are only the already approved AWX/Sentry retirement resources, while the 17 in-place metadata updates remain unrelated SSH-key representation drift.
- Operational caveat: ignoring `image_id` deliberately preserves existing disks/VMs when the named base image is rebuilt. It also means changing the desired base image for existing machines will require an explicit controlled recreation or temporary removal of the ignore rule; this must be reviewed rather than applied implicitly.

## Avoiding instance-group restarts for SSH-key rotation

Assessment date: 2026-09-15.

- Current drift was introduced by commit `b202bb5`: group `USER_SSH_KEY` input changed from the old variable/file fallback to `local.vm_ssh_key = chomp(file("${path.module}/files/youdo.pub"))`. This changes the rendered multiline `user-data`, so both instance-group templates are updated.
- Standalone VM metadata can be updated live, but Yandex Instance Groups rules explicitly classify `instance_template.metadata` changes as requiring VM restart. There is no Terraform/Yandex switch that makes the same group-template metadata change live.
- Recommended long-term design: migrate SSH authorization to Yandex Cloud OS Login (prefer SSH certificates), install/verify the OS Login agent on existing Ubuntu 22.04 hosts, enable OS Login once, and manage access through IAM/Identity Hub. The initial group-template migration may require one controlled rolling restart, but later key/user changes no longer touch instance metadata and do not restart groups.
- Alternative when OS Login is not available: manage `/home/<user>/.ssh/authorized_keys` in-guest through Ansible or another configuration agent. Keep group `user-data` stable and use it only for bootstrap.
- Immediate workaround for a retirement-only apply: add a narrowly scoped Terraform lifecycle ignore for the group template's `user-data`, or restore the exact previously rendered `user-data` representation. Ignore rules conceal future intended metadata changes and must be documented/removed after SSH access is moved elsewhere.
- A targeted apply of only retirement resources can also avoid the current group update, but it is an exceptional operational workaround and leaves the SSH metadata drift pending for the next full apply.

## Failed master apply after base-image migration (2026-09-17)

- GitLab pipeline `138961`, job `3154035` (`apply:test-infra`), merge commit `7e712f93b000b234293a9aed66d44f693041d14f`, failed after a partial apply. Runner: `gitlab-runner-docker-1` (`172.28.0.171`), Terraform `1.7.5`, Yandex provider `0.127.0`.
- The apply plan was `0 to add, 17 to change, 7 to destroy`. Terraform successfully destroyed all seven approved AWX/Sentry objects: two Ansible hosts, both VMs, both boot disks, and the Sentry data disk. It also completed 14 of the 17 in-place changes to standalone VMs. Because Terraform persists state incrementally, do not assume the failed job rolled these changes back.
- Both Nomad/Consul instance-group updates failed because the request retained deleted image ID `fd8tpn447q9l6en2gqvi`. The current named image lookup succeeded as `fd8ot9ko30559cfp1p0o`, but the newly added nested `ignore_changes` retained the old image ID from state. The pending SSH-key/user-data template update caused the provider to submit a new instance template, and Yandex Cloud rejected that template while validating the deleted retained image.
- Corrective choices for the groups require an operational decision: either temporarily remove the nested image ignore and perform a controlled rolling migration to the current image (7 agents and 3 masters, preserving quorum and checking Nomad/Consul health), or suppress/revert the pending group `user-data` update so no template update is submitted. The latter leaves the old image reference and SSH-key drift unresolved. Do not blindly retry the same apply; it will fail again.
- `yandex_compute_instance.zabbix-test` failed separately. The intended `core_fraction` change from `20` to `100` requires stopping the VM, but the resource lacks `allow_stopping_for_update = true`. Either add that flag and accept a controlled Zabbix restart or revert the CPU-fraction change.
- Non-fatal warning: `test-infra/terraform.tfvars` still sets undeclared `shared_network_name`; both its variable and corresponding data source are commented out. Remove the stale tfvars entry or restore the declaration if it is still required.
- Before the next apply, run a fresh plan and verify actual post-failure state. Expected completed actions from the trace are all seven destroys and 14 standalone metadata updates; the two groups and Zabbix update remain pending unless changed out of band.

### Prepared remediation

- On local branch `DevOps-859-delete-old-vms`, both Nomad/Consul group lifecycle blocks now also ignore `instance_template[0].metadata["user-data"]`. This prevents the pending SSH-key representation drift from submitting an instance-template update and therefore avoids revalidating the deleted image reference during the next ordinary apply. The existing nested image ignore remains in place; consequently both the old image reference and group SSH-key drift are intentionally deferred.
- Scaling caveat: a pure `fixed_scale.size` reduction should update only `scale_policy`, so it should not revalidate the ignored image or create a new disk. It will permanently delete the selected group VMs and their group-managed boot disks. Increasing the group, replacing an unhealthy VM through auto-healing, or changing any non-ignored `instance_template` field may still fail because the live group template retains deleted image ID `fd8tpn447q9l6en2gqvi`. Treat the lifecycle ignore as a temporary apply workaround, not a repair of the group template.
- `yandex_compute_instance.zabbix-test` now sets `allow_stopping_for_update = true`, allowing the intended `core_fraction = 20 -> 100` update. Applying it can stop/restart the Zabbix VM and should be done with monitoring downtime awareness.
- Changed files: `test-infra/compute-group-nomad-agent-test.tf`, `test-infra/compute-group-nomad-master-test.tf`, and `test-infra/compute-zabbix-test.tf`.
- Verification: targeted `terraform fmt -check` passed; `terraform validate` passed outside the filesystem sandbox with the installed Ansible, Helm, and Yandex providers. A live post-failure plan has not yet been run, so it remains the required check before apply.

## Related recipes

- [Rebuilt cloud image with the same name makes Terraform plan mass disk and VM replacements](../../../../../general/knowledge/terraform/image-rebuild-forces-disk-replacement.md)
