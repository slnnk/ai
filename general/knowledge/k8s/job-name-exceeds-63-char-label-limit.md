---
system: k8s
status: verified
checked: 2026-08-30
tags: [kubernetes, job, labels, 63-characters, helm, naming, migrations]
---
# Kubernetes Job rejected: `spec.template.labels ... must be no more than 63 characters`

## Symptom

`helm install`/`kubectl apply` of a Job fails validation although the Job **name** is a legal
DNS subdomain (names may be up to 253 characters):

```text
Job.batch "<name>" is invalid: spec.template.labels: Invalid value: "<name>": must be no more than 63 characters
```

Typical trigger: Helm-generated migration hooks named `<release>-migration-<hook>` where the
release name already embeds a long task/branch identifier.

## Cause

The Job controller copies the Job name into the pod template labels
`job-name` / `batch.kubernetes.io/job-name` (unless you set them yourself). Label **values**
are limited to 63 characters, so any Job name longer than 63 characters fails even though
the name field itself would accept it. The error surfaces at admission, so `--atomic`
installs roll back and leave hook resources behind.

## Fix

Guarantee Job names of at most 63 characters, deterministically and without collisions:

1. Shorten the fixed suffixes. Encode the hook kind compactly instead of repeating words
   (`-mpre`, `-mpost`, `-mpre-mock`, `-mpost-mock` instead of
   `-migration-pre-migrations-mock`). Keep the human-readable original in a separate label
   (for example `migration-name`).
2. Add a guard for the remaining cases. Plain `trunc 63` is unsafe because different hooks
   can collide after truncation; keep a readable prefix and append a hash of the full name:

   ```gotemplate
   {{- define "job.name" -}}
   {{- $full := printf "%s-%s" .release .hook -}}
   {{- if gt (len $full) 63 -}}
   {{- printf "%s-%s" (trunc 54 $full | trimSuffix "-") (sha256sum $full | trunc 8) -}}
   {{- else -}}{{ $full }}{{- end -}}
   {{- end -}}
   ```

3. Add a chart test that renders the real values and asserts every Job name length and
   uniqueness at the boundary (`tests/migration-job-names.sh` style: `helm template ... |
   yq '.metadata.name'` and `awk 'length>63'`).

## Limits

- The same 63-character rule applies to anything copied into labels: StatefulSet
  `controller-revision-hash`, Service names used as label selectors, etc.
- If the release name is derived from branch names, cap the derived identifier (for example
  59 characters for a `dev-` prefixed namespace) at generation time as well.
- Verified on Kubernetes 1.34 API server; the rule is old and applies to all versions.
