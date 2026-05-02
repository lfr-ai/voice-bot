"""Mock LLM adapter for testing."""

from __future__ import annotations

from typing import Any


class MockLLMAdapter:
    """Mock LLM adapter that returns predefined responses."""

    def __init__(self, response_text: str = "Test LLM response") -> None:
        self.response_text = response_text
        self.call_count = 0
        self.last_system_prompt: str | None = None
        self.last_user_prompt: str | None = None

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        _deployment_name: str,
        _max_completion_tokens: int = 1024,
        _temperature: float = 0.0,
        **_kwargs: Any,
    ) -> str:
        """Return mock response."""
        self.call_count += 1
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        return self.response_text

    async def async_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        _deployment_name: str,
        _max_completion_tokens: int = 1024,
        _temperature: float = 0.0,
        **_kwargs: Any,
    ) -> str:
        """Return mock response asynchronously."""
        self.call_count += 1
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        return self.response_text


class FailingLLMAdapter(MockLLMAdapter):
    """Mock LLM adapter that simulates failures."""

    def chat(
        self,
        _system_prompt: str,
        _user_prompt: str,
        *,
        _deployment_name: str,
        _max_completion_tokens: int = 1024,
        _temperature: float = 0.0,
        **_kwargs: Any,
    ) -> str:
        """Simulate LLM failure."""
        raise RuntimeError("LLM processing failed")

    async def async_chat(
        self,
        _system_prompt: str,
        _user_prompt: str,
        *,
        _deployment_name: str,
        _max_completion_tokens: int = 1024,
        _temperature: float = 0.0,
        **_kwargs: Any,
    ) -> str:
        """Simulate async LLM failure."""
        raise RuntimeError("LLM processing failed")
