"""Root GraphQL mutations."""

from __future__ import annotations

import strawberry

from ekko.presentation.graphql.types import StreamCommandInput, StreamStatusType


@strawberry.type
class Mutation:
    """Root mutation type."""

    @strawberry.mutation
    async def control_stream(self, command: StreamCommandInput) -> StreamStatusType:
        """Start or pause the audio stream."""
        if command.action not in {"start", "pause"}:
            return StreamStatusType(active=False, message=f"Unknown action: {command.action}")
        return StreamStatusType(
            active=command.action == "start",
            message=f"Stream {command.action}ed",
        )
