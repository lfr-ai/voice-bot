"""Transcript protocol."""

from __future__ import annotations

from typing import Any, Protocol


class TranscriptProtocol(Protocol):
    stream_name: str
    text: str
    segments: Any
    info: Any
