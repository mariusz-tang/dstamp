"""Functional tests for the get command."""

import re
from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from dstamp import main, parse, round
from dstamp.format import Format

NOW = datetime(2025, 1, 2, 12, 53, 42, 12)
NOW_ROUNDED = NOW.replace(microsecond=0)


class GetOutput:
    """Represents get command output."""

    def __init__(self, raw_output: str):
        self.has_datetime_error = (
            "could not be parsed as a datetime" in raw_output
            or "invalid datetime" in raw_output
        )
        self.has_offset_error = (
            "could not be parsed as a offset" in raw_output
            or "invalid offset" in raw_output
        )
        if self.has_datetime_error or self.has_offset_error:
            # Either of these means the program aborted so no other information
            # will be displayed.
            return

        self.has_rounding_error = "Invalid rounding precision:" in raw_output
        if self.has_rounding_error:
            # Rounding error means the program aborted so no other information
            # will be displayed.
            return

        self.copied_to_clipboard = main.COPY_SUCCESS_TEXT in raw_output

        lines = raw_output.splitlines()
        m = re.fullmatch(r"<t:(\d+):([tTdDfFR])>", lines[1])
        assert m is not None, "No timestamp in output"
        self.timestamp = int(m[1])
        self.format_code = m[2]


@pytest.fixture
def get(app):
    """Return an app runner for the get command."""

    def run(*args):
        error_code, output = app("get", *args)
        return error_code, GetOutput(output)

    return run


@freeze_time(NOW)
def test_defaults(get):
    error_code, output = get()
    assert error_code == 0
    assert not output.has_datetime_error
    assert not output.has_offset_error
    assert not output.has_rounding_error
    assert output.timestamp == NOW_ROUNDED.timestamp()
    assert output.format_code == Format.RELATIVE.value
    assert not output.copied_to_clipboard


@pytest.mark.parametrize(
    "time,expected_datetime",
    [
        ("20mar2026,4pm", datetime(2026, 3, 20, 16)),
        ("20", NOW_ROUNDED.replace(hour=20, minute=0, second=0)),
        ("tmrw", NOW_ROUNDED.replace(hour=0, minute=0, second=0) + timedelta(1)),
        ("yesterday,now", NOW_ROUNDED - timedelta(1)),
    ],
)
@freeze_time(NOW)
def test_time_argument(get, time, expected_datetime):
    error_code, output = get(time)
    assert error_code == 0
    assert output.timestamp == expected_datetime.timestamp()


def test_invalid_time(get):
    error_code, output = get("25pm")
    assert error_code == 1
    assert output.has_datetime_error


@pytest.mark.parametrize(
    "offset,expected_timedelta",
    [
        ("2d", timedelta(2)),
        ("1m", timedelta(minutes=1)),
        ("2d-3m", timedelta(2, minutes=-3)),
    ],
)
@freeze_time(NOW)
def test_offset_cli_option(get, offset, expected_timedelta):
    error_code, output = get("--offset", offset)
    assert error_code == 0
    assert output.timestamp == (NOW_ROUNDED + expected_timedelta).timestamp()


@freeze_time(NOW)
def test_offset_cli_option_negative(get):
    # Values beginning with - don't work without the = notation.
    # This is not a test for that fact, it's just testing that values beginning
    # with - are interpretted correctly at all.
    error_code, output = get("--offset=-5s")
    assert error_code == 0
    assert output.timestamp == (NOW_ROUNDED + timedelta(seconds=-5)).timestamp()


def test_invalid_offset(get):
    error_code, output = get("--offset=10g")
    assert error_code == 1
    assert output.has_offset_error


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


def round_time(time, raw_precision):
    return round.time_to_precision(time, parse.rounding_precision(raw_precision))


@freeze_time(NOW)
def test_round_cli_option(get):
    error_code, output = get("--round")
    assert error_code == 0
    # 10m is the default rounding precision.
    assert output.timestamp == round_time(NOW, "10m").timestamp()


@freeze_time(NOW)
def test_round_config_option(get, config_path):
    config_path.write_text("round = true")
    error_code, output = get()
    assert error_code == 0
    # 10m is the default rounding precision.
    assert output.timestamp == round_time(NOW, "10m").timestamp()


@freeze_time(NOW)
def test_round_cli_option_overrides_config(get, config_path):
    config_path.write_text("round = false")
    error_code, output = get("--round")
    assert error_code == 0
    # 10m is the default rounding precision.
    assert output.timestamp == round_time(NOW, "10m").timestamp()


@freeze_time(NOW)
def test_no_round_cli_option_overrides_config(get, config_path):
    config_path.write_text("round = true")
    error_code, output = get("--no-round")
    assert error_code == 0
    # 10m is the default rounding precision.
    assert output.timestamp == NOW_ROUNDED.timestamp()


@pytest.mark.parametrize("precision", ["3s", "4m", "12h"])
@freeze_time(NOW)
def test_precision_cli_option(get, precision):
    error_code, output = get("--round", "--precision", precision)
    assert error_code == 0
    assert output.timestamp == round_time(NOW, precision).timestamp()


@freeze_time(NOW)
def test_precision_cli_option_overrides_config(get, config_path):
    config_path.write_text('precision = "3m"')
    error_code, output = get("--round", "--precision", "12h")
    assert error_code == 0
    assert output.timestamp == round_time(NOW, "12h").timestamp()


def test_invalid_precision(get):
    error_code, output = get("--round", "--precision", "24h")
    assert error_code == 1
    assert output.has_rounding_error
