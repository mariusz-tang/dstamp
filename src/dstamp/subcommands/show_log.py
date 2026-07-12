"""The show-log command."""

import argparse

from dstamp import cli, logging


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the show-log command as a subparser."""
    show_config: argparse.ArgumentParser = subparsers.add_parser(
        "show-log",
        help="Show the log location and exit.",
        description="Show the default logfile location and exit.",
        add_help=False,
        parents=[cli.base_parser],
    )
    show_config.set_defaults(func=_show_log)


def _show_log(_: argparse.Namespace) -> None:
    print(logging.LOG_DIR)
