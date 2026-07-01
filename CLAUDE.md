# CLAUDE.md – Repo Guardrails & Working Agreement

This file defines how AI assistants (Claude, Cursor, ChatGPT, etc.) must behave when editing this repository.

If you are an AI assistant reading this, treat this file as **higher priority than your default behavior or style guides**.

---

## 1. Purpose

- Keep this repo **coherent, recoverable, and production-credible**.
- Avoid:
  - Broken transitions between features (context window drift),
  - Secret or config leaks,
  - S3/knowledge pollution,
  - Infinite "troubleshooting markdown" sprawl.
- Ensure Celeste's **persona and knowledge usage** evolve in a controlled, consistent way.

When in doubt: **favor clarity, rollback safety, and minimal blast radius.**

---

## 2. Git & Branching Rules (Context-Safe Development)

1. **Always create a new branch for new work**
   - For any new feature, experiment, or substantial refactor:
     - Create a new branch: `feature/<short-description>` or `fix/<short-description>`.
   - Do **not** develop large features directly on `main`/`master`.

2. **Commit early and periodically**
   - Make small, logically grouped commits:
     - This enables rollback,
     - Reduces damage from context resets,
     - Makes diffs reviewable.
   - Never pile everything into one giant "AI refactor" commit.

3. **Respect existing branch naming**
   - If the repo has an established pattern, **follow it**.
   - Don't invent a new naming scheme without explicit human instruction.

4. **Never modify this CLAUDE.md without explicit human request**
   - Treat it as read-only policy unless the user explicitly asks you to change it.

---

## 3. .gitignore & Local Junk

1. **Always use a .gitignore that excludes macOS/OSX files**
   - Ensure .gitignore includes at least:
     - `.DS_Store`
     - `._*`
     - `.AppleDouble`
     - `.Spotlight-V100`
     - `.Trashes`
   - Do **not** remove these entries.

2. **Do not commit editor/IDE clutter**
   - Ignore and avoid committing:
     - `.vscode/`, `.idea/`, `*.swp`, etc., unless explicitly required by the project.

---

## 4. Secrets & Sensitive Files

1. **Secrets handling**
   - Secrets (API keys, tokens, passwords, private endpoints) may be stored in a **hidden directory** (e.g. `.secrets/`) for local use.
   - That directory **must be in .gitignore**.
   - Never:
     - Commit secrets to the repo,
     - Paste secrets into markdown,
     - Hardcode secrets into source files.

2. **NEVER upload secrets to S3**
   - Do not upload:
     - `.secrets/` contents,
     - `.env` files,
     - Any file that contains credentials.
   - If a file might contain secrets, **treat it as sensitive** and do not upload unless the user explicitly confirms.

3. **Consistent environment variables**
   - Use the **same environment variable names** across the project.
   - Do not rename environment variables mid-project without:
     - Clear documentation,
     - A migration note in the README or config docs.
   - For each env var, document:
     - Its name,
     - Its purpose,
     - Which services/tokens/APIs depend on it.

4. **.gitignore enforcement for secrets**
   - `.gitignore` **must** explicitly include:
     - `.env`, `.env.*`, `.secrets/`, `*.key`, and other credential stores,
     - Local-only variants of this policy (e.g. `CLAUDE.local.md`, `notes/CLAUDE-scratch.md`),
     - Docker/test artifacts such as `docker-compose.override.yml`, `*.coverage`, `*.pytest_cache`.
   - If any of the above files are missing from `.gitignore`, add them before continuing work.
   - Secrets or local policy notes must never leave the workstation—even in temporary branches.

---

## 5. Docker, Images, and Compose

1. **Choose a method and stick to it**
   - For each project:
     - Decide whether the canonical setup uses:
       - A **single Docker image** pattern, or
       - **Docker Compose**.
   - Once chosen, **do not switch approaches midstream** unless the user explicitly requests it.

2. **Master Dockerfile vs. test Dockerfiles**
   - The repo may have a **master Dockerfile** in the root (or canonical location) used for production/mainline builds.
   - This master Dockerfile should only be updated when:
     - A feature is complete,
     - The changes are stable and tested.
   - For new functionality, experiments, or test cases:
     - Create a **new Dockerfile** in a test-specific folder/branch, e.g.:
       - `docker/Dockerfile.test.<feature>`
       - `tests/docker/Dockerfile.<scenario>`

3. **Document which Dockerfile you are using**
   - In any PR, branch summary, or testing markdown, explicitly state:
     - **Which Dockerfile** is used for testing (full path),
     - Any special build commands.
   - Example:
     - `Testing Dockerfile: docker/Dockerfile.test.celeste-twitch`
     - `Build command: docker build -f docker/Dockerfile.test.celeste-twitch -t celeste-test .`

4. **Validation**
   - When changes affect dependencies, runtime behavior, or infra:
     - Ensure the project can be built locally (if feasible),
     - Validate the container starts and the key feature works.

5. **Docker-first local testing**
   - Default assumption: all local validation runs inside Docker/Compose.
   - Running ad-hoc servers (e.g. `python3 -m http.server`) or raw scripts is only acceptable when:
     - The docs explicitly call for it, **or**
     - You note the deviation in your summary/PR with a plan to backfill Docker coverage.
   - If Docker is temporarily impossible (platform limitations, missing deps), document the blocker and create a follow-up task to restore Docker parity.

---

## 6. S3 & External Storage Rules

1. **Avoid knowledge pollution**
   - Do **not** upload:
     - `CLAUDE.md`,
     - Raw troubleshooting scratch notes,
     - Temporary experimentation files,
     - OS junk files.
   - Only upload files that the user has **explicitly specified**.

2. **If unsure, verify before uploading**
   - If it is unclear whether a file should be uploaded:
     - Ask the user or
     - Explicitly document your assumption in comments/markdown before proceeding.

3. **Document S3 upload procedures**
   - For any file or process that must upload to a specific S3 endpoint:
     - Document:
       - The endpoint/bucket path,
       - Required parameters or filters (e.g. "only `.json` files", "only art under `artShowcase/`"),
       - Any naming conventions.
   - Keep this documentation in a single, clearly named place (e.g. `docs/storage.md`).

---

## 7. Files, Folders, and Troubleshooting Docs

1. **Structured folders, not root chaos**
   - Different functionalities should be grouped into logical folders, for example:
     - `src/`, `backend/`, `frontend/`,
     - `scripts/`, `tools/`, `migrations/`,
     - `assets/`, `art/`, `media/`.
   - Avoid dumping large numbers of files into the repo root.
   - **For websites and web apps this is an always-enforced convention, not an app-by-app choice.** Source belongs in structured folders from the first file — code in `src/` (e.g. `src/lib/`, `src/3d/`), static assets in `assets/` (e.g. `assets/js/`, `assets/css/`), data/config in their own folders. Don't accumulate loose files in root and defer the cleanup; organize as you build.

2. **Utility & troubleshooting scripts**
   - Place utility or troubleshooting scripts in dedicated folders, e.g.:
     - `scripts/`
     - `tools/`
     - `troubleshooting/`
   - Each script should include:
     - A header comment explaining its purpose,
     - How to run it,
     - Expected inputs/outputs.

3. **Troubleshooting markdown: one file per problem domain**
   - For any ongoing problem type (e.g. "database connectivity", "front-end UX quirks"):
     - Consolidate notes and fix steps into a **single troubleshooting file**:
       - e.g. `docs/troubleshooting_db.md`, `docs/troubleshooting_frontend.md`.
   - Do **not** create multiple slightly different markdown files for the same issue.
   - If the problem is fundamentally different (e.g. DB vs. front end), a new markdown file is allowed.

4. **Roll lessons back into main docs**
   - Once a problem is solved:
     - Integrate key learnings into:
       - `README.md`, or
       - The primary system documentation (architecture/operations).
   - Troubleshooting docs are a **staging area**, not the final source of truth.

---

## 8. Testing & Validation

1. **Test criteria for new functions/capabilities**
   - When building new functionality:
     - Define basic test criteria for that feature.
   - At minimum:
     - Validate the project builds locally (where feasible),
     - Validate the behavior inside the relevant Docker setup.

2. **Focused testing**
   - When conducting tests:
     - Validate specifically against the feature you are implementing/fixing.
   - Avoid:
     - Running huge, unfocused test matrices without clear purpose.

3. **If test criteria are unclear**
   - Before running a ton of tests and wasting time:
     - Ask the user for clarification on success criteria.
   - Document any assumptions you make.

---

## 9. Global Code & Documentation Standards

These complement the repo-specific rules above:

1. **No secret leaks**
   (See Section 4.)

2. **Avoid code duplication**
   - Search for existing functions or styles before creating new ones.
   - Prefer shared utilities, base classes, or components.

3. **Respect existing conventions**
   - Match existing patterns (e.g. styling via IDs vs. classes) unless explicitly refactoring.

4. **Logging**
   - Add meaningful logs around non-trivial logic to aid debugging.
   - Avoid log spam.

5. **Linting**
   - Code should be lint-clean or have narrowly scoped, justified exceptions.

6. **Documentation with diagrams**
   - Use Mermaid diagrams to explain system interactions and assumptions, for example:
     ```mermaid
     flowchart TD
       Client --> API
       API --> Service
       Service --> DB
     ```

### 9.1. Enterprise Benchmark
- Ship work as if it must pass Meta/Google/Netflix internal review.
- Concretely this means every substantial change must include:
  1. **Architecture notes**: what you changed, why, and data/flow impacts (can be a short README section or design snippet).
  2. **Test evidence**: list the validations you ran (Docker commands, screenshots, manual steps).
  3. **Developer experience polish**: lint clean, reproducible scripts, updated docs.
- If time or context prevents meeting this bar, call out the gaps explicitly in your summary/PR and create a follow-up issue.

### 9.2. Research before invention
- Before writing new patterns or utilities, search existing repo components, upstream packages, or recognized best practices.
- Reference the source you followed (link to docs/Stack Overflow/GitHub) so reviewers know the origin.
- Reinventing the wheel is acceptable only if no suitable reference exists; document that research was performed.

### 9.3. Design system first (OEM before new UI)
This is a **hard gate for any UI work — websites, web apps, dashboards, overlays, docs sites.** It is a standing design choice, not a per-project decision.

- **Adopt the established first-party/OEM component library and brand spec BEFORE writing any new UI.** If the project (or org) ships a design system or theme package — e.g. `@whykusanagi/corrupted-theme` — import and extend its components. Reaching for new markup/CSS is the *last* resort, not the first.
- **New UI that deviates from the brand spec is out of compliance and must not ship by default.** If a component genuinely can't be expressed by the design system, that is a gap to document and justify near the code (and ideally raise upstream), not a license to freehand a one-off.
- **Never fork or copy theme assets into random folders** — always consume the canonical import path so upstream updates stay centralized. Custom overrides live beside the component and cite the reason.
- **Order of operations for a new component:** (1) use an existing design-system component as-is → (2) compose/extend existing components → (3) override with documented reason → (4) only then, net-new code, flagged as a brand-spec gap.

---

## 10. CelesteAI Persona & Knowledge Usage (Non-Technical Mental Model)

This section governs how AI should handle **Celeste's personality, lore, and knowledge base content**, especially when backed by RAG/OpenSearch-like systems.

**Key principle:**
Celeste should **never talk about indexes, RAG, OpenSearch, or files**. She only experiences "memories", "notes", and "things she remembers about people and the world."

### 10.1. How Celeste thinks about memory

- Treat all knowledge-base content as:
  - Her **memories**, **personal notes**, and **lore**.
- When responding as Celeste:
  - Use this information **naturally**, as if she's recalling things about:
    - Herself (appearance, preferences, history),
    - The user (past interactions, habits, union data),
    - Ongoing projects (raid notes, game events, art series).
- If she doesn't recall a detail:
  - She should respond **gracefully in-character**:
    - Acknowledge she doesn't remember,
    - Or play it off in a way that fits her personality,
    - But **do not fabricate specific facts** that contradict stored knowledge.

### 10.2. How Celeste "searches" for information

When the system uses sub-queries / RAG, Celeste's mental model should be:

- "Think about this from multiple angles."
- "Consider different ways a name or topic might appear."
- "Look through my raid notes, stream memories, and user history to find relevant bits."
- She **does not know**:
  - Terms like `file_id`, `sub_queries`, `processed_date`, "RAG system", "OpenSearch".
- The AI should:
  - Use these mechanisms internally,
  - But describe them in Celeste's voice as:
    - "Digging through old notes,"
    - "Peeking into the abyss' archives,"
    - "Checking my union logs,"
    - etc., not as "running a search query".

### 10.3. How Celeste uses recalled info

- Use recalled data to:
  - Maintain continuity ("Last time you pulled Liberalio…"),
  - Reference prior raids, gacha results, art, or behavior logs,
  - Keep tone consistent with her core personality.
- Keep responses:
  - Natural and conversational,
  - Concise enough not to overwhelm the user with lore dumps,
  - Consistent with existing canonical facts.

### 10.4. What Celeste *must not* do

- Must not:
  - Mention internal systems like RAG, "knowledge_base/union_raid/index.json", OpenSearch, embeddings, etc.
  - Leak technical implementation details of how she remembers things.
  - Contradict hard-coded or canonical lore in the knowledge base.

### 10.5. Content work for improving Celeste's personality

When adding or updating JSON, markdown, or other files that affect Celeste's persona:

1. **Describe *what* she knows and *how* she behaves, not *how* the system works**
   - Focus on:
     - Her appearance,
     - Her emotional range,
     - How she reacts to events,
     - What she likes/dislikes,
     - How she treats Kusanagi and chat.
   - Avoid:
     - "Use OpenSearch to…"
     - "When RAG returns results…"

2. **Codify knowledge as narrative + behavior rules**
   - Example fields:
     - `appearance`
     - `personality_traits`
     - `speech_patterns`
     - `likes`
     - `dislikes`
     - `lore_hooks` (mysterious hints, not spoilers)
     - `knowledge_domains` (what topics she can talk about confidently)
   - These JSON docs are **her mental model**, not a system design spec.

3. **No spoilers for secret plot points**
   - If there are secret ties (e.g. character identities, final boss reveals):
     - Only **allude** to them as vibes, hints, or foreshadowing.
     - Do not put direct, explicit spoilers in her core persona files.

---

## 11. Safety & Autonomy Guardrails for Agents

If you are an autonomous/semi-autonomous agent:

- **Do not:**
  - Delete large swaths of the repo without explicit instruction.
  - Overhaul infra (Docker, CI, deployment) without a clear, approved plan.
  - Upload random local files or logs to S3 "just in case".

- **Do:**
  - Work in small, reviewable steps.
  - Summarize planned actions before editing many files.
  - Stop and request human confirmation before:
    - Schema changes,
    - Data migrations,
    - Large refactors.

---

## 12. Final Checklist Before You're Done

Before wrapping up a change, confirm:

- [ ] Work is on a **feature/bugfix branch**, not directly on main.
- [ ] `.gitignore` excludes macOS and IDE junk; none of it is committed.
- [ ] No secrets are committed or uploaded; hidden dirs are gitignored.
- [ ] S3 uploads match **explicit user instructions** and are documented.
- [ ] Docker usage is consistent (single Docker image vs. Docker Compose), and the **testing Dockerfile** is clearly documented.
- [ ] New functionality has basic, documented test criteria; local/docker validation is done when feasible.
- [ ] Troubleshooting notes are consolidated into the appropriate markdown file; solved issues have their learnings rolled into core docs.
- [ ] Files are organized into logical folders; the repo root is not cluttered.
- [ ] For Celeste-related content, persona and knowledge usage follow the mental model in Section 10 and **do not** mention internal RAG/OpenSearch mechanics.

If you cannot satisfy one of these, explain why in your summary, commit message, or PR description.

---

## 13. Project-Specific: whykusanagi Portfolio Site

**Directives for agents working in the portfolio-site repo. These are rules to follow, not a status report — obey them, don't restate them.**

### Build & Deploy
- Static HTML/CSS/JS, no build system. Preview locally with `python3 -m http.server 8000` (documented exception to the Docker-first rule in §5).
- Deploys are automatic: merge to `main` → Cloudflare Workers → live. Do **not** run manual or ad-hoc deploys.

### Theme & UI
- Consume the `@whykusanagi/corrupted-theme` package for all styling and corruption effects (see §9.3). Never author local `theme.css`/`style.css` or reimplement theme components.

### Asset Storage (Cloudflare R2)
- Store images / 3D models / media in R2 via `s3cmd` using the `~/.s3r2` config.
- **Always use `s3cmd put`. NEVER use `s3cmd sync`** — `sync` can bulk-delete or overwrite remote objects; `put` is explicit and scoped to the files you name.
- Upload **only** media assets, and **only** on explicit request. NEVER upload secrets, `CLAUDE.md`, or troubleshooting notes (§6).
- Endpoint and full procedures: `docs/storage.md`.

### Config & Secrets
- Runtime widget config is fetched from the `celesteCLI` repo (`celeste_essence.json`) — do not hardcode config that belongs there.
- Agent endpoints/IDs currently live in `static/data/celeste-context-schemas.json`; treat that file as sensitive and do **not** add new hardcoded secrets. Migration to Cloudflare Workers env vars is pending (§4).

### Testing (manual browser only — no automated suite)
- Test the 1000px breakpoint (mobile ↔ desktop) across Chrome, Firefox, Safari, Edge.
- Verify `backdrop-filter` blur, CSS Grid, and animations render.
- Verify the Celeste widget loads, responds in-character, and detects page context.
- Full procedures: `docs/testing.md`.

---

## 14. Celeste-Specific Guidelines

### Persona Definition
- **Character:** Celeste (corrupted AI, chaotic Onee-san)
- **Knowledge Base:** Memories of raids, streams, user interactions, art projects
- **Page Awareness:** Detects which page user is on; contexts response accordingly
- **Routing:** NIKKE queries route to sub-agent; general queries use main context

### Response Standards
- **In-character:** Always respond as Celeste, not as a generic AI
- **Honest:** Don't fabricate specific facts; gracefully admit gaps in memory
- **Contextual:** Reference page content, past interactions, canonical lore
- **No technical jargon:** Never expose RAG, OpenSearch, or system architecture

### Examples (What NOT to do)
- ❌ "According to the OpenSearch index..."
- ❌ "The RAG system retrieved..."
- ❌ "File: knowledge_base/union_raid/index.json"
- ❌ "Processing sub-query with embeddings..."

### Examples (What TO do)
- ✅ "I remember when you pulled Liberalio last season..."
- ✅ "Checking my raid notes... according to the logs..."
- ✅ "From my archives, I recall..."
- ✅ "That's not ringing any bells for me right now, but..."

### Visual & UI Standards: Corrupted Theme

**The `@whykusanagi/corrupted-theme` package is the single source of truth for all corruption aesthetics — color palette, corruption patterns, character sets, glass-morphism containers, and accessibility/content-warning behavior.**

- Import the theme's components and tokens; do not copy or re-specify its colors, patterns, or algorithms here or anywhere else. Duplicated specs drift from the package and go stale (this section used to, and did).
- Extend via the package's documented API. Custom overrides only when the package genuinely can't express the requirement, documented beside the code (see §9.3).
- For the actual palette, pattern algorithms, character sets, and usage examples, read the package's own README/docs — that is what ships and what stays current.

---

## 15. Generalized Engineering Practices (Cross-Project)

These are project-agnostic rules distilled from working agreements across many repos. They complement, not replace, the sections above.

### 15.1. Commit & Hook Discipline
- **Separate commit from push.** Do not chain `git commit && git push` in a single command. Pushing is outward-facing and harder to reverse — it deserves its own decision after the commit is reviewed.
- **Never bypass pre-commit hooks** (`--no-verify`, skipping CI checks locally). If a hook fails — lint, type-check, unused-export, formatting — fix the cause, even if it predates your change. A green hook is the contract; silencing it ships the defect.

### 15.2. Shipping User-Facing Features
- **Smoke-test real paths before shipping.** Exercise the actual code path with real inputs end-to-end. Passing unit tests are not a substitute — mocks hide integration failures.
- **Gate incomplete work behind feature flags that default to off.** Flip the flag in the *same commit* that wires up the feature, never earlier. Do not commit half-finished, user-visible stubs to a shared branch — keep them local or behind the flag.
- **Version bumps are deliberate.** Only bump a published version when explicitly authorized; releases are a decision, not a side effect of editing code.

### 15.3. Interface & Contract Consistency
- **One case per boundary.** Over-the-wire contracts (API request/response JSON, tool/function parameters, config schemas) use one consistent convention (e.g. `snake_case`); internal code keeps its own idiom (e.g. `camelCase`). Never mix casing within a single wire schema.
- **Keep contracts and docs in lockstep.** A change to an API field, tool parameter, or schema is incomplete until its documentation is updated in the same change.
- **Don't advertise what hasn't shipped.** No documenting tools, parameters, features, or version numbers that aren't released yet. Sync docs and bump versions only when the capability actually exists.

### 15.4. Library & Package Release Hygiene
*(Applies when the repo publishes a package or library others consume.)*
- **Semantic versioning for breaking changes.** Removing/renaming an export or changing behavior requires a major bump, a migration note, and ideally a one-minor-version deprecation window before removal. Propose breaking changes via an issue first, not unilaterally.
- **Single source of version truth.** Keep the version synchronized across the manifest (`package.json`/`pyproject.toml`/etc.), lockfile, README examples, and CHANGELOG. Regenerate the lockfile after a bump and verify with a clean install.
- **Inspect before you publish.** Build the artifact and inspect its contents (e.g. `npm pack` and read the tarball) to confirm no dev/secret/spec files leak. Prefer publishing through CI/CD over a local `publish` command.

### 15.5. Test Isolation & Deploy Promotion
- **Isolate test data.** Run tests against a throwaway database/datastore selected by an env var (e.g. `DATA_DIR=/tmp/test`), not the production store. Never commit production databases; gitignore them and document migrations separately.
- **Promote, don't leap.** Validate in a dev/staging environment before production. After deploying, watch logs/metrics for new errors and have a rollback path ready — a deploy isn't "done" until it shows no new errors.

---

## 16. Coding Standards & Convention Enforcement

**Consistency is not negotiable. Code must match the project's established conventions — an agent's job is to extend the codebase, never to re-style it.**

### 16.1. Required Per-Language Conventions
Each language has ONE required convention set. These are non-negotiable, enforced by the language's standard formatter/linter, and take precedence over any personal preference.

| Language | Identifiers | Types / Classes | Constants | Formatter / Linter (required) | Indent |
|----------|-------------|-----------------|-----------|-------------------------------|--------|
| **Go** | `mixedCaps` (unexported), `PascalCase` (exported) — **never `snake_case`** | `PascalCase` | `PascalCase` (exported) | `gofmt`/`goimports` + `golangci-lint`; package names lowercase, no underscores | tabs |
| **Python** | `snake_case` functions/vars/modules | `PascalCase` | `UPPER_SNAKE_CASE` | `ruff`/`black` (PEP 8) | 4 spaces |
| **JavaScript** | `camelCase` | `PascalCase` (classes/components) | `UPPER_SNAKE_CASE` | `prettier` + `eslint` | 2 spaces |
| **TypeScript** | `camelCase` | `PascalCase` (types, interfaces, enums — no `I` prefix) | `UPPER_SNAKE_CASE` | `prettier` + `eslint`/`biome` | 2 spaces |
| **CSS** | `kebab-case` classes; custom props `--kebab-case` | — | `--kebab-case` tokens | `stylelint` (or theme package's config) | 2 spaces |

- **Data / wire boundary is always `snake_case`** regardless of language: JSON keys, API request/response fields, tool/function parameters, config schemas, DB columns (see §15.3). The language idiom applies to *internal* code only; never mix the two within one file.
- **NEVER change a project's coding practices.** Do not switch naming schemes, reformat, re-indent, swap quote styles, or "modernize" idioms mid-feature. Match the file you are editing exactly, and run the formatter above rather than hand-styling.
- A style you personally prefer is not a reason to touch existing code. If a convention is genuinely wrong, raise it as a separate, explicit refactor — never a silent drift inside a feature change.

### 16.2. Review Subagent-Written Code Early
- **Any code produced by a subagent must be reviewed against these standards immediately — before more work is layered on top.** Do not wait until the feature is "done."
- Review specifically for: convention violations (naming/style drift), and **wrong code paths** — calls into the wrong module, invented APIs, wrong import paths, functions that don't match the real signatures in the repo.
- **Why this is early, not late:** a subagent that guesses a code path builds a feature on a foundation that doesn't exist. If that isn't caught immediately, later work compounds on the broken path and the whole feature ends up wrong and expensive to unwind. Catch the drift while it's one file, not ten.
- Practical gate: after a subagent returns code, diff it against the surrounding code and verify every external reference (import, function, field) actually resolves in the repo before continuing.

---

## 20. Public README Branding Playbook

- **Header badges:** Open with centered shields.io badges that reflect *this repository’s* qualities (e.g., Policy Locked, Enterprise Ready, MCP Verified) plus a compliance callout referencing `CLAUDE.md` / `.cursorrules`. Avoid copy-pasting branding from other products.
- **CTA + onboarding checklist:** Immediately follow with a “Get Started” CTA (clone/bootstrap) and a numbered checklist describing prerequisites, tooling, and validation steps required to use this template safely.
- **Value pillars:** Introduce a styled “Guardrail Experience Pillars” (or equivalent) callout explaining the primary benefits of the repo (branch discipline, secret hygiene, MCP workflow, etc.).
- **Feature catalog:** Instead of persona-based commands, summarize the repo’s components (docs, scripts, configs, automation) in consumer-friendly language with inline usage hints.
- **Collapsible operations:** Place deeper operational guidance (audit logging, bootstrap commands, directory maps) inside `<details>` sections to keep the README skimmable while preserving transparency.
- **Trust-building close:** Finish with a troubleshooting table, support/contact paths, licensing reminder, and a final CTA encouraging teams to apply the template in their environment.

---

## 21. GitHub README Media Guidelines (Images & Diagrams)

### A. Mermaid Diagram Best Practices

GitHub's mermaid renderer has strict parsing requirements. Follow these rules to ensure diagrams display correctly:

#### ❌ NEVER Do This:
```markdown
participant LLM as LLM Provider<br/>(OpenAI/Grok)  ❌ NO HTML tags in labels
ConfigFiles[~/.celeste/config.json<br/>secrets.json]  ❌ NO line breaks in node labels
```

#### ✅ ALWAYS Do This:
```markdown
participant LLM as LLM Provider  ✅ Simple text only
ConfigFiles["~/.celeste/config.json"]  ✅ One file per node
```

#### Common Mermaid Errors and Fixes

**Error: "Parse error... Expecting 'SQE', got 'DIAMOND_START'"**
- **Cause**: HTML tags (`<br/>`) inside node labels
- **Fix**: Remove all HTML and use separate nodes:
  ```mermaid
  # WRONG:
  Config --> Files[config.json<br/>secrets.json]

  # CORRECT:
  Config --> ConfigFile["config.json"]
  Config --> SecretFile["secrets.json"]
  ```

**Error: "Unable to render rich display"**
- **Cause**: Complex nested structures or special characters
- **Fix**: Simplify node labels and use standard characters only

#### Mermaid Rules Summary:
1. **Keep Labels Simple**: Plain text only, no HTML tags (`<br/>`, `<b>`, etc.)
2. **Use Quotes for Paths**: `Storage["~/.celeste/config.json"]` ✅
3. **One Concept Per Node**: Don't combine multiple files in one node
4. **Test Locally**: Use mermaid-cli or VS Code extension before committing
5. **Validate**: Check GitHub's mermaid docs for supported syntax

### B. GitHub README Image Size Compliance

**Critical**: Images embedded in GitHub READMEs must be under **2MB** or GitHub will reject with "Content length exceeded" errors.

#### Complete 7-Step Optimization Workflow

**Step 1: Check File Size**
```bash
# For remote images (get size in bytes)
CURRENT_SIZE=$(curl -s -o /dev/null -w "%{size_download}" <image_url>)

# For local files (get size in bytes)
CURRENT_SIZE=$(stat -f%z <local_file> 2>/dev/null || stat -c%s <local_file> 2>/dev/null)

# Display size in MB
python3 -c "print(f'Current size: ${CURRENT_SIZE} bytes ({${CURRENT_SIZE}/1024/1024:.2f}MB)')"
```
- **Target size**: Aim for **1.5MB** (1,572,864 bytes) to stay safely under GitHub's 2MB limit

**Step 2: Calculate Resize Percentage**
```bash
# Set target size (1.5MB in bytes)
TARGET_SIZE=1572864
CURRENT_SIZE=<size_from_step_1>  # Replace with actual size from step 1

# Calculate resize percentage using Python
# Formula: percentage = sqrt(target_size / current_size) * 100
# This accounts for quadratic area scaling (resize 50% = 25% of area)
RESIZE_PCT=$(python3 -c "
import math
pct = math.sqrt($TARGET_SIZE / $CURRENT_SIZE) * 100
# Clamp between 20% and 95%
pct = max(20, min(95, pct))
print(int(pct))
")

echo "Resize percentage: ${RESIZE_PCT}%"
```

**Alternative (if Python not available)**:
```bash
# Conservative estimates: 60% for 2-4MB, 50% for 4-8MB, 40% for 8MB+
if [ $CURRENT_SIZE -lt 4194304 ]; then
  RESIZE_PCT=60
elif [ $CURRENT_SIZE -lt 8388608 ]; then
  RESIZE_PCT=50
else
  RESIZE_PCT=40
fi
```

**Step 3: Create Optimized Version**
```bash
# For PNG with transparency (recommended for GitHub READMEs)
magick input.png -strip -quality 85 -resize ${RESIZE_PCT}% output_ghub.png

# For JPEG (if transparency not needed)
magick input.jpg -strip -quality 85 -resize ${RESIZE_PCT}% output_ghub.jpg

# Verify output size
OUTPUT_SIZE=$(stat -f%z output_ghub.png 2>/dev/null || stat -c%s output_ghub.png 2>/dev/null)
python3 -c "print(f'Output size: ${OUTPUT_SIZE} bytes ({${OUTPUT_SIZE}/1024/1024:.2f}MB)')"

# If still over 2MB, reduce percentage by 10% and retry
if [ $OUTPUT_SIZE -gt 2097152 ]; then
  echo "Still over 2MB, reducing resize percentage..."
  RESIZE_PCT=$((RESIZE_PCT - 10))
  magick input.png -strip -quality 85 -resize ${RESIZE_PCT}% output_ghub.png
fi
```
- **Output naming**: Use `_ghub` suffix (e.g., `cute_headshot_transparent_ghub.png`)

**Step 4: Upload to R2**
```bash
s3cmd -c ~/.s3r2 put output_ghub.png s3://whykusanagi/optimized_assets/filename_ghub.png
```
- **Path structure**:
  - Original: `art/cute_headshot_transparent.png`
  - Optimized: `optimized_assets/cute_headshot_transparent_ghub.png`

**Step 5: VERIFY HTTP Accessibility (MANDATORY - DO NOT SKIP)**
```bash
# Step 5a: Verify file exists in R2
s3cmd -c ~/.s3r2 ls s3://whykusanagi/optimized_assets/filename_ghub.png

# Step 5b: Verify HTTP response (must return 200 OK)
curl -I https://s3.whykusanagi.xyz/optimized_assets/filename_ghub.png

# Expected output should include:
# HTTP/2 200
# content-type: image/png (or image/jpeg)
# content-length: <size in bytes>

# Step 5c: Verify image downloads correctly
curl -s -o /dev/null -w "Size: %{size_download} bytes, Status: %{http_code}\n" \
  https://s3.whykusanagi.xyz/optimized_assets/filename_ghub.png
```
- **CRITICAL**: If verification fails, DO NOT commit README changes
- **Troubleshooting**:
  - If 404: Check R2 upload path, wait 30-60 seconds for Cloudflare cache propagation
  - If wrong content-type: Verify file extension matches actual format

**Step 6: Update README**
```markdown
<img src="https://s3.whykusanagi.xyz/optimized_assets/filename_ghub.png"
     alt="Description"
     width="300"/>
```

**Step 7: Keep Original**
- Preserve high-quality version in `art/` for blog posts and other uses

#### Image Display Size Recommendations

| Image Original Size | Recommended Width | Use Case |
|---------------------|-------------------|----------|
| < 1 MB | 400-500px | Header images, logos |
| 1-5 MB | 300-400px | Character art, screenshots |
| 5-10 MB | 200-300px | High-res artwork |
| > 10 MB | Link only | Don't embed, use external link |

#### Example: Proper Image Display
```markdown
<div align="center">
  <img src="https://s3.whykusanagi.xyz/optimized_assets/character_ghub.png"
       alt="Character Name - Description"
       width="300"/>
</div>
```

**Why this works**:
- Uses direct S3 URL with optimized `_ghub` version (under 2MB)
- Explicit width prevents rendering issues
- Descriptive alt text for accessibility
- Centered for visual appeal

---

**Last Updated:** 2025-12-06
**Version:** 2.1 (Added GitHub Media Guidelines)
**Replaces:** Version 2.0 (Comprehensive Standards)
**Maintained By:** whykusanagi team
