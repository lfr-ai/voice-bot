# Architecture analysis and migration plan

This document maps the existing project layout to a Clean Architecture structure and lists recommended changes to align with the golden-standard templates (`koda_automation` and `copier-fullstack-template`).

## Current layout (selected)
- `src/voice/config` — configuration
- `src/voice/interaction` — FastAPI entrypoint and static UI
- `src/voice/models` — mixed domain, infra, and 3rd-party client code
- `src/voice/managers` — orchestration helpers
- `src/voice/utils` — cross-cutting helpers

## Target layout (Clean Architecture)
- `src/voice/core/` — pure domain types, value objects, protocols, exceptions
- `src/voice/application/` — use cases, services, DTOs, orchestration logic
- `src/voice/infrastructure/` — concrete adapters (DB, external clients, STT, audio streamer)
- `src/voice/presentation/` — FastAPI routers, API models, HTTP dependencies
- `src/voice/composition/` — composition root (create_app, DI wiring)
- `src/voice/config/` — configuration and settings (Pydantic)
- `src/voice/prompts/` — LLM prompts
- `src/voice/utils/` — logging, helpers

## Short-term gaps to address (minimal, non-breaking)
1. Add a `composition.create_app()` factory and migrate `interaction/main.py` to call it. Maintain current top-level app for backwards compatibility during transition.
2. Add `core/` and `application/` folders (initially empty) and add guidelines for where new code should live.
3. Move any pure-domain models from `models/` into `core/` and create Protocols for external dependencies used by application services.
4. Add tests layout and Taskfile for common commands.
5. Add CI, DevContainer, Dockerfile, pre-commit (already present), and `.env.example` (added).

## Migration plan (phases)
- Phase 1 (this PR): Documentation, composition root, CI, devcontainer, containerfile, env example, and gap analysis.
- Phase 2: Create `core`, `application`, `infrastructure`, and `presentation` folders; begin moving and refactoring modules with Protocol interfaces and unit tests.
- Phase 3: Add frontend scaffold (from `copier-fullstack-template`) into `frontend/` or connect to existing static files; add Playwright & Vitest if desired.
- Phase 4: Add comprehensive CI workflows (lint/test/build/release), Renovate, Dependabot, and release automation.

## Implemented governance and productivity scaffolding

- Root governance/tooling files added:
	- `.editorconfig`, `.gitattributes`, `.dockerignore`, `.hadolint.yaml`
	- `.lychee.toml`, `.markdownlint-cli2.yaml`, `.shellcheckrc`
	- `.typos.toml`, `.yamllint.yaml`, `bandit.toml`, `.secrets.baseline`
	- `cspell.json`, `renovate.json`
- CI normalized and consolidated under `.github/workflows/ci.yml`.
- `.github` scaffolding added for:
	- copilot instructions (`.github/copilot-instructions.md`)
	- scoped instructions (`.github/instructions/*.instructions.md`)
	- skills (`.github/skills/*/SKILL.md`)
	- hook governance (`.github/hooks/*`)
	- agent profiles (`.github/agents/*.agent.md`)
- Local architecture enforcement script added:
	- `scripts/check_architecture_boundaries.py`
	- wired into `task architecture` and `task check`
- Dev environment scaffolding expanded:
	- `.devcontainer/compose.yml`, `Containerfile.dev`, lifecycle/support files
	- `docker/compose.yml` + `compose.dev/test/prod/override.yml`
	- updated VS Code settings, launch profile, and MCP config.

## Notes
- Keep runtime behavior unchanged during Phase 1. App factory will call existing startup/shutdown logic.
- Ensure type hints and mypy pass during refactors.
