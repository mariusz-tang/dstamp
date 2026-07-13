"""Config file utilities.

The functions in this module do not create a config file if one does not exist.
"""

import pathlib
from typing import Any

import platformdirs

import dstamp


def default_path() -> pathlib.Path:
    """Return the default config file path.

    Note that the file does not necessarily exist.
    """
    config_dir = platformdirs.user_config_path(dstamp.APP_NAME)
    return config_dir / "config.toml"


_VALID_KEYS = {
    "copy",
    "format",
    "precision",
    "quiet",
    "verbose",
}


def clean(config: dict) -> tuple[dict[str, Any], set[str]]:
    """Clean a config dict so it contains only valid keys.

    Returns a dictionary containing the cleaned config and a set containing the
    invalid keys that were found in the input.
    """
    cleaned_config = {key: value for key, value in config.items() if key in _VALID_KEYS}
    unknown_keys = config.keys() - _VALID_KEYS
    return cleaned_config, unknown_keys
