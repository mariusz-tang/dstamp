"""functional/test_get.py

This module contains functional tests for the dstamp get command.
"""

from collections import namedtuple
from datetime import datetime

import pytest
from freezegun import freeze_time

from dstamp import parse, round
from dstamp.format import Format
from tests.utils.parse import DstampGetOutput
from tests.utils.patched_time import now

GetResult = namedtuple("GetResult", ["error_code", "output"])


@pytest.fixture
def get(app):
    """Return an app runner for the get command."""

    def run(*args):
        result = app("get", *args)
        output = DstampGetOutput(result.output)
        return GetResult(result.error_code, output)

    return run


@freeze_time(now)
def test_no_parameters(get):
    result = get()
    assert result.error_code == 0
    assert result.output.timestamp.timestamp == int(now.timestamp())


def test_copy_to_clipboard_cli_option(get):
    result = get("--copy-to-clipboard")
    assert result.error_code == 0
    assert result.output.copied_to_clipboard


def test_copy_to_clipboard_config_option(get, config_path):
    result = get()
    assert result.error_code == 0
    assert not result.output.copied_to_clipboard
    config_path.write_text("copy_to_clipboard = true")
    result = get()
    assert result.error_code == 0
    assert result.output.copied_to_clipboard


def test_no_copy_cli_option(get, config_path):
    config_path.write_text("copy_to_clipboard = true")
    result = get("--no-copy-to-clipboard")
    assert result.error_code == 0
    assert not result.output.copied_to_clipboard


@pytest.mark.parametrize("format", (format for format in Format))
def test_get_output_format_cli_option(get, format: Format):
    result = get("--output-format", format.name)
    assert result.error_code == 0
    assert result.output.timestamp.format_code == format.value


def test_output_format_config_option(get, config_path):
    result = get()
    assert result.error_code == 0
    assert result.output.timestamp.format_code == Format.RELATIVE.value
    config_path.write_text('output_format = "short-time"')
    result = get()
    assert result.error_code == 0
    assert result.output.timestamp.format_code == Format.SHORT_TIME.value


def test_round_and_precision_config_cli_options(get):
    result = get("15jun2025,537pm")
    assert result.error_code == 0
    assert result.output.timestamp.timestamp == int(
        datetime(2025, 6, 15, 17, 37).timestamp()
    )

    result = get("15jun2025,537pm", "--round", "--precision", "10m")
    assert result.error_code == 0
    assert (
        result.output.timestamp.timestamp == datetime(2025, 6, 15, 17, 40).timestamp()
    )

    result = get("15jun2025,537pm", "--round", "--precision", "3H")
    assert result.error_code == 0
    assert result.output.timestamp.timestamp == datetime(2025, 6, 15, 18).timestamp()


def test_invalid_precision(get):
    result = get()
    assert result.error_code == 0
    assert not result.output.has_rounding_error

    result = get("--round", "--precision", "1000")
    assert result.error_code == 1
    assert result.output.has_rounding_error

    result = get("--round", "--precision", "60m")
    assert result.error_code == 1
    assert result.output.has_rounding_error

    result = get("--round", "--precision", "24h")
    assert result.error_code == 1
    assert result.output.has_rounding_error


@freeze_time(now)
def test_rounding_and_precision_config_options(get, config_path):
    result = get()
    assert result.error_code == 0
    assert result.output.timestamp.timestamp == int(now.timestamp())

    # The default precision is 10m
    result = get("--round")
    assert result.error_code == 0
    assert (
        result.output.timestamp.timestamp
        == round.time_to_precision(now, parse.rounding_precision("10m")).timestamp()
    )

    config_path.write_text('round = true\nprecision = "15m"')
    result = get()
    assert result.error_code == 0
    assert (
        result.output.timestamp.timestamp
        == round.time_to_precision(now, parse.rounding_precision("15m")).timestamp()
    )
