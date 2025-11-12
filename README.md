# Repo Guardrails Template

A minimal, transportable template for enforcing good engineering habits. **Just 2 essential files!**

## What's Included

- **`.cursorrules`** - All file templates, coding standards, and AI assistant guidelines
- **`bootstrap.py`** - Script to generate configuration files on-demand

## Quick Start

### Option 1: Full Setup (Recommended)

```bash
# Copy files to your new project
cp .cursorrules /path/to/new-project/
cp bootstrap.py /path/to/new-project/

# Generate all config files
cd /path/to/new-project
python bootstrap.py

# Set up pre-commit hooks
make setup
```

### Option 2: Cursor-Only (Minimal)

```bash
# Just copy .cursorrules
cp .cursorrules /path/to/new-project/

# Cursor will create files as needed using templates from .cursorrules
# No bootstrap needed!
```

## How It Works

1. **`.cursorrules`** contains all file templates and guidelines
2. **`bootstrap.py`** generates configuration files when you need them
3. **Cursor AI** uses `.cursorrules` to create files on-demand

## Philosophy

- ✅ **Lightweight** - Only essential files
- ✅ **Transportable** - Copy 2 files to any project
- ✅ **On-demand** - Files created when needed
- ✅ **Single source of truth** - All templates in `.cursorrules`

## What Gets Generated

When you run `bootstrap.py`, it creates:
- Configuration files (`.gitignore`, `.editorconfig`, etc.)
- Tooling configs (`pyproject.toml`, `package.json`, etc.)
- Directory structure (`src/`, `tests/`, `docs/`, etc.)
- Docker setup
- CI/CD workflows (optional)

## Customization

Edit `.cursorrules` to:
- Modify file templates
- Change coding standards
- Adjust project structure
- Customize AI assistant behavior

## License

[Add your license here]
