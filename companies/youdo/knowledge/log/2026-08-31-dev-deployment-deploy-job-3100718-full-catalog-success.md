---
system: dev-deployment
status: verified
checked: 2026-08-31
tags: [jenkins, gitlab-ci, full-catalog, build-145, build-147, ingress-report, dns, dev-devops-689]
---
# Dev deployment: successful fresh 13-service run

Date: 2026-08-31  
System: B2B ephemeral dev deployment  
GitLab job: `3100718`, pipeline `137654`, project `423` (`youdo.business`)  
Jenkins build: `test/145`  
Namespace: `dev-devops-689`

## Findings

### Result

GitLab job `1 deploy dev` and Jenkins build `145` completed with `SUCCESS`. The primary service was resolved from GitLab project ID `423` to canonical Jenkins service name `youdo-business`. Jenkins used `jenkins-pipelines` revision `2eafc2ee` and the published `helm-charts/master` migration-name correction `4ab8743`.

The run installed all 13 catalog releases into a freshly recreated namespace:

- `youdo-business`
- `youdo-business-auth-service`
- `youdo-business-billing-service`
- `youdo-business-doc-generator`
- `youdo-business-landings`
- `youdo-business-mobile-id`
- `youdo-business-tkb-proxy`
- `youdo-business-tochka-proxy`
- `youdo-kitcut`
- `youdo-notifications`
- `youdo-sms-service`
- `docvalidation`
- `fns`

The primary used MR `3567` / pipeline `137654`, commit `83b2e24f`. All dependencies were selected from `master` and successful image-producing pipelines. Short migration names (`-mpre`, `-mpost`, and mock variants) worked at runtime, including the services that failed in build `142`.

### Runtime verification

At the post-build check:

- all Deployments and PostgreSQL StatefulSets were Ready;
- every application pod was Running with zero restarts;
- all migration pods were Completed;
- no Warning events existed in the namespace;
- all configured readiness endpoints behind `.dev.youdo.corp` ingress returned HTTP 200;
- all seven `.dev.youdo.sg` endpoints returned HTTP 200 when addressed directly through dev Traefik with the correct Host header.

The `youdo-business` worker now requests and limits memory at `512Mi` in both the live Deployment and primary branch `devops/dev.yml`. Its pod remained Ready with zero restarts during verification. This supersedes the former live-only override warning.

### DNS gap

Normal DNS resolution for the generated `*.dev.youdo.sg` hostnames does not reach the dev cluster:

- `.dev.youdo.sg` resolved to public address `178.154.207.53` and returned HTTP 301 to `https://youdo.sg/`;
- `.dev.youdo.corp` and the dev Traefik LoadBalancer use `10.16.26.101`;
- forcing each `.dev.youdo.sg` hostname to `10.16.26.101` returned HTTP 200 on its configured readiness path.

The Kubernetes ingress objects and services therefore work; DNS/routing for task-specific `.dev.youdo.sg` names is the remaining external-access defect. Determine whether split DNS/wildcard DNS should point these names at dev Traefik or whether ephemeral values should use `.dev.youdo.corp`.

### Subsequent manual verification

On 2026-08-31 the operator asked to treat the following manually checked scenarios as successful:

- repeat-deploy preservation of non-primary releases/pods;
- extend and delete cleanup semantics;
- `fns` as primary;
- negative primary-`master` rejection;
- no-task-ID fallback naming and cleanup.

No job/build identifiers were supplied for these checks, so they are operator-reported evidence rather than independently trace-correlated evidence. Actual `auto_stop_in` expiry remains unverified. A later read-only check still found the build-145 namespace present with all 13 revision-1 releases; this describes current retained state and does not negate the separately reported manual lifecycle scenario.

### Ingress reporting runtime proof

Later on 2026-08-31, GitLab pipeline `137718` / job `3103126` triggered Jenkins build `147`. Both completed successfully using published revisions `jenkins-pipelines/master` `8ae44be0` and `gitlab-ci-templates/master` `7ddb8813`.

- Jenkins archived `generated/ingress-urls.txt`, printed it in the console, and rendered 26 clickable ingress links in the build description.
- The artifact contained 26 service/component URLs; seven `*.dev.youdo.sg` addresses used HTTPS and the remaining 19 used HTTP.
- GitLab printed the same report, retained `ingress-urls.txt` and `environment-description.md`, and updated Environment `456` (`dev/devops-689-k8s`) through the Environments API using `CI_JOB_TOKEN`.
- A read-only Environment API check confirmed the full 26-link Markdown description and successful last deployment from job `3103126`.

## Open items

- Resolve DNS/routing for task-specific `.dev.youdo.sg` names (resolved on 2026-09-01 via the public test nginx; see `2026-09-01-dev-deployment-ingress-public-smoke.md`).
- Verify a real `auto_stop_in` expiry.

## Portable lesson

none
