"""Common enums used across the voice-bot codebase.

Purpose
- Centralize enumerations so the rest of the codebase imports one canonical source
  for provider names, model modes, audio encodings, and other shared constants.

Design
- Uses StrEnum when available (Python 3.11+); falls back to a str/Enum mixin.
"""
from __future__ import annotations

from enum import Enum
from typing import List

try:
    # Python 3.11+ provides StrEnum which behaves like `str` and `Enum`
    from enum import StrEnum  # type: ignore
except Exception:  # pragma: no cover - fallback for older runtimes
    class StrEnum(str, Enum):
        """Fallback StrEnum for older Python versions."""


class LLMProvider(StrEnum):
    """Canonical LLM provider identifiers."""

    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OTHER = "other"


class ModelMode(StrEnum):
    """Which API surface to use for a given model invocation."""

    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"


class ModelFamily(StrEnum):
    GPT = "gpt"
    TEXT = "text"
    CODE = "code"
    OTHER = "other"


class ModelName(StrEnum):
    """Common model names (not exhaustive). Add entries as needed."""

    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    GPT_4_1 = "gpt-4.1"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    UNKNOWN = "unknown"


class AudioEncoding(StrEnum):
    PCM16 = "pcm16"
    WAV = "wav"
    FLAC = "flac"
    MP3 = "mp3"
    OPUS = "opus"


class TranscriptionProvider(StrEnum):
    WHISPER = "whisper"
    FASTER_WHISPER = "faster_whisper"
    GOOGLE = "google"
    AZURE = "azure"
    OTHER = "other"


class ContentType(StrEnum):
    TRANSCRIPT = "transcript"
    SUMMARY = "summary"
    METADATA = "metadata"
    EVENT = "event"


class Environment(StrEnum):
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MessageRole(StrEnum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    TOOL = "tool"


class EventType(StrEnum):
    START = "start"
    STOP = "stop"
    ERROR = "error"
    TRANSCRIBE = "transcribe"
    SUMMARIZE = "summarize"


def enum_values(enum_cls: type[StrEnum]) -> List[str]:
    """Return the string values of an enum class in declaration order.

    Example: enum_values(LLMProvider) -> ["openai", "azure_openai", ...]
    """

    return [e.value for e in enum_cls]


__all__ = [
    "LLMProvider",
    "ModelMode",
    "ModelFamily",
    "ModelName",
    "AudioEncoding",
    "TranscriptionProvider",
    "ContentType",
    "Environment",
    "LogLevel",
    "MessageRole",
    "EventType",
    "enum_values",
]
"""Comprehensive, stable enumeration module for the voice-bot project.

This module centralizes all enumerated constants used across layers. Keep
backwards-compatible names for values referenced elsewhere (do not rename
existing members without a deprecation step).

Design notes:
- Prefer StrEnum for textual identifiers so environment variables and
  configuration may reference the string value directly.
- Provide a small set of commonly used enums (audio, llm, stt, queues,
  transcript lifecycle, and telemetry flags).
"""

from __future__ import annotations

from enum import IntEnum, StrEnum, unique


@unique
class Environment(StrEnum):
    """Deployment environment identifiers.

    Use :class:`Environment` values in configuration and feature gating.
    Values are lowercase to make them friendly for env vars and logs.
    """

    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"


@unique
class LLMProvider(StrEnum):
    """Canonical provider identifiers for LLM adapters.

    Keep the short provider id stable since configuration (env vars) and
    persisted deployment mappings depend on the string values.
    """

    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"


@unique
class ChatModel(StrEnum):
    """Common chat model identifiers used as canonical names in the app."""

    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    GPT_5 = "gpt-5"


@unique
class STTProvider(StrEnum):
    """Speech-to-text backends supported by the application."""

    WHISPER = "whisper"
    FASTER_WHISPER = "faster_whisper"
    AZURE_SPEECH = "azure_speech"
    GOOGLE_SPEECH = "google_speech"


@unique
class AudioFormat(StrEnum):
    """Common audio container/encoding formats."""

    WAV = "wav"
    FLAC = "flac"
    MP3 = "mp3"
    OGG = "ogg"


@unique
class AudioChannel(IntEnum):
    """Audio channel counts (monophonic/stereo)."""

    MONO = 1
    STEREO = 2


@unique
class SampleRate(IntEnum):
    """Common audio sampling rates (Hz)."""

    SR_8000 = 8000
    SR_16000 = 16000
    SR_22050 = 22050
    SR_44100 = 44100
    SR_48000 = 48000
    SR_96000 = 96000


@unique
class BitDepth(IntEnum):
    """Common PCM bit depths."""

    BITS_8 = 8
    BITS_16 = 16
    BITS_24 = 24
    BITS_32 = 32


@unique
class QueueName(StrEnum):
    """Canonical names for in-process queues used by QueueManager."""

    TRANSCRIPTS = "transcripts"
    COMMANDS = "commands"
    EVENTS = "events"
    METRICS = "metrics"


@unique
class TranscriptStatus(StrEnum):
    """Lifecycle status for transcript items."""

    RECEIVED = "received"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@unique
class MessageRole(StrEnum):
    """Roles in chat/message payloads."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@unique
class LogLevel(IntEnum):
    """Convenient mapping of standard logging levels to ints."""

    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


@unique
class DeploymentTarget(StrEnum):
    """Where the application is intended to run in a deployment pipeline."""

    LOCAL = "local"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"
    AZURE_CONTAINER_APPS = "azure_container_apps"
    AZURE_FUNCTIONS = "azure_functions"


@unique
class FeatureFlag(StrEnum):
    """Feature flags used to gate optional runtime capabilities."""

    RAG_ENABLED = "rag_enabled"
    USE_AZURE_KEYVAULT = "use_azure_keyvault"
    ENABLE_TELEMETRY = "enable_telemetry"


__all__ = [
    "Environment",
    "LLMProvider",
    "ChatModel",
    "STTProvider",
    "AudioFormat",
    "AudioChannel",
    "SampleRate",
    "BitDepth",
    "QueueName",
    "TranscriptStatus",
    "MessageRole",
    "LogLevel",
    "DeploymentTarget",
    "FeatureFlag",
]
