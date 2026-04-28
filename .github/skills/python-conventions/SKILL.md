---
name: python-conventions
description: Python standards for typing, logging, and maintainability.
---

# Skill: Python Conventions

## Rules

- Prefer concrete types over `Any`.
- Use keyword-only args for functions with multiple configuration-style parameters.
- Use structured logging over `print()`.
- Catch specific exceptions and chain with `raise ... from e`.
