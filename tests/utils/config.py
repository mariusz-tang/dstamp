"""config.py

This module contains utilities for handling config files in test cases.
"""

from pathlib import Path

test_dir = Path(__file__).resolve().parent.parent
test_config_dir = test_dir / "dstamp_config"


def _get_path_to_config_file(name: str) -> Path:
    return test_config_dir / f"{name}.toml"


EMPTY_CONFIG_PATH = _get_path_to_config_file("empty")
COPY_CONFIG_PATH = _get_path_to_config_file("copy")
SHORT_TIME_FORMAT_CONFIG_PATH = _get_path_to_config_file("output_format_shorttime")
INVALID_TOML_PATH = _get_path_to_config_file("invalid")
ROUNDING_CONFIG_PATH = _get_path_to_config_file("rounding")
