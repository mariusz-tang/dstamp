# PYTHON_ARGCOMPLETE_OK
"""Dstamp's CLI interface."""

import argparse
from collections.abc import Iterable

import argcomplete

from dstamp import exceptions, subcommands

# Add the help option manually so we can change the help message.
parser = argparse.ArgumentParser(
    description="Discord timestamp generator", add_help=False
)
parser.add_argument(
    "-h",
    "--help",
    action="store_true",
    help="Show this help message and exit. For command-specific help, use "
    "%(prog)s -h COMMAND",
)
parser.set_defaults(print_help=parser.print_help)
parser.add_argument(
    "--version",
    action="version",
    version="%(prog)s 2",
    help="Show version number and exit",
)

subparsers = parser.add_subparsers()
subcommands.register_all(subparsers)


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    argcomplete.autocomplete(parser)
    parsed_args = parser.parse_args(args)

    if not hasattr(parsed_args, "func") or parsed_args.help:
        parsed_args.print_help()
        return

    try:
        parsed_args.func(parsed_args)
    except exceptions.DstampError as e:
        parser.error(str(e))
