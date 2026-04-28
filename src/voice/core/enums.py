"""Centralized enums for the voice-bot project.

This module provides a stable set of string/int enums used by the
application layers (core, application, infrastructure).
"""

from __future__ import annotations

from enum import StrEnum, IntEnum, unique
from typing import List


@unique
class LLMProvider(StrEnum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    GOOGLE = "google"
    OTHER = "other"


@unique
class ChatModel(StrEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    GPT_5 = "gpt-5"


@unique
class STTProvider(StrEnum):
    WHISPER = "whisper"
    FASTER_WHISPER = "faster_whisper"
    AZURE_SPEECH = "azure_speech"
    GOOGLE_SPEECH = "google_speech"


@unique
class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    """Canonical enums for the voice-bot project.

    Keep the set of enums compact and stable. Import these from any layer in the
    project to avoid duplicated literal strings.
    """

    from __future__ import annotations

    from enum import Enum, IntEnum, unique
    """Authoritative enums used by the voice application.

    This module is a stable, flat collection of enums. The legacy
    `enums.py` can act as a shim that re-exports these definitions.
    """

    from __future__ import annotations

    from enum import Enum, IntEnum, unique
    from typing import List

    try:  # Python 3.11+ has StrEnum
        from enum import StrEnum  # type: ignore
    except Exception:  # pragma: no cover - fallback for older runtimes
        class StrEnum(str, Enum):
            """Fallback StrEnum for older Python versions."""


    def enum_values(enum_cls: type[StrEnum]) -> List[str]:
        """Return the string values of an enum class in declaration order."""

        return [e.value for e in enum_cls]


    @unique
    class Environment(StrEnum):
        LOCAL = "local"
        DEV = "dev"
        TEST = "test"
        STAGING = "staging"
        PROD = "prod"


    @unique
    class LLMProvider(StrEnum):
        OPENAI = "openai"
        AZURE_OPENAI = "azure_openai"
        ANTHROPIC = "anthropic"
        COHERE = "cohere"
        OTHER = "other"


    @unique
    class ChatModel(StrEnum):
        GPT_3_5_TURBO = "gpt-3.5-turbo"
        GPT_4 = "gpt-4"
        GPT_4O = "gpt-4o"
        GPT_5 = "gpt-5"


    @unique
    class STTProvider(StrEnum):
        WHISPER = "whisper"
        FASTER_WHISPER = "faster_whisper"
        AZURE_SPEECH = "azure_speech"
        GOOGLE_SPEECH = "google_speech"
        OTHER = "other"


    @unique
    class AudioFormat(StrEnum):
        WAV = "wav"
        FLAC = "flac"
        MP3 = "mp3"
        OGG = "ogg"
        PCM16 = "pcm16"


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
        TRANSCRIPTS = "transcripts"
        COMMANDS = "commands"
        EVENTS = "events"
        METRICS = "metrics"


    @unique
    class TranscriptStatus(StrEnum):
        RECEIVED = "received"
        QUEUED = "queued"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"


    @unique
    class MessageRole(StrEnum):
        SYSTEM = "system"
        USER = "user"
        ASSISTANT = "assistant"
        TOOL = "tool"


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
        LOCAL = "local"
        DOCKER = "docker"
        KUBERNETES = "kubernetes"
        AZURE_CONTAINER_APPS = "azure_container_apps"
        AZURE_FUNCTIONS = "azure_functions"


    @unique
    class FeatureFlag(StrEnum):
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
        "enum_values",
    ]
    @unique
    class AudioFormat(StrEnum):
        WAV = "wav"
        FLAC = "flac"
        MP3 = "mp3"
        OGG = "ogg"


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
        TRANSCRIPTS = "transcripts"
        COMMANDS = "commands"
        EVENTS = "events"
        METRICS = "metrics"


    @unique
    class TranscriptStatus(StrEnum):
        RECEIVED = "received"
        QUEUED = "queued"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"


    @unique
    class DeploymentTarget(StrEnum):
        LOCAL = "local"
        DOCKER = "docker"
        KUBERNETES = "kubernetes"
        AZURE_CONTAINER_APPS = "azure_container_apps"
        AZURE_FUNCTIONS = "azure_functions"


    @unique
    class FeatureFlag(StrEnum):
        RAG_ENABLED = "rag_enabled"
        USE_AZURE_KEYVAULT = "use_azure_keyvault"
        ENABLE_TELEMETRY = "enable_telemetry"


    def enum_values(enum_cls: Type[StrEnum]) -> List[str]:
        """Return list of string values for a StrEnum class in declaration order."""

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
        "AudioFormat",
        "AudioChannel",
        "SampleRate",
        "BitDepth",
        "QueueName",
        "TranscriptStatus",
        "DeploymentTarget",
        "FeatureFlag",
        "enum_values",
    ]
        BITS_8 = 8
        BITS_16 = 16
        BITS_24 = 24
        BITS_32 = 32


    @unique
    class AudioFormat(StrEnum):
        WAV = "wav"
        MP3 = "mp3"
        FLAC = "flac"
        OGG = "ogg"
        M4A = "m4a"


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
    class DeploymentTarget(StrEnum):
        LOCAL = "local"
        DOCKER = "docker"
        KUBERNETES = "kubernetes"
        AZURE_CONTAINER_APPS = "azure_container_apps"
        AZURE_FUNCTIONS = "azure_functions"


    def enum_values(enum_cls: type[StrEnum]) -> List[str]:
        """Return the string values of a StrEnum class in declaration order."""

        return [e.value for e in enum_cls]


    __all__ = [
        "LLMProvider",
        "ChatModel",
        "STTProvider",
        "Environment",
        "MessageRole",
        "LogLevel",
        "QueueName",
        "TranscriptStatus",
        "FeatureFlag",
        "BitDepth",
        "AudioFormat",
        "AudioChannel",
        "SampleRate",
        "DeploymentTarget",
        "enum_values",
    ]
        OGG = "ogg"
        PCM16 = "pcm16"

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
        TOOL = "tool"

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
        "enum_values",
    ]
