"""Authoritative enums for the Ekko project.

This module centralizes enumerated constants used across layers. Use this
file as the single source-of-truth for shared string and int constants.

Convention: ``StrEnum`` + ``@unique`` + ``auto()`` for all string enums.
"""

from __future__ import annotations

from enum import IntEnum, StrEnum, auto, unique


def enum_values(enum_cls: type[StrEnum]) -> list[str]:
    """Return the string values of a StrEnum class in declaration order."""

    return [e.value for e in enum_cls]


@unique
class Environment(StrEnum):
    LOCAL = auto()
    DEV = auto()
    TEST = auto()
    STAGING = auto()
    PROD = auto()


@unique
class LLMProvider(StrEnum):
    OPENAI = auto()
    AZURE_OPENAI = auto()
    ANTHROPIC = auto()
    COHERE = auto()
    GOOGLE = auto()
    OTHER = auto()


@unique
class ChatModel(StrEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    GPT_5 = "gpt-5"


@unique
class STTProvider(StrEnum):
    WHISPER = auto()
    FASTER_WHISPER = auto()
    AZURE_SPEECH = auto()
    GOOGLE_SPEECH = auto()
    OTHER = auto()


@unique
class AudioFormat(StrEnum):
    WAV = auto()
    FLAC = auto()
    MP3 = auto()
    OGG = auto()
    PCM16 = auto()


@unique
class AudioChannel(IntEnum):
    MONO = 1
    STEREO = 2


@unique
class SampleRate(IntEnum):
    SR_8000 = 8000
    SR_16000 = 16000
    SR_22050 = 22050
    SR_44100 = 44100
    SR_48000 = 48000
    SR_96000 = 96000


@unique
class BitDepth(IntEnum):
    BITS_8 = 8
    BITS_16 = 16
    BITS_24 = 24
    BITS_32 = 32


@unique
class QueueName(StrEnum):
    TRANSCRIPTS = auto()
    COMMANDS = auto()
    EVENTS = auto()
    METRICS = auto()


@unique
class TranscriptStatus(StrEnum):
    RECEIVED = auto()
    QUEUED = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@unique
class MessageRole(StrEnum):
    SYSTEM = auto()
    USER = auto()
    ASSISTANT = auto()
    TOOL = auto()


@unique
class LogLevel(IntEnum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@unique
class DeploymentTarget(StrEnum):
    LOCAL = auto()
    DOCKER = auto()
    KUBERNETES = auto()
    AZURE_CONTAINER_APPS = auto()
    AZURE_FUNCTIONS = auto()


@unique
class FeatureFlag(StrEnum):
    RAG_ENABLED = auto()
    ENABLE_TELEMETRY = auto()


__all__ = [
    "AudioChannel",
    "AudioFormat",
    "BitDepth",
    "ChatModel",
    "DeploymentTarget",
    "Environment",
    "FeatureFlag",
    "LLMProvider",
    "LogLevel",
    "MessageRole",
    "QueueName",
    "STTProvider",
    "SampleRate",
    "TranscriptStatus",
    "enum_values",
]
