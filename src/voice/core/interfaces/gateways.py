"""Gateway protocols for external service integrations."""

from __future__ import annotations

from typing import Protocol


class OpenAIGateway(Protocol):
    """Protocol for an OpenAI gateway used by application services."""

    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_completion_tokens: int,
    ) -> str: ...
