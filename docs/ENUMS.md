# Enums Reference

This file documents the canonical enums defined in `src/voice/core/enums.py`.

Highlights
- `LLMProvider` – provider identifiers used across adapters and configuration.
- `ModelMode` – indicates chat, completion, or embedding surfaces; used to select the adapter API.
- `AudioEncoding` – audio formats supported by ingestion and streaming adapters.

Usage
- Import the enum and refer to members by name: `from voice.core.enums import LLMProvider`.
- Prefer using enum values (e.g., `LLMProvider.OPENAI.value`) for external configuration fields.

Extending
- Add new values to `enums.py` and update any `registry/naming_registry.json` if using the
  naming-registry workflow.
