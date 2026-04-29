"""Core domain exceptions."""


class VoiceBotError(Exception):
    """Base exception for all voice-bot domain errors."""


class ConfigurationError(VoiceBotError):
    """Raised when configuration is invalid or missing."""


class AudioDeviceError(VoiceBotError):
    """Raised when an audio device cannot be found or initialized."""


class STTError(VoiceBotError):
    """Raised when speech-to-text processing fails."""


class LLMError(VoiceBotError):
    """Raised when an LLM call fails."""


class PromptNotFoundError(VoiceBotError):
    """Raised when a prompt template file cannot be found."""
