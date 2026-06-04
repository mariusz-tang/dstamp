"""The get timestamp command."""

import argparse
import datetime as dt
import logging
from typing import Any

import pyperclip

from dstamp import discord, exceptions, parse, round

logger = logging.getLogger(__name__)


def register(subparsers: argparse._SubParsersAction, config: dict) -> None:
    """Register the get command as a subparser."""
    get: argparse.ArgumentParser = subparsers.add_parser(
        "get",
        help="Generate a timestamp",
        description="Generate a Discord-compatible timestamp",
        epilog="Some options can be set via config file. See %(prog)s -h show-config",
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
        choices=_output_formats.keys(),
        default="long-datetime",
        help="The output format to use. The default is long-datetime",
    ).completer = _output_format_completer  # ty: ignore[unresolved-attribute]
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
    get.set_defaults(print_help=get.print_help, func=_get, **config)


_output_formats = {
    "short-time": ("t", "18:01"),
    "long-time": ("T", "18:01:06"),
    "short-date": ("d", "29/05/2026"),
    "long-date": ("D", "29 May 2026"),
    "short-datetime": ("f", "29 May 2026 at 18:01"),
    "long-datetime": ("F", "Friday 29 May 2026 at 18:01"),
    "relative": ("R", "3 minutes ago"),
}


def _output_format_completer(**_: Any) -> dict:  # pragma: nocover
    return {key: "e.g. " + _output_formats[key][1] for key in _output_formats}


def _get(args: argparse.Namespace) -> None:
    datetime = _get_datetime(args.date, args.time)
    logger.info(f"using datetime: {datetime}")

    if args.offset:
        datetime += parse.offset(args.offset)
        logger.info(f"datetime after offset: {datetime}")

    precision = parse.precision(args.precision)
    datetime_rounded = round.datetime(datetime, precision)
    logger.info(f"datetime after rounding: {datetime_rounded}")

    format_code = _output_formats[args.format][0]
    timestamp = discord.timestamp(datetime_rounded, format_code)
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
