"""main.py

This module contains the commands provided by dstamp.
"""

from datetime import datetime
from typing import Optional

import typer
from typing_extensions import Annotated

from . import clipboard, format, parse

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback():
    """Discord Timestamp Generator."""


@app.command("get")
def get_timestamp(
    time: Annotated[
        datetime,
        typer.Argument(
            default_factory=datetime.now,
            show_default=False,
            help="The date and time to which the timestamp should point. "
            "If omitted, the current time is used.",
        ),
    ],
    offset: Annotated[
        Optional[str],
        typer.Argument(
            show_default=False,
            help="Optional offset to apply to TIME. Examples: 2d3h1m, +3s, -1w3d.",
        ),
    ] = None,
    output_format: Annotated[
        format.Format,
        typer.Option(
            help="The format in which the timestamp will be displayed in Discord."
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
    ] = False,
):
    """
    Generate a Discord timestamp.

    If TIME is omitted, uses the current time.
    """
    delta = parse.parse_offset(offset)
    output = format.convert_to_discord_format(time + delta, output_format)
    print(output)
    if copy_to_clipboard:
        clipboard.copy(output)


if __name__ == "__main__":
    app()
