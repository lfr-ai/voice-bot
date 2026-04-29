"""JWT authentication middleware."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response

    from ekko.config.settings.base import BaseAppConfig

from ekko.core.enums import Environment

logger = logging.getLogger(__name__)

_PUBLIC_PATHS = frozenset({"/health", "/docs", "/openapi.json", "/redoc"})


@dataclass(frozen=True, slots=True)
class UserProfile:
    """Authenticated user profile attached to request state."""

    username: str
    roles: frozenset[str] = frozenset()


@final
class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authenticate requests via JWT Bearer token."""

    def __init__(self, app, *, environment: Environment, jwt_adapter, default_user_id: str = "dev-user") -> None:
        super().__init__(app)
        self._environment = environment
        self._jwt_adapter = jwt_adapter
        self._default_user_id = default_user_id

    @classmethod
    def from_config(cls, app, *, settings: BaseAppConfig, jwt_adapter):
        """Create middleware from application settings."""
        return cls(app, environment=settings.environment, jwt_adapter=jwt_adapter)

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process authentication for each request."""
        if request.url.path in _PUBLIC_PATHS:
            return await call_next(request)

        if self._environment == Environment.LOCAL:
            request.state.user = UserProfile(username=self._default_user_id, roles=frozenset({"admin"}))
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

        token = auth_header.removeprefix("Bearer ")
        payload = self._jwt_adapter.decode_token(token)
        if payload is None:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        request.state.user = UserProfile(username=payload.sub)
        return await call_next(request)
