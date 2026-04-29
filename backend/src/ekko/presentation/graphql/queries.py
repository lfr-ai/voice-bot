"""Root GraphQL queries."""

from __future__ import annotations

import strawberry

from ekko.presentation.graphql.types import DependencyHealthType, HealthType


@strawberry.type
class Query:
    """Root query type."""

    @strawberry.field
    async def health(self) -> HealthType:
        """Basic health check."""
        from ekko.config.settings import get_settings

        settings = get_settings()
        return HealthType(
            status="ok",
            environment=settings.environment.value,
            dependencies=[],
        )

    @strawberry.field
    async def health_ready(self) -> HealthType:
        """Deep health check with dependency probes."""
        from ekko.config.settings import get_settings

        settings = get_settings()

        deps: list[DependencyHealthType] = []

        # Database probe
        try:
            from sqlalchemy import text

            from ekko.infrastructure.db.engine import get_engine

            engine = get_engine()
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            deps.append(DependencyHealthType(name="database", healthy=True))
        except Exception as exc:
            deps.append(DependencyHealthType(name="database", healthy=False, detail=str(exc)))

        all_healthy = all(d.healthy for d in deps)
        return HealthType(
            status="ok" if all_healthy else "degraded",
            environment=settings.environment.value,
            dependencies=deps,
        )
