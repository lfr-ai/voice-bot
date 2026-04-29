# Developer README

This guide describes the local developer workflow for `voice-bot`.

## Setup

1. Install dependencies with uv (recommended):

```bash
uv sync --all-extras
```

1. Optional: use the dev container.

Open in VS Code and run **Dev Containers: Reopen in Container**.

## Daily Commands

- Start app: `task dev`
- Run tests: `task test`
- Run integration tests: `task test:integration`
- Lint/type checks: `task lint`
- Run all hooks: `task precommit`
- Full quality gate: `task check`

## Development

Recommended developer setup:

This repository originally used PDM. Astral's `uv` is the recommended project
toolchain (package/runtime manager). To migrate, run
`scripts/migrate_to_uv.sh`.

Using uv (recommended):

```bash
# Install deps
uv sync --all-extras

# Run hooks
uvx pre-commit run --all-files

# Run tests
uvx pytest -q
```

Alternative: install uv and sync with groups:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --all-groups
```

Install pre-commit via pipx or the included helper script:

```bash
uvx pipx run pre-commit install
# or
./scripts/bootstrap-uv.sh
```

Devcontainer: open repository in VS Code and reopen in container to get a
consistent dev environment.

## Quality and Security Tooling

`pre-commit` hooks include Ruff, mypy, Bandit, detect-secrets, typos, and
yamllint.

Clean Architecture boundaries are checked by:

- CI workflow (`.github/workflows/ci.yml`)
- Local script (`scripts/check_architecture_boundaries.py`)

Supporting policy/config files include:

- `.editorconfig`, `.yamllint.yaml`, `.markdownlint-cli2.yaml`, `.typos.toml`
- `.lychee.toml`, `.hadolint.yaml`, `.secrets.baseline`

## Container Workflows

Dev container config: `.devcontainer/`

Compose matrix: `docker/compose.yml` + environment overrides in
`docker/compose.*.yml`
