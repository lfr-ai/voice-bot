from pathlib import Path

from voice.config.config import Config

cfg = Config()


def _validate_file_path(dir_path: Path, filename: str, suffix: str) -> Path:
    """
    Validate and return the path to a file.

    Args:
        dir_path (Path): Path to the directory of the file.
        filename (str): Name of the file.
        suffix (str): Extension of the file.

    Returns:
        Path: Validated file path.
    """
    path = dir_path / filename
    if not path.is_file():
        raise FileNotFoundError(f"File '{filename}' not found in '{dir_path}'.")
    elif path.suffix != suffix:
        raise ValueError(f"File '{filename}' must have a '{suffix}' extension.")
    return path


def load_prompt(filename: str) -> str:
    """
    Load a prompt from a .txt-file.

    Args:
        filename (str): Name of the file.
    """
    prompt_path = _validate_file_path(cfg.PROMPT_DIR_PATH, filename, ".txt")
    return prompt_path.read_text()
