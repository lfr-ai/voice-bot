"""Production environment configuration."""

from ekko.config.settings.base import BaseAppConfig
from ekko.core.enums import Environment


class ProductionConfig(BaseAppConfig):
    """Settings for the production environment."""

    environment: Environment = Environment.PROD
    debug: bool = False
    log_level: str = "WARNING"
