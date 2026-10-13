---
system: nexus
status: verified
checked: 2026-10-13
tags: [nexus, pypi, python, recovery, gitlab]
---
# Nexus PyPI recovery plan and data library inventory

## Summary

The user requested a recovery plan and a complete audit of GitLab group `data` for Python libraries. Following explicit approval "Сделай 1", Nexus stage 1 is applied and independently GET-verified: two PyPI stores, hosted/proxy/group repositories, role `nx-pypi` and CI user `pypi`. The user separately updated DNS to `10.18.24.233`; legacy index GET routing at the new IP is verified; default workstation DNS and runner-side access remain to verify. Follow-up restored `youdo-basis==10.0.2` with exact wheel/sdist hashes after approved retry and local fallback; see [execution log](2026-10-13-nexus-pypi-basis-recovery.md). No repository source/lock change was needed.

Python UV base-image build [3222108](https://gitlab.youdo.sg/data/dockers/-/jobs/3222108) succeeded after the user enabled instance runners. The next extraform build [3222248](https://gitlab.youdo.sg/data/extraform/-/jobs/3222248), tag `0.31.17`, fails downloading `youdo-basis==10.0.2` from a locked legacy PyPI URL. At the initial diagnosis, Nexus had no PyPI repositories and workstation DNS resolved `pypi.youdo.local` to former Nexus `10.16.24.23`, whose endpoint timed out. The applied stage and user DNS update below supersede that initial infrastructure state. Runner-side resolution remains unverified.

## Task and context

Nexus was rebuilt without former package blobs. Earlier recovery covered Docker, Maven, NuGet, npm and raw repositories. PyPI is an additional missing ecosystem. This plan extends image recovery tracked in DevOps-891 and the live Nexus recovery backlog; it does not reopen or modify either YouTrack task.

Exact failed artifact URL:
`http://pypi.youdo.local/repository/pypi-private/packages/youdo-basis/10.0.2/youdo_basis-10.0.2-py3-none-any.whl`.
The application uses `uv sync --frozen`; restoring only a new index URL does not replace absolute artifact URLs and hashes already recorded in locks.

## Initial verified Nexus state and proposal (historical)

Read-only REST inventory found no PyPI repositories, PyPI blob stores or dedicated PyPI user/role. Existing anonymous access is enabled. Realms are `NexusAuthenticatingRealm`, `DockerToken`, `NpmToken`; keep these and unrelated repositories/accounts unchanged. Existing Basic authentication supports PyPI; no additional PyPI realm is required.

| Object | Proposed configuration (not applied) |
|---|---|
| Hosted File blob store | `pypi-hosted` |
| Proxy File blob store | `pypi-cache` |
| Hosted repository | `pypi-private`, `pypi-hosted`, strict content validation, `ALLOW_ONCE` |
| Proxy repository | `pypi-proxy`, `pypi-cache`, upstream `https://pypi.org/`, `indexPath=/simple` |
| Group repository | `pypi`, members `pypi-private`, then `pypi-proxy` |
| Consolidated role | `nx-pypi`: PyPI browse/read; add/edit only on `pypi-private` |
| CI identity | Restore user `pypi`, role `nx-pypi`; group `data` CI variable `PYPI_USERNAME=pypi` was GET-verified2026-10-13 (`protected=true`, scope `*`). No username overrides exist in the subgroup or nine publisher projects. Password remains in group `PYPI_PASSWORD`; value not printed or persisted. |

Publish jobs use `PYPI_REPOSITORY`, `PYPI_USERNAME`, `PYPI_PASSWORD`; Makefile equivalents are `YOUDO_PYPI_REPOSITORY`, `YOUDO_PYPI_USERNAME`, `YOUDO_PYPI_PASSWORD`. Keep values in existing GitLab CI/secret storage; do not write them in the plan.

The three repository payloads in `~/ai-data/nexus-pypi-recovery/pypi-plan.json` were checked against the installed Nexus OpenAPI required fields, properties and enums. This validates the proposal structure, not successful creation.

Legacy route source: `automation-services/roles/nginx/templates/vhost/pypi.youdo.local.j2` and `inventories/prod_yandex/group_vars/nexus-prod.yml`. The vhost forwards GET paths unchanged, maps legacy root POST publication to `/repository/pypi-private`, and redirects `/simple/` to `/repository/pypi/simple/`. Restore equivalent routing on the new Nexus and update DNS after approval. An explicit POST `/repository/pypi-private/` must use a dedicated route to avoid the old rule duplicating the prefix. The public `nexus.youdo.com` vhost currently lacks a PyPI location; add one only if the consumer inventory requires it.

## Applied Nexus stage 1 (2026-10-13)

Authorization: the user requested "Сделай 1", covering the proposed Nexus repositories, stores and CI identity. `restore_pypi.py --apply` created File blobs `pypi-hosted`/`pypi-cache`; repositories `pypi-private` (hosted, strict content validation, `ALLOW_ONCE`), `pypi-proxy` (upstream `https://pypi.org/`, `/simple`), and `pypi` (private first, proxy second); role `nx-pypi`; active user `pypi` with that sole role. Its password matches existing group `data` `PYPI_PASSWORD`, accessed at runtime without printing or saving the value. Role grants PyPI browse/read and only `pypi-private` add/edit.

A separate read-only `restore_pypi.py --verify` succeeded: exact repository configs, blob paths, role privileges and user were read back. Valid CI credentials returned HTTP200 for private/group index reads; deliberately invalid credentials returned401. Previous repositories, users and roles were unchanged, as were blob configurations, realms and anonymous access. The first preservation comparison flagged only decreasing `availableSpaceInBytes`, a dynamic storage metric; verification was corrected to exclude only that metric and rerun successfully. This was a verification-helper correction, not a Nexus configuration change.

The user separately supplied `dig pypi.youdo.local @172.28.0.9` at 17:29 MSK: authoritative answer `10.18.24.233`, TTL3600. Independent `dig +short pypi.youdo.local @172.28.0.9` confirmed the new address. Workstation default resolver `127.0.0.53` still returns former `10.16.24.23`, and ordinary HTTP requests time out; stale cache versus upstream resolver is not diagnosed. Forced requests to `10.18.24.233` with `Host: pypi.youdo.local` returned GET `/repository/pypi-private/simple/`200 and `/repository/pypi/simple/`200 (Simple index), while `/simple/` returned301 to `http://pypi.youdo.local/repository/pypi/simple/`. Existing nginx already supports these GET/index routes; no nginx mutation was needed. POST publication mapping was not exercised. Default-DNS propagation, runner-network access, exact missing artifact paths and publication compatibility remain separate work. Upstream package retrieval and missing library bytes have not been verified/restored by stage 1.

## First library restored (2026-10-13)

Approved local publication restored `youdo-basis==10.0.2`; Nexus component metadata confirms exact locked wheel and sdist SHA256. Historical hatchling1.27.0 and uv-dynamic-versioning0.5.0 reproduced both hashes from unchanged release source. Runner171/172 host DNS and indexHTTP200 now verify the new endpoint; image/container verification remains separate. Publication used actual CI repository URL and credentials; no source/lock change. Original publish retry3222818 remained pending after approved project207 shared-runner enablement and was canceled for local fallback. See [basis execution and approvals](2026-10-13-nexus-pypi-basis-recovery.md). Extraform0.31.17 local release image built successfully from actual GitSHA3c04a38b with unchanged lock/Dockerfile; original checkout branch restored clean. Runtime-required registry tag0-31-17 was pushed after approval and independently manifest/config digest-verified; no alias, deployment or cron execution. Subsequent batch restored26of32 versions with artifact-type/hash limits; read-only live inventory found23periodic parents/eightimages among160jobs. See [batch execution](2026-10-13-nexus-pypi-library-batch-recovery.md).

## Library inventory and rebuild order

The recursive GitLab audit covered all **62** projects in `data`, including subgroups and archived projects. **33** projects have Python packaging metadata; this alone does not make them library publishers. **Nine** confirmed PyPI library publishers were found. Classification: 9 publishers, 19 consumers, 4 packaged services/projects, 1 image repository, 2 templates and 27 other projects. Locks and requirements identify **32 distinct exact package versions** plus the equivalent spelling `youdo-basis==3.1` for `3.1.0`; all canonical versions have release tags. This is the minimum observed recovery set, not a claim about every deployed Nomad ref. `data/eventum` is a service, distinct from `data/python-libraries/eventum`. Archived `data/tcesst` and `data/terk` also build service images rather than publishing libraries.

| Publisher | Distribution | Latest observed Git tag | Exact versions required by observed locks/requirements |
|---|---|---|---|
| [data/python-libraries/basis](https://gitlab.youdo.sg/data/python-libraries/basis) | `youdo-basis` | `10.0.2` | `10.0.2`, `2.1.0`, `2.1.2`, `3.0.4`, `3.0.9`, `3.1.0`, `8.1.3` |
| [data/python-libraries/aio-service-client](https://gitlab.youdo.sg/data/python-libraries/aio-service-client) | `youdo-aio-service-client` | `8.0.1` | `2.2.2`, `3.1.1`, `4.1.0`, `6.0.1`, `8.0.1` |
| [data/python-libraries/eventum](https://gitlab.youdo.sg/data/python-libraries/eventum) | `youdo-eventum` | `5.0.1` | `0.0.1`, `1.0.1`, `3.0.4`, `5.0.1` |
| [data/python-libraries/basis-fastapi](https://gitlab.youdo.sg/data/python-libraries/basis-fastapi) | `youdo-basis-fastapi` | `2.1.0` | `0.6.3`, `2.1.0` |
| [data/python-libraries/toster](https://gitlab.youdo.sg/data/python-libraries/toster) | `youdo-toster` | `6.1.1` | `4.1.0`, `4.2.0`, `6.0.0`, `6.1.1` |
| [data/castle](https://gitlab.youdo.sg/data/castle) | `youdo-castle` | `6.0.0` | `1.0.1`, `5.2.0`, `5.2.1` |
| [data/python-libraries/metronom](https://gitlab.youdo.sg/data/python-libraries/metronom) | `youdo-metronom` | `4.0.0-alpha.1` | `3.2.3` |
| [data/python-libraries/basis-aiohttp](https://gitlab.youdo.sg/data/python-libraries/basis-aiohttp) | `youdo-basis-aiohttp` | `7.0.0` | `2.1.1`, `2.2.3`, `2.9.0`, `5.1.1` |
| [data/python-libraries/iss](https://gitlab.youdo.sg/data/python-libraries/iss) | `youdo-iss` | `2.0.0` | `1.0.1`, `2.0.0` |

The observed current internal dependency graph starts with independent libraries `basis`, `aio-service-client`, `toster`, `castle`, `metronom`, `iss`; then `aio-service-client` → `eventum` → `basis-fastapi`, which also depends on `basis`. First restore `basis 10.0.2` for the actual extraform incident. Restore the modern chain `aio-service-client 8.0.1` → `eventum 5.0.1` → `basis-fastapi 2.1.0` after `basis 10.0.2`.

Legacy consumers require a separate version graph, not substitution by the latest packages: `data/budget_estimator` locks `aio-service-client 6.0.1`, `basis 8.1.3`, `eventum 3.0.4`, `basis-fastapi 0.6.3`. `basis-aiohttp 7.0.0` additionally requires the older basis6/eventum3 dependency family. Check each selected release's own lock/dependency constraints before scheduling its build.

`castle 6.0.0` release source contains `[tool.hatch.build] packages = ["basis_fastapi"]`, which is inconsistent with the castle package. This is suspicious build configuration; no rebuild was run to prove a failure. Review package inclusion before publishing; a required source fix needs a separately approved branch/MR.

Exact version-to-consumer mapping and all 62 classifications are in `~/ai-data/nexus-pypi-recovery/data-summary.json`; the actual `extraform 0.31.17` private lock block is in `extraform-0.31.17-private-lock.txt`. Detailed release SHA, source snippets and lock artifact URL/hash records are in `~/ai-data/nexus-pypi-recovery/data-details.json`. The source audit and classification are local generated evidence, not copied package contents.

## Recovery sequence and progress

1. Use the completed group publisher/consumer inventory and its 32 exact package versions: package distribution names, required versions, source tags/SHA, build tools, publication jobs, internal dependency graph, lock URLs/hashes and target endpoints. Audit active Nomad job refs separately before claiming every production-required version is covered.
2. Check original wheels/sdists in backups, retained CI artifacts and package caches before rebuilding. For `youdo-basis 10.0.2`, tag SHA is `0fa692f2624270e69f489a1ad2b065f5ca721dae`; [pipeline116600](https://gitlab.youdo.sg/data/python-libraries/basis/-/pipelines/116600) / publish2254150 has no distribution archive in artifact metadata, only a log. This does not rule out backups or other caches. No packages were downloaded.
3. Completed after explicit approval: two File stores, hosted/proxy/group repositories, CI user `pypi` and role `nx-pypi`; exact settings and authentication verified by independent reads. Unrelated objects, realms and anonymous settings are preserved.
4. DNS changed by the user: `pypi.youdo.local` → `10.18.24.233` according to `dig @172.28.0.9` at 17:29 MSK, TTL3600. New-IP legacy index GET routes are verified without nginx changes. Verify default resolver propagation, POST publication mapping and exact `/repository/pypi-private/packages/...` paths; change routing only if a gap is found and separately approved. Check DNS and index/locked-artifact routing from the actual Docker runner/build network. Restore index browsing and compatible legacy publication URLs before publish-job retries.
5. Restore required exact library versions in internal dependency order from original release tags/SHA. First satisfy `youdo-basis 10.0.2` for extraform. Prefer original artifact republication where hashes are locked; rebuild where originals are unavailable. Before each retry, check that the original job uses compatible runner/image/auth/publication URL. Do not replace old tags or upgrade dependencies implicitly.
6. Compare rebuilt artifacts' SHA256 with hashes in consumer locks before treating a version as recovered. A source-equivalent rebuild can produce different bytes. A mismatch requires an explicitly reviewed lockfile/source change; disabling hash verification is not part of the plan. Historical release/tag consumers need the same decision, not a blind retry of their unchanged source.
7. Verify published names/versions, simple-index links/hashes and HEAD exact locked artifact URLs through Nexus metadata only, without downloading packages. Then, after separate authorization, retry extraform and the dependent image jobs. Rebuild all identified Nomad periodic-job images after their package dependencies are restored; deployments and periodic-job executions remain separate actions.

## Evidence and key commands

Generated data stays outside the KB Git repository in `~/ai-data/nexus-pypi-recovery/`:
- `data-inventory.json`, `data-summary.json`, `data-details.json`: recursive GitLab group inventory, all-project classification, version-to-consumer map and release/lock evidence.
- `nexus-inventory.json`, `nexus-openapi.json`, `pypi-plan.json`: sanitized initial Nexus state, API schema and proposed/applied configuration.
- `nexus-before-pypi-create.json`, `pypi-create-verification.json`: pre-change sanitized snapshot and independently read-back applied configuration/authentication checks.
- `restore_pypi.py --apply` and `restore_pypi.py --verify`: authorized stage-1 apply and subsequent read-only verification; CI secret accessed in memory only.
- `build-failures-291.json`, `base-build-failures.json`: sanitized CI metadata/error excerpts.
- `release-207-10.0.2.json`: original release and artifact metadata.
- Read-only helpers `audit_data.py`, `inspect_nexus.py`, `inspect_base_failure.py`, `inspect_release.py`.

Key reads: `GET /api/v4/groups/data/projects?include_subgroups=true`; recursive `repository/tree`, relevant source files and tags; `GET /api/v4/projects/215/jobs`, `/projects/291/jobs`, `/projects/207/pipelines?ref=10.0.2`; Nexus repository/blob-store/security/realm metadata and live OpenAPI; `getent hosts pypi.youdo.local` and HEAD index endpoint. Tokens stay in `~/ai/current/.env` and process memory.

## Risks and limits

The verified current failure is a legacy-endpoint timeout, not a confirmed package hash mismatch. The latter is a recovery risk inferred from frozen locks and rebuilding. Original distribution bytes may be absent. Default-branch locks do not prove the complete deployed Nomad version set. Proposal payload validation does not verify upstream connectivity or credentials from runners. Remote changes, publication and repository source changes require the user's prescribed approvals.

## References

- [Sonatype PyPI repository configuration](https://help.sonatype.com/en/create-a-pypi-repository.html).
- [Sonatype PyPI clients and authentication](https://help.sonatype.com/en/configure-pypi-with-nexus.html).
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).
- [Previous extraform image diagnosis](2026-10-13-gitlab-extraform-python-uv-runner-disabled.md).

## Changed files

This work log, existing Nexus/GitLab system maps, `~/ai/TODO.md`, generated local audit/proposal artifacts and `~/ai/.sync-notes`. No repository task files changed. The authorized Nexus stage-1 objects were created; the user changed DNS separately. No library publication or CI retry was run.

## Final default DNS checkpoint

The later read-only `default-pypi-dns-final-verification.json` verifies default workstation resolution to10.18.24.233 and ordinary `/simple/` redirect to the PyPI group index with HTTP200, without forced address or package downloads. Earlier stale workstation DNS statements describe the initial stage and are superseded. Actual runner-container resolver behavior and legacy root POST publication mapping remain separate limits.
