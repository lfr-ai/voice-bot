"""Tests for the JWT adapter."""

from datetime import UTC, datetime

import pytest

from ekko.infrastructure.auth.jwt_adapter import JWTAdapter, TokenPayload


@pytest.fixture
def adapter():
    return JWTAdapter(secret_key="test-secret-key", expire_minutes=30)


class TestJWTAdapter:
    def test_create_access_token(self, adapter):
        token = adapter.create_access_token(subject="testuser")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self, adapter):
        token = adapter.create_access_token(subject="testuser")
        payload = adapter.decode_token(token)
        assert payload is not None
        assert isinstance(payload, TokenPayload)
        assert payload.sub == "testuser"
        assert isinstance(payload.exp, datetime)

    def test_decode_invalid_token(self, adapter):
        payload = adapter.decode_token("invalid.token.here")
        assert payload is None

    def test_decode_wrong_secret(self, adapter):
        token = adapter.create_access_token(subject="testuser")
        other_adapter = JWTAdapter(secret_key="wrong-secret")
        payload = other_adapter.decode_token(token)
        assert payload is None

    def test_token_subject_preserved(self, adapter):
        token = adapter.create_access_token(subject="user@example.com")
        payload = adapter.decode_token(token)
        assert payload is not None
        assert payload.sub == "user@example.com"

    def test_token_expiry_is_future(self, adapter):
        token = adapter.create_access_token(subject="testuser")
        payload = adapter.decode_token(token)
        assert payload is not None
        assert payload.exp > datetime.now(UTC)
