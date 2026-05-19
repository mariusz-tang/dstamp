"""Dstamp's CLI interface."""

import argparse
from collections.abc import Iterable

from dstamp import subcommands

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
subcommands.register_all(subparsers)


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    parsed_args = parser.parse_args(args)

    if hasattr(parsed_args, "func"):
        parsed_args.func(parsed_args)
    else:
        parser.print_help()
