"""Test environment configuration."""

from voice.config.settings.base import BaseAppConfig
from voice.core.enums import Environment


class TestingConfig(BaseAppConfig):
    """Settings for automated test runs."""

    environment: Environment = Environment.TEST
    debug: bool = False
    log_level: str = "WARNING"
    postgresql_name: str = "voice_test"
