"""Local development configuration."""

from ekko.config.enums import Environment
from ekko.config.settings.base import BaseAppConfig


class LocalConfig(BaseAppConfig):
    """Settings for local developer machines."""

    environment: Environment = Environment.LOCAL
    debug: bool = True
    log_level: str = "DEBUG"
