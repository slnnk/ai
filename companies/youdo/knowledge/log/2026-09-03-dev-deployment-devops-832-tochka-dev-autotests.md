---
system: dev-deployment
status: hypothesis
checked: 2026-09-03
tags: [devops-832, tochka, autotests, plan, gitlab-ci-templates, target-env-suffix]
---
# DevOps-832: Tochka post-deploy autotests plan

Date: 2026-09-03

This is a plan (`status: hypothesis`); the "Current status" section below records which parts were later runtime-proven. Runtime evidence lives in `2026-09-03-dev-deployment-devops-832-tochka-dev-autotests-prepared.md` and `~/ai/current/knowledge/systems/dev-deployment/post-deploy-autotests.md`.

## Current status and remaining work (updated 2026-09-04)

The original implementation phases below are retained as the design history. The Tochka pilot itself is now runtime-proven. All three `DevOps-832-dev-autotests` branches are pushed and clean:

- `gitlab-ci-templates` at `34b63d6` (`fix smoke autostart`);
- `youdo-business-tochka-proxy-tests` at `02dcaea` (`prepare tests for dev env`);
- `youdo-business-tochka-proxy` at `8090532` (`increase memory limits`).

Verified end-to-end result:

- pipeline `137961`, successful deploy retry job `3112466`, Jenkins build 153;
- deploy automatically played `smoke tests` job `3112464` after Jenkins success;
- smoke passed operationally with 603 JUnit cases: 587 passed, 16 skipped, 0 failed/errors;
- `regression tests` job `3112465` exists and remains manual;
- all four Tochka workloads use 512Mi memory requests and 1Gi limits and completed smoke with zero restarts/OOM;
- `TARGET_ENV_SUFFIX=-devops-832`, namespace ownership validation, deploy artifact transfer, Allure/JUnit publication, and the renamed job lookup are runtime-proven.

### Remaining plan

1. **Completed in source:** Jenkins rollout post-check race fix is merged to `jenkins-pipelines/master` as `20b9d78`. Runtime proof moves to the next service onboarding run.
2. **Completed in source:** doc-generator MR 34 is merged to `master` through `bdee550d` and sets API to 512Mi request / 1Gi limit.
3. **Completed in source:** `youdo.business` MR 3738 is merged to `master` through `b7d1df43` and sets automation-web to 512Mi request / 1Gi limit. This intentionally becomes the value to validate, despite the older live patch being 896Mi/1280Mi.
4. **Completed for the original environment:** manual Tochka regression job `3112465` succeeded. It predates the memory merges and is not their runtime proof.
5. **Prepare every selected autotest integration before coordinated merge:** Billing routing/autostart is runtime-proven by pipeline `137991` / Jenkins `155` / smoke `3114321`, but regression `3114322` caused a Billing webapp OOM at 256Mi and 532 imported 502 failures. Raise Billing to an initial 512Mi request / 1Gi limit and rerun regression. Continue preparing TKB, main `youdo-business`, and other approved integrations on feature branches without piecemeal merge of the shared rollout.
6. **Infrastructure verification status:** Billing build 155 confirmed the full catalog consumes both new master memory settings and all current pods had zero restarts/OOM after smoke. Billing does not exercise doc-generator or automation endpoints, so their values lack relevant load proof. Jenkins `20b9d78` was loaded and its checks passed, but the fresh namespace did not produce an old ReplicaSet deletion; prove that exact race on a repeat deploy.
7. **Merge the completed autotest rollout together:** merge test-project changes, shared templates, and service includes/configuration in dependency order; replace temporary template feature refs with `master`.
8. **Final closeout:** run representative end-to-end deployments, confirm automatic smoke/manual regression and Allure/JUnit, verify safe namespace cleanup, then update DevOps-A-50 and the authoritative map.

Known non-blocking observations retained for ownership:

- the test image receives `TEST_GROUP=smoke`, but QA code historically hard-codes the `regress` tag; do not change under this DevOps task;
- Gradle `ignoreFailures=true`, credential fallback, and the unrelated retry probe remain QA-owned;
- `allow_failure: true` must remain until QA makes the suite a reliable gate.

## Scope and working branches

At the start of the work, all three clean local feature branches were named `DevOps-832-dev-autotests` and pointed at their respective `master` revisions:

- `/home/slnnk/git/gitlab-ci-templates` at `7ddb881`;
- `/home/slnnk/git/youdo-business-tochka-proxy-tests` at `e586a46`;
- `/home/slnnk/git/youdo-business-tochka-proxy` at `2b08e1e`.

The pilot keeps the existing Nomad `autotest` jobs and the QA-owned test behaviour intact and adds dedicated Kubernetes `smoke tests` and `regression tests` jobs in the new `autotests-dev` stage. `youdo.business` MR 3567 is already merged to `master` as `a4f80388`, so Tochka may select it as a normal dependency.

## Explicit scope boundary

The only product-test repository change in DevOps-832 is support for Kubernetes target addressing through `TARGET_ENV_SUFFIX`, with full backward compatibility for `TARGET_HOST`. The existing JUnit tag selection, Gradle `ignoreFailures`, hard-coded token fallback, retry implementation, test cases, and report semantics belong to QA and are not changed or treated as blockers for this infrastructure pilot. Because of those known limitations, the new job remains `allow_failure: true` and its result is operational evidence that the existing suite ran, not a certified deployment gate.

## Phase 1 — Add the Kubernetes address mode

Repository: `youdo-business-tochka-proxy-tests`.

1. Introduce two explicit target modes:
   - Kubernetes: `TARGET_ENV_SUFFIX=-<deploy-id>`;
   - legacy Nomad: existing `TARGET_HOST=testN`.
2. Make the smallest localized change to the current endpoint construction. Kubernetes mode must produce:
   - `http://youdo-business-tochka-proxy-mock-webapp${TARGET_ENV_SUFFIX}.dev.youdo.corp`;
   - `http://youdo-business-tochka-proxy-mock-worker${TARGET_ENV_SUFFIX}.dev.youdo.corp`;
   - `https://b2bautomation${TARGET_ENV_SUFFIX}.dev.youdo.sg`.
   Kubernetes mode takes precedence when `TARGET_ENV_SUFFIX` exists; otherwise the current `TARGET_HOST` construction remains byte-for-byte compatible.
3. Add focused tests only for endpoint construction and mode precedence; do not alter test selection or execution semantics.
4. Build the Docker image locally where possible. Push the branch and let its pipeline publish the branch-specific tag `devops-832-dev-autotests`; use that tag for the service pilot instead of `latest`.

## Phase 2 — Add shared dev-autotest orchestration

Repository: `gitlab-ci-templates`.

1. In `v3/.main.yml`, add stage `autotests-dev` immediately after the existing `autotest` stage and before `deploy-prod`. Do not rename or alter the legacy stage.
2. Reuse the existing `AUTOTESTS`, `AUTOTESTS_IMAGE`, `AUTOTESTS_IMAGE_REPO`, and `AUTOTESTS_IMAGE_TAG` contract. Inclusion of `v3/.autotests-dev.yml` is the opt-in; no parallel set of dev variables is needed.
3. Reuse the existing MR autotest rule; the new job exists only in projects that explicitly include its template.
4. Create `v3/.autotests-dev.yml` with a reusable hidden job based on the existing Docker-in-Docker test/report/upload flow. Add:
   - `stage: autotests-dev`;
   - artifact `dependencies` on `1 deploy dev` (stage ordering provides execution ordering);
   - the same resource group as deploy/update/delete;
   - `TARGET_ENV_SUFFIX` derived strictly from validated `DEV_NAMESPACE`;
   - verification that namespace labels `createdBy`, `environment`, and `jenkinsJobId` still match `JENKINS_BUILD_NUMBER` before tests start;
   - a Docker-run invocation of the pinned `kubectl:1.34.0` image for namespace verification, avoiding a new combined CI image in the pilot;
   - reuse of the existing report/JUnit publication behaviour without changing it;
   - logging of namespace, Jenkins build URL, image tag/digest, and target suffix.
5. Define `smoke tests` and `regression tests`. Smoke is auto-played after a successful deploy, regression remains manual, and both remain `allow_failure: true`; DevOps-832 does not certify which JUnit tags the QA project actually selects internally.
6. Extend the end of `1 deploy dev`: when the existing `AUTOTESTS=true`, enumerate all pages of manual jobs in the current pipeline and play the job named `smoke tests` when exactly one exists. Zero matches means the optional dev template is not included and is a no-op; multiple matches are an error. The call happens after `deploy-dev.env` is created; stage ordering and `dependencies` make deploy artifacts available. Reuse the existing protected `AUTOTESTS_GITLAB_TOKEN` only for GitLab API access.
7. Add shell-level contract tests for namespace/suffix validation, job lookup cardinality, and failure responses. Lint all modified YAML and validate the composed service configuration through GitLab CI Lint after the feature branch is pushed.

## Phase 3 — Expose the required Tochka worker and opt in

Repository: `youdo-business-tochka-proxy`.

1. In `devops/dev.yml`, enable a ClusterIP Service for `mock-worker` and add only an internal ingress based on `youdo-business-tochka-proxy-mock-worker.dev.youdo.corp`. Add `/_/heartbeat` probes if a rendered/runtime check confirms that endpoint on the worker.
2. Do not add a public `.dev.youdo.sg` worker route. Confirm the public nginx cannot route the worker hostname.
3. Point the shared includes temporarily at `gitlab-ci-templates/DevOps-832-dev-autotests` and include `v3/.autotests-dev.yml`.
4. Set the existing `AUTOTESTS_IMAGE_TAG=devops-832-dev-autotests` for the pilot pipeline. The same backward-compatible branch image is used by both the legacy manual jobs and the new dev job.
5. Render/lint the Tochka values against `helm-charts/master` and check that the generated worker Service/Ingress names remain within Kubernetes limits.

## Phase 4 — End-to-end pilot

1. Push template and test-image branches first, then push the Tochka service branch so all referenced artifacts exist.
2. Confirm the MR pipeline contains the unchanged legacy `autotest` matrix plus the new `autotests-dev` stage with exactly two dev jobs: `smoke tests` and `regression tests`.
3. Start `1 deploy dev` manually. Verify Jenkins deploys Tochka as primary using `youdo.business/master`, returns `DEV_NAMESPACE`/build metadata, and auto-plays exactly one `smoke tests` job while regression remains manual.
4. In the smoke trace verify:
   - namespace ownership matches the Jenkins build;
   - suffix came from that namespace;
   - all three endpoints are task-specific and contain no `.yandex-test.youdo.local` host;
   - mock webapp, mock worker, and automation-web preflight successfully;
   - the existing test container completed and its existing Allure/JUnit outputs were processed normally.
5. Repeat deploy for the same task and confirm deploy/test/delete serialization and stale-build rejection.
6. Delete the namespace and verify namespace, releases, PVC/PV, and environment state are cleaned up.

## Phase 5 — Merge and stabilize

1. Merge in dependency order: test project, shared templates, then Tochka service.
2. After the template merge, remove the temporary feature `ref` from the Tochka include and validate against `master`.
3. Keep the job `allow_failure: true` until QA separately fixes and owns its tag selection, exit-code, credential, and retry semantics; changing gate policy is outside DevOps-832.
4. Update DevOps-A-50 and the global dev-deployment map with pipeline/job/Jenkins identifiers, image digest, endpoint proof, and any known flakes.

## Acceptance criteria

- Existing Nomad smoke/regression jobs still accept `TARGET_HOST` and are unchanged operationally.
- Manual `1 deploy dev` starts exactly one Tochka dev smoke job after a successful Jenkins deployment.
- The dev job tests the exact namespace/build exported by deploy and cannot race update/delete jobs for the same resource group.
- No old Nomad hostname is used in Kubernetes mode.
- The mock worker is reachable only through the internal task-specific route, not public nginx.
- No test-selection, exit-code, credential, retry, or test-case behaviour is changed by DevOps-832.

## Portable lesson

none
