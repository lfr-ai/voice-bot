"""Staging environment configuration."""

from voice.config.settings.base import BaseAppConfig
from voice.core.enums import Environment


class StagingConfig(BaseAppConfig):
    """Settings for the pre-production staging environment."""

    environment: Environment = Environment.STAGING
    debug: bool = False
    log_level: str = "INFO"
