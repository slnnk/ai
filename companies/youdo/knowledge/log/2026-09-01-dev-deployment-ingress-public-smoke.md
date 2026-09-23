---
system: dev-deployment
status: verified
checked: 2026-09-01
tags: [ingress, nginx, traefik, dns, public-smoke, youtrack, dev-devops-689, automation-services]
---
# Dev deployment: public ingress smoke and documentation closeout

Date: 2026-09-01 (Europe/Moscow)

## Context

- Environment: `dev-devops-689`, GitLab Environment `456`.
- Public DNS address observed for all task hosts: `178.154.207.53`.
- Dev Traefik comparison address: `10.16.26.101:80`.
- Public nginx change: `automation-services/master` merge `ccd39521`, regexp commit `f18471ca`.

## Findings

All checks used normal public HTTPS resolution and certificate verification. No public request redirected to `youdo.sg`; TLS verification result was zero. Public root response codes exactly matched direct HTTP requests to Traefik with the same `Host` header.

| Host | Public/direct root | Readiness | Result |
| --- | --- | --- | ---: |
| `business-auth-ext-devops-689.dev.youdo.sg` | 404 / 404 | `/_/heartbeat` | 200 |
| `business-auth-int-devops-689.dev.youdo.sg` | 404 / 404 | `/_/heartbeat` | 200 |
| `b2bautomation-devops-689.dev.youdo.sg` | 401 / 401 | `/health` | 200 |
| `business-api-devops-689.dev.youdo.sg` | 404 / 404 | `/health` | 200 |
| `business-devops-689.dev.youdo.sg` | 200 / 200 | `/health` | 200 |
| `employee-devops-689.dev.youdo.sg` | 500 / 500 | `/health` | 200 |
| `s-devops-689.dev.youdo.sg` | 404 / 404 | `/health` | 200 |

The root `401`, `404`, and `500` statuses are application responses because direct Traefik returns the same values. They are not nginx fallback or redirect behavior. Kubernetes showed both auth pods Ready with zero restarts and declared `/_/heartbeat`; the five other externally exposed components use `/health`.

## Changes

Documentation: YouTrack article `DevOps-A-50` (`Dev deployment`) was updated through the API after reading and validating its prior revision. The final GET confirmed the new date, full-catalog evidence, ingress/environment reporting, nginx merge, all seven hosts, and the current hardening plan. Article `updated` timestamp after the write: `1788214721108`.

## Open items

- `employee-devops-689.dev.youdo.sg/` root HTTP 500 is an application response; investigated separately in `2026-09-01-dev-deployment-employee-web-root-500.md`.

## Portable lesson

none
