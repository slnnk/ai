---
system: youtrack
status: verified
checked: 2026-10-11
tags: [youtrack, api, knowledge-base, articles, access]
---
# YouTrack YouDo: access to the API and the knowledge base

Last checked: 2026-10-11 (Europe/Moscow).

## Access

- YouTrack: `https://youtrack.youdo.com/youtrack`.
- REST API: `https://youtrack.youdo.com/youtrack/api`.
- The token is stored only in `~/ai/current/.env`, variable `YOUTRACK_TOKEN`.
- API authorization: `Authorization: Bearer $YOUTRACK_TOKEN`.

## Verified article

- Article: `DevOps-A-50`, title `Dev deployment`.
- URL: `https://youtrack.youdo.com/youtrack/articles/DevOps-A-50/Dev-deployment`.
- API resource: `/api/articles/DevOps-A-50`.
- 2026-08-25: reading (`GET`, HTTP 200) and editing (`POST`, HTTP 200) with the token from `YOUTRACK_TOKEN` were confirmed.
- The write check was a no-op: unchanged `summary` and `content` were sent to the API; the `updated` timestamp did not change (`1787660623871`), no actual changes to the article occurred.
- 2026-08-30: reading the article through the API was confirmed again. The article is marked as current as of 2026-08-28 and contains the same continuation plan as the authoritative map `~/ai/current/knowledge/systems/dev-deployment/overview.md` (formerly `knowledge/dev-deployment.md`); no write to YouTrack was performed.
- 2026-09-01: the article was updated after the rollout was completed: added the fresh full-catalog build `145` / GitLab job `3100718`, the ingress report Jenkins build `147` / GitLab job `3103126` / Environment `456`, the merge of the public nginx routing, and the HTTPS/readiness smoke results of all seven `.dev.youdo.sg` hosts. The old rollout plan was replaced with the current hardening/operations backlog. POST and the subsequent GET succeeded; the saved `updated` timestamp is `1788214721108`.

## Safe basic check

For reading, request only the necessary fields, for example `id,idReadable,summary,updated`. Before updating, fetch the current `content` so as not to overwrite parallel changes. Do not print the token value to the console and do not copy it into Markdown or scripts.

## Recovery access verification (2026-10-11)

- The user reported YouTrack was restored. Existing `YOUTRACK_TOKEN` returns HTTP200 from `GET /api/users/me`, login `a.solonenko`, ID `25-546`; no tooling-token rotation/loss is established.
- `GET /api/admin/integrations/vcsHostingProcessors` returns HTTP200 and 14 integrations. Automation-services integration `230-3` is enabled, server `155-1` (`GitLabServer`), Site project `66-0`.
- GitLab hook-specific credentials may differ from the tooling token. Historical hook 72 HTTP401 therefore does not prove the working API token changed. After explicit approval ("Да, отправить тест #109"), one GitLab hook 109 Push-test POST returned HTTP201. Database delivery log confirms HTTP204 at `2026-10-11T15:45:58.390632Z`, duration `0.052193`; prior entry also HTTP204 at `15:45:43.857373Z`. Hook `recent_failures=0`, `disabled_until=NULL`. Current webhook delivery/authentication works after recovery; issue updates and linkage were not verified end to end. Historical hook 56 HTTP404 and hook 72 HTTP401 remain legacy-cleanup findings.
- Related evidence: [GitLab recovery audit](../log/2026-10-11-gitlab-restored-server-verification.md).
