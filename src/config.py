"""GROOT-01 configuration loader."""

from pathlib import Path

import yaml



CONFIG_FILE = Path("config.yaml")



def load_config() -> dict:
    """Load GROOT configuration from YAML."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config if config else {}
