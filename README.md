<div align="center">
  <img src="https://img.shields.io/badge/Live%20on-Discord-7289DA?logo=discord&logoColor=white" alt="Live on Discord" />
  <img src="https://img.shields.io/badge/Enterprise-Ready-34D399" alt="Enterprise Ready" />
  <img src="https://img.shields.io/badge/Commands-40%2B-8B5CF6" alt="Command Count" />
</div>

> ⚖️ **Compliance:** This README follows the guardrails defined in [`CLAUDE.md`](CLAUDE.md) / [`.cursorrules`](.cursorrules). Update all three in lockstep.

## Invite Celeste to Your Workspace

<a href="https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=8" target="_blank"><img src="https://img.shields.io/badge/Invite%20Celeste-Click%20to%20Authorize-9333EA?logo=discord" alt="Invite Celeste" /></a>

**Onboarding checklist**
1. Confirm you have Discord admin rights and an audit log retention policy.
2. Create a `#celeste-console` text channel plus a private `#celeste-ops` channel for escalation.
3. Review allowed scopes (`bot`, `applications.commands`) and permissions (Manage Messages, Read Message History, Attach Files).
4. Run a dry-run validation: invoke `/celeste ping`, `/celeste brief`, and `/celeste raid status` from a staging server.
5. Capture screenshots + logs for compliance, then roll out to production guilds.

## Celeste Experience Pillars

> ### Celeste Experience Pillars
> - **Context-Aware Banter** – Celeste references union history and page context without ever exposing RAG jargon.
> - **Raid Intel on Tap** – `/celeste raid status` summarizes boss HP, weak points, and recommended loadouts per squad.
> - **Live Moderation Assist** – Inline hints keep mods aware of escalation paths before Celeste takes automated action.
> - **Enterprise Guardrails** – Every response is logged, reproducible, and mapped to the policies in `CLAUDE.md`.

## Command Catalog

### Conversation Persona
- `/celeste ping` – Sanity check for widget reachability • _params:_ none.
- `/celeste vibe <topic>` – Short lore drop tailored to `<topic>` • _params:_ `topic` (string, required).
- `/celeste recap [channel]` – Summarizes the last 50 messages in `[channel]` • _params:_ `channel` (defaults to current).

### Discovery Persona
- `/celeste brief <game>` – Sends a one-pager on the specified `<game>` • _params:_ `game` (enum from roster).
- `/celeste dropscan <keyword>` – Surfaces merch, art, or clips tagged with `<keyword>` • _params:_ `keyword` (string).
- `/celeste schedule` – Lists upcoming streams/events • _params:_ optional `range` (default 7d).

### Raid Persona
- `/celeste raid status <union>` – Live boss HP, weak points, rotation tips • _params:_ `union` (string/id).
- `/celeste raid assign <member> <role>` – Suggests squad placement for `<member>` • _params:_ `member` mention, `role` (tank/dps/support).
- `/celeste raid log [boss]` – Links the last N clear videos for `[boss]` • _params:_ `boss` optional.

### Moderation Persona
- `/celeste mod alert <reason>` – Opens an escalation thread citing the guardrail clause • _params:_ `reason` (string + preset tags).
- `/celeste mod sweep [channel]` – Flags suspicious attachments in `[channel]` • _params:_ optional `channel`.
- `/celeste mod notes <user>` – Retrieves prior interventions for `<user>` • _params:_ `user` mention.

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
| **Project-Specific Notes** | Anchor the current whykusanagi portfolio setup. | Static HTML/CSS/JS via Cloudflare Workers, manual browser testing at the 1000px breakpoint + cross-browser, Celeste widget config from `celesteCLI`, secrets refactor tracked on `feature/secrets-refactor`. |

<details>
<summary><strong>Deep Operational Details (audit logging, automations, bootstrap)</strong></summary>

### Files & Bootstrap Kit
| File | Purpose |
| --- | --- |
| `CLAUDE.md` / `.cursorrules` | Authoritative guardrails + persona guidance (keep synchronized). |
| `bootstrap.py` | Generates configs, Docker scaffolding, and lint stacks on demand. |
| `requirements.txt` | Locked Python toolchain (FastAPI, lint/test, detect-secrets) for immediate install. |
| `bootstrap directories` | `src/backend`, `src/frontend`, `tests`, `docs`, `scripts`, `docker`, etc. |

```bash
# Canonical bootstrap flow
cp .cursorrules CLAUDE.md bootstrap.py /your/project
python bootstrap.py
pip install -r requirements.txt
make setup
npm install   # optional for frontend scaffold
make gen-config
```

### Automations & Audit Trails
- **Audit logging:** Every slash command is mirrored to the private `#celeste-ops` channel with correlation IDs.
- **Detect-secrets:** `bootstrap.py` auto-generates `.secrets.baseline`; run `pre-commit run detect-secrets` before merging.
- **Docker parity:** Local validation defaults to `docker/Dockerfile`; deviations must be documented in PR descriptions.

</details>

## Troubleshooting & Support

| Symptom | What to check | Resolution |
| --- | --- | --- |
| Slash commands missing | Confirm `applications.commands` scope + Discord permissions | Re-invite with correct scopes, then run `/celeste ping` |
| Raid data stale | Widget can’t reach `celesteCLI` artifacts | Revalidate CDN token, rerun `/celeste raid status <union>` |
| Moderation alerts too noisy | Escalation channel misconfigured | Update `/celeste mod alert` defaults via `/celeste settings` |
| Bootstrap errors | Missing Python deps | `pip install -r requirements.txt` then rerun `python bootstrap.py` |

**Contact paths**
- Incident hotline: `#celeste-ops` (Discord) – staffed 24/7
- Email: `support@whykusanagi.xyz`
- Deployment approvals: submit via `docs/decisions/ADR-template.md`

## Licensing & Next Steps

This template ships with enterprise guardrails; add your preferred license text under `LICENSE`.

Ready to ship Celeste?

<a href="https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=8" target="_blank"><img src="https://img.shields.io/badge/Install%20Celeste-Start%20the%20Raid-EC4899?logo=discord" alt="Install Celeste" /></a>
