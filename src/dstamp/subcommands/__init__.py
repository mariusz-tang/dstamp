"""Dstamp subcommands."""

import argparse

from . import get, show_config


def register_all(subparsers: argparse._SubParsersAction, config: dict) -> None:
    """Register all subcommands as subparsers."""
    get.register(subparsers, config)
    show_config.register(subparsers)


__all__ = ["register_all"]
