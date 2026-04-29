"""LLM port protocol for provider-agnostic chat/completion interfaces."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMProtocol(Protocol):
    """Protocol for provider-agnostic LLM adapters.

    Implementations should support both sync and async invocation.
    """

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        deployment_name: str,
        max_completion_tokens: int = 1024,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> str: ...

    async def async_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        deployment_name: str,
        max_completion_tokens: int = 1024,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> str: ...
