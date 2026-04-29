"""Strawberry GraphQL types."""

from __future__ import annotations

import strawberry


@strawberry.type
class DependencyHealthType:
    """Health status of a single service dependency."""

    name: str
    healthy: bool
    detail: str = ""


@strawberry.type
class HealthType:
    """Application health check result."""

    status: str
    environment: str
    dependencies: list[DependencyHealthType]


@strawberry.type
class TranscriptType:
    """A speech-to-text transcript."""

    text: str
    source: str
    timestamp: str


@strawberry.type
class StreamStatusType:
    """Current audio stream status."""

    active: bool
    message: str


@strawberry.input
class StreamCommandInput:
    """Input for stream control mutations."""

    action: str  # "start" or "pause"
