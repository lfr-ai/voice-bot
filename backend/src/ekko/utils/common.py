from pathlib import Path

from ekko.config.settings import get_settings

SETTINGS = get_settings()


def _validate_file_path(dir_path: Path, filename: str, suffix: str) -> Path:
    """Validate and return a path to a file.

    Raises FileNotFoundError or ValueError on failure.
    """

    path = dir_path / filename
    if not path.is_file():
        raise FileNotFoundError(f"File '{filename}' not found in '{dir_path!s}'.")
    if path.suffix != suffix:
        raise ValueError(f"File '{filename}' must have a '{suffix}' extension.")
    return path


def load_prompt(filename: str) -> str:
    """Load a prompt text file from the configured prompts directory."""
    prompt_dir = SETTINGS.prompt_dir_path
    prompt_path = _validate_file_path(Path(prompt_dir), filename, ".txt")
    return prompt_path.read_text(encoding="utf8")
