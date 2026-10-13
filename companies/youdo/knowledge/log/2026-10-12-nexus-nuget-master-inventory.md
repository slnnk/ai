---
system: nexus
status: verified
checked: 2026-10-12
tags: [nexus, nuget, recovery, inventory]
---
# NuGet master dependency inventory and library source mapping

## Summary

Scanned164unique checkouts under ~/git without modifying working copies. Read157current remote master snapshots pinned by SHA;62repositories consume NuGet. Extracted3198consumed reference occurrences,387package IDs and1131ID/version expressions.52private/custom library IDs with143requested version pairs are absent from both nuget.org and current Nexus. Source catalog youdo/Lib and already scanned consumers provide candidates for all52; historical YouDo.Extensions and Serilog.Sinks.Exceptional source relationships are hypotheses. BaGet reachability timed out, so absence there is unverified. No committed lock/assets files; indirect private dependencies are not complete.

## Task and authorization

User requested every service under ~/git, using current master, and supplied https://gitlab.youdo.sg/youdo/Lib as the source-library catalog. Read-only remote GitLab/feed requests and local report/helper creation only. No package restoration, pipeline, commit or deploy requested or performed.

## Method and actions

Subagent inventory deduplicated Git common directories:165checkouts/164unique repositories. Scanner /home/slnnk/ai-data/nexus-recovery/scan_nuget_master.py resolves live GitLab master SHA and reads archives pinned to it. Existing local branches/files were untouched. Parses .NET project PackageReference, central PackageVersion, packages.config, NuGet.Config source URLs and tool manifests. Ancestor Directory.Build.props/targets and Directory.Packages.props plus static imports provide versions; standalone central declarations excluded from actual consumers. Generated packages/bin/obj/vendor/node_modules references excluded. Secret-bearing configs were parsed in memory; output contains only sanitized source URLs and package metadata, no credential values.

Classifier /home/slnnk/ai-data/nexus-recovery/classify_nuget.py discovers PackageBaseAddress in service indexes and checks package version indexes for nuget.org/current Nexus/BaGet. BaGet service-index connection timeout; no version checks possible there. Successful public package exact-version checks distinguish publicly available dependencies; missing requested versions treated as recovery candidates or public version gaps. Builder /home/slnnk/ai-data/nexus-recovery/build_nuget_report.py generates CSV artifacts and source mappings.

## Artifacts

All generated data outside git: /home/slnnk/ai-data/nexus-recovery/nuget-inventory/.

- restore-libraries.csv:52rows, package/required versions/consumers/source candidates/confidence.
- restore-packages.csv:143rows, one ID/version per row with consumers, source and SHA/file/line evidence.
- services.csv:62NuGet consumers with pinned master SHA, feed declarations and missing libraries.
- public-version-gaps.csv:3public packages with requested versions not found: AspNetCore.HealthChecks.UI.Client8.0.2, NetVips.Native.win-x648.13.3, Serilog.Enrichers.Sensitive1.8.0. Bare PackageReference versions are minimum constraints; newer public versions may resolve but can change behavior. These are separate from private package restoration.
- dynamic-versions.csv:4floating public references with matching public versions and Microsoft.AspNetCore.App SDK-managed no-version references. Not private restoration targets.
- coverage.csv/inventory.json:164repository outcomes, including skipped/failed cases.
- consumed-references.json:3198actual occurrences; references.json retains central declarations separately.
- availability.json:per-package feed metadata and1131requested expression outcomes (980public exact pairs,146exact missing pairs including3public gaps,5dynamic/SDK entries).
- libraries-catalog.json/source-candidates.json:live library projects and SHA/file/evidence/confidence mappings.

## Coverage and limits

157master snapshots read. YouDoApp defaultdevelop, android-exporter main, claude-code-config-infra main lackmaster and were not silently substituted. anroid-docker-image and one_test return project404 to current credentials; existence vs access cannot be determined. admin-final (noncompanyGitLab) and ai-skills(noorigin) have no local NuGet manifests and were excluded. Group youdo/Lib contains30projects;29master archives read,Youdo.Utils branch/archive404.

No full MSBuild evaluation or restore. Conditions remain candidate references and are not evaluated by target framework/configuration. Dynamic/recursive imports, effective source overrides in CI/Docker/base-image/global NuGet settings, and environment variables are not simulated. All explicit consumed versions resolved except SDK-managed Microsoft.AspNetCore.App; no committed lock/project.assets files were present. Floating public references are not pinned, so list is requested dependencies rather than a full restored lock graph. Exact requested versions may differ from what minimum constraints select when missing.

Library source candidate identity is supported by PackageId/AssemblyName/project filename where available, not proof that currentmaster produces each required historical version. Historical tags/commits and caches/artifacts need separate inspection before rebuilding. DocXToPdfConverter1.1.0-youdo is a custom version despite the base package being public. Existing Nexus remains unchanged except normal proxy cache population during GET. Service and library repositories remain untouched.

## Restoration list

| Library | Required versions | Consumers | Source candidates |
|---|---|---:|---|
| Coworking | 1.0.7, 1.3.3, 1.3.4 | 8 | youdo/Lib/Coworking |
| DocXToPdfConverter | 1.1.0-youdo | 1 | youdo/Lib/Net-Core-DocX-HTML-To-PDF-Converter |
| FluentMigratorCore.Consolisator | 0.3.11, 1.1.0, 1.7.0, 1.8.1, 1.9.1 | 34 | youdo/Lib/FluentMigratorCore |
| FluentMigratorCore.Extensions | 1.8.1 | 2 | youdo/Lib/FluentMigratorCore |
| Kaiena | 1.0.8 | 2 | youdo/Lib/Kaiena |
| RabbitHole | 1.4.1, 1.4.2, 1.4.3 | 6 | youdo/Lib/rabbit-hole |
| Serilog.Sinks.Exceptional | 1.0.2, 1.0.4 | 14 | youdo/Lib/serilog.sinks.exceptional |
| Youdo.Business.Auth.Client | 0.0.31, 0.0.37 | 2 | youdo/microservices/youdo-business-auth-service |
| Youdo.Business.Auth.Lib | 0.0.31, 0.0.37 | 2 | youdo/microservices/youdo-business-auth-service |
| YouDo.Business.Platform.Events | 0.3.17, 0.3.2, 0.3.20, 0.5.4, 0.5.6, 0.5.8 | 8 | youdo/Lib/youdo-business-platform-events |
| YouDo.Caching | 2.2.4, 2.4.2 | 2 | youdo/Lib/YouDo.Caching |
| YouDo.Chronos | 1.0.7, 1.0.9 | 4 | youdo/Lib/Chronos |
| YouDo.Chronos.Configuration.Extensions | 1.0.0, 1.0.1 | 3 | youdo/Lib/youdo.chronos.configuration.extensions |
| YouDo.Contracts.Abstractions | 1.0.0 | 5 | youdo/Lib/YouDo.Contracts |
| YouDo.CQRS | 2.0.0 | 5 | youdo/Lib/youdo.cqrs |
| YouDo.Data | 2.7.4 | 2 | youdo/Lib/YouDo.Data |
| YouDo.Data.Common | 2.7.4 | 2 | youdo/Lib/YouDo.Data |
| YouDo.Data.Core | 2.5.4, 2.7.4 | 11 | youdo/Lib/YouDo.Data |
| YouDo.Disposables | 1.0.0 | 1 | youdo/Lib/YouDo.Disposables |
| YouDo.Extensions | 1.2.3 | 1 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Caching | 1.7.1, 1.9.1 | 2 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Contract | 1.8.1, 1.9.2 | 3 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.CQRS | 1.9.4, 1.9.5 | 5 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Hosting | 3.0.1, 3.0.3, 3.0.5, 4.0.0, 4.0.1 | 11 | youdo/Lib/youdo.extensions, youdo/Lib/youdo.microservices.lib |
| YouDo.Extensions.Jobs.Hangfire | 1.8.1, 1.9.1 | 3 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.MessageBus | 1.2.4, 1.5.0, 1.9.1, 1.9.2, 1.9.4 | 5 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.MessageBus.MassTransit | 1.8.1, 1.9.1, 1.9.2 | 6 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Net | 1.5.0, 1.8.1 | 2 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Sentry | 1.9.0 | 1 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Tracing | 0.3.4, 0.3.5, 1.2.3, 1.8.1 | 5 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Tracing.Linq2Db | 0.3.3, 0.3.4, 0.3.5, 1.2.3, 1.5.0 | 6 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Tracing.OpenTelemetry | 1.7.1, 1.9.5 | 3 | youdo/Lib/youdo.extensions |
| YouDo.Extensions.Tracing.OpenTelemetry.Linq2Db | 1.9.5 | 1 | youdo/Lib/youdo.extensions |
| YouDo.Mailer | 1.0.3, 1.0.3-prerelease-23572-update-ms-lib-8-679 | 4 | youdo/mail/mailer |
| YouDo.MaxMessenger.Bot | 0.5.4, 0.5.6 | 2 | youdo/Lib/youdo.maxapi |
| YouDo.Microservices.Common | 2.0.3, 2.0.4, 2.0.5, 3.0.4, 4.0.0 | 13 | youdo/Lib/youdo.microservices.lib |
| YouDo.Microservices.Core | 2.0.3, 3.0.1, 3.0.2, 3.0.3, 3.0.4, 3.0.7, 4.0.0 | 20 | youdo/Lib/youdo.microservices.lib |
| YouDo.Push.Apns | 1.0.4 | 1 | youdo/Lib/YouDo.Push |
| YouDo.Push.Huawei | 0.0.6 | 1 | youdo/Lib/YouDo.Push |
| YouDo.Serilog.Sinks.Exceptional | 1.0.5 | 7 | youdo/Lib/serilog.sinks.exceptional |
| YouDo.ServiceCore.Application | 0.3.1, 0.4.1, 0.5.0, 0.6.0, 1.0.14, 1.0.15, 1.0.16 | 22 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Common | 0.5.0, 1.0.14, 1.0.15, 1.0.16 | 11 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Configuration | 0.4.1, 0.5.0, 0.6.0, 1.0.14, 1.0.15 | 12 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.DistributedLock | 0.5.0, 0.5.1, 0.6.0, 1.0.14, 1.0.15, 1.0.16 | 11 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.HttpClient | 0.5.0, 0.6.0, 1.0.14, 1.0.15, 1.0.16 | 9 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Logging | 0.5.0, 0.6.0, 1.0.14, 1.0.15 | 11 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Metrics | 0.5.0, 0.6.0, 1.0.14, 1.0.15 | 6 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.RabbitMq | 1.0.14, 1.0.15 | 5 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Testing | 0.5.0, 0.6.0, 1.0.14, 1.0.15, 1.0.16 | 7 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Tracing | 1.0.14, 1.0.15 | 2 | youdo/Lib/youdo.servicecore |
| YouDo.ServiceCore.Validation | 1.0.14, 1.0.15, 1.0.16 | 7 | youdo/Lib/youdo.servicecore |
| YouDo.TextValidation.Contracts | 0.0.8 | 2 | youdo/microservices/textvalidation |

## Verification

CSV row counts checked:52libraries/143version pairs/62consumers; every report records pinnedmaster SHA/file evidence. Helpers support --help; scan/parser syntax check passed. No success claim for package rebuild or service restore. Follow-up remains in ~/ai/TODO.md.
