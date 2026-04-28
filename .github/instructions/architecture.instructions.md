---
description: Clean Architecture boundaries for Python source files
applyTo: "src/voice/**/*.py"
---

# Architecture Instructions

- Keep dependency direction inward.
- Avoid imports from `infrastructure` inside `application`.
- Avoid imports from `application`/`infrastructure`/`presentation` inside `core`.
- Keep domain logic out of adapters and transport layers.
