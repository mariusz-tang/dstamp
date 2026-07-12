"""Config file utilities.

The functions in this module do not create a config file if one does not exist.
"""

import pathlib
import tomllib
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


def parse(path: pathlib.Path | None = None) -> tuple[dict[str, Any], set[str]]:
    """Parse `path` as a config file and return the corresponding defaults dict.

    If `path` is `None`, the default given by `default_path()` is used.

    If `path` does not exist, it is treated as if it were an empty file.

    Returns a dictionary containing the parsed config and a set of invalid keys
    that were found at `path`.
    """
    if not path:
        path = default_path()

    if not path.is_file():
        return {}, set()

    config = tomllib.loads(path.read_text())
    cleaned_config = {key: value for key, value in config.items() if key in _VALID_KEYS}
    unknown_keys = config.keys() - _VALID_KEYS
    return cleaned_config, unknown_keys
