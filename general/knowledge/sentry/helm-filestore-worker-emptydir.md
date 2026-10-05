---
system: sentry
status: verified
checked: 2026-10-02
tags: [sentry, helm, kubernetes, sourcemaps]
---
# Sentry Helm: artifact assemble fails with filesystem filestore

## Summary
With the `sentry-kubernetes/charts` chart and `filestore.backend: filesystem`, sourcemap and debug-file uploads never assemble: the PVC is mounted only into web, workers get `emptyDir`. Fix by moving filestore to S3 (or GCS).

## Symptom
- `sentry-cli sourcemaps upload`: chunk upload 200, `POST .../artifactbundle/assemble/` returns `{"state":"created","missingChunks":[]}`, polling returns `{"state":"error","detail":"internal server error"}`; reproducible with a two-file probe.
- No artifact bundles in the project; minified stack traces. `@sentry/vite-plugin` does not poll assemble and logs upload errors, so builds stay green.

## Cause
Chart default `filestore.filesystem.persistence.persistentWorkers: false`: the PVC (`/var/lib/sentry/files`) is mounted only into `sentry-web`; `sentry-worker`, cron and consumers get an `emptyDir` at the same path. Web stores chunks on the PVC, `assemble_artifacts` runs in the worker and cannot read them. Check: compare `.spec.template.spec.volumes` of the web and worker deployments.

## Fix
- Preferred: `filestore.backend: s3` with `filestore.s3.{existingSecret, accessKeyIdRef, secretAccessKeyRef, bucketName, endpointUrl, region_name, addressing_style}`. Settings are global: they go into the shared config and the chart injects `S3_ACCESS_KEY_ID`/`S3_SECRET_ACCESS_KEY` into every Sentry pod.
- Alternative: `persistentWorkers: true` — the claim is then mounted into ~30 deployments; with a ReadWriteOnce volume all of them must run on one node (Multi-Attach otherwise), so it needs ReadWriteMany storage.
- Verify read-only: `sentry exec -c "from sentry.models.files.utils import get_storage; s=get_storage(); print(type(s).__name__, s.exists('x'))"` inside a worker pod.

## Limits
- Switching backend drops the PVC from the release (`pvc.yaml` renders only for `filesystem`, no keep policy): Helm deletes it. Check what is stored first: `SELECT type, count(*), sum(size) FROM sentry_file GROUP BY type;`.
- Every `config.yml` change restarts almost all Sentry pods; the post-upgrade `kafka-provisioning` hook can keep the release `pending-upgrade` for 10+ minutes.
- Checked on chart 27.6.2 / Sentry 25.9.0.
