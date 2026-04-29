"""Shared development environment configuration."""

from ekko.config.settings.base import BaseAppConfig
from ekko.core.enums import Environment


class DevelopmentConfig(BaseAppConfig):
    """Settings for the shared dev environment."""

    environment: Environment = Environment.DEV
    debug: bool = True
    log_level: str = "DEBUG"
