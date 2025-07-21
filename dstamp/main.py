"""main.py

This module contains the commands provided by dstamp.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from . import clipboard, config, console, format, parse, round

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback():
    """Discord Timestamp Generator."""


FROM_CONFIG = "from config"


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
        Optional[format.Format],
        typer.Option(
            "--output-format",
            "-f",
            show_default=FROM_CONFIG,
            help="The format in which the timestamp will be displayed in Discord.",
        ),
    ] = None,
    copy_to_clipboard: Annotated[
        Optional[bool],
        typer.Option(
            "--copy-to-clipboard/--no-copy",
            "-x",
            show_default=FROM_CONFIG,
            help="If set, copy the timestamp to clipboard. "
            "On Linux, requires that xsel or xclip be installed.",
        ),
    ] = None,
    config_path: Annotated[
        Optional[Path],
        typer.Option(
            "--config",
            "-c",
            show_default=False,
            exists=True,
            dir_okay=False,
            help="If specified, read config from this file instead of the default "
            "location.",
        ),
    ] = None,
    do_rounding: Annotated[
        bool,
        typer.Option(
            "--round/--no-round",
            "-r",
            help="If specified, round TIME based on --precision.",
        ),
    ] = False,
    precision: Annotated[
        str,
        typer.Option(
            "--precision",
            "-p",
            help="The precision to which TIME will be rounded if --round is specified.",
        ),
    ] = "10m",
):
    """
    Generate a Discord timestamp.

    If TIME is omitted, uses the current time.
    """
    cfg = config.get(config_path)
    output_format = fill_value(output_format, cfg.output_format)

    target_time = time + offset
    if do_rounding:
        target_time = try_round(target_time, precision)

    output = format.convert_to_discord_format(target_time, output_format)

    console.info(f"Using time: {round.round_time_to_precision(target_time, "1s")}.")
    console.print(output)

    copy_to_clipboard = fill_value(copy_to_clipboard, cfg.copy_to_clipboard)
    if copy_to_clipboard:
        clipboard.copy(output)


def fill_value(user_provided_value, filler_value):
    """
    Return filler_value is user_provided value is None.

    Otherwise, return user_provided_value.
    """
    if user_provided_value is not None:
        return user_provided_value
    return filler_value


def try_round(time, precision):
    try:
        return round.round_time_to_precision(time, precision)
    except round.RoundingError as e:
        console.error(f"There was an error in rounding:\n{e.message}")
        raise typer.Exit(code=1)


@app.command()
def show_config(
    path: Annotated[
        Optional[Path],
        typer.Argument(
            show_default=False,
            exists=True,
            dir_okay=False,
            help="If specified, use this config file instead of the default.",
        ),
    ] = None,
):
    """Show the currently-active configuration settings and file location."""
    if path is None:
        path = config.get_config_path()
    console.info(f"Using config at {path}\n")
    console.print(config.get(path))


if __name__ == "__main__":  # pragma: no cover
    app()
