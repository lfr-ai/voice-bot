"""Core domain interfaces (protocols / abstract ports)."""

from voice.core.interfaces.audio import AudioStreamerControllerProtocol, STTService
from voice.core.interfaces.chat import ChatPort
from voice.core.interfaces.gateways import OpenAIGateway
from voice.core.interfaces.transcript import TranscriptProtocol

__all__ = [
    "AudioStreamerControllerProtocol",
    "ChatPort",
    "OpenAIGateway",
    "STTService",
    "TranscriptProtocol",
]
