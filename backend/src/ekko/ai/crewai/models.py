"""Pydantic output models for CrewAI tasks."""

from __future__ import annotations

from pydantic import BaseModel


class TranscriptAnalysis(BaseModel):
    """Structured output from transcript analysis."""

    key_topics: list[str]
    sentiment: str
    action_items: list[str]
    follow_up_questions: list[str]
    summary: str


class VoiceResponse(BaseModel):
    """Structured output from voice assistant response."""

    response_text: str
    confidence: float = 1.0
