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


@freeze_time(now)
def test_get():
    result = runner.invoke(app, ["get"])
    output = DstampOutput(result.output)
    assert output.timestamp.timestamp == int(now.timestamp())
    assert output.timestamp.format_code == Format.RELATIVE.code
    assert not output.copied_to_clipboard
