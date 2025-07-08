"""config.py

This module contains the config file loader and parser.
"""

import tomllib
from functools import cache
from pathlib import Path

import typer
from pydantic import BaseModel

from . import format

APP_NAME = "dstamp"


class DstampConfig(BaseModel):
    copy_to_clipboard: bool = False
    output_format: format.Format = format.Format.RELATIVE

    def __str__(self):
        def convert_to_line(option):
            if type(option) is str:
                option = (option, getattr(self, option))
            name, value = option
            return f"{name}: {value}"

        options = (
            "copy_to_clipboard",
            ("output_format", self.output_format.value),
        )
        lines = (convert_to_line(option) for option in options)
        return "\n".join(lines)


@cache
def get(config_path: Path) -> DstampConfig:
    """Load the config file and return config object."""
    config_path = config_path or get_config_path()

    raw_config = {}
    if config_path.is_file():
        with open(config_path, "rb") as f:
            raw_config = tomllib.load(f)

    config = DstampConfig(**raw_config)
    return config


def get_config_path() -> Path:
    app_dir = typer.get_app_dir(APP_NAME)
    return Path(app_dir) / "config.toml"
