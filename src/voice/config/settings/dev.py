"""Shared development environment configuration."""

from voice.config.settings.base import BaseAppConfig
from voice.core.enums import Environment


class DevelopmentConfig(BaseAppConfig):
    """Settings for the shared dev environment."""

    environment: Environment = Environment.DEV
    debug: bool = True
    log_level: str = "DEBUG"
