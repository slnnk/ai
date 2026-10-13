---
system: nomad-test
status: verified
checked: 2026-10-13
tags: [terraform, nomad, vk-cloud, recovery]
---
# DevOps-893 VK test environment copy and first Traefik plan

## Task

Implement the approved DevOps-893 branch locally and prepare the first individually deployed service. User requires copying all of `yandex-test` as-is into separate `vk-test`, changing only necessary target values. Final corrected Consul state path is `terraform/vkcloud-terraform`.

## Context

User approved `DevOps-893-recover-nomad-on-vk` from origin/master in existing `/home/slnnk/git/terraform`. Read-only fetch advanced master to34b581b; clean checkout switched to the approved new branch. User then clarified whole-root copy instead of a reduced bootstrap configuration. Additional preflight was explicitly stopped; no new exhaustive checks added.

## Actions

Copied28 tracked environment files from current master. Changed target suffix/DC to vk-test; backend path as above. Preserved currently active/commented declarations, images and resources except required CSI conversion. Latest master disables multiple jobs/modules previously seen on the old branch; they remain disabled in the copy. Old yandex-test root and shared modules unchanged.

Converted CSI job/resource/plugin identity to plugin-vk-csi-monolith/vk-csi, Cinder image v1.34.1 (previous HEAD availability check), host network for metadata, matching unix socket and Vault-rendered cloud.conf. Target policy vk-csi and secret/vk/csi field cloud_conf are required when that service is deployed. No cloud credentials provisioned; compatibility not yet exercised.

Ran Terraform init with existing mirror and providers, using VK_TEST_* credentials only through subprocess environment. Backend initialized successfully; provider lock generated for linux_amd64. Validate failed inside sandbox because provider local sockets were blocked; elevated validate passed with inherited deprecated hcl2.enabled warnings. Traefik Nomad job validation passed with inherited task-network deprecation warning. Saved targeted Terraform plan:1add/0change/0destroy, only nomad_job.traefik2, job traefik2-service, default namespace,3 allocations, traefik:v2.9.8, ports80/8080,500CPU/1000MiB per allocation.

## Findings

25 of28 copied files differ only by target-address/DC substitution. Other differences are main.tf (backend path and HCL formatting), nomad.tf (CSI resource identity), and jobs/csi-plugin.hcl (driver/auth conversion). No yandex-test suffix remains in the target source. Yandex S3 endpoint remains because existing buckets are reachable and is not an environment-suffix replacement.

Plan saved at `~/ai-data/nomad-vk-access/traefik.tfplan`. CLI helper `terraform_stage.py` supports init/validate/targeted plan/apply, sources only VK_TEST_* and uses NOMAD_TOKEN/CONSUL_HTTP_TOKEN environment. Apply phase executes that saved plan; NOT executed yet. No source credentials written.

## Changes

User corrections October13: exclude unused test16/test17 from vk-test/nomad.tf Redis stand list; delete nomad_job.redis-autotest and copied vk-test/jobs/redis-autotest.hcl. These are explicit task exceptions to the as-is environment copy; original yandex-test unchanged. Regenerated Redis-only saved plan1add/0change/0destroy and inspected task groups redis0–redis15 (16 allocations,16GiB reservation). No Redis apply or deletions in runtime occurred; Redis-autotest was never deployed in VK.

User requested explicit Traefik map details after deployment. Expanded current/service-addresses.env with observation date, image/job/namespace, health routes, node names and direct HTTP/dashboard URLs for each of the three instances. Removed an obsolete comment claiming Traefik addresses were unknown. Used existing deployment/health evidence; no extra remote checks performed.

Created vk-test root28 files and .terraform.lock.hcl. No edits to old root, CI, shared modules or production configs. No git add/commit/push/MR creation. Branch approval and corrected final naming recorded here and in the deployment plan.

## Status and risks

User explicitly approved Traefik apply with `Примени` on October13. Executed saved plan through terraform_stage.py apply; completed1add/0change/0destroy. GET verification: all3 allocations/tasks running, Consul proxy and proxy-ui checks passing on10.18.26.30/.10/.21, ports80/8080. State ownership recorded at approved terraform/vkcloud-terraform. No runtime corrections were needed. Next Redis-only plan prepared separately, not applied; approval pending. The previous pending-Traefik paragraph below is historical and superseded by this result.

Traefik apply awaits explicit external-action approval. Planned command from target root: `terraform apply -input=false /home/slnnk/ai-data/nomad-vk-access/traefik.tfplan`, via environment-only credential helper. It creates the first Nomad job and persists ownership in Consul state terraform/vkcloud-terraform. Plan is intentionally targeted for the user-requested individual recovery, not full environment convergence. Later service deployment and diagnosed errors will be handled individually. CSI needs new Vault secret/policy before its own apply.

## Portable lesson

none
