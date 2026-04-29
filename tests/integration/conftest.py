"""Integration conftest."""

import pytest


@pytest.fixture
def integration_settings():
    """Settings configured for integration testing."""
    from ekko.config.settings import BaseAppConfig
    from ekko.core.enums import Environment

    return BaseAppConfig(environment=Environment.TEST, debug=False)
