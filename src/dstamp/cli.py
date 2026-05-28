# PYTHON_ARGCOMPLETE_OK
"""Dstamp's CLI interface."""

import argparse
from collections.abc import Iterable

import argcomplete

from dstamp import exceptions, subcommands


def construct_parser() -> argparse.ArgumentParser:
    """Create the dstamp CLI argument parser."""
    # Add the help option manually so we can change the help message.
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Discord timestamp generator",
        epilog="Some options can be set via config file. See %(prog)s -h show-config",
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

    return parser


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    parser = construct_parser()
    argcomplete.autocomplete(parser)
    parsed_args = parser.parse_args(args)

    if not hasattr(parsed_args, "func") or parsed_args.help:
        parsed_args.print_help()
        return

    try:
        parsed_args.func(parsed_args)
    except exceptions.DstampError as e:
        parser.error(str(e))
