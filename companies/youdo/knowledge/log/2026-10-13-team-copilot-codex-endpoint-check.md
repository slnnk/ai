---
system: team-copilot
status: verified
checked: 2026-10-13
tags: [kubernetes, codex, dns]
---
# team-copilot: Codex token and endpoint connectivity

## Task

Verify DNS and authenticated OpenAI/Codex requests from `mks-infra` pods.

## Context

Runtime URL follow-up: fetched `origin/master` at `4cb09b8` without switching the clean local `DevOps-802-deploy` checkout (`f306afe`). Live deployment uses image `registry.youdo.sg/youdo/utils/team-copilot:master-9`, `AGENT_PROVIDER=codex`, empty `MODEL`. Runtime dependencies include `@openai/codex: 0.162.1`. Fetched source launches `codex exec --strict-config --skip-git-repo-check --json` (`src/agent/providers/codex.ts:38`), forwards `CODEX_ACCESS_TOKEN` (`src/agent/process-env.ts:11`), and supplies no `base_url` or `model_provider` overrides (`src/agent/providers/codex-config.ts`). URL-only extraction from the latest 500 deployment log lines confirmed `https://api.openai.com/v1/responses`. This establishes the endpoint referenced by the running application; it does not establish why its CLI-selected authorization differs from the working manual Codex-backend call. `.gitlab-ci.yml:108` separately probes `https://chatgpt.com/`, `https://chatgpt.com/cdn-cgi/trace` and `https://auth.openai.com/` for diagnostics.

Context `admin@mks-infra`, namespace `team-copilot`. Deployment references Secret `team-copilot-codex-auth`, key `CODEX_ACCESS_TOKEN`. No `OPENAI_API_KEY` key was present in namespace Secrets. Secret values were never printed or saved.

## Actions

User authorized temporary test pods and authenticated endpoint checks. Used `kubectl --context admin@mks-infra run ... --namespace team-copilot --restart=Never --rm -i`; injected only the required Secret key via `secretKeyRef`. All test pods were deleted after execution.

## Findings

- After the user reported service recovery, repeated the same streaming POST to `api.openai.com/v1/responses` with the current Secret value, `gpt-6.1-sol`, `stream: true`, `store: false` from namespace `team-copilot`. DNS remained `10.255.0.31`; response remained HTTP 401 `rejected_by_access_enforcement` / `no_matching_rule`. Temporary pod `openai-recovery-check` was deleted. This check does not establish whether the application itself recovered; its CLI may supply a different request context.

- Follow-up Secret inspection decoded the value locally in memory and checked for the three-part JWT format. The stored `CODEX_ACCESS_TOKEN` is opaque/non-JWT; `aud` and `scope` cannot be read from a JWT payload. The token was not printed or persisted; no claim values or effective permissions were inferred from its format.

- Pod DNS server: `10.96.0.10`. Latest lookup: `api.openai.com` -> `10.255.0.31`; `chatgpt.com` -> `10.255.0.11`.
- Earlier `chatgpt.com` lookup returned `8.47.69.0` and `8.6.112.0`, and Codex models returned HTTP 403 HTML. Cause of DNS change was not investigated.
- POST `https://api.openai.com/v1/responses` with `CODEX_ACCESS_TOKEN`, model `gpt-4.1-mini`, consistently returned HTTP 401, `rejected_by_access_enforcement`, `no_matching_rule`.
- GET `https://chatgpt.com/backend-api/codex/models?client_version=0.162.1` after the DNS change returned HTTP 200 and ten models, including `gpt-6.1-sol`.
- POST `https://chatgpt.com/backend-api/codex/responses` with the same token, model `gpt-6.1-sol`, `instructions: Reply briefly.`, user text `Reply only: OK`, `stream: true`, `store: false` returned HTTP 200, text `OK`, event `response.completed`, status `completed`; usage 17 input and 5 output tokens.
- The token works on the tested Codex backend routes. The API Platform endpoint rejected it; this alone does not mean it expired. Precise authorization policy behind the API Platform rejection remains unverified.
- Documentation follow-up: https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference explicitly supports `api.openai.com/v1/responses` for the Sign in with ChatGPT plan usage flow, requiring an account-available model, `store: false` and `stream: true`. https://developers.openai.com/siwc/token-sharing-open-source/sign-in specifies `resource: https://api.openai.com/v1` and plan usage scopes `resource.invoke` and `chatgpt.tokens.use.direct`. Therefore the observed rejection does not establish that OAuth tokens are categorically unsupported on the public API. Tests also changed model and streaming; endpoint-only causality is unproven. No announcement of a relevant auth removal was found in the current API/Codex changelogs. Token scopes/audience and an identical-payload comparison were not checked.

## Changes

GET `https://api.openai.com/v1/models` with the same Secret token returned HTTP 401, `type: invalid_request_error`, `code: invalid_api_key`, message `Incorrect API key provided` (credential fragments omitted). DNS `10.255.0.31`. Temporary pod `openai-models-check` was deleted. This verifies rejection by that public catalog endpoint, while the Codex backend accepted the credential; token format/scopes/audience still were not inspected.

Follow-up controlled comparison: POST to `https://api.openai.com/v1/responses` with the exact successful Codex request body (`gpt-6.1-sol`, same instructions/input, `stream: true`, `store: false`) and the same Authorization/Content-Type/Accept headers returned HTTP 401 `rejected_by_access_enforcement` / `no_matching_rule`; DNS `10.255.0.31`. Only URL differed from the successful backend request. This rules out the original model/streaming differences as the sole cause of this failure. Token scopes and remote authorization rules remain unverified. Temporary pod `openai-stream-check` was deleted.

Knowledge log only. No deployment, Secret, repository or persistent cluster configuration changes.

## Risks and limits

Successful inference verifies the tested model and request at this time only. No refresh-token lifecycle or application configuration was examined.

## Portable lesson

none
