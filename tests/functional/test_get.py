"""functional/test_get.py

This module contains functional tests for the dstamp get command.
"""

from datetime import datetime

import pytest
from freezegun import freeze_time

from dstamp import main, parse, round
from dstamp.format import Format
from tests.utils.parse import Timestamp
from tests.utils.patched_time import now


class GetOutput:
    """Represents dstamp get command output."""

    def __init__(self, raw_output: str):
        lines = raw_output.splitlines()
        self.has_rounding_error = "Invalid rounding precision:" in raw_output

        if self.has_rounding_error:
            # Rounding error means the program aborted so no other information
            # will be displayed.
            return

        timestamp = Timestamp(lines[1])
        self.timestamp = timestamp.timestamp
        self.format_code = timestamp.format_code
        self.copied_to_clipboard = main.COPY_SUCCESS_TEXT in raw_output


@pytest.fixture
def get(app):
    """Return an app runner for the get command."""

    def run(*args):
        error_code, output = app("get", *args)
        return error_code, GetOutput(output)

    return run


@freeze_time(now)
def test_no_parameters(get):
    error_code, output = get()
    assert error_code == 0
    assert output.timestamp == int(now.timestamp())


def test_copy_to_clipboard_cli_option(get):
    error_code, output = get("--copy-to-clipboard")
    assert error_code == 0
    assert output.copied_to_clipboard


def test_copy_to_clipboard_config_option(get, config_path):
    error_code, output = get()
    assert error_code == 0
    assert not output.copied_to_clipboard
    config_path.write_text("copy_to_clipboard = true")
    error_code, output = get()
    assert error_code == 0
    assert output.copied_to_clipboard


def test_no_copy_cli_option(get, config_path):
    config_path.write_text("copy_to_clipboard = true")
    error_code, output = get("--no-copy-to-clipboard")
    assert error_code == 0
    assert not output.copied_to_clipboard


@pytest.mark.parametrize("format", (format for format in Format))
def test_get_output_format_cli_option(get, format: Format):
    error_code, output = get("--output-format", format.name)
    assert error_code == 0
    assert output.format_code == format.value


def test_output_format_config_option(get, config_path):
    error_code, output = get()
    assert error_code == 0
    assert output.format_code == Format.RELATIVE.value
    config_path.write_text('output_format = "short-time"')
    error_code, output = get()
    assert error_code == 0
    assert output.format_code == Format.SHORT_TIME.value


def test_round_and_precision_config_cli_options(get):
    error_code, output = get("15jun2025,537pm")
    assert error_code == 0
    assert output.timestamp == int(datetime(2025, 6, 15, 17, 37).timestamp())

    error_code, output = get("15jun2025,537pm", "--round", "--precision", "10m")
    assert error_code == 0
    assert output.timestamp == datetime(2025, 6, 15, 17, 40).timestamp()

    error_code, output = get("15jun2025,537pm", "--round", "--precision", "3H")
    assert error_code == 0
    assert output.timestamp == datetime(2025, 6, 15, 18).timestamp()


def test_invalid_precision(get):
    error_code, output = get()
    assert error_code == 0
    assert not output.has_rounding_error

    error_code, output = get("--round", "--precision", "1000")
    assert error_code == 1
    assert output.has_rounding_error

    error_code, output = get("--round", "--precision", "60m")
    assert error_code == 1
    assert output.has_rounding_error

    error_code, output = get("--round", "--precision", "24h")
    assert error_code == 1
    assert output.has_rounding_error


@freeze_time(now)
def test_rounding_and_precision_config_options(get, config_path):
    error_code, output = get()
    assert error_code == 0
    assert output.timestamp == int(now.timestamp())

    # The default precision is 10m
    error_code, output = get("--round")
    assert error_code == 0
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision("10m")).timestamp()
    )

    config_path.write_text('round = true\nprecision = "15m"')
    error_code, output = get()
    assert error_code == 0
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision("15m")).timestamp()
    )
