"""The get timestamp command."""

import argparse
import datetime as dt

import pyperclip

from dstamp import config, discord, exceptions, parse, round


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the get command as a subparser."""
    get: argparse.ArgumentParser = subparsers.add_parser(
        "get",
        help="Generate a timestamp",
        description="Generate a Discord-compatible timestamp",
        add_help=False,
    )
    get.add_argument(
        "date",
        nargs="?",
        help="Examples: 1jan2025, 30may2020, 6jun. If the year is omitted, the "
        "current year is used. If the entire date is omitted, the current date "
        "is used. Accepts special keywords: today, tomorrow, tmrw, yesterday",
    )
    get.add_argument(
        "time",
        nargs="?",
        help="Examples: 1, 15, 1730, 35004pm. If omitted, midnight is used. If "
        "the date is also omitted, the current time is used instead. Can be "
        "provided even if the date is omitted. Accepts special keywords: now "
        "(current time), midnight, noon",
    )
    get.add_argument(
        "-c",
        "--copy",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="If set, copy the result to clipboard. Enabled by default",
    )
    get.add_argument(
        "-f",
        "--format",
        choices=_format_codes.keys(),
        default="long-datetime",
        help="The output format to use. The default is long-datetime",
    )
    get.add_argument(
        "-o",
        "--offset",
        help="An offset to apply to the date and time. Examples: 1d (one day), "
        "3h5m (three hours and five minutes), 5s (five seconds). The only valid "
        "units are d (days), h (hours), m (minutes), and s (seconds). Units can "
        "be repeated, for example 5s3d2s would be three days and seven (5+2) "
        "seconds. Units can be specified in any order. To specify a backwards "
        "offset, prefix the offset with b, for example b1d would be backwards "
        "one day",
    )
    get.add_argument(
        "-p",
        "--precision",
        default="1s",
        help="The precision to which the date and time should be rounded. "
        "Examples: 1s, 30m, 2h, 24h, 60s, 60m. The only valid units are h "
        "(hours), m (minutes), and s (seconds). The quantity must be a factor "
        "of 60 (minutes or seconds) or 24 (hours). The default is 1s",
    )
    get.set_defaults(
        print_help=get.print_help,
        func=_get,
        **config.parse(config.default_path()),
    )


_format_codes = {
    "short-time": "t",
    "long-time": "T",
    "short-date": "d",
    "long-date": "D",
    "short-datetime": "f",
    "long-datetime": "F",
    "relative": "R",
}


def _get(args: argparse.Namespace) -> None:
    datetime = _get_datetime(args.date, args.time)

    if args.offset:
        datetime += parse.offset(args.offset)

    precision = parse.precision(args.precision)
    datetime_rounded = round.datetime(datetime, precision)

    timestamp = discord.timestamp(datetime_rounded, _format_codes[args.format])
    print(timestamp)

    if args.copy:
        pyperclip.copy(timestamp)
        print("Copied to clipboard!")


def _get_datetime(date: str | None, time: str | None) -> dt.datetime:
    if not date:
        # Use current time if neither date nor time are provided.
        return dt.datetime.now()
    if not time:
        date_or_time = _parse_date_or_time(date)
        if isinstance(date_or_time, dt.date):
            # Use midnight if only date is provided.
            return dt.datetime.combine(date_or_time, dt.time())
        # Use current date if only time is provided.
        return dt.datetime.combine(dt.date.today(), date_or_time)
    # Note that it's not possible for time to be defined but not date because
    # they are both optional positional arguments.
    return dt.datetime.combine(parse.date(date), parse.time(time))


def _parse_date_or_time(input: str) -> dt.date | dt.time:
    try:
        return parse.date(input)
    except exceptions.ParserFormatError:
        return parse.time(input)
