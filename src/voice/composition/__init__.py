"""Composition root — DI container and application factory."""

from voice.composition.app_factory import create_app
from voice.composition.container import Container

__all__ = ["Container", "create_app"]
