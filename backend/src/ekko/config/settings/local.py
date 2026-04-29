"""Local development configuration."""

from ekko.config.settings.base import BaseAppConfig
from ekko.core.enums import Environment


class LocalConfig(BaseAppConfig):
    """Settings for local developer machines."""

    environment: Environment = Environment.LOCAL
    debug: bool = True
    log_level: str = "DEBUG"
