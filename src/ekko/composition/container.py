"""Dependency-injection container.

Follows the cached-property pattern from the golden standard: each service is
built once on first access and reused for the lifetime of the container.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import Any, final

from ekko.config.settings import BaseAppConfig, get_settings


@final
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

    # ── Auth ─────────────────────────────────────────────────
    @cached_property
    def jwt_adapter(self) -> Any:
        """Lazily build the JWT adapter."""
        from ekko.infrastructure.auth.jwt_adapter import JWTAdapter

        return JWTAdapter(
            secret_key=self.settings.jwt_secret_key.get_secret_value(),
            expire_minutes=self.settings.jwt_expire_minutes,
        )

    # ── OpenAI ───────────────────────────────────────────────
    @cached_property
    def openai_gateway(self) -> Any:
        """Lazily build the OpenAI gateway."""
        from ekko.infrastructure.openai.openai_client import AzureOpenAIClient

        return AzureOpenAIClient(settings=self.settings)

    # ── STT ──────────────────────────────────────────────────
    @cached_property
    def stt_service(self) -> Any:
        """Lazily build the STT service."""
        from ekko.infrastructure.adapters.stt_adapter import (
            create_faster_whisper_stt,
        )

        return create_faster_whisper_stt(settings=self.settings)

    # ── Audio ────────────────────────────────────────────────
    @cached_property
    def audio_controller(self) -> Any:
        """Lazily build the audio streamer controller."""
        from ekko.infrastructure.adapters.audio_streamer_adapter import (
            create_audio_streamer_controller,
        )

        return create_audio_streamer_controller(self.settings)

    # ── Application services ─────────────────────────────────
    @cached_property
    def summarizer_service(self) -> Any:
        """Lazily build the summarizer service."""
        from ekko.application.services.summarizer_service import SummarizerService

        return SummarizerService(
            gateway=self.openai_gateway,
            settings=self.settings,
        )
