"""GraphQL permission classes."""

from __future__ import annotations

import typing

from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    """Check that the request has a valid authenticated user."""

    message = "Authentication required"

    def has_permission(self, source: typing.Any, info: Info, **kwargs: typing.Any) -> bool:
        request = info.context.get("request")
        if request is None:
            return False
        user = getattr(request.state, "user", None)
        return user is not None
