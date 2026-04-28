# Contributing

Please read `README.md` and follow the coding conventions in `.github/copilot-instructions.md`.

Thank you for contributing! Please follow these guidelines.

- Use `uv` to manage dependencies (see `pyproject.toml`).
- Run linters and tests before submitting PRs:

```bash
# Install dependencies
uv sync --all-extras

# Run pre-commit hooks
uvx pre-commit run --all-files

# Run tests
uvx pytest -q
```

If you prefer PDM it is still supported; the repo contains the original `pdm.lock`.

- Branch naming: feature/..., fix/..., chore/...
- Follow Conventional Commits; commitizen is configured in `pyproject.toml`.
