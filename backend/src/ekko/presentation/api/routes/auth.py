"""Authentication endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ekko.presentation.api.schemas.auth import TokenRequest, TokenResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=TokenResponse)
async def create_token(body: TokenRequest) -> TokenResponse:
    """Issue a JWT access token.

    In production, this would validate credentials against a user store.
    For development, any username/password combination is accepted.
    """
    from ekko.config.settings import get_settings
    from ekko.infrastructure.auth.jwt_adapter import JWTAdapter

    settings = get_settings()
    adapter = JWTAdapter(
        secret_key=settings.jwt_secret_key.get_secret_value(),
        expire_minutes=settings.jwt_expire_minutes,
    )
    token = adapter.create_access_token(subject=body.username)
    return TokenResponse(access_token=token, token_type="bearer")
