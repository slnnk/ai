---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [nomad, csi, vk-cloud, ssd, DevOps-893]
---
# DevOps-893 VK CSI SSD disk lifecycle verification

## Summary

User requested creation, attachment and deletion of an SSD disk. Full lifecycle passed through vk-csi: ceph-ssd 1 GiB, ext4 mount, 4 MiB write/read with SHA-256 verification, detach and deletion. Cloud and Nomad disk lookup returned 404 afterward; test job removed and allocation complete.

## Context

All eight Cinder CSI nodes/controllers were healthy after the previous deployment correction. Use a temporary default-namespace volume and job named devops-893-csi-ssd-smoke. Credentials loaded in memory from current/.env and secret/admin/vk-csi; no secret values persisted. Current Cinder types: ceph-ssd, ceph-hdd, high-iops, high-iops-ha.

## Actions

- Created local bounded test helper and HCL job under ~/ai-data/nomad-vk-access, outside the Terraform repository. Nomad HCL validation passed; actual runtime verified driver behavior.
- Created CSI volume through PUT /v1/volume/csi/devops-893-csi-ssd-smoke/create with parameters type=ceph-ssd, availability=MS1, requested capacity 1073741824 bytes, ext4 and single-node-writer/file-system capability.
- Cinder confirmed volume d66c4c17-c0c4-48b3-a491-19bf41d69b1d, actual ceph-ssd type and size 1 GiB.
- Started temporary job using redis:6 with a shell I/O task; allocation 86d5de6f-6a2f-9bbe-6164-f36e727bdfe9 on node 46d9c273-4121-6899-d8ba-da8f1aee7615. Mounted /dev/vdb at /data with ext4 rw. Wrote 4 MiB random data, synced, verified SHA-256: /data/probe.bin: OK and CSI_SSD_IO_OK.
- Cinder status in-use with one attachment confirmed cloud-side attachment.
- Stopped/purged only the temporary job. CLI monitor returned nonzero for the cancelled deployment even though the stop succeeded; verified DesiredStatus=stop directly and resumed cleanup. Helper now uses job stop -detach -purge to avoid treating cancelled deployment monitoring as a stop failure.
- Verified Cinder available with attachments=[] and Nomad empty ReadAllocs/WriteAllocs, then DELETE /v1/volume/csi/devops-893-csi-ssd-smoke/delete.
- Verified disk lookup 404 in both cloud and Nomad. Final GET verification: zero test jobs, zero test CSI volumes, allocation ClientStatus=complete.

## Findings

The deployed plugin can provision an SSD, attach it, mount/format ext4, read/write, unpublish and delete it. Use type=ceph-ssd explicitly for SSD workloads; this evidence covers one node and one temporary disk, not a performance benchmark or migration test.

## Changes

No Terraform repository edits, Git publication or permanent cloud disks. Test artifacts: csi_disk_test.py, csi-ssd-smoke.hcl, csi-ssd-smoke-result.json and cinder-volume-types.json under ~/ai-data/nomad-vk-access. Updated existing system map and address-map verification comments; no new network address was introduced.

## References

- https://developer.hashicorp.com/nomad/api-docs/volumes
- https://developer.hashicorp.com/nomad/docs/job-specification/volume
- https://developer.hashicorp.com/nomad/docs/job-specification/volume_mount
- https://github.com/vk-cs/terraform-vkcs-compute
