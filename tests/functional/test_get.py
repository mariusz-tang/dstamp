"""functional/test_get.py

This module contains functional tests for the dstamp get command.
"""

from datetime import datetime

import pytest
from freezegun import freeze_time

from dstamp import round
from dstamp.format import Format
from tests.utils import config, dstamp_cli
from tests.utils.patched_time import now


@freeze_time(now)
def test_no_parameters():
    output = dstamp_cli.run_get()
    assert output.timestamp.timestamp == int(now.timestamp())


def test_copy_to_clipboard_cli_option():
    output = dstamp_cli.run_get("-x")
    assert output.copied_to_clipboard
    output = dstamp_cli.run_get("--copy-to-clipboard")
    assert output.copied_to_clipboard


def test_copy_to_clipboard_config_option():
    output = dstamp_cli.run_get()
    assert not output.copied_to_clipboard
    output = dstamp_cli.run_get(f"--config {config.COPY_CONFIG_PATH}")
    assert output.copied_to_clipboard


def test_no_copy_cli_option():
    output = dstamp_cli.run_get(f"--config {config.COPY_CONFIG_PATH} --no-copy")
    assert not output.copied_to_clipboard


@pytest.mark.parametrize("format", (format for format in Format))
def test_get_output_format_cli_option(format: Format):
    output = dstamp_cli.run_get(f"--output-format {format.value}")
    assert output.timestamp.format_code == format.code
    output = dstamp_cli.run_get(f"-f {format.value}")
    assert output.timestamp.format_code == format.code


def test_output_format_config_option():
    output = dstamp_cli.run_get()
    assert output.timestamp.format_code == Format.RELATIVE.code
    output = dstamp_cli.run_get(f"--config {config.SHORT_TIME_FORMAT_CONFIG_PATH}")
    assert output.timestamp.format_code == Format.SHORT_TIME.code


def test_round_and_precision_config_cli_options():
    output = dstamp_cli.run_get("15jun2025,537pm")
    assert output.timestamp.timestamp == int(datetime(2025, 6, 15, 17, 37).timestamp())

    output = dstamp_cli.run_get("15jun2025,537pm --round --precision 10m")
    assert output.timestamp.timestamp == datetime(2025, 6, 15, 17, 40).timestamp()

    output = dstamp_cli.run_get("15jun2025,537pm -rp 3H")
    assert output.timestamp.timestamp == datetime(2025, 6, 15, 18).timestamp()


def test_invalid_precision():
    output = dstamp_cli.run_get()
    assert not output.has_rounding_error

    output = dstamp_cli.run_get("-rp 1000")
    assert output.has_rounding_error

    output = dstamp_cli.run_get("-rp 60m")
    assert output.has_rounding_error

    output = dstamp_cli.run_get("-rp 24h")
    assert output.has_rounding_error


@freeze_time(now)
def test_rounding_and_precision_config_options():
    output = dstamp_cli.run_get()
    assert output.timestamp.timestamp == int(now.timestamp())

    # The default precision is 10m
    output = dstamp_cli.run_get("-r")
    assert (
        output.timestamp.timestamp
        == round.round_time_to_precision(now, "10m").timestamp()
    )

    output = dstamp_cli.run_get(f"--config {config.ROUNDING_CONFIG_PATH}")
    assert (
        output.timestamp.timestamp
        == round.round_time_to_precision(now, "15m").timestamp()
    )
