"""GraphQL router for FastAPI integration."""

from __future__ import annotations

from strawberry.fastapi import GraphQLRouter

from ekko.presentation.graphql.schema import schema

graphql_router = GraphQLRouter(schema, path="/graphql")
