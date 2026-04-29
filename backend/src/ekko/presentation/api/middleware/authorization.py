"""Role-based authorization middleware."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, final

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response

from ekko.core.enums import Environment

logger = logging.getLogger(__name__)

_PUBLIC_PATHS = frozenset({"/health", "/docs", "/openapi.json", "/redoc", "/auth/token"})


@final
class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Check user roles against required roles."""

    def __init__(self, app, *, environment: Environment, authorized_roles: frozenset[str]) -> None:
        super().__init__(app)
        self._environment = environment
        self._authorized_roles = authorized_roles

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in _PUBLIC_PATHS or self._environment == Environment.LOCAL:
            return await call_next(request)

        user = getattr(request.state, "user", None)
        if user is None:
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

        if not user.roles & self._authorized_roles:
            logger.warning("Authorization denied for user %s", user.username)
            return JSONResponse(status_code=403, content={"detail": "Insufficient permissions"})

        return await call_next(request)
