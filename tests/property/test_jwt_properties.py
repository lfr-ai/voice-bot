"""Property-based tests for JWT adapter."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from ekko.infrastructure.auth.jwt_adapter import JWTAdapter


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("EKKO_ENVIRONMENT", raising=False)


class TestJWTProperties:
    @given(
        subject=st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=("L", "N", "P"))),
    )
    @settings(max_examples=20)
    def test_roundtrip(self, subject):
        """Any non-empty subject survives encode->decode roundtrip."""
        adapter = JWTAdapter(secret_key="prop-test-secret", expire_minutes=30)
        token = adapter.create_access_token(subject=subject)
        payload = adapter.decode_token(token)
        assert payload is not None
        assert payload.sub == subject

    @given(
        secret=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("L", "N"))),
    )
    @settings(max_examples=10)
    def test_different_secrets_reject(self, secret):
        """Tokens signed with one secret are rejected by a different one."""
        adapter1 = JWTAdapter(secret_key=secret + "a", expire_minutes=30)
        adapter2 = JWTAdapter(secret_key=secret + "b", expire_minutes=30)
        token = adapter1.create_access_token(subject="user")
        payload = adapter2.decode_token(token)
        assert payload is None
