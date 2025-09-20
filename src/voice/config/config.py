import getpass
import socket
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """
    Configuration class for storing settings.
    """

    # System info
    USER_ID = getpass.getuser()
    HOSTNAME = socket.gethostname()

    # Paths
    PACKAGE_DIR_PATH: Path = Path(__file__).resolve().parents[1]
    ROOT_DIR_PATH: Path = PACKAGE_DIR_PATH.parents[1]
    SRC_DIR_PATH: Path = ROOT_DIR_PATH / "src"
    LOGS_DIR_PATH: Path = ROOT_DIR_PATH / "logs"
    PROMPT_DIR_PATH: Path = PACKAGE_DIR_PATH / "prompts"
    INTERACTION_DIR_PATH: Path = PACKAGE_DIR_PATH / "interaction"

    # Audio streamer
