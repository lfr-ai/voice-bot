"""Tests for GraphQL schema assembly."""

import strawberry

from ekko.presentation.graphql.schema import schema
from ekko.presentation.graphql.types import (
    DependencyHealthType,
    HealthType,
    StreamCommandInput,
    StreamStatusType,
    TranscriptType,
)


class TestGraphQLTypes:
    def test_health_type_fields(self):
        h = HealthType(status="ok", environment="local", dependencies=[])
        assert h.status == "ok"
        assert h.environment == "local"
        assert h.dependencies == []

    def test_dependency_health_type(self):
        d = DependencyHealthType(name="db", healthy=True, detail="")
        assert d.name == "db"
        assert d.healthy is True

    def test_stream_status_type(self):
        s = StreamStatusType(active=True, message="running")
        assert s.active is True

    def test_transcript_type(self):
        t = TranscriptType(text="hello", source="mic", timestamp="2024-01-01")
        assert t.text == "hello"

    def test_stream_command_input(self):
        c = StreamCommandInput(action="start")
        assert c.action == "start"


class TestSchema:
    def test_schema_is_strawberry_schema(self):
        assert isinstance(schema, strawberry.Schema)

    def test_schema_has_query(self):
        assert schema is not None
        assert schema.execute_sync("{ __typename }") is not None
