from __future__ import annotations

from typing import Any

from openai import AzureOpenAI

from voice.config.config import Config


class AzureOpenAIClient:
    """Infrastructure adapter implementing the OpenAIGateway protocol.

    This class wraps the AzureOpenAI SDK client and exposes a simple
    chat(...) method returning the assistant text.
    """

    def __init__(self, cfg: Config) -> None:
        self._client = AzureOpenAI(
            api_key=cfg.OPENAI_KEY,
            api_version=cfg.OPENAI_VERSION,
            azure_endpoint=cfg.OPENAI_ENDPOINT,
        )

    def chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_completion_tokens: int,
        **kwargs: Any,
    ) -> str:
        """Call the Azure OpenAI chat completions API and return assistant text.

        Args:
            system_prompt: system instructions
            user_prompt: user message
            model: model identifier
            temperature: sampling temperature
            max_completion_tokens: maximum tokens
            **kwargs: forwarded to the SDK

        Returns:
            Assistant text from the response.
        """
        # Cast messages to Any to satisfy the SDK typing expectations and mypy
        messages: Any = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
        ]
        response = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            **kwargs,
        )
        # Ensure a str is returned (SDK may provide richer content objects)
        content = response.choices[0].message.content
        return str(content or "")
