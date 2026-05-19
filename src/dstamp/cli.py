"""Dstamp's CLI interface."""

import argparse
import datetime as dt
from collections.abc import Iterable

from dstamp import discord, parse

parser = argparse.ArgumentParser()
subcommands = parser.add_subparsers()
get = subcommands.add_parser("get")
get.add_argument("date", nargs="?")
get.add_argument("time", nargs="?")


def run_get(args: argparse.Namespace) -> None:
    """Execute the get subcommand."""
    datetime = _get_datetime(args.date, args.time)
    print(discord.timestamp(datetime, "F"))


def _get_datetime(date: str | None, time: str | None) -> dt.datetime:
    if not date:
        return dt.datetime.now()
    if not time:
        date_or_time = _parse_date_or_time(date)
        if isinstance(date_or_time, dt.date):
            return dt.datetime.combine(date_or_time, dt.time())
        return dt.datetime.combine(dt.date.today(), date_or_time)
    return dt.datetime.combine(parse.date(date), parse.time(time))


def _parse_date_or_time(input: str) -> dt.date | dt.time:
    try:
        return parse.date(input)
    except parse.FormatError:
        return parse.time(input)


get.set_defaults(func=run_get)


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        parser.print_help()
