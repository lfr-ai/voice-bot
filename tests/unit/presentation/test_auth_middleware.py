"""Tests for authentication middleware."""

import pytest

from ekko.infrastructure.auth.jwt_adapter import JWTAdapter
from ekko.presentation.api.middleware.authentication import (
    UserProfile,
)


@pytest.fixture
def jwt_adapter():
    return JWTAdapter(secret_key="test-secret", expire_minutes=30)


class TestUserProfile:
    def test_defaults(self):
        profile = UserProfile(username="test")
        assert profile.username == "test"
        assert profile.roles == frozenset()

    def test_with_roles(self):
        profile = UserProfile(username="admin", roles=frozenset({"admin", "user"}))
        assert "admin" in profile.roles
        assert "user" in profile.roles

    def test_frozen(self):
        profile = UserProfile(username="test")
        with pytest.raises(AttributeError):
            profile.username = "other"
