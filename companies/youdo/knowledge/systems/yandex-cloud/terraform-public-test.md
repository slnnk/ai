---
system: yandex-cloud
status: verified
checked: 2026-09-17
tags: [terraform, yandex-tf, public-test, base-image]
---
# Yandex Terraform: public-test

Last verified: 2026-09-17.

## Scope and access

- Repository: `/home/slnnk/git/yandex-tf`; safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yandex-tf.git`.
- Terraform root: `/home/slnnk/git/yandex-tf/public-test`.
- Remote state: Consul at `consul.service.selectel.consul:8500`, datacenter `selectel`, path `terraform/yandex-public-test`.
- The root manages the Linux and Windows public-test machines in `test-folder`/`subnet-test`. The Yandex provider uses ignored `public-test/key.json`; CI copies the key from GitLab Secure Files and also writes `sa-terraform.json` from the protected `YC_TERRAFORM_KEY` variable.
- CI jobs: `validate:public-test` runs `tflint`, `plan:public-test` creates the reviewed plan, and `apply:public-test` is manual on `master` for changes below `public-test/**`.

## Shared Ubuntu 22.04 base-image overwrite mitigation (2026-09-17)

- Changed the Linux machine's image data source from hard-coded ID `fd8tpn447q9l6en2gqvi` to `name = "yc-base-image-ubuntu-22-04"` in `var.folder_id`.
- Added `ignore_changes = [image_id, snapshot_id]` to `yandex_compute_disk.boot_disk_public-test-linux`.
- The separate Windows image `yc-sql-service-os01` and `public-test-sql` boot disk were intentionally left unchanged.
- `terraform validate` succeeds with provider `yandex-cloud/yandex` 0.127.0. The named image resolves to current ID `fd8ot9ko30559cfp1p0o`.
- Read-only verification command: `terraform plan -refresh=false -lock=false -detailed-exitcode -no-color -compact-warnings`. Result: `0 to add, 1 to change, 0 to destroy`; only the pre-existing in-place Linux VM metadata update remains, with no disk or VM replacement.
- Operational caveat: ignored `image_id` preserves the existing Linux boot disk across image rebuilds. Re-imaging requires a separately reviewed controlled recreation or temporary removal of the ignore rule.
- The single in-place change is `yandex_compute_instance.public-test-linux.metadata["user-data"]`. It originates from commit `b202bb5`, which switched SSH-key rendering to `local.vm_ssh_key`; it is unrelated to the image-name change. No public-test resource is planned for deletion or replacement.

## Related recipes

- [Rebuilt cloud image with the same name makes Terraform plan mass disk and VM replacements](../../../../../general/knowledge/terraform/image-rebuild-forces-disk-replacement.md)
