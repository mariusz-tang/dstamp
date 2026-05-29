# PYTHON_ARGCOMPLETE_OK
"""Dstamp's CLI interface."""

import argparse
import pathlib
from collections.abc import Iterable

import argcomplete

from dstamp import config, exceptions, subcommands


def construct_parser(config: dict) -> argparse.ArgumentParser:
    """Create the dstamp CLI argument parser."""
    # Add the help option manually so we can change the help message.
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Discord timestamp generator",
        epilog="Some options can be set via config file. See %(prog)s -h show-config",
        suggest_on_error=True,
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
        version="%(prog)s 3",
        help="Show version number and exit",
    )
    parser.add_argument(
        "--config",
        metavar="CONFIG_PATH",
        type=pathlib.Path,
        help="Alternative config file to use instead of the default. Should be "
        "a TOML file.",
    )

    subparsers = parser.add_subparsers(title="commands")
    subcommands.register_all(subparsers, config)

    return parser


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    default_config = config.parse()
    parser = construct_parser(default_config)
    argcomplete.autocomplete(parser)

    parsed_args = parser.parse_args(args)

    if parsed_args.config:
        # Re-parse the arguments with defaults from the new config.
        # We use this method because the config path needs to be known at parse
        # time, but we cannot determine an overridden config path before parsing.
        new_config = config.parse(parsed_args.config)
        parser = construct_parser(new_config)
        parsed_args = parser.parse_args(args)

    if not hasattr(parsed_args, "func") or parsed_args.help:
        parsed_args.print_help()
        return

    try:
        parsed_args.func(parsed_args)
    except exceptions.DstampError as e:
        parser.error(str(e))
