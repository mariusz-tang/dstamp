"""config.py

This module contains config file utilities.
"""

from pathlib import Path

import platformdirs

APP_NAME = "dstamp"


def get_config_path() -> Path:
    app_dir = platformdirs.user_config_path(APP_NAME, ensure_exists=True)
    return app_dir / "config.toml"
