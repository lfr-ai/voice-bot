"""Dependency-injection container.

Follows the cached-property pattern from the golden standard: each service is
built once on first access and reused for the lifetime of the container.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Any

from voice.config.settings import BaseAppConfig, get_settings


@dataclass
class Container:
    """Application-scoped DI container.

    Usage::

        container = Container.from_config()
        stt = container.stt_service
    """

    settings: BaseAppConfig

    @classmethod
    def from_config(cls) -> Container:
        """Build a container from the current environment settings."""
        return cls(settings=get_settings())

    @cached_property
    def openai_gateway(self) -> Any:
        """Lazily build the OpenAI gateway."""
        from voice.infrastructure.openai.openai_client import AzureOpenAIClient

        return AzureOpenAIClient(settings=self.settings)

    @cached_property
    def stt_service(self) -> Any:
        """Lazily build the STT service."""
        from voice.infrastructure.adapters.stt_adapter import (
            create_faster_whisper_stt,
        )

        return create_faster_whisper_stt(settings=self.settings)

    @cached_property
    def audio_controller(self) -> Any:
        """Lazily build the audio streamer controller."""
        from voice.infrastructure.adapters.audio_streamer_adapter import (
            create_audio_streamer_controller,
        )

        return create_audio_streamer_controller(self.settings)

    @cached_property
    def summarizer_service(self) -> Any:
        """Lazily build the summarizer service."""
        from voice.application.services.summarizer_service import SummarizerService

        return SummarizerService(
            gateway=self.openai_gateway,
            settings=self.settings,
        )
