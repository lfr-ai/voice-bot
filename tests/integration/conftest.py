"""Integration conftest."""

import pytest


@pytest.fixture
def integration_settings():
    """Settings configured for integration testing."""
    from voice.config.settings import BaseAppConfig
    from voice.core.enums import Environment

    return BaseAppConfig(environment=Environment.TEST, debug=False)
