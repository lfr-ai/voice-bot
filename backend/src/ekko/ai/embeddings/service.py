"""Embedding service using LangChain OpenAI embeddings."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ekko.config.settings.base import BaseAppConfig

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Embedding service backed by LangChain OpenAI embeddings.

    Lazily initializes the embedding model on first use.
    """

    def __init__(self, *, settings: BaseAppConfig) -> None:
        self._settings = settings
        self._model = None

    def _get_model(self):
        if self._model is None:
            from langchain_openai import OpenAIEmbeddings

            kwargs = {"model": self._settings.rag_embedding_model}
            if self._settings.openai_api_key:
                kwargs["api_key"] = self._settings.openai_api_key.get_secret_value()
            self._model = OpenAIEmbeddings(**kwargs)
        return self._model

    async def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        model = self._get_model()
        return await model.aembed_query(text)

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple text strings."""
        model = self._get_model()
        return await model.aembed_documents(texts)
