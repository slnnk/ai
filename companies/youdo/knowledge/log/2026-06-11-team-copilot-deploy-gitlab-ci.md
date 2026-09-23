---
system: team-copilot
status: verified
checked: 2026-06-11
tags: [team-copilot, gitlab-ci, kubernetes, mks-infra, vault-secrets-operator, pvc, storageclass, anthropic]
---
# team-copilot: GitLab CI/CD deploy setup

Date: 2026-06-11
Project: `/home/slnnk/git/team-copilot`
Reference project: `/home/slnnk/git/oncall-bot`

## Task

Configure Docker image build and Kubernetes deploy through GitLab CI analogous to `oncall-bot`.

## Changes

Implemented:

- Extended `.gitlab-ci.yml` from build-only to build + deploy:
  - builds Docker image with Docker-in-Docker;
  - pushes `$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG` and `$CI_REGISTRY_IMAGE:latest`;
  - deploys on Git tags via `bitnami/kubectl`;
  - waits for Vault-synced app secret;
  - applies PVC and deployment;
  - sets deployment container image to the CI image tag;
  - waits for rollout.
- Added Kubernetes manifests under `k8s/`:
  - `namespace.yaml`: namespace `team-copilot`;
  - `vaultstaticsecret.yaml`: app env from `secret/dotnet/team-copilot`, registry pull secret from `secret/admin/gitlab-registry`;
  - `pvc.yaml`: `team-copilot-data`, 2Gi RWO;
  - `deployment.yaml`: single replica, `Recreate` strategy, `/data` mount, `/healthz` readiness/liveness probes, env defaults for `DB_PATH`, `CLAUDE_CONFIG_DIR`, `HEALTH_PORT`.
- Updated `README.md` with GitLab CI/CD and Kubernetes setup notes.

## Context

Required external setup:

- GitLab CI variable `KUBECONFIG` must contain kubeconfig content for the target cluster.
- Vault Secrets Operator must exist in the cluster.
- Vault path `secret/dotnet/team-copilot` must contain required env vars from `.env.example`.
- Vault path `secret/admin/gitlab-registry` must contain Docker registry config for image pulls.

## Actions

Verification:

- YAML syntax parsed successfully with Ruby `YAML.load_stream` for `.gitlab-ci.yml` and all `k8s/*.yaml` manifests.
- `npm run build` could not be completed locally because dependencies were missing.
- Attempted `npm ci`; it failed because npm could not resolve internal Nexus host `msk3-nexus.youdo.corp` from the sandbox (`ENOTFOUND`) and npm exited with `Exit handler never called!`.

Notes:

- A partial ignored `node_modules/` may exist from the failed local `npm ci`; it is not tracked by git.
- Deployment image placeholder is `registry.youdo.sg/youdo/utils/team-copilot:latest`; CI replaces it during deploy with `$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG`.

## Findings

### Deploy check: 2026-06-11

User reported GitLab deploy failure for tag/ref `test-01`: CI waited for `team-copilot-env` and failed with `secrets "team-copilot-env" not found`.

Checked Kubernetes context `admin@mks-infra` (user called it `mks-infra`). Findings:

- Namespace `team-copilot` exists and is Active.
- `VaultStaticSecret/team-copilot-env` exists with `mount: secret`, `path: dotnet/team-copilot`.
- `VaultStaticSecret/gitlab-registry` is Healthy and synced; Kubernetes secret `gitlab-registry` exists.
- Kubernetes secret `team-copilot-env` does not exist.
- `VaultStaticSecret/team-copilot-env` status is Unhealthy / SecretSynced=False.
- Vault error from VSO: `GET http://vault.service.consul:8200/v1/secret/dotnet/team-copilot` returns `403 permission denied`.
- Vault Secrets Operator pod in namespace `vault` is running.
- The namespace has no custom `VaultAuth`; default VSO auth uses Vault role `monitoring`. That role can read `admin/gitlab-registry` but currently cannot read `dotnet/team-copilot`.

Likely fix: update Vault policy/role used by VSO to allow read access to `secret/dotnet/team-copilot`, or create a dedicated Vault role/VaultAuth for `team-copilot` and set `spec.vaultAuthRef` on the app `VaultStaticSecret`.

### Rollout monitoring: 2026-06-11

After Vault policy was fixed, `VaultStaticSecret/team-copilot-env` synced successfully and Kubernetes secret `team-copilot-env` was created with 22 keys.

Deploy initially blocked on PVC:

- `team-copilot-data` was Pending.
- Event: `no persistent volumes available for this claim and no storage class is set`.
- Cluster has StorageClass `fast.ru-2c` and no default storage class.

Fixed local manifest `k8s/pvc.yaml` by adding `storageClassName: fast.ru-2c` and patched the existing Pending PVC in cluster. PVC bound to `pvc-ed753344-5aa2-4321-af4a-c8b40dafce1e`, capacity 2Gi, RWO.

Final state:

- `deployment/team-copilot`: 1/1 Ready, image `registry.youdo.sg/youdo/utils/team-copilot:test-01`.
- `pod/team-copilot-57c575d9d8-n4z5w`: Running, 1/1, 0 restarts, IP `10.10.160.39`, node `mks-infra-node-zy1co`.
- Logs show bot authenticated as `b2b-copilot`, health HTTP listening on port 8080, WebSocket connected to `wss://youdo.loop.ru/api/v4/websocket`, and `ws open`.

### CI rollout timeout follow-up: 2026-06-11

GitLab job failed at `kubectl rollout status --timeout=180s` while rollout was still unavailable. Current cluster state after manual PVC patch is healthy: deployment 1/1, pod Running, 0 restarts. The timeout happened before the PVC fix was reflected in repo and while the initial image pull was still in progress.

Repo updates made:

- `k8s/pvc.yaml`: set `storageClassName: fast.ru-2c`.
- `.gitlab-ci.yml`: increased rollout timeout from `180s` to `600s`.

YAML syntax validated for `.gitlab-ci.yml` and `k8s/pvc.yaml`.

### Image tag format update: 2026-06-11

Changed GitLab CI `IMAGE_TAG` from `$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG` to `$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG-$CI_PIPELINE_IID` so master/tag builds do not overwrite the same branch tag. `latest` is still pushed as a floating alias, while deploy uses the unique `IMAGE_TAG`.

### Latest deploy check: 2026-06-11

Checked latest deployment after image tag format update. Current running image is `registry.youdo.sg/youdo/utils/team-copilot:master-5` with digest `sha256:4ce54f81b514de4354e551ca3335823bc63cec8882683ec4fc27c17baa04a7d6`.

State:

- `deployment/team-copilot`: 1/1 Ready, generation 6 observed, Available=True, Progressing=True.
- Current pod `team-copilot-56d8576bd-f87mw`: Running, Ready=True, 0 restarts, node `mks-infra-node-zy1co`, IP `10.10.160.21`.
- PVC `team-copilot-data`: Bound, 2Gi, StorageClass `fast.ru-2c`.
- `VaultStaticSecret/team-copilot-env`: Healthy=True, SecretSynced=True, path `secret/dotnet/team-copilot`; old 403 events are stale before policy fix.
- Logs show bot authenticated as `b2b-copilot`, health HTTP listening on 8080, Loop websocket opened, and a later `posted` event processed with mention check false.

### Claude endpoint/auth check: 2026-06-11

User asked whether the service has Claude endpoints configured. Checked repo and live pod:

- No explicit Claude/Anthropic URL is hardcoded in app code.
- `src/agent/options.ts` passes `ANTHROPIC_BASE_URL` to the Claude Code subprocess if it exists in `process.env`.
- Kubernetes secret `team-copilot-env` currently does not contain `ANTHROPIC_BASE_URL`; Claude Code uses its defaults.
- From the running pod, `api.anthropic.com` resolves and HTTPS responds with HTTP 403 without auth, so outbound DNS/HTTPS path exists.
- From the running pod, `claude.ai` resolves and redirects to `https://www.anthropic.com/app-unavailable-in-region`.
- App logs show Claude Code failures on real agent runs: `Failed to authenticate. API Error: 403 Request not allowed`.

Conclusion: deployment is healthy, but Claude Code runtime authentication/access is blocked by account/region/endpoint policy, not by Kubernetes readiness. If using an internal Anthropic/Claude proxy, add `ANTHROPIC_BASE_URL` to `secret/dotnet/team-copilot` and restart rollout.

### Anthropic access recheck: 2026-06-11

Checked from running pod `deploy/team-copilot` in namespace `team-copilot`:

- DNS resolves both `api.anthropic.com` and `claude.ai` to `160.79.104.10`.
- `GET https://api.anthropic.com/` returns HTTP 403 with JSON `forbidden / Request not allowed`.
- `POST https://api.anthropic.com/v1/messages` without credentials also returns HTTP 403 `Request not allowed`, not an auth-specific 401/invalid-key response.
- `GET https://claude.ai/` returns HTTP 302 to `https://www.anthropic.com/app-unavailable-in-region`.

Conclusion: TCP/TLS/DNS are working, but Anthropic/Cloudflare is denying requests from this egress path at application/region policy level.

## Open items

- Provide `ANTHROPIC_BASE_URL` (internal proxy) in `secret/dotnet/team-copilot` if the bot must reach Claude from this egress path.

## Portable lesson

- [`~/ai/general/knowledge/k8s/pvc-pending-no-default-storageclass.md`](../../../../general/knowledge/k8s/pvc-pending-no-default-storageclass.md)
- [`~/ai/general/knowledge/k8s/vault-secrets-operator-403-permission-denied.md`](../../../../general/knowledge/k8s/vault-secrets-operator-403-permission-denied.md)
