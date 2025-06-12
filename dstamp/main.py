from datetime import datetime

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
):
    output = format.convert_to_discord_format(time, output_format)
    print(output)


if __name__ == "__main__":
    app()
