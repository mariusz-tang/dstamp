"""config.py

This module contains config file utilities.
"""

from pathlib import Path

import platformdirs

APP_NAME = "dstamp"


def get_config_path() -> Path:  # pragma: no cover
    # This function is patched in all our tests.
    app_dir = platformdirs.user_config_path(APP_NAME)
    return Path(app_dir) / "config.toml"
