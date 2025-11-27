# Repo Guardrails Template

A baseline template for Claude/Cursor-assisted development so we never have to restate coding standards, local nuances, or workflow rules from scratch. Drop these files into any repo to inherit the exact same guardrails.

## Files in This Template

| File | Purpose |
| --- | --- |
| `CLAUDE.md` | Authoritative working agreement and narrative persona guidance. Treat as read-only unless the user explicitly requests edits. |
| `.cursorrules` | Same rules as `CLAUDE.md`, formatted for Cursor so the agent always reads the complete policy before editing. |
| `bootstrap.py` | Generates config scaffolding (linters, directory layout, Docker, etc.) on demand. |
| `requirements.txt` | Locked Python toolchain (FastAPI, lint/test stack, detect-secrets) used immediately after bootstrapping. |

> `CLAUDE.md` and `.cursorrules` are **kept in lockstep**. Update both if policy changes so every assistant sees the same instructions.

## Quick Start

### Option 1: Full Project Bootstrap (Recommended)
```bash
cp .cursorrules /path/to/project/
cp CLAUDE.md /path/to/project/
cp bootstrap.py /path/to/project/
cd /path/to/project
python bootstrap.py
pip install -r requirements.txt
make setup   # installs pre-commit hooks defined by the template
npm install  # optional: only if using the frontend scaffold
make gen-config
```

### Option 2: Cursor-Only
Just copy `.cursorrules` (and optionally `CLAUDE.md` for humans). Cursor will auto-create files using the embedded templates when they are missing.

## Guardrail Themes at a Glance

| Section | Why it exists | Enterprise implication |
| --- | --- | --- |
| **Purpose & Expectations** | Keep the repo coherent, recoverable, and production-credible. | Default to clarity, rollback safety, and persona continuity instead of speculative coding. |
| **Git & Branching** | Preserve readable history and safe rollbacks. | Ship on `feature/` or `fix/` branches, commit in small units, and never touch `CLAUDE.md` without approval. |
| **.gitignore & Secrets Hygiene** | Prevent junk files and sensitive data from leaking. | Maintain the mandated `.gitignore`, store secrets in `.secrets/`/env vars, and document env usage in `docs/environment.md`. |
| **Docker, Storage, & Structure** | Ensure consistent runtime stories and organized repos. | Declare the canonical Docker flow, log deviations, centralize S3 steps in `docs/storage.md`, and keep code/tests/docs in the right folders. |
| **Testing & Quality Bar** | Provide audit-ready evidence for every change. | Define success criteria early, capture manual/browser proof, reuse existing utilities, and keep lint/format clean. |
| **Safety & Autonomy Guardrails** | Avoid runaway refactors or surprise infra edits. | Socialize multi-file plans, get confirmation before schema/migration work, and don’t delete large areas without approval. |
| **Final Checklist** | Catch last-mile regressions. | Before merge, verify branch hygiene, `.gitignore`, Docker docs, test evidence, S3 adherence, and Celeste persona compliance. |
| **Celeste Persona** | Maintain the corrupted Onee-san voice consistently. | Speak via “memories/notes,” stay page-aware, admit gaps honestly, and never mention RAG/OpenSearch mechanics. |
| **MCP & Cloud Workflow** | Keep deployments observable and reversible. | Always run the MCP check/status/log loop (`list_mcp_resources() → deploy → verify → logs`) and never assume tooling is unavailable. |
| **AI Assistant Checklist** | Align every agent with the same playbook. | Suggest `make precommit`, enforce Docker parity, reuse utilities, add Mermaid diagrams for architecture changes, and avoid unnecessary files. |
| **Project-Specific Notes** | Anchor the current whykusanagi portfolio setup. | Static HTML/CSS/JS via Cloudflare Workers, manual browser testing at the 1000px breakpoint and across browsers, Celeste widget config from `celesteCLI`, secrets refactor tracked on `feature/secrets-refactor`. |

## Included Templates

- Backend FastAPI skeleton (`src/backend/app.py`) and logging config.
- Frontend logging helper, base CSS utilities, and example unit test.
- Config files: `.editorconfig`, `.gitignore`, `pyproject.toml`, `package.json`, `.pre-commit-config.yaml`.

Copy these into new projects or let `bootstrap.py` materialize them when needed. Update `docs/architecture.md`, `docs/testing.md`, and `docs/environment.md` whenever you change architecture, test scope, or environment variables.

## Suggested Workflow for New Projects

1. **Bootstrap** the repo with the files above.
2. **Read `CLAUDE.md`** to understand the full guardrails; Cursor agents automatically load `.cursorrules`.
3. **Plan work on a branch**, documenting the Dockerfile, test plan, and MCP checks you will run.
4. **Implement + Test**, ensuring structured logging, lint cleanliness, and documented manual browser coverage where relevant.
5. **Update docs** (architecture diagrams with Mermaid, troubleshooting files, storage guidelines) whenever behavior or infra changes.
6. **Before committing**, run `make precommit` and verify MCP service status/logs if deployments are involved.

## License

Add your desired license text here.
