# RELEASE.md — Release Readiness & Branch Hygiene

The standardized answer to "is this ready to release?" and "why do I have 40 open PRs and a graveyard of dead branches?" Fill the `<placeholders>`. Pairs with `IAC.md` (the pipeline that enforces this) and `SECURITY.md`.

> **Principle:** a release is a deliberate, gated event — not a side effect of pushing. Every branch has exactly two fates: merged or deleted. Nothing lingers.

---

## 1. Definition of Done (before a release is "ready")

A change is release-ready only when **all** of these are true. CI enforces most; the rest are a human/agent gate.

- [ ] **On a branch, merged via PR** — never released straight off a long-lived local branch (§ branch hygiene below).
- [ ] **CI green end to end** — format, lint, test (with coverage threshold), security scan, container/build jobs all pass (`IAC.md` §1).
- [ ] **No known high/critical CVEs** — dependency + container scans clean or explicitly waived with justification (`SECURITY.md`).
- [ ] **Secrets clean** — secret scan passed; no secret/env files tracked; nothing sensitive in the built artifact.
- [ ] **Conventional-commit history** — commits follow `type(scope): subject` so version + CHANGELOG can be derived automatically.
- [ ] **CHANGELOG reflects reality** — user-facing changes, breaking changes, and migration notes present (auto-generated is fine; review it).
- [ ] **Version bumped correctly** — semver: breaking → major, feature → minor, fix → patch. Breaking changes carry a migration note (`CLAUDE.md` §15.4).
- [ ] **Docs updated** — README/architecture and any changed API/contract match the code (`CLAUDE.md` §15.3); finished specs/decisions rolled back from the planning layer (§7.4 / §17).
- [ ] **Smoke-tested** — the actual built artifact/image runs and its key path works, not just unit tests (`CLAUDE.md` §15.2).
- [ ] **Deploy + rollback path known** — you know how it ships and how to roll it back (`IAC.md` §5).

If a box can't be checked, either fix it or explicitly note the gap in the release notes — do not release silently around it.

---

## 2. Standardized Release Flow

Automate the mechanical parts; keep the decision human.

1. **Merge features to the default branch** via reviewed PRs (squash, conventional-commit title).
2. **A release-automation bot maintains a standing "release PR"** (e.g. release-please) that accumulates the next version bump + CHANGELOG from the merged conventional commits.
   - It needs a **PAT, not the default CI token** — tags created by `GITHUB_TOKEN` don't trigger downstream workflows. Fall back: `secrets.<RELEASE_TOKEN> || secrets.GITHUB_TOKEN`.
3. **Cutting a release = merging that release PR.** That creates the version tag.
4. **The tag triggers the build-and-publish workflow** — cross-platform build, archive, SHA256 checksums, **signed** manifest/tags, artifacts attached to the GitHub Release (`IAC.md` §3).
5. **Deploy** is branch/tag-gated and runs only after build succeeds.

Pre-releases: tag with a suffix (`v1.2.0-rc.1`); CI auto-flags them (`prerelease: contains(ref, '-')`).

---

## 3. Branch & PR Hygiene (no sprawl)

**Every branch is merged or deleted. There is no third state.**

### Branch rules
- Branch names follow the repo convention: `feature/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`.
- **Delete the branch on merge** — enable "automatically delete head branches" in repo settings so nothing accumulates.
- **A branch that can't merge gets closed, not abandoned.** If a PR's approach is dead, close it and delete the branch; capture anything worth keeping as a task/note (§17) first.
- **Prune stale branches on a cadence.** A branch with no commits in `<30>` days and no open PR is a candidate for deletion — audit and remove (see §4).

### PR rules
- **One logical change per PR**; keep them small and reviewable (`CLAUDE.md` §2).
- **Don't let PRs rot.** A PR open past `<14>` days is either merged, or closed with a reason. Draft PRs for work-in-progress so they're not counted as review-ready.
- **Require CI green + review before merge**; protect the default branch.

### Dependabot (the usual source of PR pileup)
- **Group updates** so related deps arrive as one PR, not twenty (`SECURITY.md` — group `x/*`, framework families, etc.).
- **Cap the queue** with `open-pull-requests-limit` (e.g. `5`).
- **Auto-merge low-risk updates**: enable auto-merge so patch/minor dependency PRs that pass CI merge themselves — no human babysitting.
  ```yaml
  # .github/workflows/dependabot-auto-merge.yml (sketch)
  # on: pull_request; if actor == 'dependabot[bot]' and update-type is patch/minor:
  #   gh pr merge --auto --squash "$PR_URL"
  ```
- **Review only major bumps by hand** — those are the ones that break things.
- Weekly schedule, conventional-commit prefixes (`chore(deps)`) so release automation classifies them.

---

## 4. Periodic Cleanup (run this, don't let it drift)

A quick audit to keep the repo tidy (adapt to `gh`):

```bash
# Merged branches still lying around (delete after confirming)
gh pr list --state merged --limit 50 --json headRefName -q '.[].headRefName'

# Open PRs older than 14 days
gh pr list --state open --json number,title,updatedAt,author \
  -q '.[] | select(.updatedAt < (now - 14*86400 | todate))'

# Dependabot PRs piled up
gh pr list --state open --author 'app/dependabot' --json number,title

# Local branches already merged into main
git branch --merged main | grep -vE '^\*|main'
```

For each: **merge it, or close-and-delete it.** Log anything worth keeping as a task before deleting. Never bulk-delete without eyeballing the list first.

---

## Checklist (tl;dr)

- [ ] Definition of Done (§1) all green before cutting a release.
- [ ] Release = merge the automated release PR → signed, checksummed tag build.
- [ ] Delete-on-merge enabled; no branch left in limbo.
- [ ] Dependabot grouped + capped + auto-merged for patch/minor.
- [ ] Stale-branch / old-PR audit run on a cadence.
