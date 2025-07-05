"""config.py

This module contains the config file loader and parser.
"""

import tomllib
from pathlib import Path

import typer
from pydantic import BaseModel

APP_NAME = "dstamp"


class DstampConfig(BaseModel):
    copy_to_clipboard: bool | None = None


def get() -> DstampConfig:
    app_dir = typer.get_app_dir(APP_NAME)
    config_path = Path(app_dir) / "config.toml"

    raw_config = {}
    if config_path.is_file():
        with open(config_path, "rb") as f:
            raw_config = tomllib.load(f)

    config = DstampConfig(**raw_config)
    return config
