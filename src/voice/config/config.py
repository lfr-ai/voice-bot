import getpass
import os
import socket
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pyaudiowpatch import paInt16

ROOT_DIR_PATH = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR_PATH / ".env")


@dataclass
class Config:
    """
    Configuration class for storing settings.
    """

    # System info
    USER_ID = getpass.getuser()
    HOSTNAME = socket.gethostname()

    # Paths
    ROOT_DIR_PATH: Path = ROOT_DIR_PATH
    SRC_DIR_PATH: Path = ROOT_DIR_PATH / "src"
    PACKAGE_DIR_PATH: Path = SRC_DIR_PATH / "voice"
    LOGS_DIR_PATH: Path = ROOT_DIR_PATH / "logs"
    PROMPT_DIR_PATH: Path = PACKAGE_DIR_PATH / "prompts"
    INTERACTION_DIR_PATH: Path = PACKAGE_DIR_PATH / "interaction"
    AUDIO_STREAMER_TCP_SERVER_MODULE_PATH: str = (
        "voice.models.audio_streamer.audio_streamer_tcp_server"
    )

    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 6500
    AUDIO_STREAMER_TCP_PORT: int = 6600

    # Azure OpenAI settings
    OPENAI_VERSION: str = "2025-03-01-preview"

    # Azure credentials
    OPENAI_KEY: str = os.getenv("OPENAI_KEY", "")
    OPENAI_ENDPOINT: str = "https://swedencentral.api.cognitive.microsoft.com/"

    # Audio settings
    AUDIO_FORMAT: int = paInt16
    AUDIO_FRAMES_PER_BUFFER: int = 1024

    # Axillary constants
    SLEEP_DELAY_SECONDS: float = 0.1
    WAIT_TIMEOUT_SECONDS: int = 2
    MAX_READ_BYTES: int = 100
