"""utils/dstamp_cli.py

This module provides functions for executing dstamp commands.
"""

import contextlib

from dstamp.main import app
from tests.utils import parse


def run_get(capsys, args: str | None = None) -> parse.DstampGetOutput:
    return _run(capsys, "get", args, parse.DstampGetOutput)


def _run(capsys, keyword: str, raw_args: str | None, output_class):
    """
    Run the command and parse the output.

    The command must not contain spaces in any arguments (even in quoted
    strings).
    """
    command = _make_command(keyword, raw_args)
    args = command.split(" ")
    with contextlib.suppress(SystemExit):
        app.meta(args, result_action="return_value")
    result = capsys.readouterr().out
    return output_class(result)


def _make_command(keyword: str, args: str | None) -> str:
    if args is None:
        return keyword
    return f"{keyword} {args}"
