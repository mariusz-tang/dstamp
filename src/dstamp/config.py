"""Config file utilities.

The functions in this module do not create a config file if one does not exist.
"""

import pathlib
import tomllib
import warnings

import platformdirs

_APP_NAME = "dstamp"


def default_path() -> pathlib.Path:
    """Return the default config file path.

    Note that the file does not necessarily exist.
    """
    config_dir = platformdirs.user_config_path(_APP_NAME)
    return config_dir / "config.toml"


_VALID_KEYS = {
    "copy",
    "format",
    "precision",
}


def parse(path: pathlib.Path) -> dict:
    """Parse `path` as a config file and return the corresponding defaults dict.

    If `path` does not exist, it is treated as if it were an empty file.
    """
    if not path.exists():
        return {}

    config = tomllib.loads(path.read_text())

    if unknown_keys := config.keys() - _VALID_KEYS:
        warnings.warn(
            f"unknown keys in config file: {', '.join(unknown_keys)}", stacklevel=2
        )

    return config
