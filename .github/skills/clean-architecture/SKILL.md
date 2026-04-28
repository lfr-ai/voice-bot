---
name: clean-architecture
description: Enforce Clean Architecture boundaries and dependency direction.
---

# Skill: Clean Architecture

## Rules

- Dependencies must point inward: `presentation/infrastructure -> application -> core`.
- `core/` has no framework imports.
- `application/` depends on interfaces/protocols, not concrete infrastructure.
- Keep business rules in `application` and `core`, not in transport/adapters.

## Quick Checklist

- [ ] New files are placed in the correct layer
- [ ] Imports do not violate layer boundaries
- [ ] No circular dependencies introduced
