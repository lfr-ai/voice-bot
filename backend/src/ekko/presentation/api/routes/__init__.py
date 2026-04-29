"""Presentation routers."""

from ekko.presentation.api.routes.auth import auth_router
from ekko.presentation.api.routes.health import router as health_router
from ekko.presentation.api.routes.stream import router as stream_router

__all__ = ["auth_router", "health_router", "stream_router"]
