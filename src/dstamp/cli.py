"""Dstamp's CLI interface."""

import argparse
from collections.abc import Iterable

from dstamp import exceptions, subcommands

parser = argparse.ArgumentParser(description="Discord timestamp generator")
parser.add_argument("--version", action="version", version="%(prog)s 2")
subparsers = parser.add_subparsers()
subcommands.register_all(subparsers)


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    parsed_args = parser.parse_args(args)

    if not hasattr(parsed_args, "func"):
        parser.print_help()
        return

    try:
        parsed_args.func(parsed_args)
    except exceptions.DstampError as e:
        parser.error(str(e))
