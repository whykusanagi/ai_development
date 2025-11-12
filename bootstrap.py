#!/usr/bin/env python3
"""
Bootstrap script to generate repo guardrails files on-demand.
Run this script to set up a new project with guardrails.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# File templates
TEMPLATES: Dict[str, str] = {
    ".editorconfig": """root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
""",
    ".gitattributes": """* text=auto eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
""",
    ".gitignore": """# Python
__pycache__/
*.pyc
.venv/

# Node
node_modules/

# Secrets & local configs
.env
.env.*
config/config.yaml
.secrets/

# Build artifacts
build/
dist/
coverage/

# Agent scratch docs
tests/_md_scratch/
""",
    ".jscpd.json": json.dumps({
        "threshold": 0,
        "reporters": ["console"],
        "min-lines": 5,
        "min-tokens": 50,
        "ignore": [
            "**/node_modules/**",
            "**/__pycache__/**",
            "**/build/**",
            "**/dist/**",
            "**/tests/_md_scratch/**"
        ],
        "languages": ["javascript", "typescript", "python", "css", "html"]
    }, indent=2),
    ".prettierrc": json.dumps({
        "printWidth": 100,
        "singleQuote": True,
        "trailingComma": "all"
    }, indent=2),
    ".eslintrc.cjs": """module.exports = {
  root: true,
  env: { browser: true, es2022: true, node: true },
  extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended", "prettier"],
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint"],
  ignorePatterns: ["dist", "build", "node_modules"],
  rules: {
    "no-duplicate-imports": "error"
  }
};
""",
    "commitlint.config.cjs": """module.exports = { extends: ["@commitlint/config-conventional"] };
""",
    "pyproject.toml": """[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]
fix = true

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true
warn_unused_ignores = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-q"
testpaths = ["tests"]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
""",
    "package.json": json.dumps({
        "name": "repo-guardrails-template",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "lint": "eslint . --ext .js,.ts,.tsx",
            "format": "prettier -w .",
            "commitmsg": "commitlint --edit $GIT_PARAMS"
        },
        "devDependencies": {
            "@commitlint/cli": "^19.0.0",
            "@commitlint/config-conventional": "^19.0.0",
            "@typescript-eslint/eslint-plugin": "^7.0.0",
            "@typescript-eslint/parser": "^7.0.0",
            "eslint": "^9.0.0",
            "eslint-config-prettier": "^9.0.0",
            "prettier": "^3.2.0",
            "typescript": "^5.5.0"
        }
    }, indent=2),
    "tsconfig.json": json.dumps({
        "compilerOptions": {
            "target": "ES2022",
            "module": "ESNext",
            "lib": ["ES2022", "DOM"],
            "moduleResolution": "node",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "outDir": "./dist",
            "rootDir": "./src/frontend"
        },
        "include": ["src/frontend/**/*"],
        "exclude": ["node_modules", "dist"]
    }, indent=2),
    ".pre-commit-config.yaml": """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-json

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
        files: \\.(js|ts|tsx|css|json|md)$

  - repo: https://github.com/kucherenko/jscpd
    rev: "3.5.10"
    hooks:
      - id: jscpd
        additional_dependencies: []
        args: ["--config", ".jscpd.json"]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
""",
    "Makefile": """# Makefile for repo guardrails
.PHONY: setup precommit up smoke lint test docs-check gen-config

setup:
\tpip install pre-commit && pre-commit install

precommit:
\tpre-commit run --all-files

up:
\tdocker compose up --build -d api

smoke:
\tdocker compose run --rm smoke

lint:
\tnpm run lint || true && ruff . && black --check . && mypy src/backend || true

test:
\tpytest -q

docs-check:
\tbash scripts/docs_changed_check.sh || true

gen-config:
\tpython scripts/gen_config.py
""",
    "docker-compose.yml": """services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8080:8080"
    environment:
      - APP_ENV=local
    volumes:
      - ./config:/app/config:ro
  smoke:
    image: python:3.11-slim
    depends_on: [api]
    volumes:
      - ./:/w
    working_dir: /w
    command: ["python", "scripts/smoke_api.py", "http://api:8080/health"]
""",
    "docker/Dockerfile": """FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install pytest ruff black mypy fastapi uvicorn[standard]
COPY src/backend /app/src/backend
COPY scripts/smoke_api.py /app/scripts/
ENV PORT=8080
CMD ["uvicorn", "src.backend.app:app", "--host", "0.0.0.0", "--port", "8080"]
""",
    "docker/dev.Dockerfile": """FROM node:20-bookworm
WORKDIR /workspace
COPY package.json /workspace/
RUN npm i -D
COPY . /workspace
""",
    "config/config.example.yaml": """# Example configuration file
# Copy this to config.yaml and fill in your values
# config.yaml is gitignored and should never be committed

app:
  name: "repo-guardrails-template"
  env: "${APP_ENV:-development}"
  port: "${PORT:-8080}"

database:
  host: "${DB_HOST:-localhost}"
  port: "${DB_PORT:-5432}"
  name: "${DB_NAME:-appdb}"
  user: "${DB_USER:-user}"
  # password: "${DB_PASSWORD}"  # Set via environment variable

logging:
  level: "${LOG_LEVEL:-INFO}"
  format: "%(asctime)s %(levelname)s %(name)s - %(message)s"
""",
    "CODEOWNERS": """# Default owners for everything in the repo
* @maintainers

# Specific paths
/.github/ @devops
/docs/ @tech-leads
/src/backend/ @backend-team
/src/frontend/ @frontend-team
""",
    ".vscode/settings.json": json.dumps({
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "[python]": {
            "editor.defaultFormatter": "ms-python.black-formatter",
            "editor.formatOnSave": True
        },
        "[javascript]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[typescript]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[json]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "[yaml]": {
            "editor.defaultFormatter": "esbenp.prettier-vscode"
        },
        "files.eol": "\\n",
        "files.insertFinalNewline": True,
        "files.trimTrailingWhitespace": True,
        "python.linting.enabled": True,
        "python.linting.ruffEnabled": True,
        "eslint.validate": ["javascript", "typescript"]
    }, indent=2),
}

# Directory structure to create
DIRECTORIES = [
    "src/backend",
    "src/frontend/scripts",
    "src/frontend/styles",
    "tests/unit",
    "tests/integration",
    "tests/_md_scratch",
    "scripts",
    "docs/decisions",
    "config",
    "docker",
    ".github/workflows",
    ".vscode",
    "tools",
]


def create_file(path: Path, content: str) -> None:
    """Create a file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"  ⚠️  {path} already exists, skipping...")
        return
    path.write_text(content)
    print(f"  ✅ Created {path}")


def create_directory(path: Path) -> None:
    """Create a directory."""
    path.mkdir(parents=True, exist_ok=True)
    if not (path / ".gitkeep").exists():
        (path / ".gitkeep").write_text("")
        print(f"  ✅ Created {path}/")


def generate_secrets_baseline() -> None:
    """Generate secrets baseline if detect-secrets is available."""
    try:
        subprocess.run(
            ["detect-secrets", "scan", "--baseline", ".secrets.baseline"],
            check=False,
            capture_output=True,
        )
        if Path(".secrets.baseline").exists():
            print("  ✅ Generated .secrets.baseline")
        else:
            # Create minimal baseline
            baseline = {
                "version": "1.5.0",
                "plugins_used": [],
                "filters_used": [],
                "results": {},
                "generated_at": "2024-01-01T00:00:00Z"
            }
            Path(".secrets.baseline").write_text(json.dumps(baseline, indent=2))
            print("  ✅ Created .secrets.baseline")
    except FileNotFoundError:
        # Create minimal baseline
        baseline = {
            "version": "1.5.0",
            "plugins_used": [],
            "filters_used": [],
            "results": {},
            "generated_at": "2024-01-01T00:00:00Z"
        }
        Path(".secrets.baseline").write_text(json.dumps(baseline, indent=2))
        print("  ✅ Created .secrets.baseline (minimal)")


def main():
    """Main bootstrap function."""
    print("🚀 Bootstrapping repo guardrails...\n")

    # Create directories
    print("📁 Creating directories...")
    for dir_path in DIRECTORIES:
        create_directory(Path(dir_path))

    # Create files
    print("\n📄 Creating configuration files...")
    for file_path, content in TEMPLATES.items():
        create_file(Path(file_path), content)

    # Generate secrets baseline
    print("\n🔐 Generating secrets baseline...")
    generate_secrets_baseline()

    print("\n✨ Bootstrap complete!")
    print("\n📋 Next steps:")
    print("  1. Run: make setup")
    print("  2. Run: npm install (if using frontend)")
    print("  3. Run: make gen-config")
    print("  4. Start developing!")


if __name__ == "__main__":
    main()

