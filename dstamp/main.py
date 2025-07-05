"""main.py

This module contains the commands provided by dstamp.
"""

from datetime import datetime, timedelta

import typer
from typing_extensions import Annotated

from . import clipboard, config, format, parse

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback():
    """Discord Timestamp Generator."""


@app.command("get")
def get_timestamp(
    time: Annotated[
        datetime,
        typer.Argument(
            parser=parse.datetime_string,
            show_default=False,
            help="The date and time to which the timestamp should point. "
            "If omitted, the current time is used.",
        ),
    ] = "",
    offset: Annotated[
        timedelta,
        typer.Option(
            "--offset",
            "-o",
            parser=parse.offset,
            show_default=False,
            help="Optional offset to apply to TIME. Examples: 2d3h1m, +3s, -1w3d.",
        ),
    ] = "",
    output_format: Annotated[
        format.Format,
        typer.Option(
            "--output-format",
            "-f",
            help="The format in which the timestamp will be displayed in Discord.",
        ),
    ] = format.Format.RELATIVE,
    copy_to_clipboard: Annotated[
        bool,
        typer.Option(
            "--copy-to-clipboard/--no-copy",
            "-x",
            help="If set, copy the timestamp to clipboard. "
            "On Linux, requires that xsel or xclip be installed.",
        ),
    ] = None,
):
    """
    Generate a Discord timestamp.

    If TIME is omitted, uses the current time.
    """
    output = format.convert_to_discord_format(time + offset, output_format)
    cfg = config.get()
    copy_to_clipboard = get_value_after_config(
        copy_to_clipboard, cfg.copy_to_clipboard, False
    )
    print(output)
    if copy_to_clipboard:
        clipboard.copy(output)


def get_value_after_config(cli_value, config_value, default):
    if cli_value is not None:
        return cli_value
    if config_value is not None:
        return config_value
    return default


if __name__ == "__main__":
    app()
