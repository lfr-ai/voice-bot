import logging
from pathlib import Path


class Logger:
    """
    Wrapper for making file-based loggers.
    """

    @staticmethod
    def create(name: str, filename: Path | str) -> logging.Logger:
        """
        Create a logger with the specified name, writing to the specified file.

        Args:
            name (str): Name of the logger.
            filename (Path | str): Name of the file.

        Returns:
            logging.Logger: The configured logger.
        """
        logger = logging.getLogger(name)
        handler = logging.FileHandler(filename)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
