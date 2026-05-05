"""functional/test_get.py

This module contains functional tests for the dstamp get command.
"""

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
def test_defaults(get):
    error_code, output = get()
    assert error_code == 0
    assert not output.has_rounding_error
    assert output.timestamp == now.timestamp()
    assert output.format_code == Format.RELATIVE.value
    assert not output.copied_to_clipboard


def test_copy_to_clipboard_cli_option(get):
    error_code, output = get("--copy-to-clipboard")
    assert error_code == 0
    assert output.copied_to_clipboard


def test_copy_to_clipboard_config_option(get, config_path):
    config_path.write_text("copy-to-clipboard = true")
    error_code, output = get()
    assert error_code == 0
    assert output.copied_to_clipboard


def test_copy_cli_option_overrides_config(get, config_path):
    config_path.write_text("copy-to-clipboard = false")
    error_code, output = get("--copy-to-clipboard")
    assert error_code == 0
    assert output.copied_to_clipboard


def test_no_copy_cli_option_overrides_config(get, config_path):
    config_path.write_text("copy-to-clipboard = true")
    error_code, output = get("--no-copy-to-clipboard")
    assert error_code == 0
    assert not output.copied_to_clipboard


@pytest.mark.parametrize("format", (format for format in Format))
def test_format_cli_option(get, format):
    error_code, output = get("--output-format", format.name)
    assert error_code == 0
    assert output.format_code == format.value


@pytest.mark.parametrize("format", (format for format in Format))
def test_format_config_option(get, config_path, format):
    config_path.write_text(f'output-format = "{format.name}"')
    error_code, output = get()
    assert error_code == 0
    assert output.format_code == format.value


def test_format_cli_option_overrides_config(get, config_path):
    config_path.write_text('output-format = "SHORTTIME"')
    error_code, output = get("--output-format", "RELATIVE")
    assert error_code == 0
    assert output.format_code == "R"


@freeze_time(now)
def test_round_cli_option(get):
    error_code, output = get("--round")
    assert error_code == 0
    # 10m is the default rounding precision.
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision("10m")).timestamp()
    )


@freeze_time(now)
def test_round_config_option(get, config_path):
    config_path.write_text("round = true")
    error_code, output = get()
    assert error_code == 0
    # 10m is the default rounding precision.
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision("10m")).timestamp()
    )


@freeze_time(now)
def test_round_cli_option_overrides_config(get, config_path):
    config_path.write_text("round = false")
    error_code, output = get("--round")
    assert error_code == 0
    # 10m is the default rounding precision.
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision("10m")).timestamp()
    )


@freeze_time(now)
def test_no_round_cli_option_overrides_config(get, config_path):
    config_path.write_text("round = true")
    error_code, output = get("--no-round")
    assert error_code == 0
    # 10m is the default rounding precision.
    assert output.timestamp == now.timestamp()


@pytest.mark.parametrize("precision", ["3s", "4m", "12h"])
@freeze_time(now)
def test_precision_cli_option(get, precision):
    error_code, output = get("--round", "--precision", precision)
    assert error_code == 0
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision(precision)).timestamp()
    )


@freeze_time(now)
def test_precision_cli_option_overrides_config(get, config_path):
    config_path.write_text('precision = "3m"')
    error_code, output = get("--round", "--precision", "12h")
    assert error_code == 0
    assert (
        output.timestamp
        == round.time_to_precision(now, parse.rounding_precision("12h")).timestamp()
    )


def test_invalid_precision(get):
    error_code, output = get("--round", "--precision", "24h")
    assert error_code == 1
    assert output.has_rounding_error
