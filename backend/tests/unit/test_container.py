"""Tests for the DI container."""

from ekko.composition.container import Container
from ekko.config.settings import BaseAppConfig
from ekko.infrastructure.auth.jwt_adapter import JWTAdapter


class TestContainer:
    def test_from_config(self):
        container = Container.from_config()
        assert isinstance(container.settings, BaseAppConfig)

    def test_settings_injection(self):
        settings = BaseAppConfig()
        container = Container(settings=settings)
        assert container.settings is settings

    def test_jwt_adapter(self):
        settings = BaseAppConfig()
        container = Container(settings=settings)
        adapter = container.jwt_adapter
        assert isinstance(adapter, JWTAdapter)

    def test_jwt_adapter_cached(self):
        settings = BaseAppConfig()
        container = Container(settings=settings)
        first = container.jwt_adapter
        second = container.jwt_adapter
        assert first is second
