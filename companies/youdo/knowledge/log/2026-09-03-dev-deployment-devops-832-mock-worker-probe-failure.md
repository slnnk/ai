---
system: dev-deployment
status: verified
checked: 2026-09-03
tags: [devops-832, tochka, mock-worker, probes, tcp-probe, hangfire, dev-devops-832]
---
# DevOps-832: mock-worker probe blocks dev deployment

Date: 2026-09-03  
Namespace: `dev-devops-832`  
Service: `youdo-business-tochka-proxy`  
Scope: read-only Kubernetes diagnosis; no cluster changes made.

## Findings

The full catalog was deployed and all observed workloads were healthy except `youdo-business-tochka-proxy-devops-832-mock-worker`. The pod remained `Running` but `0/1 Ready`, accumulated four restarts during the initial check, and prevented the Tochka Deployment from becoming available.

Kubernetes events show both liveness and readiness probes returning HTTP 404 from `/_/heartbeat`. Kubelet repeatedly killed the otherwise successfully started worker; the resulting exit code 137 was probe-driven termination, not evidence of OOM. Application logs showed successful PostgreSQL/Hangfire initialization and RabbitMQ bus startup.

A direct request from an existing pod to the worker pod IP confirmed:

- `GET /_/heartbeat` → HTTP 404;
- `GET /_/hangfire` → HTTP 200.

The internal ingress returned 503 because the Service had no Ready endpoints while the readiness probe was failing.

Cause: the local DevOps-832 `devops/dev.yml` change enabled HTTP liveness/readiness probes at `/_/heartbeat` without runtime confirmation. The worker exposes its Hangfire/job-trigger HTTP server but does not map that heartbeat route in the deployed image.

Do not use the Hangfire dashboard as a health probe. The minimal infrastructure correction is to replace the worker HTTP probes with TCP probes on its existing port. TCP probes retain rollout readiness evidence that the listener is accepting connections without requiring product-code changes.

## Changes

The local `youdo-business-tochka-proxy/devops/dev.yml` was corrected on 2026-09-03: both mock-worker probes now use `type: tcp`. `helm lint` passed and the rendered Deployment contains `tcpSocket.port: 8080` for liveness and readiness.

## Open items

The source change is not yet applied to the running namespace; push it and repeat the deployment.

No secret values were recorded.

## Portable lesson

none
