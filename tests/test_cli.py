import contextlib
import re
import typing
import unittest.mock
from datetime import datetime

import freezegun
import pytest
import pytest_mock

import dstamp.cli


class AppRunner[T](typing.Protocol):
    def __call__(self, *args: str) -> T: ...


@pytest.fixture
def app(capsys: pytest.CaptureFixture) -> AppRunner[str]:
    """Return an app runner."""

    def run(*args: str) -> str:
        with contextlib.suppress(SystemExit):
            # We collect error information in other ways, so we can safely
            # ignore SystemExit. Otherwise, this would cause tests which
            # intentionally cause errors to fail.
            dstamp.cli.run(args)
        out, err = capsys.readouterr()
        return out or err

    return run


class GetOutput:
    def __init__(self, raw_output: str) -> None:
        m = re.search(r"error: (.+)", raw_output)
        self.error_text = m[1] if m else ""
        if self.error_text:
            # There won't be any meaningful output after an error is emitted.
            return

        m = re.match(r"<t:(-?\d+):([dDfFRsStT])>", raw_output)
        assert m, "No timestamp in output"
        self.timestamp = int(m[1])
        self.format_code = m[2]
        self.copied_to_clipboard = "Copied to clipboard!" in raw_output


@pytest.fixture
def get(app: AppRunner[str]) -> AppRunner[GetOutput]:
    def run(*args: str) -> GetOutput:
        return GetOutput(app("get", *args))

    return run


@pytest.fixture(autouse=True)
def copy_mock(mocker: pytest_mock.MockerFixture) -> unittest.mock.Mock:
    return mocker.patch("dstamp.subcommands.get.pyperclip.copy")


def test_no_args_prints_help(
    app: AppRunner[str], mocker: pytest_mock.MockFixture
) -> None:
    print_help = mocker.patch("dstamp.cli.parser.print_help")
    app()
    print_help.assert_called_once()


@freezegun.freeze_time(datetime.fromtimestamp(1234567890.2139))
def test_get_no_args_returns_current_time(get: AppRunner[GetOutput]) -> None:
    output = get()
    assert output.timestamp == 1234567890


def test_get_no_args_uses_long_full_format(get: AppRunner[GetOutput]) -> None:
    output = get()
    assert output.format_code == "F"


def test_get_date_only_uses_midnight(get: AppRunner[GetOutput]) -> None:
    output = get("10jan2025")
    assert output.timestamp == datetime(2025, 1, 10).timestamp()


@freezegun.freeze_time("October 10 2025")
def test_get_time_only_uses_current_date(get: AppRunner[GetOutput]) -> None:
    output = get("9pm")
    assert output.timestamp == datetime(2025, 10, 10, 21).timestamp()


def test_get_date_and_time(get: AppRunner[GetOutput]) -> None:
    output = get("25jun2028", "550pm")
    assert output.timestamp == datetime(2028, 6, 25, 17, 50).timestamp()


def test_get_no_args_produces_no_error_text(get: AppRunner[GetOutput]) -> None:
    output = get()
    assert not output.error_text


@pytest.mark.parametrize(
    ("args", "expected_error_text"),
    [
        (["bad date format", "0000"], "invalid date format"),
        (["32jan", "0000"], "input represents an invalid date"),
        (["1jan", "bad time format"], "invalid time format"),
        (["1jan", "2500"], "input represents an invalid time"),
        (["32jan"], "input represents an invalid date"),
        (["2500"], "input represents an invalid time"),
        (["bad format"], "invalid time format"),
    ],
)
def test_get_invalid_data_prints_error(
    get: AppRunner[GetOutput], args: list[str], expected_error_text: str
) -> None:
    output = get(*args)
    assert expected_error_text in output.error_text


def test_get_copy_enabled_by_default(
    get: AppRunner[GetOutput], copy_mock: unittest.mock.Mock
) -> None:
    output = get()
    timestamp = f"<t:{output.timestamp}:{output.format_code}>"
    copy_mock.assert_called_with(timestamp)
    assert output.copied_to_clipboard


def test_get_copy_option(
    get: AppRunner[GetOutput], copy_mock: unittest.mock.Mock
) -> None:
    output = get("--copy")
    timestamp = f"<t:{output.timestamp}:{output.format_code}>"
    copy_mock.assert_called_with(timestamp)
    assert output.copied_to_clipboard


def test_get_copy_short_option(
    get: AppRunner[GetOutput], copy_mock: unittest.mock.Mock
) -> None:
    output = get("-c")
    timestamp = f"<t:{output.timestamp}:{output.format_code}>"
    copy_mock.assert_called_with(timestamp)
    assert output.copied_to_clipboard


def test_get_no_copy_option(
    get: AppRunner[GetOutput], copy_mock: unittest.mock.Mock
) -> None:
    output = get("--no-copy")
    copy_mock.assert_not_called()
    assert not output.copied_to_clipboard


@pytest.mark.parametrize("option_name", ["-f", "--format"])
@pytest.mark.parametrize(
    ("option_value", "expected_format_code"),
    [
        ("short-time", "t"),
        ("long-time", "T"),
        ("short-date", "d"),
        ("long-date", "D"),
        ("short-datetime", "f"),
        ("long-datetime", "F"),
        ("relative", "R"),
    ],
)
def test_get_output_format_option(
    get: AppRunner[GetOutput],
    option_name: str,
    option_value: str,
    expected_format_code: str,
) -> None:
    output = get(option_name, option_value)
    assert output.format_code == expected_format_code
