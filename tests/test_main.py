"""test_main.py

This module contains tests for the dstamp.main module.
These are predominantly functional tests on the commands offered by Dstamp.
"""

import pytest
from freezegun import freeze_time
from typer.testing import CliRunner

from dstamp.format import Format
from dstamp.main import app
from tests.utils import config
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


def test_get_copy_to_clipboard_cli_option():
    output = get_output_for_command("get -x")
    assert output.copied_to_clipboard
    output = get_output_for_command("get --copy-to-clipboard")
    assert output.copied_to_clipboard


def test_get_copy_to_clipboard_config_option():
    output = get_output_for_command("get")
    assert not output.copied_to_clipboard
    output = get_output_for_command(f"get --config {config.COPY_CONFIG_PATH}")
    assert output.copied_to_clipboard


def test_get_no_copy_cli_option():
    output = get_output_for_command(f"get --config {config.COPY_CONFIG_PATH} --no-copy")
    assert not output.copied_to_clipboard


@pytest.mark.parametrize("format", (format for format in Format))
def test_get_output_format_cli_option(format: Format):
    output = get_output_for_command(f"get --output-format {format.value}")
    assert output.timestamp.format_code == format.code
    output = get_output_for_command(f"get -f {format.value}")
    assert output.timestamp.format_code == format.code


def test_get_output_format_config_option():
    output = get_output_for_command("get")
    assert output.timestamp.format_code == Format.RELATIVE.code
    output = get_output_for_command(
        f"get --config {config.SHORT_TIME_FORMAT_CONFIG_PATH}"
    )
    assert output.timestamp.format_code == Format.SHORT_TIME.code
