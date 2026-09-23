# Prompt: extract a portable recipe from a log entry

Use after an incident or investigation was written up in `knowledge/log/` and it contains a
lesson that would hold at any employer.

---

Read `~/ai/AGENTS.md` and the recipe template in `~/ai/general/knowledge/README.md`. Then read
the log entry `<LOG_PATH>`.

1. Decide whether it contains a lesson about a technology's behaviour, a failure mode with a
   fix, or a diagnostic technique that is independent of this company. If not, reply
   "no portable lesson" with one sentence why, and stop.
2. Check `~/ai/general/knowledge/<technology>/` for an existing recipe on the same failure
   mode. If one exists, extend it (add the new symptom variant, version, or limit) and
   update `checked`; do not create a duplicate.
3. Otherwise create it with
   `python3 ~/ai/general/scripts/new_note.py recipe <technology> <slug>` and fill Symptom,
   Cause, Fix, Limits. Rewrite from scratch in generic terms: no company name, hostnames,
   IPs, internal URLs, ticket ids, repository names or people. Keep exact error messages,
   commands and config keys. Use RFC 5737 addresses in examples. The file must be
   publishable as is.
4. In the log entry set `## Portable lesson` to a relative link to the recipe.
5. Run `python3 ~/ai/general/scripts/kb_lint.py` and fix findings. Append one line to
   `~/ai/.sync-notes` describing what you did. Do not commit.
