# AGENTS.md — Ekko Repository Guide

## Architecture

Clean Architecture with strict dependency direction:
`presentation/infrastructure → application → core`

```
src/ekko/
  ai/               # CrewAI agents, PII anonymization, chains, embeddings, prompts
  core/             # Domain: enums, interfaces, exceptions, entities, value_objects
  application/      # Use cases: services, DTOs, handlers, mappers
  composition/      # DI container (Container dataclass + cached_property), app factory
  config/           # Settings: base + per-env subclasses (local/dev/test/staging/prod), logging
  infrastructure/   # Adapters: STT, audio streaming, OpenAI, persistence, LLM, auth
  presentation/     # API routes, GraphQL (Strawberry), middleware, schemas
  cli/              # CLI entry points
  utils/            # Common helpers, logger, types

frontend/
  src/
    application/    # hooks, stores (zustand)
    domain/         # models, types, schemas (zod)
    infrastructure/ # api clients, config
    lib/            # utilities (cn helper)
    presentation/   # components (ui/common/layout), pages, features, styles
    router/         # React Router config

tests/
  unit/             # Mirrors src/ structure
  integration/      # API integration tests
  property/         # Hypothesis property-based tests
  performance/      # Benchmarks (pytest-benchmark)
  e2e/              # End-to-end tests
  database/         # Migration and ORM model tests
  factories/        # factory-boy factories
  fixtures/         # Shared test data
  mocks/            # Reusable mock objects
  utils/            # assertion_helpers, mock_builder

registry/           # Naming registry (JSON → generated constants)
```

## Tooling

| Tool | Purpose |
|------|---------|
| uv | Python dependency management and command execution |
| Bun | Frontend runtime and package manager |
| Taskfile.yml | Task runner (`task test`, `task lint`, `task dev`, etc.) |
| Ruff | Python linting (30+ rule groups) + formatting |
| Biome | Frontend linting + formatting |
| Pre-commit | Git hooks (ruff, biome, gitleaks, commitizen, etc.) |
| Vitest | Frontend unit testing |
| Playwright | Frontend E2E testing |
| pytest | Backend testing (unit, integration, property, performance, e2e) |
| shadcn | UI component CLI (see `.github/skills/frontend-react-stack/`) |

## Key Commands

```bash
task install          # Install all dependencies
task dev              # Run backend + frontend in dev mode
task test:unit        # Run unit tests
task test:property    # Run property-based tests
task test:coverage    # Tests with coverage report
task lint             # Run all linters
task format           # Format all code
task check            # Full quality gate
task db:migrate       # Run alembic migrations
task storybook        # Run Storybook dev server
```

## Skills

See `.github/skills/` for coding convention skills:
- `clean-architecture` — Layer boundaries and dependency direction
- `python-conventions` — Typing, logging, maintainability
- `testing-conventions` — Test quality and structure
- `frontend-react-stack` — React, shadcn/ui, Tailwind, Vitest conventions
- `naming-registry` — Canonical naming definitions

## Configuration

- Environment settings: `src/ekko/config/settings/` (base → local/dev/test/staging/prod)
- Settings factory: `get_settings()` with `EKKO_ENVIRONMENT` env var
- Naming registry: `registry/naming_registry.json` → `src/ekko/core/registry_constants.py`
- GraphQL: Strawberry schema at `/graphql` with subscriptions
- CrewAI agents: YAML-based config in `src/ekko/ai/crewai/config/`
