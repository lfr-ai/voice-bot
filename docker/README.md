# Docker

Compose environments follow a base-plus-override model.

## Files

- `compose.yml`: base service definitions.
- `compose.override.yml`: local default overrides.
- `compose.dev.yml`: development runtime and source mounts.
- `compose.test.yml`: test execution profile.
- `compose.prod.yml`: production-oriented runtime profile.

## Typical Usage

- Local dev: base + dev
- CI tests: base + test
- Production-like: base + prod
