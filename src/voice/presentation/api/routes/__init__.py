"""API route modules."""

from voice.presentation.api.routes.health import router as health_router
from voice.presentation.api.routes.stream import router as stream_router

__all__ = ["health_router", "stream_router"]
