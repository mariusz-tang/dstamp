from datetime import datetime

import clipman
import typer
from typing_extensions import Annotated

from . import format

app = typer.Typer(no_args_is_help=True)


@app.command()
def main(
    time: datetime,
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
    output = format.convert_to_discord_format(time, output_format)
    print(output)
    if copy_to_clipboard:
        clipman.init()
        clipman.set(output)
        print("Copied to clipboard!")


if __name__ == "__main__":
    app()
