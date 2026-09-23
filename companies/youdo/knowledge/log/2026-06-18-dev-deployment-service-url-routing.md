---
system: dev-deployment
status: verified
checked: 2026-06-18
tags: [helm-charts, routing, jenkins, dev-yml, youdo-business-auth-service, sentry, environment]
---
# Dev deployment: service URL routing prototype

Date: 2026-06-18
Project: helm-charts / Jenkins ephemeral dev deploy
Repositories:
- /home/slnnk/git/helm-charts
- /home/slnnk/git/youdo-business-auth-service
- /home/slnnk/git/jenkins-pipelines

## Task

Prototype centralized Jenkins-generated env URL routing for service deploys where service-specific env variable names differ by repository.

## Context

- Service: youdo-business-auth-service
- Old reference config: /home/slnnk/git/youdo-business-auth-service/devops/config.yml
- Variables examined:
  - ServiceUrl: self URL for business-auth-int endpoint.
  - YouDo__HttpClient__SmsClient__Host: dependency URL for youdo-business mock API.

## Actions

Decision/prototype:
- Keep deploy-combination-specific URL logic out of service devops/dev.yml.
- Add a central routing catalog example in /home/slnnk/git/helm-charts/examples/jenkins/service-url-routing.yaml.
- Jenkins should generate a final values overlay and pass it after the service values file.

Validated scenarios for BUILD_NUMBER=123:
1. Only youdo-business-auth-service selected:
   - ServiceUrl=https://business-auth-int-123.dev.youdo.sg
   - YouDo__HttpClient__SmsClient__Host=http://youdo-business-mock-api.dev.youdo.corp/youdo/api
2. youdo-business-auth-service and youdo-business selected:
   - ServiceUrl=https://business-auth-int-123.dev.youdo.sg
   - YouDo__HttpClient__SmsClient__Host=http://youdo-business-mock-api-123.dev.youdo.corp/youdo/api

Validation commands:
- helm template youdo-business-auth-service-123 ./microservice --namespace dev-123 --values /home/slnnk/git/youdo-business-auth-service/devops/dev.yml --values examples/jenkins/generated-overlays/youdo-business-auth-service.only-auth.yml --set-string global.projectName=youdo-business-auth-service-123 --set-string global.buildNumber=123 --set-string global.namespace=dev-123 --set-string image.registry=registry.example.com/youdo-business-auth-service --set-string image.tag=v1
- helm template youdo-business-auth-service-123 ./microservice --namespace dev-123 --values /home/slnnk/git/youdo-business-auth-service/devops/dev.yml --values examples/jenkins/generated-overlays/youdo-business-auth-service.with-youdo-business.yml --set-string global.projectName=youdo-business-auth-service-123 --set-string global.buildNumber=123 --set-string global.namespace=dev-123 --set-string image.registry=registry.example.com/youdo-business-auth-service --set-string image.tag=v1

Changed files in helm-charts:
- docs/agents-ephemeral-deploy-plan.md
- docs/service-deploy-notes/youdo-business-auth-service.md
- docs/service-url-routing.md
- examples/jenkins/service-url-routing.yaml
- examples/jenkins/generated-overlays/youdo-business-auth-service.only-auth.yml
- examples/jenkins/generated-overlays/youdo-business-auth-service.with-youdo-business.yml

Next steps (at the time of the prototype):
- Implement catalog parsing and generated overlay creation in /home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile.
- Store generated overlays as Jenkins build artifacts.
- Decide whether ServiceUrl should use dev.youdo.sg or dev.youdo.corp consistently with Ingress DNS.

### Update after user decision

- Routing metadata should live in each service repository, in the same devops/dev.yml file, not in a central helm-charts catalog.
- Updated /home/slnnk/git/youdo-business-auth-service/devops/dev.yml:
  - env.ServiceUrl baseline is now https://business-auth-int.dev.youdo.sg.
  - Added top-level routing.env with rules for ServiceUrl and YouDo__HttpClient__SmsClient__Host.
- Removed the central prototype catalog file from helm-charts examples.
- Jenkins next step: after checkout, read service devops/dev.yml routing.env and generate an overlay passed after devops/dev.yml.

### Jenkins pipeline update

- Updated /home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile.
- Added helpers:
  - yamlDoubleQuoted
  - renderEnvOverlay
  - applyBuildIdTemplate
  - joinUrl
  - buildRoutingEnvValue
  - writeServiceRoutingOverlay
- Pipeline now reads service devops/dev.yml with Jenkins readYaml.
- If routing.env exists, it writes generated/{serviceName}-routing.yml, archives it, and passes it after service devops/dev.yml in helm template and helm upgrade --install.
- Supported routing types: selfUrl and dependencyUrl.
- dependencyUrl switches to selectedHostTemplate when targetService is in effectiveServicesForDeploy; otherwise uses defaultHost.
- Local Groovy parse was not run because groovy is not installed in the working environment. Jenkins job requires Pipeline Utility Steps readYaml.

### Config.yml vs dev.yml env comparison

- Checked /home/slnnk/git/youdo-business-auth-service/devops/config.yml webEx_env/webEx1_env against current devops/dev.yml.
- Missing from dev.yml compared to old config.yml:
  - Environment
  - YouDo__Tracing__JaegerAgentConfig__Host
  - YouDo__Tracing__JaegerAgentConfig__Port
  - Sentry__Environment
  - Sentry__Release
  - Sentry__ServerName
- BaseDomain is present as per-service env for web-int/web-ext, not global ConfigMap env.
- ConnectionStrings__default is intentionally represented as pgService alias.
- ServiceUrl and YouDo__HttpClient__SmsClient__Host are present and now have routing metadata.
- Sentry__Dsn is present but intentionally empty in dev.yml; do not copy old DSN value into notes or committed values.
- Jaeger host values from old config use NOMAD_IP_* and are not directly portable to Kubernetes.

### BaseDomain cleanup

- Moved BaseDomain in /home/slnnk/git/youdo-business-auth-service/devops/dev.yml from services[].env to top-level env because web-int and web-ext use the same value.
- Verified helm template renders BaseDomain once in ConfigMap data.

### Environment variables update

- Added env.Environment=Staging to /home/slnnk/git/youdo-business-auth-service/devops/dev.yml.
- Changed env.ASPNETCORE_ENVIRONMENT from Development to Staging to match old devops/config.yml.
- Verified helm template renders both values in ConfigMap.

Checked /home/slnnk/git/youdo.servicecore for Environment variables:
- EnvironmentInfo.Name reads ENVIRONMENT, then ENVIRONMENT_NAME, then ASPNETCORE_ENVIRONMENT, then defaults to unknown.
- ServiceCore configuration loads appsettings.json, appsettings.{EnvironmentInfo.Name}.json, appsettings.{EnvironmentInfo.Name}.overrides.json, then environment variables.
- Therefore ENVIRONMENT/Environment can affect ServiceCore config file selection if the env var is actually exported as ENVIRONMENT or maps case-insensitively in the platform/runtime.
- ASPNETCORE_ENVIRONMENT still controls ASP.NET IWebHostEnvironment behavior such as env.IsProduction().
- Recommendation: keep Environment and ASPNETCORE_ENVIRONMENT aligned for this service dev flow, currently Staging.

### Environment naming update

- Changed /home/slnnk/git/youdo-business-auth-service/devops/dev.yml env.Environment and env.ASPNETCORE_ENVIRONMENT from Staging to Development for dev namespaces.
- Verified helm template renders both as Development.

### Additional env migration

- Added empty YouDo__Tracing__JaegerAgentConfig__Host and YouDo__Tracing__JaegerAgentConfig__Port to /home/slnnk/git/youdo-business-auth-service/devops/dev.yml.
- Added Sentry__ServerName={{ .Values.global.namespace }}.
- Did not add Sentry__Environment or Sentry__Release per user decision.
- Verified helm template renders Sentry__ServerName as dev-123 for the validation command.

### Sentry update

- Added Sentry__Environment=Development and Sentry__Release={{ .Values.image.tag }} to /home/slnnk/git/youdo-business-auth-service/devops/dev.yml.
- Kept Sentry__ServerName as {{ .Values.global.namespace }}.
- Verified helm template renders Sentry__Environment=Development, Sentry__Release=v1, Sentry__ServerName=dev-123 for the validation command.

### Sentry correction

- Updated Sentry__Environment to "Development_{{ .Values.global.namespace }}".
- Kept Sentry__Release as "{{ .Values.image.tag }}".
- Verified helm template renders Sentry__Environment=Development_dev-123 for namespace dev-123.

### Sentry DSN vault secret

- Added secrets entry to /home/slnnk/git/youdo-business-auth-service/devops/dev.yml.
- Vault path: dev/projects/youdo-business-auth-service.
- Vault key: SentryDsn.
- Kubernetes env name: Sentry__Dsn.
- Removed Sentry__Dsn from plain env so it now comes only from VaultStaticSecret.
- Verified helm template renders VaultStaticSecret with path dev/projects/youdo-business-auth-service and transformation key Sentry__Dsn.

## Findings

- Routing metadata belongs in each service's `devops/dev.yml` (`routing.env`), not in a central catalog; Jenkins renders the generated overlay and passes it after the service values.
- `ENVIRONMENT`/`Environment` and `ASPNETCORE_ENVIRONMENT` should be kept aligned for a service in the dev flow (final value for this service at the time: `Development`).
- Secret values (Sentry DSN) come only from Vault via `VaultStaticSecret`; the plain-env copy was removed.

## Changes

- `/home/slnnk/git/helm-charts`: docs and example overlays listed above (central catalog example later removed).
- `/home/slnnk/git/youdo-business-auth-service/devops/dev.yml`: routing.env, BaseDomain, Environment/ASPNETCORE_ENVIRONMENT, Jaeger placeholders, Sentry variables, Vault secret mapping.
- `/home/slnnk/git/jenkins-pipelines/pipelines/deploy-dev-b2b.Jenkinsfile`: routing overlay helpers.

## Open items

- Decide whether ServiceUrl should use dev.youdo.sg or dev.youdo.corp consistently with Ingress DNS.
- Jenkins job requires Pipeline Utility Steps readYaml (later found not installed; see 2026-09-04 notes on the Python/PyYAML fallback).

## Portable lesson

none
