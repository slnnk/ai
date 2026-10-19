---
system: gitlab-ci
status: verified
checked: 2026-10-16
tags: [gitlab-ci, nomad, variables]
---
# Prevent inherited CI variables from redirecting deployments

## Symptom

A deployment selects the intended Nomad datacenter but registers in another cluster and cannot find eligible nodes. The job YAML declares the intended address/token, yet the CLI uses a different endpoint.

## Cause

GitLab project/group CI variables take precedence over job-level YAML variables. Inherited generic NOMAD_ADDR/NOMAD_TOKEN can therefore override values declared in a deployment job. Successful YAML validation and job rendering do not verify the effective runtime endpoint.

## Fix

Inspect effective project, ancestor-group and pipeline variable metadata before publishing target changes. Keep token values out of output. Pass the reviewed target explicitly to the CLI using purpose-specific source variables:

```sh
nomad job run -address="$TARGET_NOMAD_ADDR" -token="$TARGET_NOMAD_TOKEN" job.nomad
```

Remove misleading shadowed job-level declarations. Preserve unrelated environment jobs. Test command expansion with intentionally wrong generic inherited NOMAD_ADDR/TOKEN and placeholder credentials; require the intended explicit address/token arguments. This tests precedence without making a deployment request.

## Limits

Purpose-specific variables also need effective-scope and inheritance checks. Use masked credentials and avoid shell tracing that exposes secrets. Explicit CLI arguments do not validate ACLs, connectivity, routing or application health. If a wrong-target job was already registered, inspect its version/history/allocations before proposing cleanup; do not assume deleting it is harmless or authorized.
