"""The show-config command."""

import argparse

from dstamp import cli, config


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the show-config command as a subparser."""
    show_config: argparse.ArgumentParser = subparsers.add_parser(
        "show-config",
        help="Show the default config location and exit",
        description="Show the default configuration file location and exit",
        epilog="The config file should contain valid TOML. Valid keys are copy "
        "(bool), format (string), precision (string), quiet (bool), and verbose "
        "(bool), which override the default values for the corresponding options "
        "for other commands.",
        add_help=False,
        parents=[cli.base_parser],
    )
    show_config.set_defaults(func=_show_config)


def _show_config(_: argparse.Namespace) -> None:
    print(config.default_path())
