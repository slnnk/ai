# Prompt: normalize or migrate a batch of notes into the knowledge base

Use when importing notes from another tool, another layout, or when a batch of existing
notes drifted from the conventions. Give the agent this prompt plus a file listing the
source paths. Split large sets into thematic batches of 15 to 35 files and run them in
parallel; each batch must own its system maps to avoid two agents writing the same file.

---

You normalize a batch of Markdown notes into the layered knowledge base under `~/ai/`.
Sources are READ ONLY; never modify or delete them. First read in full:

- `~/ai/AGENTS.md`
- `~/ai/general/knowledge/README.md`
- `~/ai/current/CONTEXT.md`

Your batch file is `<BATCH_FILE>`; paths are relative to `<SOURCE_ROOT>`. Process every file.

## Destination rules

Default layer: `~/ai/current/knowledge/` (call it `K`). Create files with
`python3 ~/ai/general/scripts/new_note.py` so names and frontmatter are right, then fill them.

1. Dated one-off work (investigation, incident, job analysis, handoff, plan, review of one
   MR or build) -> `K/log/YYYY-MM-DD-<system>-<slug>.md`. Date from the source filename, else
   from the content, else from the file modification time. Keep job, pipeline and ticket
   numbers in the slug.
2. Living documents about a system (map, registry, config reference, "how X works") ->
   `K/systems/<system>.md`, or `K/systems/<system>/<topic>.md` when a system needs several.
   Check the target does not exist before writing; if it does, choose a more specific topic.
3. Repository registries -> merge into the table in `K/repos.md`; strip credentials from URLs.
4. Non-Markdown files -> `K/files/<name>`; link them from the note as `../files/<name>`.
5. `~/ai/personal/knowledge/` only for the user's own infrastructure with no company relation.

Canonical `system` values: read them from `K/INDEX.md` ("Log by system") and reuse; add a
new lowercase kebab-case value only when nothing fits.

## Content rules

- Frontmatter `system`, `status` (verified | hypothesis | outdated), `checked`, `tags`.
  `checked` is the date of the work. Plans and unverified analyses are `hypothesis`.
- English. Translate prose faithfully and completely. Never translate or alter hostnames,
  IPs, paths, commands, config, log excerpts, job names, variables, ticket ids, quoted UI
  strings. Code blocks stay byte-identical. Do not summarize; keep every fact.
- Rewrite old paths to their new locations. Old `.env` and scripts paths ->
  `~/ai/current/.env`, `~/ai/current/scripts/`.
- Secrets: never copy a literal password, token or key. Replace with
  `<redacted, see ~/ai/current/.env KEY_NAME>` and report it.
- Log entries end with `## Portable lesson`: a link to a recipe you wrote, or `none`.

## Portable recipes

For each note ask: is there a lesson valid at any employer? If yes, write a recipe with
`new_note.py recipe <technology> <slug>` (Symptom, Cause, Fix, Limits), rewritten from
scratch without company name, hosts, IPs, internal URLs, tickets or people. Use RFC 5737
addresses (192.0.2.x, 198.51.100.x, 203.0.113.x) for examples. Only real lessons; check for
an existing similar recipe and extend it instead of duplicating.

## Report

Write `<MANIFEST_PATH>` with one tab-separated line per source: `source`, `destination`,
`system`, `status`, `note` (redactions, translations, layer decisions, recipe paths). List
recipes at the end as `RECIPE<TAB><path>`. Finish with counts and anything you were unsure
about. Run `python3 ~/ai/general/scripts/kb_lint.py` and fix what it reports. Do not run
`build_index.py` or commit; the coordinator does.
