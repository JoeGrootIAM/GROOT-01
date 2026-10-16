"""GROOT-01 simple human-readable logging."""

import logging
from pathlib import Path



def setup_logging(log_file: str) -> logging.Logger:
    """Create and configure the GROOT logger."""
    path = Path(log_file).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("groot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(path)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )
        logger.addHandler(handler)

    return logger



def log_action(logger: logging.Logger, action: str, result: str, details: str) -> None:
    """Record an observable GROOT action."""
    logger.info("%s | %s | %s", action, result, details)
