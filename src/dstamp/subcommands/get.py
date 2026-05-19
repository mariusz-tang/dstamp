"""The get timestamp command."""

import argparse
import datetime as dt

from dstamp import discord, parse


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the get command as a subparser."""
    get = subparsers.add_parser("get")
    get.add_argument("date", nargs="?")
    get.add_argument("time", nargs="?")
    get.set_defaults(func=_get)


def _get(args: argparse.Namespace) -> None:
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
