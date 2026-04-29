"""Backwards-compatible re-exports from core.interfaces."""

from voice.core.interfaces.audio import (
    AudioStreamerControllerProtocol,
    STTService,
)
from voice.core.interfaces.chat import ChatPort
from voice.core.interfaces.transcript import TranscriptProtocol as Transcript

__all__ = [
    "AudioStreamerControllerProtocol",
    "ChatPort",
    "STTService",
    "Transcript",
]
