"""LLM adapter that bridges the existing ChatModelAdapter to the AI layer.

This module wraps ``infrastructure.llm.chat_adapter.ChatModelAdapter`` so it
can be used by the AI layer and CrewAI components.
"""

from __future__ import annotations

from typing import Any

from ekko.config.settings import BaseAppConfig, get_settings


class LLMAdapter:
    """Provider-agnostic LLM adapter powered by LangChain.

    This delegates to the existing ``ChatModelAdapter`` from the infrastructure
    layer while providing a clean interface for the AI layer.
    """

    def __init__(self, *, settings: BaseAppConfig | None = None) -> None:
        self._settings = settings or get_settings()
        self._default_deployment = self._settings.llm_default_deployment or self._settings.rag_llm_model

    @property
    def default_deployment(self) -> str:
        return self._default_deployment

    def _get_adapter(self):
        from ekko.infrastructure.llm.chat_adapter import ChatModelAdapter

        return ChatModelAdapter(settings=self._settings)

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        deployment_name: str | None = None,
        max_completion_tokens: int = 1024,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> str:
        """Synchronous chat completion."""
        adapter = self._get_adapter()
        return adapter.chat(
            system_prompt,
            user_prompt,
            deployment_name=deployment_name or self._default_deployment,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            **kwargs,
        )

    async def async_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        deployment_name: str | None = None,
        max_completion_tokens: int = 1024,
        temperature: float = 0.0,
        **kwargs: Any,
    ) -> str:
        """Asynchronous chat completion."""
        adapter = self._get_adapter()
        return await adapter.async_chat(
            system_prompt,
            user_prompt,
            deployment_name=deployment_name or self._default_deployment,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            **kwargs,
        )
