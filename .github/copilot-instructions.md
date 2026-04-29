---
description: Repository development conventions for voice-bot
applyTo: "**"
---

# voice-bot — Development Instructions

## Architecture and Boundaries

- Follow Clean Architecture dependency direction: `presentation/infrastructure -> application -> core`.
- `src/ekko/core/` must remain framework-independent — no imports from infrastructure/presentation.
- `src/ekko/application/` can import from `core` and configuration, but not concrete adapters.
- `src/ekko/infrastructure/` implements protocols declared in `core/interfaces/`.
- `src/ekko/composition/` wires everything together via the `Container` DI pattern.
- `src/ekko/presentation/api/routes/` contains FastAPI routers (health, stream, etc.).

## Backend Stack

- Python 3.12+, FastAPI, Pydantic, SQLAlchemy, Alembic
- Settings: `voice.config.settings.get_settings()` — env-specific subclasses of `BaseAppConfig`
- Enums: `StrEnum` + `@unique` + `auto()` in `voice.core.enums`
- DI Container: `voice.composition.Container` with `@cached_property`
- Testing: pytest, hypothesis, factory-boy, pytest-asyncio, pytest-benchmark
- Naming registry: `registry/naming_registry.json` → generated constants

## Frontend Stack

- React 19, TypeScript, Vite 6 + SWC, Bun
- UI: shadcn/ui (Radix + Tailwind CSS v4) — use CLI, never copy-paste
- State: Zustand, TanStack React Query
- Linting: Biome (not Prettier/ESLint)
- Testing: Vitest + React Testing Library + fast-check, Playwright for E2E
- See `.github/skills/frontend-react-stack/SKILL.md` for full conventions

## Tooling and Commands

- Use `uv` for Python dependency and command execution.
- Use `bun` for frontend package management and scripts.
- Preferred project commands are in `Taskfile.yml`.
- Run `task check` (lint + tests + typecheck) before finalizing changes.

## Quality Rules

- Keep changes minimal and scoped.
- Update docs in the same change when behavior or setup changes.
- Use typed Python signatures and avoid `Any` unless truly unavoidable.
- Use `cn()` for Tailwind class merging, semantic color tokens only.

## Security Rules

- Never commit secrets.
- Keep `.env.example` updated when new environment variables are introduced.
- Use `detect-secrets` and `gitleaks` via pre-commit hooks.
