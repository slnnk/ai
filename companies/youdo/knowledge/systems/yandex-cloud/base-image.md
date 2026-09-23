---
system: yandex-cloud
status: verified
checked: 2026-09-17
tags: [packer, base-image, ubuntu-22-04, yc-base-image, gitlab-ci]
---
# Yandex Cloud base image

Last verified: 2026-09-17.

## Purpose and repository

- Repository: `/home/slnnk/git/yc-base-image`.
- Safe origin: `git@gitlab.youdo.sg:sysadmins/yandex/yc-base-image.git`.
- Builds the shared Ubuntu 22.04 base image in Yandex Cloud with Packer and the `base_linux` Ansible role from `automation-services`.
- GitLab job: `image_build` in `.gitlab-ci.yml`; it runs only for `master` and uses the `dind` runner tag.

## Build flow

1. GitLab CI uses `registry.youdo.sg/youdo/base-images/packer:1.10.2`.
2. The job clones `sysadmins/automation-services` and obtains the `base_linux_login_user_password` value through the shared Vault login template. The secret value must not be copied into notes.
3. Packer reads CI variables through `env()` defaults in `base_image.pkr.hcl`; no `packer -var` flags are required.
4. `YC_IMAGE_NAME` is the project/group CI variable with the stable base name. Job variable `YC_OS_VERSION` is the OS suffix, and GitLab expands `YC_FULL_IMAGE_NAME` as `${YC_IMAGE_NAME}-${YC_OS_VERSION}`.
5. Packer reads the final name from `YC_FULL_IMAGE_NAME`. The source YC family is supplied separately as `YC_SOURCE_IMAGE_FAMILY=ubuntu-2204-lts`; it is not derived from the display suffix.
6. The output YC image family remains `base-images`, and the created image receives label `role=base`.
7. Before building, CI deletes an existing image with the same full name; after building, it labels that same full name.

## Configuration and diagnostics

- Packer template: `base_image.pkr.hcl`.
- CI pipeline: `.gitlab-ci.yml`.
- Ansible entry playbook: `base_role.yml`.
- Shared role source during CI: cloned `automation-services/roles` via `ANSIBLE_ROLES_PATH`.
- Shared Vault template: `sysadmins/devops-tools/gitlab-ci-templates/.vault_login.yml`; last inspected from `origin/master` at `fb09f3e3be28481d81fe2beaa1111c19a75a84ad` on 2026-09-17. It exports the requested field after OIDC login and leaves `errexit` and `pipefail` enabled.
- YC folder, zone, subnet, service-account key and base image name are supplied by GitLab CI variables; access secrets are not stored in the repository notes.
- Image status can be checked in the Yandex Cloud image list for the configured folder or with `yc compute image list` using the CI service-account context.
- Merge request pipelines run `packer_validate` in the `validate` stage. YC setup is scoped to `image_build.before_script`, so linting does not clone `automation-services`, authenticate to Vault, or configure YC.

## Verification

- `packer fmt -check base_image.pkr.hcl`
- `packer validate -syntax-only base_image.pkr.hcl`
- `packer inspect base_image.pkr.hcl`

The Packer checks were run on 2026-09-17 with the same `packer:1.10.2` container image used by CI.

## Incident: invalid image name on 2026-09-17

- Pipeline `138934`, build job `3153485`, commit `b8a668e635788c27e8c41e21325d8b09a1ec199e` reached Yandex Cloud and completed Vault login, temporary VM creation, SSH, and all Ansible tasks successfully.
- Image creation failed with YC `InvalidArgument: Name: invalid resource name` for `yc-base-image-ubuntu-22.04`.
- Root cause: YC Compute image names allow only lowercase Latin letters, digits, and hyphens; the dot in `22.04` is invalid.
- Packer cleaned up the temporary instance and boot disk; no image artifact was created.
- The preceding validation job `3153484` passed because `packer fmt`, `validate -syntax-only`, and `inspect` do not validate provider-side resource-name constraints.
- Output suffix changed to `ubuntu-22-04`; the human-readable dotted version remains only in `YC_IMAGE_DESCRIPTION`.
- `validate packer` now checks `YC_FULL_IMAGE_NAME` against `^[a-z][a-z0-9-]{1,61}[a-z0-9]$` before running Packer and prints the invalid value plus YC naming requirements on failure.

## Related

- Consumers of this image and the 2026-09-17 overwrite mitigation: `terraform-network.md`, `terraform-prod.md`, `terraform-public-test.md`, `terraform-test-infra.md` in this directory.
- Recipe: [Rebuilt cloud image with the same name makes Terraform plan mass disk and VM replacements](../../../../../general/knowledge/terraform/image-rebuild-forces-disk-replacement.md)
