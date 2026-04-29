"""Audio stream request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel


class StreamResponse(BaseModel):
    """Audio stream control response."""

    status: str
    message: str
