---
system: automation-services
status: verified
checked: 2026-06-05
tags: [nginx, routing, traefik, business.youdo.com, public-docs, s3, youdo-business]
---
# nginx business.youdo.com routing

Date: 2026-06-05
Project: automation-services
Repository: /home/slnnk/git/automation-services
Area: Ansible role roles/nginx, prod_selectel balancers

## Finding

Investigated who serves `https://business.youdo.com/docs/terms/dogovor_smz_05_05_26.pdf` from nginx role configuration.

`roles/nginx/templates/vhost/business.youdo.com.j2` has no dedicated `location` for `/docs/terms` or this PDF. The HTTPS server for `business.youdo.com business-api.youdo.com` uses generic `location /` and proxies requests to `$proxy_backend`.

`$proxy_backend` is set to `nginx_proxy_traefik` when defined, otherwise to `nginx_traefik_addr`. In prod_selectel balancers no explicit `nginx_traefik_addr` override was found for this vhost, so role default applies: `proxy.service.consul`.

Special case: `/survey-questionnare/` is proxied to `b2b-landing-questionnaire.proxy.youdo.local`, unrelated to `/docs/terms`.

## Relevant files

- `roles/nginx/templates/vhost/business.youdo.com.j2`
- `roles/nginx/defaults/main.yml`
- `inventories/prod_selectel/group_vars/balancers`
- `inventories/prod_selectel/group_vars/balancers_public`
- `inventories/prod_selectel/group_vars/balancer_redirect`

## Conclusion

From nginx role alone, the PDF is not served as local nginx static content. It is proxied to Traefik via `proxy.service.consul`; the backend application/service behind Traefik decides the final handler for `/docs/terms/dogovor_smz_05_05_26.pdf`.


## Application follow-up: youdo.business

Date: 2026-06-05
Repository: /home/slnnk/git/youdo.business

Checked how `https://business.youdo.com/docs/terms/dogovor_smz_05_05_26.pdf` is handled by the application.

Production routing in `devops/production.hcl`: Traefik routes `Host(business.youdo.com)` to service `youdo-business-web`. The public controller is `YouDo.Business.Web/Controllers/PublicDocumentsController.cs` with anonymous route `GET /docs/{category}/{fileName}` and alias `GET /public-docs/{category}/{fileName}`.

For the URL above:
- category route value: `terms` -> `PublicDocCategory.Terms`
- fileName route value: `dogovor_smz_05_05_26.pdf`

The controller dispatches `DownloadPublicDocByOriginalNameQuery(category, fileName)`. The query handler reads S3 manifest through `PublicDocsS3.GetManifestJsonAsync(category)`, deserializes it, finds a non-deleted `DocumentFile` whose `OriginalFileName` equals the requested filename case-insensitively, then reads the S3 object by `file.Key` through `PublicDocsS3.ReadForDownloadAsync`.

S3 layout from code/config:
- Base prefix: `public-docs` by default/config.
- Terms manifest key: `public-docs/terms/index.json`.
- File objects are stored as `public-docs/{category}/files/{generated_slug}_{yyyy-MM-dd}_v{version}.{ext}`.
- Public URLs are generated as `${BusinessWeb.ExternalEndpoint}/docs/{categorySlug}/{OriginalFileName}`.

Conclusion: the visible URL filename is not necessarily the physical S3 object name. It is matched against `OriginalFileName` in the category manifest. If `dogovor_smz_05_05_26.pdf` exists as a non-deleted file in `public-docs/terms/index.json`, the app returns the corresponding S3 object inline. Otherwise it returns 404.

## Public docs upload path vs doc-generator

Date: 2026-06-05
Repositories:
- /home/slnnk/git/youdo.business
- /home/slnnk/git/youdo-business-doc-generator

Checked whether public document URL handling/upload is related to `youdo-business-doc-generator`.

Conclusion: public docs upload is not handled by doc-generator. `youdo-business-doc-generator` has S3 access, but only reads files from the business bucket (`GetObjectAsync`) to load templates/signatures and returns generated DOCX/PDF streams to callers. No `PutObjectAsync` usage was found in the doc-generator repo.

Public docs upload path is in `youdo.business`:
- Admin UI: `YouDo.B2b.Automation.Web/spa/src/components/compliance/PublicDocsPage.tsx`
- API routes: `YouDo.B2b.Automation.Web/spa/src/api/apiRoutes.ts`, endpoints `/publicDocs/{category}/create` and `/publicDocs/{category}/{documentId}/addDocumentFile`
- Controller: `YouDo.B2b.Automation.Web/Controllers/PublicDocsController.cs`
- Commands: `CreatePublicDocCommand` and `ReplacePublicDocCommand`
- Storage implementation: `YouDo.Business.Managers/Handlers/PublicDocs/PublicDocsS3.cs`

`PublicDocsS3` uploads the PDF object to S3 with `PutObjectAsync`, then writes/updates the manifest JSON with another `PutObjectAsync`.

For terms category, expected manifest key is `public-docs/terms/index.json`; uploaded file keys are generated under `public-docs/terms/files/`.
