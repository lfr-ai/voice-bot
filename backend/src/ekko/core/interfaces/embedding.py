"""Embedding port protocol for provider-agnostic embedding interfaces."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingProtocol(Protocol):
    """Protocol for text embedding services."""

    async def embed_text(self, text: str) -> list[float]: ...

    async def embed_texts(self, texts: list[str]) -> list[list[float]]: ...
