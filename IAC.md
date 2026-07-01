# IAC.md — Infrastructure as Code & CI/CD Playbook

Generalized, reusable conventions for CI/CD pipelines, containerization, release automation, and deployment. Fill the `<placeholders>` with your own registry, domains, secret names, and versions. This complements the guardrails in `CLAUDE.md`; nothing here overrides those.

> **Principle:** infrastructure is code — version it, review it, and let CI enforce it. Nothing reaches production that a pipeline didn't build, test, and gate.

---

## 1. CI Pipeline Structure

**Triggers**
- Gate merges on `pull_request`; also run on `push` to the default branch (post-merge sanity) and expose `workflow_dispatch` for manual re-runs.
- Cancel superseded runs: a `concurrency` group keyed on `${{ github.event.pull_request.number || github.ref }}` with `cancel-in-progress: true`.
- Use `paths` / `paths-ignore` to skip expensive builds on docs/config/media-only changes.

**Job layout**
- Split into parallel single-purpose jobs — `lint`, `test`, `security`, `container-test`, `build` — not one monolith.
- Gate the build behind the quality jobs: `needs: [lint, test, container-test]`, so an artifact is only produced after checks pass.
- Scope permissions to the minimum per job (`permissions: contents: read`); elevate only where a job needs it.
- Add `timeout-minutes` to bound runaway jobs, and `if: always()` on log/report/artifact-upload steps so diagnostics survive failures.

**What "pass" means (make these hard failures)**
- **Formatting:** run the formatter in list mode and assert empty output (e.g. `test -z "$(gofmt -l .)"` / `prettier --check`).
- **Lint:** zero warnings, or narrowly-scoped, justified suppressions.
- **Tests:** run with the race/thread checker on where available; enforce a **coverage threshold** and fail below it.
- **Build validation:** assert the artifact exists and is non-empty, and that declared package `exports`/entrypoints resolve on disk — don't trust exit code 0 alone.
- Add a job that compiles the **full** artifact (not just the sub-package unit tests exercise) to catch embed/binding/link mismatches.

**Canonical stages seen in practice**
```
format/vet → lint → test (race + coverage) → security (secret-scan + vuln-scan)
           → container-test (compose integration + image smoke) → build (gated, version-stamped)
           → release (archive + checksum + sign + publish) → deploy (branch-gated)
```

---

## 2. Caching & Matrix Builds

- **Cross-OS matrix** (`ubuntu`, `macos`, `windows`) to catch platform-specific bugs; guard OS-specific steps with `if: matrix.os == ...`.
- Run coverage/upload on **one canonical matrix cell** only (`if: matrix.os == 'ubuntu-latest' && matrix.version == '<primary>'`) to avoid duplicate reports.
- Prefer the language setup action's built-in cache (`cache: npm` / `cache: true`) over hand-rolled cache steps.
- When hand-rolling, **key the cache on the lockfile hash** with a restore-key fallback:
  `key: ${{ runner.os }}-<eco>-${{ hashFiles('**/<lockfile>') }}`.
- **Cache Docker layers** via the Actions backend: `cache-from: type=gha`, `cache-to: type=gha,mode=max`.
- **Pin the toolchain from the project file** (`go-version-file: go.mod`, `.nvmrc`, `.tool-versions`) so CI and repo never drift.

---

## 3. Release Automation

- **Two-stage release:** an automated version-bump/CHANGELOG PR (e.g. release-please) maintained on the default branch → merging it creates the tag → the tag triggers the build-and-publish workflow.
  - Release automation that creates tags needs a **PAT, not the default token** — tags created by the default `GITHUB_TOKEN` do not trigger downstream workflows. Fall back safely: `secrets.<RELEASE_TOKEN> || secrets.GITHUB_TOKEN`.
- **Tag-triggered builds:** `on: push: tags: ['v*']`. Derive the version from the ref: `VERSION=${GITHUB_REF#refs/tags/v}`.
- **Stamp version + commit into the artifact** at build time (linker flags / build args), so a shipped binary can self-report its provenance.
- **Cross-compile a release matrix** (OS × arch) from one runner where the toolchain allows; build on the **native runner** when the target requires it (e.g. real Windows binaries).
- Ship **self-contained** artifacts where possible (e.g. `CGO_ENABLED=0`) and document the tradeoff.
- **Package per-platform archives + generate SHA256 checksums** for every artifact.
- **Sign releases in CI** (GPG-sign the checksum manifest, or use signed tags/commits) using non-interactive/loopback pinentry; publish signatures alongside artifacts and document verification steps.
- Auto-flag pre-releases from the tag: `prerelease: ${{ contains(github.ref_name, '-') }}`. Let the platform generate release notes.
- **Fail loudly on missing outputs:** `if-no-files-found: error` / `fail_on_unmatched_files: true`.

---

## 4. Docker & Containers

- **One canonical setup per repo** (single image *or* Compose) — add a CI step that fails if stray `Dockerfile*` / `docker-compose*` files appear. Test-only variants go in a dedicated folder with explicit names (see `CLAUDE.md` §5).
- **Multi-stage builds:** heavy toolchain in a `builder` stage, minimal runtime image (e.g. alpine/distroless) in the final stage.
- **Layer for cache:** copy lockfiles and fetch dependencies *before* copying source (`COPY <manifest> <lock>` → install → `COPY . .`).
- **Run as a non-root user** created in the image (`adduser`, uid ≥ 1000, `COPY --chown`).
- CGo/native toolchains needed at build time can be dropped at runtime — enable them only in the builder stage; document why.
- **Integration tests via Compose:** mock external dependencies, gate on `depends_on: condition: service_healthy` with a `healthcheck`, and propagate the exit code:
  `docker compose up --abort-on-container-exit --exit-code-from <test-runner>`.
- **Smoke-test the built image** before deploy: run the container, wait, `curl -f <health-endpoint>`, stop.
- **Build on PRs, push on merge:** `push: ${{ github.event_name != 'pull_request' }}`.
- **Derive image tags from git context** (`docker/metadata-action`: branch/PR ref, sha prefix, `latest` on default branch).
- **Restrict build platforms to what you deploy** (`platforms: linux/amd64`) to halve build time; document the choice.
- **Registry login via the ephemeral job token** (`docker/login-action` with `github.actor` / `secrets.GITHUB_TOKEN`).

---

## 5. Deploy Targets

Pick per project; gate every deploy job on branch + event and `needs: [build]`:
`if: github.ref == 'refs/heads/main' && (github.event_name == 'push' || github.event_name == 'workflow_dispatch')`.

- **Edge / serverless (e.g. Cloudflare Workers):** named environments in config (`[env.production]` / `[env.development]`), pinned `compatibility_date`, route/zone bindings, resource bindings (KV, D1, static assets) declared in config, and observability + source-map upload enabled for prod debugging. Document non-obvious invocations *in the config file itself*.
- **Container registry:** build image in CI, tag from git context, push on merge.
- **VM / droplet (SSH pull-and-restart):** authenticate to registry → `docker pull` → stop/rm old → `docker run --restart unless-stopped --env-file <file>`; use `set -e`, a bounded `command_timeout`, and pass only a **whitelisted** env allowlist into the remote shell.
- **Declarative PaaS:** deploy from a spec file via the vendor CLI (e.g. `<cli> apps create --spec <app>.yaml --wait`).

---

## 6. Secrets in CI

- **Inject every credential via the CI secret store** (`${{ secrets.* }}`) — registry tokens, SSH keys, signing keys, deploy tokens. Never commit them.
- **Runtime secrets live in the platform, not repo config.** Config files (`wrangler.toml`, `compose.yml`) only *document* required env vars as comments; real values are set via the platform (`wrangler secret put`, dashboard, `--env-file`).
- **Base64-encode multiline secrets** (e.g. a GPG private key) for safe transport through env vars; decode at point of use.
- **Full history only when needed:** `fetch-depth: 0` for steps that require it (secret scanning, release notes) — otherwise keep the shallow default.
- **Tests use fake/mock credentials** hardcoded in the test service (e.g. `API_KEY=test-key-12345`), never real ones.

---

## 7. CI/CD Cost Efficiency — run expensive jobs only when needed

CI minutes are not free, and the expensive minutes (native Windows/macOS runners, multi-arch binary builds, full packaging/signing) are the ones you want to spend **rarely**. The goal: fast, cheap validation on every PR; heavy builds only when cutting a release.

**Tier the work by trigger:**

| Runs on | Jobs | Rationale |
|---------|------|-----------|
| **Every PR + push** (cheap, fast) | format, lint, vet, **unit tests**, quick single-platform compile check, secret scan, dependency audit | This is the quality gate — must run every time, but it's all cheap Linux minutes. |
| **Release only** (`push: tags: ['v*']` / release event) | cross-platform binary matrix, **native Windows/macOS runners**, multi-arch builds, full packaging + checksums + signing, all-platform image builds | Expensive and only meaningful at release. Do **not** attach these to `pull_request`. |
| **On demand / nightly** (`workflow_dispatch` / `schedule`) | full cross-platform build if you want pre-release confidence, heavy e2e, scheduled security scans | Opt-in, not per-PR. |

**Concrete rules:**
- **Never build release binaries on `pull_request`.** A Windows runner spinning up to cross-compile on every PR is pure waste — that job belongs on the tag/release trigger only. Validate *that it compiles* on one platform in PR CI; build *all platforms* at release.
- **Don't run the full OS matrix on every PR.** Run the primary platform (e.g. `ubuntu-latest`) on PRs; run the `[ubuntu, macos, windows]` matrix only at release or nightly. Reserve cross-platform for when a platform-specific bug would actually ship.
- **Dependabot PRs get the cheap tier only.** A dependency bump needs lint + test + audit, not a Windows binary build. Combined with grouping + auto-merge (`RELEASE.md` §3), they cost minutes, not hours, and clear themselves.
- **Skip work that can't be affected:** `paths-ignore` for docs/media-only changes; `concurrency: cancel-in-progress` to kill superseded runs; cache dependencies + Docker layers (§2) so re-runs are cheap.
- **Restrict build platforms to what you deploy** (`platforms: linux/amd64`) rather than building arches you never ship (§4).
- **Split workflows by trigger** (a `ci.yml` on `pull_request`, a separate `release.yml` on `tags`) so the expensive file simply never fires on PRs — the cleanest way to guarantee the separation.

> Net effect: a feature PR or a dependabot bump runs minutes of cheap Linux CI; the multi-platform, signed binary build happens once, when you actually tag a release.

---

## Checklist

- [ ] PR-gated CI with cancel-superseded concurrency and least-privilege permissions.
- [ ] Expensive builds (native Windows/macOS, multi-arch binaries) run on release/tags only — never on PRs or dependabot.
- [ ] Format/lint/test are hard failures; coverage threshold enforced.
- [ ] Build gated behind quality jobs; full-artifact compile validated.
- [ ] Dependency + Docker-layer caching keyed on lockfile.
- [ ] Automated version-bump/CHANGELOG → tag → signed, checksummed release.
- [ ] One canonical container setup; multi-stage; non-root; smoke-tested.
- [ ] Deploy jobs branch+event gated; secrets from CI store; config documents (not stores) runtime secrets.
