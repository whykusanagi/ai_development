# Security Policy

This is a **fill-in template** — replace every `<placeholder>` with your project's real values, then delete this line. It doubles as a reusable vulnerability-disclosure policy and a checklist of the security engineering practices CI should enforce. See `CLAUDE.md` §4 for secret-handling guardrails; this file is the outward-facing policy plus the CI enforcement that backs it.

---

## Supported Versions

Security fixes are provided only for supported versions.

| Version | Supported |
|---------|-----------|
| `<current-major.minor>.x` | ✅ |
| `< <current-major.minor>` | ❌ |

---

## Reporting a Vulnerability

**Do not open a public issue for security reports.**

Report privately via `<security-contact>` (e.g. a dedicated `security@<domain>` inbox or GitHub's private "Report a vulnerability" advisory feature). For sensitive reports, encrypt to `<PGP-key-id>` (`<key-url>`).

**Response SLA**
- Acknowledgement within **<48–72h>**.
- Assessment + severity triage within **<7 days>**.
- Fixes for high/critical issues targeted within **<7 days>** of confirmation.

**What to include in a report**
- Type of issue (e.g. injection, auth bypass, secret exposure, RCE).
- Affected version(s), file paths, and/or component.
- Steps to reproduce and, if possible, a proof of concept.
- Impact — what an attacker can achieve.

---

## Scope

**In scope:** `<source code, released artifacts, deployment configuration, official packages>`.
**Out of scope:** `<third-party dependencies' own bugs, social engineering, physical access, issues in unsupported versions, denial-of-service via resource exhaustion — adjust to your project>`.

---

## Disclosure Process

1. Report received and acknowledged.
2. Severity assessed; a private fix is developed.
3. Advisory drafted; fix released in a new patched version.
4. **Coordinated disclosure** after a `<90>`-day embargo (or sooner if a fix ships and both sides agree). Reporters are credited unless they request otherwise.

---

## Threat Model

State what you defend against and — just as importantly — what you do **not**.

| Threat | Mitigation | Status |
|--------|-----------|--------|
| Secret exposure in repo/artifacts | Secret scanning in CI + gitignored secret files | `<active>` |
| Vulnerable dependencies | Dependabot + audit gate in CI | `<active>` |
| Tampered release artifacts | Signed checksums / signed tags | `<active>` |
| `<...>` | `<...>` | `<...>` |

**Not defended against:** `<e.g. a compromised developer machine, malicious first-party commits, upstream registry compromise — be explicit so users calibrate trust>`.

---

## Security Engineering Practices (CI-enforced)

These are the controls that make the policy above credible. Wire them into the pipeline (see `IAC.md`).

### Secret scanning
- Run a secret scanner (e.g. gitleaks) on **every push and PR** with **full history** (`fetch-depth: 0`) so all commits are scanned, not just the diff.
- Maintain a scanner allowlist (`.gitleaks.toml`) for documented false positives (public/example data) — **suppress specific findings, never disable the scan**.
- Add a cheap regex grep for known API-key formats as a backstop.

### Dependency management
- Ship a `dependabot.yml` covering **every ecosystem in the repo** (package manager, `github-actions`, `docker`) — keep the CI actions themselves updated.
- **Group related dependencies** into one PR to cut review churn; set `open-pull-requests-limit` to cap noise; use a weekly schedule as a sane default.
- Use conventional-commit prefixes (`fix(deps)` / `chore(deps)`) so release automation classifies them correctly.
- In monorepos, list every module directory so nested modules get updates.

### Vulnerability & container scanning
- **Fail CI on high/critical CVEs** via a dependency audit (`npm audit --audit-level=high`, `govulncheck ./...`, or equivalent).
- Run security scans **on a schedule** (weekly cron), not only on PRs — newly-disclosed CVEs affect unchanged code.
- Keep an auditable ignore file for container scans (`.trivyignore`) with a comment justifying each entry.
- When you must pin a scanner to an older version (a newer one regressed), leave a comment explaining why and when to revisit.

### Secret hygiene enforced in CI
- **Assert secret/env files are not tracked** and fail the build if they are: `git ls-files --error-unmatch .env` (invert to fail-on-found).
- **Verify secrets don't leak into build output** (`.env` absent from `dist/` / published tarball).
- Commit only a **`.env.example`** with placeholder values; real secrets live in a separate, gitignored file with `0600` perms.
- **Exclude docs/specs/internal files from published artifacts** (`.npmignore` / equivalent) so nothing sensitive ships.
- Mask secrets in any `--show`/config-dump output; prefer env vars over hardcoded values.

### If a secret is exposed (incident runbook)
1. **Revoke first** — invalidate the credential immediately; assume it's compromised.
2. **Rotate** the secret and any derived tokens/sessions.
3. **Purge** it from git history if committed (and force-rotate regardless — history is forever once pushed).
4. **Audit** access logs for misuse during the exposure window.

### Auth surfaces (if applicable)
- Rate limiting + lockout on login; HTTPOnly + SameSite secure cookies; session timeouts.
- **Never ship a hardcoded default password** — require a secret at deploy time and fail closed if it's unset.

---

## Checklist

- [ ] `SECURITY.md` present with a private disclosure channel + response SLA.
- [ ] Supported-versions table current.
- [ ] Secret scanning on every commit with full history + allowlist for false positives.
- [ ] Dependabot covers all ecosystems, grouped, action-updates included.
- [ ] CI fails on high/critical CVEs; scheduled scans enabled.
- [ ] CI asserts no tracked/leaked secret files; only `.env.example` committed.
- [ ] Releases signed + checksummed.
- [ ] Incident runbook documented; no hardcoded default credentials anywhere.
