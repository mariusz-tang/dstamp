"""Dstamp's CLI interface."""

import argparse
from collections.abc import Iterable
from datetime import datetime

import dstamp.discord

parser = argparse.ArgumentParser()
subcommands = parser.add_subparsers()
get = subcommands.add_parser("get")


def run_get(_: argparse.Namespace) -> None:
    """Execute the get subcommand."""
    print(dstamp.discord.timestamp(datetime.now(), "F"))


get.set_defaults(func=run_get)


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        parser.print_help()
