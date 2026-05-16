from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"


def load_yaml_config(config_name: str) -> dict[str, Any]:
    """
    Load a YAML configuration file from the config directory.

    Example:
        load_yaml_config("validation.yaml")
        load_yaml_config("modeling.yaml")
    """
    config_path = CONFIG_DIR / config_name

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        return {}

    if not isinstance(config, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {config_path}")

    return config