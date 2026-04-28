from __future__ import annotations

from typing import Protocol


class OpenAIGateway(Protocol):
    """Protocol for an OpenAI gateway used by application services.

    Implementations must be side-effect free for calls and return plain data
    structures (no framework types).
    """

    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_completion_tokens: int,
    ) -> str:
        """Send a chat completion request and return assistant text.

        Args:
            system_prompt: system-level instructions
            user_prompt: user message
            model: model identifier
            temperature: sampling temperature
            max_completion_tokens: maximum tokens to return

        Returns:
            The assistant's text response.
        """

        ...
