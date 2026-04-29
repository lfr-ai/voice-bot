"""Staging environment configuration."""

from ekko.config.settings.base import BaseAppConfig
from ekko.core.enums import Environment


class StagingConfig(BaseAppConfig):
    """Settings for the pre-production staging environment."""

    environment: Environment = Environment.STAGING
    debug: bool = False
    log_level: str = "INFO"
