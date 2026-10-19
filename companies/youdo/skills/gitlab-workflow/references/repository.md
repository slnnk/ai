# Find and inspect the right checkout

1. Consult `~/ai/current/knowledge/repos.md` by full GitLab group/project path.
   Reuse the registered checkout, including existing legacy locations. Otherwise
   inspect immediate checkouts under `~/git`; do not start with a disk-wide search.
2. Run local inspection, for example:

   ```bash
   python3 ~/ai/current/scripts/gitlab_repo.py inspect --project sysadmins/automation-services
   ```

   Output includes sanitized project/origin, checkout, branch, HEAD, upstream,
   cached divergence and staged/unstaged/untracked status (first 50 paths, with
   total count). It performs no fetch or other mutation. Use `git status --short`
   in the selected checkout if the list is truncated.
3. If absent, run the explicit `clone` phase with the same `--project`, a concise
   `--purpose` and `--system`. It clones full history into `~/git/<project-name>`
   and appends the verified mapping to the existing catalog. It does not overwrite
   an occupied destination or clean up a failed clone. Explain name collisions
   rather than inventing a second checkout. No remote GitLab state is changed.
4. Multiple matches require `--repo /absolute/existing/checkout`. Both fetch and
   push origins must identify the requested project. Do not rewrite remotes or
   credentials to make a check pass. A mismatching catalog entry is a conflict,
   not a reason to silently clone elsewhere.
5. Read applicable project instructions; inspect identity and current local
   changes before task work. Do not rewrite identity. Use the existing checkout;
   a worktree requires an explicit user request.

## Choose the revision

- MR analysis: obtain the MR's exact source SHA through GET, then inspect that
  revision locally. An already checked-out branch is not proof of the MR revision.
- Failed CI: use the failed pipeline/job commit SHA.
- New changes: choose the project's actual base/target, not an assumed master.
- Historical question: inspect the stated revision; avoid irrelevant refreshes.

`refresh --project ...` performs only `git fetch origin`, preserving the working
tree/index and current branch; it does not pull, prune, merge or switch branches.
After fetching, compare local and remote refs. If an exact MR/job SHA is missing,
fetch the specific needed ref explicitly, then verify its SHA. Use `git show`,
`git diff` and local searches without switching branches during investigation.
Honor sandbox/network approval requirements if clone/fetch cannot run normally.

Detached HEAD is reported explicitly. A dirty checkout is not an automatic stop
for read-only work. Before any approved switch/edit, determine whether the user's
changes conflict. Explain an actual conflict before moving or discarding anything;
do not stash/reset or create a worktree as an automatic workaround.

## Catalog and output

Store path, credential-free origin, purpose, system and observation date. Do not
store the current branch as repository metadata. The helper canonicalizes reported
origins so embedded credentials/query strings cannot enter its JSON output.
Never print `.env`, credential helpers or raw authenticated request/response data.
In findings identify the checkout and inspected SHA and whether remote state was
refreshed. Distinguish cached local refs from fresh remote observations.
