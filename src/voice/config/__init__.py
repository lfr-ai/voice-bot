"""Configuration helpers and environment parsing utilities.

Re-exports the canonical settings API so callers can write::

    from voice.config import get_settings
"""

from voice.config.settings import (
    SETTINGS,
    BaseAppConfig,
    get_settings,
)

__all__ = [
    "SETTINGS",
    "BaseAppConfig",
    "get_settings",
]
