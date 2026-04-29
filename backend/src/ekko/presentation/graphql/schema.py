"""Strawberry GraphQL schema assembly."""

from __future__ import annotations

import strawberry
from strawberry.extensions import QueryDepthLimiter

from ekko.presentation.graphql.mutations import Mutation
from ekko.presentation.graphql.queries import Query

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[QueryDepthLimiter(max_depth=10)],
)
