from voice.config.settings import BaseAppConfig
from voice.core.protocols import AudioStreamerControllerProtocol
from voice.infrastructure.audio_streamer.audio_streamer_controller import (
    AudioStreamerController,
)


def create_audio_streamer_controller(
    settings: BaseAppConfig,
) -> AudioStreamerControllerProtocol:
    return AudioStreamerController(settings)
