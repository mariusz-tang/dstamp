"""main.py

This module contains the commands provided by dstamp.
"""

import sys
from pathlib import Path

import cyclopts.config
from cyclopts import App, Parameter
from typing_extensions import Annotated

from . import clipboard, config, console, format, parse, round

app = App(help="Discord timestamp generator")


@app.meta.default
def meta(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    config_path: Annotated[Path | None, Parameter("config")] = None,
):
    if config_path is None:
        config_path = config.get_config_path()
    app.config = cyclopts.config.Toml(config_path, use_commands_as_keys=False)
    app(tokens)


@app.command(name="get")
def get_timestamp(
    time: Annotated[
        str,
        Parameter(
            help="The date and time to which the timestamp should point. "
            "If omitted, the current time is used.",
        ),
    ] = "",
    offset: Annotated[
        str,
        Parameter(
            name=["--offset", "-o"],
            help="Optional offset to apply to TIME. Examples: 2d3h1m, +3s, -3d+1d, "
            "3m-3h2h. The only acceptable units are d(ays), h(ours), m(inutes), "
            "and s(econds). Subtraction applies to all times after the - until "
            "the next +. Units can be repeated.",
        ),
    ] = "",
    output_format: Annotated[
        format.Format | None,
        Parameter(
            name=["--output-format", "-f"],
            help="The format in which the timestamp will be displayed in Discord.",
        ),
    ] = format.Format.RELATIVE,
    copy_to_clipboard: Annotated[
        bool | None,
        Parameter(
            name=["--copy-to-clipboard", "-x"],
            negative="--no-copy",
            help="If set, copy the timestamp to clipboard. "
            "On Linux, requires that xsel or xclip be installed.",
        ),
    ] = False,
    do_rounding: Annotated[
        bool | None,
        Parameter(
            name=["--round", "-r"],
            help="If specified, round TIME based on --precision.",
        ),
    ] = False,
    precision: Annotated[
        str | None,
        Parameter(
            name=["--precision", "-p"],
            help="The precision to which TIME will be rounded if --round is specified.",
        ),
    ] = "10m",
):
    """
    Generate a Discord timestamp.

    If TIME is omitted, uses the current time.

    TIME should be of the form <date>,<time>.
    Either <date> or <time> can be omitted, in which case you should omit the
    comma as well.

    <date> should be of the following form: ddmmmyyyy.

    dd and yyyy should be numbers.

    mmm should be at least the first three letters of the month. For instance,
    for August you can specify aug, augu, augus, or august.

    You can omit the year to specify the current year. You can omit <date>
    entirely to specify the current date.

    The command will also accept the following special values:
    today,
    tmrw (tomorrow),
    tomorrow,
    yesterday.

    <time> should be of the following form: hhmmss(am/pm).

    You can omit seconds to specify 0. If you do, you can omit minutes to specify
    0 as well. If you omit (am/pm), 24-hour time will be used. You can omit <time>
    entirely to specify midnight.

    If you omit both <date> and <time>, the current date and time will be used.

    The command will also accept the following special values:
    now (the current time, but not necessarily the current date),
    midnight,
    noon.

    Examples:
    5jun,1pm (5th June of the current year, 1:00pm),
    8january2025,1530 (8th January 2025, 3:30pm),
    25nov2000,13002pm (25th November 2000, 1:30:02pm),
    1jan (1st January of the current year, midnight),
    7feb2023,15 (7th February 2023, 3:00pm),
    5 (the current date, 5:00am),
    0 (the current date, midnight),
    tmrw,now (tomorrow, the current time, ie. 24 hours from the current time),
    tmrw (tomorrow, midnight).
    """
    time = parse.datetime_string(time)
    offset = parse.offset(offset)

    target_time = time + offset
    if do_rounding:
        target_time = try_round(target_time, precision)

    output = format.convert_to_discord_format(target_time, output_format)

    console.info(f"Using time: {round.round_time_to_precision(target_time, '1s')}.")
    console.print(output)

    if copy_to_clipboard:
        clipboard.copy(output)


def fill_value(user_provided_value, filler_value):
    """
    Return filler_value if user_provided value is None.

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
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    app.meta()
