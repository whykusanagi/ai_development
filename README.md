<div align="center">
  <img src="https://img.shields.io/badge/Policy-Locked-111827?style=flat-square" alt="Policy Locked" />
  <img src="https://img.shields.io/badge/Enterprise-Ready-2563EB?style=flat-square" alt="Enterprise Ready" />
  <img src="https://img.shields.io/badge/MCP-Workflow%20Verified-059669?style=flat-square" alt="MCP Workflow Verified" />
</div>

<div align="center" style="margin: 2rem 0;">

![Enterprise AI guardrails template](https://s3.whykusanagi.xyz/optimized_assets/cute_headshot_transparent_ghub.png)

</div>

> ⚖️ **Compliance:** This README follows the guardrails codified in [`CLAUDE.md`](CLAUDE.md) and [`.cursorrules`](.cursorrules). Update the trio together.

## Bootstrap the Guardrails Template

<a href="https://github.com/whykusanagi/ai_development/archive/refs/heads/main.zip" target="_blank"><img src="https://img.shields.io/badge/Get%20the%20Template-Download%20%26%20Bootstrap-9333EA?logo=github" alt="Download Template" /></a>

**Onboarding checklist**
1. Confirm you have Python 3.11+, Node 20+, Docker, and `detect-secrets` available locally.
2. Copy `CLAUDE.md`, `.cursorrules`, and `bootstrap.py` into the new repo **before** inviting AI assistants.
3. Run `python bootstrap.py`, `pip install -r requirements.txt`, `make setup`, and `make gen-config` to create the baseline structure.
4. Register MCP credentials (DigitalOcean, AWS, Azure, Cloudflare) so deployment checks can run as written.
5. Capture validation evidence (screenshots/logs) for auditors when first applying the template to a codebase.

## Guardrail Experience Pillars

> ### Guardrail Experience Pillars
> - **Policy Parity** – Humans and AI share the same authoritative instructions via `CLAUDE.md` + `.cursorrules`.
> - **Context-Safe Delivery** – Branching, commit hygiene, and MCP workflows are baked into every checklist.
> - **Secret Hygiene First** – `.gitignore`, `.secrets/`, and detect-secrets scaffolding come standard.
> - **Audit-Friendly Ops** – Troubleshooting docs, ADR templates, and logging guidance keep changes reviewable.

## Template Components

### Core Agreements
- `CLAUDE.md` – Human-readable working agreement covering persona usage, branching, secrets, MCP workflow.
- `.cursorrules` – Cursor-formatted equivalent auto-loaded for agents; keep it in sync with `CLAUDE.md`.

### Bootstrap & Tooling
- `bootstrap.py` – Generates directories, configs, Dockerfiles, pre-commit hooks, and `.secrets.baseline`.
- `requirements.txt` – Pins FastAPI, lint/test stack, `pre-commit`, and `detect-secrets` versions used across repos.
- `Makefile` / `.pre-commit-config.yaml` – One-command install plus opinionated lint/test automation.

### Reference Implementations
- `src/backend/app.py` + logging config – Minimal FastAPI health endpoint with structured logging.
- `src/frontend/` stubs – Base CSS utilities and TS logger helper for quick UI scaffolding.
- `tests/` – Unit-test template wired for pytest + FastAPI test client.

### Documentation Suite
- `docs/architecture.md`, `docs/testing.md`, `docs/environment.md` – Mermaid-ready diagrams, manual test flows, and env-var registry.
- `docs/decisions/ADR-template.md` – Lightweight ADR form for approvals.
- `docs/storage.md` – Centralized S3/R2 procedures.

## Guardrail Themes at a Glance

| Section | Why it exists | Enterprise implication |
| --- | --- | --- |
| **Purpose & Expectations** | Keep repos coherent, recoverable, production-credible. | Prefer clarity + rollback safety over speculative edits. |
| **Git & Branching** | Preserve readable history and safe rollbacks. | Always branch (`feature/…`, `fix/…`), commit in small units, never edit `CLAUDE.md` unsanctioned. |
| **.gitignore & Secrets Hygiene** | Block junk files and leaks. | Enforce the provided `.gitignore`, store secrets in `.secrets/` or env vars, document usage in `docs/environment.md`. |
| **Docker, Storage, Structure** | Guarantee consistent runtime + organization. | Declare canonical Dockerfile, log deviations, centralize S3 procedures, keep folders tidy. |
| **Testing & Quality Bar** | Supply audit-ready evidence. | Define success criteria, capture manual/browser steps, reuse shared utilities, keep lint clean. |
| **Safety & Autonomy** | Curb runaway refactors or infra surprises. | Socialize multi-file plans, pause for schema/migration work, avoid mass deletions without approval. |
| **Final Checklist** | Prevent last-mile regressions. | Before merge: branch check, `.gitignore` sweep, Docker notes, test evidence, S3 adherence, persona compliance. |
| **Celeste Persona** | Maintain knowledge continuity for CelesteAI integrations. | Talk via “memories/notes”, stay page-aware, never mention RAG/OpenSearch internals. |
| **MCP & Cloud Workflow** | Keep deployments observable. | Run `list_mcp_resources()` → deploy → verify → fetch logs, never assume tooling is unavailable. |
| **AI Assistant Checklist** | Align every agent with the guardrails. | Suggest `make precommit`, enforce Docker parity, reuse utilities, add Mermaid diagrams for architecture changes. |

<details>
<summary><strong>Operational Depth (bootstrap steps, automations, directory map)</strong></summary>

### Bootstrap Flow
```bash
cp CLAUDE.md .cursorrules bootstrap.py /path/to/new/repo
python bootstrap.py
pip install -r requirements.txt
make setup
npm install          # optional Frontend helpers
make gen-config
pre-commit run --all-files
```

### Directory Highlights
- `src/backend/` – FastAPI starter + logging config.
- `src/frontend/` – TS/CSS helpers.
- `tests/` – unit + integration scaffolding plus `_md_scratch/` for AI notes (gitignored).
- `scripts/` – smoke tests, docs guards, config generators.
- `docker/` – production Dockerfile and dev variant.

### Automations & Audit Trails
- **Detect-secrets baseline** auto-generated; update via `detect-secrets scan --baseline .secrets.baseline`.
- **Pre-commit** wires Ruff, Black, Prettier, jscpd, and detect-secrets.
- **ADR workflow** ensures every exception to guardrails is documented in `docs/decisions/`.

</details>

## Troubleshooting & Support

| Symptom | What to check | Resolution |
| --- | --- | --- |
| `bootstrap.py` failing | Python deps missing | `pip install -r requirements.txt` then rerun bootstrap.
| Pre-commit hooks slow | Large repo / missing caches | Run `pre-commit clean && pre-commit install --overwrite`.
| MCP checks blocked | Credentials not configured | Refresh API tokens/secrets, then rerun MCP status commands.|
| Detect-secrets noise | Legacy baseline | Regenerate `.secrets.baseline` and re-run `pre-commit`. |

**Support channels**
- Internal: open a thread in `#guardrails-template` with logs + steps.
- Email: `support@whykusanagi.xyz`
- Architecture approvals: submit ADR via `docs/decisions/` and link evidence.

## Licensing & Next Steps

This repo ships as a guardrail starter; add your organization’s license text under `LICENSE`.

Ready to harden your next repo?

<a href="https://github.com/whykusanagi/ai_development/archive/refs/heads/main.zip" target="_blank"><img src="https://img.shields.io/badge/Apply%20the%20Guardrails-Start%20Building-EC4899?logo=github" alt="Apply Guardrails" /></a>
