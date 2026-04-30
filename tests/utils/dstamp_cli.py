"""utils/dstamp_cli.py

This module provides functions for executing dstamp commands.
"""

from typing import Optional

from dstamp.main import app
from tests.utils import parse


def run_get(capsys, args: Optional[str] = None) -> parse.DstampGetOutput:
    return _run(capsys, "get", args, parse.DstampGetOutput)


def run_show_config(capsys, args: Optional[str] = None) -> parse.DstampShowConfigOutput:
    return _run(capsys, "show-config", args, parse.DstampShowConfigOutput)


def _run(capsys, keyword: str, raw_args: Optional[str], output_class):
    """
    Run the command and parse the output.

    The command must not contain spaces in any arguments (even in quoted
    strings).
    """
    command = _make_command(keyword, raw_args)
    args = command.split(" ")
    try:
        app(args, result_action="return_value")
    except SystemExit:
        # Todo: remove this after changing the app to return an error code
        # instead of raising SystemExit.
        pass
    result = capsys.readouterr().out
    return output_class(result)


def _make_command(keyword: str, args: Optional[str]) -> str:
    if args is None:
        return keyword
    return f"{keyword} {args}"
