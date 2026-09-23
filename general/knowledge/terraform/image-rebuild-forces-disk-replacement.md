---
system: terraform
status: verified
checked: 2026-09-17
tags: [terraform, image, boot-disk, ignore_changes, instance-group, replacement]
---
# Rebuilt cloud image with the same name makes Terraform plan mass disk and VM replacements

## Symptom

A plan that should contain a handful of changes suddenly reports dozens of replacements, for
example `30 to add, 15 to change, 37 to destroy`. Every replaced boot disk shows
`image_id = "<old-id>" -> null` (or `-> "<new-id>"`) and every dependent VM is replaced because
its boot-disk ID changes. Nothing in the repository diff explains it, and the image data source
still resolves without error.

If an instance group is involved, `terraform apply` can also fail with the cloud API rejecting the
new instance template because it still references the deleted old image ID.

## Cause

Boot disks were created from a shared base image referenced by a hard-coded image ID (or by a data
source that was later replaced). Somebody rebuilt the base image under the same human-readable
name, which deletes the old image object and creates a new one with a new ID. Terraform state still
holds the old ID, the configuration now resolves the new ID, and `image_id` on a disk is a
force-new attribute, so every disk built from that image is scheduled for replacement.

Additional trap: a `plan` refreshes only in memory. If the state's `terraform_version` marker or
serial changed between two CI plans with no matching repository diff, someone ran an apply-like
command out of band. Do not try to "fix" this by applying the replacement plan.

## Fix

1. Look the image up by a stable name in the owning folder instead of by ID:

   ```hcl
   data "yandex_compute_image" "ubuntu" {
     name      = "base-image-ubuntu-22-04"
     folder_id = var.folder_id
   }
   ```

   (Same idea for other providers: filter by name/tag, not by the immutable ID.)

2. Tell Terraform that the image of an existing disk is immutable for its lifetime:

   ```hcl
   resource "yandex_compute_disk" "boot" {
     image_id = data.yandex_compute_image.ubuntu.id
     lifecycle {
       ignore_changes = [image_id, snapshot_id]
     }
   }
   ```

   For an instance whose boot disk is declared inline, ignore the nested path instead:
   `ignore_changes = [boot_disk[0].initialize_params[0].image_id]`.
   For an instance group template:
   `ignore_changes = [instance_template[0].boot_disk[0].initialize_params[0].image_id]`.

3. Re-plan with `-refresh=false -lock=false -detailed-exitcode` first and confirm the replacements
   are gone, then run a normal refresh-enabled plan.

Newly created disks still take the current image; existing disks keep the one they were built from.

## Limits

- The ignore rule deliberately blocks automatic re-imaging. To move an existing machine to a newer
  base image, remove the rule temporarily or recreate the machine in a controlled way.
- For instance groups the ignore hides the stale image ID but does not repair the live template.
  Any *other* template change (for example metadata/`user-data`) still submits a new template, and
  the API validates the retained deleted image ID and fails. Either also ignore that changing
  attribute until a controlled rolling migration, or migrate the group to the new image on purpose.
  Pure `fixed_scale.size` reductions only touch `scale_policy` and are usually safe.
- Prevent the root cause: the image build pipeline should not overwrite an image that live disks
  depend on; publish versioned images and switch the name/family pointer instead.
- Checked with Terraform 1.7.x/1.9.x and the Yandex Cloud provider 0.127-0.136; the mechanism is
  provider-agnostic.
