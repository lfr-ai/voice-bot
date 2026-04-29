"""Backwards-compatible re-exports from core.interfaces."""

from ekko.core.interfaces.audio import (
    AudioStreamerControllerProtocol,
    STTService,
)
from ekko.core.interfaces.chat import ChatPort
from ekko.core.interfaces.transcript import TranscriptProtocol as Transcript

__all__ = [
    "AudioStreamerControllerProtocol",
    "ChatPort",
    "STTService",
    "Transcript",
]
