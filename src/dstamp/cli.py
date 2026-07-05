# PYTHON_ARGCOMPLETE_OK
"""Dstamp's CLI interface."""

import argparse
import logging
import logging.config
import pathlib
import sys
from collections.abc import Iterable

import argcomplete
import pyperclip

import dstamp.logging
from dstamp import config, exceptions, subcommands

logger = logging.getLogger(__name__)

# Use a base parser to change the help flag's help message.
base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument(
    "-h",
    "--help",
    action="help",
    help="Show this help message and exit.",
)


def construct_parser(config: dict | None = None) -> argparse.ArgumentParser:
    """Create the dstamp CLI argument parser."""
    # Add the help option manually so we can change the help message.
    parser = argparse.ArgumentParser(
        add_help=False,
        parents=[base_parser],
        description="Discord timestamp generator",
        epilog="Some options can be set via config file. See %(prog)s -h show-config",
        suggest_on_error=True,
    )
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
    subcommands.register_all(subparsers, config or {})

    return parser


def run(args: Iterable[str] | None = None) -> None:
    """Parse `args` as CLI arguments and execute the resulting command."""
    parser = construct_parser()
    argcomplete.autocomplete(parser)

    # Move help flags past subcommands so the most specific help message is shown.
    args = _move_help_to_end(args or sys.argv[1:])
    parsed_args = parser.parse_args(args)

    # Print help if no arguments are provided.
    if not hasattr(parsed_args, "func"):
        parser.print_help()
        return

    # Only log if a command was resolved.
    logging.config.dictConfig(dstamp.logging.CONFIG)
    logger.info(f"args: {args or sys.argv[1:]}")

    # Compute the config path.
    config_path = parsed_args.config or config.default_path()
    logger.info(f"using config in {config_path}")

    # Re-parse the arguments with defaults from the config.
    # We use this method because the config path needs to be known at parse
    # time, but we cannot determine an overridden config path before parsing.
    parsed_config = config.parse(config_path)
    logger.info(f"computed config options: {parsed_config}")
    parser = construct_parser(parsed_config)
    parsed_args = parser.parse_args(args)

    try:
        parsed_args.func(parsed_args)
    except exceptions.DstampError as e:
        parser.error(str(e))
    except pyperclip.PyperclipException as e:
        parser.error(f"there was a problem with the clipboard manager: {e}")
    except Exception:
        logger.exception("An unexpected error occurred.")
        parser.error("an unexpected error occurred; please report this to dstamp")


def _move_help_to_end(args: Iterable[str]) -> Iterable[str]:
    args = list(args)
    if "-h" not in args and "--help" not in args:
        return args

    # Remove --version so it doesn't override the help flag if present.
    _remove_arg(args, "--version")
    _remove_arg(args, "--help")
    _remove_arg(args, "-h")

    args.append("--help")
    return args


def _remove_arg(args: list[str], arg: str) -> None:
    while arg in args:
        args.remove(arg)
