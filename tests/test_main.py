"""test_main.py

This module contains tests for the dstamp.main module.
These are predominantly functional tests on the commands offered by Dstamp.
"""

from freezegun import freeze_time
from typer.testing import CliRunner

from dstamp.format import Format
from dstamp.main import app
from tests.utils.parse import DstampOutput
from tests.utils.patched_time import now

runner = CliRunner()


def get_output_for_command(command: str) -> DstampOutput:
    """
    Run the command and parse the output.

    The command must not contain spaces in any arguments (even in quoted
    strings).
    """
    args = command.split(" ")
    result = runner.invoke(app, args)
    return DstampOutput(result.output)


@freeze_time(now)
def test_get():
    output = get_output_for_command("get")
    assert output.timestamp.timestamp == int(now.timestamp())
    assert output.timestamp.format_code == Format.RELATIVE.code
    assert not output.copied_to_clipboard
