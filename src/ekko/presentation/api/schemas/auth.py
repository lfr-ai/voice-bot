"""Authentication request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    """Login credentials for token generation."""

    username: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
