# Gap analysis: voice-bot vs golden standards (koda_automation & copier-fullstack-template)

Summary:

- voice-bot is a small, well-structured Python package living under `src/voice`.
- It provides a FastAPI application and modular components used by the service.
- Golden repositories typically include broader infra, CI, Taskfile helpers,
  consistency checks, and a full frontend template.

Key gaps and recommended actions (exhaustive):

## Repository governance and metadata

- Add repository metadata files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, and `CHANGELOG.md` (or keep and standardize existing docs).
- Add GitHub templates: `.github/ISSUE_TEMPLATE` and `PULL_REQUEST_TEMPLATE`.

## CI/CD and Release

- Extend CI baseline with caching, matrix builds, packaging, and release
  automation (GitHub Releases or CI artifacts).
- Add security scanning jobs (Bandit, dependency checks) and secret detection.

## Developer experience

- Expand `.devcontainer` to include commonly used extensions and port
  forwarding for frontend development.
- Add or extend `Taskfile` and `scripts/` for common developer operations.

## Clean Architecture

- Create and populate skeleton packages (`core`, `application`,
  `infrastructure`, `presentation`) and re-export adapters where applicable.
- Gradually move domain logic into `core` and depend on protocols for
  infrastructure adapters.

## Frontend

- No dedicated frontend scaffold exists yet. Consider using
  `copier-fullstack-template` to scaffold a React/Vite app and wire it to the
  FastAPI back end.

## IaC

- Provide `azure/iac` Bicep modules for core infra (ACR, Web App, Storage,
  Log Analytics, Cognitive Services). Key Vault remains optional and disabled
  by default in parameter files.
- Add role assignments, managed identity bindings and optional Key Vault
  population workflows (only if Key Vault is explicitly enabled). Also add
  environment parameterization per environment.

## Tests & Quality

- Increase unit and integration coverage (move tests to core/application
  modules where appropriate).
- Add coverage reporting and threshold enforcement in CI.

Action plan (priority):

1. Harden CI (linting, security scans, matrix, caching).
2. Continue Clean-Architecture refactor incrementally and add tests.
3. Scaffold frontend and provide a local compose-based dev setup.
4. Enhance IaC with RBAC and managed identity wiring and environment params.
5. Expand tests and enforce coverage.
