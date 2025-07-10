"""utils/dstamp_cli.py

This module provides functions for executing dstamp commands.
"""

from typing import Optional

from typer.testing import CliRunner

from dstamp.main import app
from tests.utils import parse

runner = CliRunner()


def run_get(args: Optional[str] = None) -> parse.DstampGetOutput:
    return _run("get", args, parse.DstampGetOutput)


def _run(keyword: str, raw_args: Optional[str], output_class):
    """
    Run the command and parse the output.

    The command must not contain spaces in any arguments (even in quoted
    strings).
    """
    command = _make_command(keyword, raw_args)
    args = command.split(" ")
    result = runner.invoke(app, args)
    return output_class(result.output)


def _make_command(keyword: str, args: Optional[str]) -> str:
    if args is None:
        return keyword
    return f"{keyword} {args}"
