"""Dstamp subcommands."""

import argparse

from . import get


def register_all(subparsers: argparse._SubParsersAction) -> None:
    """Register all subcommands as subparsers."""
    get.register(subparsers)


__all__ = ["register_all"]
