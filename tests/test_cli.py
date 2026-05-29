import contextlib
import pathlib
import re
import tomllib
import typing
import unittest.mock
from datetime import UTC, datetime

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


type GetRunner = AppRunner[GetOutput]


@pytest.fixture
def get(app: AppRunner[str]) -> GetRunner:
    def run(*args: str) -> GetOutput:
        return GetOutput(app("get", *args))

    return run


@pytest.fixture(autouse=True)
def copy_mock(mocker: pytest_mock.MockerFixture) -> unittest.mock.Mock:
    return mocker.patch("dstamp.subcommands.get.pyperclip.copy")


def test_no_args_prints_help(app: AppRunner[str]) -> None:
    output = app()
    assert "Show this help message and exit" in output


def test_version_option_matches_pyproject(app: AppRunner[str]) -> None:
    pyproject_path = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        project_config = tomllib.load(f)

    output = app("--version")
    assert project_config["project"]["version"] in output


@freezegun.freeze_time(datetime.fromtimestamp(1234567890.2139))
def test_get_no_args_returns_current_time(get: GetRunner) -> None:
    output = get()
    assert output.timestamp == 1234567890


def test_get_date_only_uses_midnight(get: GetRunner) -> None:
    output = get("10jan2025")
    assert output.timestamp == datetime(2025, 1, 10).timestamp()


@freezegun.freeze_time("October 10 2025")
def test_get_time_only_uses_current_date(get: GetRunner) -> None:
    output = get("9pm")
    assert output.timestamp == datetime(2025, 10, 10, 21).timestamp()


def test_get_date_and_time(get: GetRunner) -> None:
    output = get("25jun2028", "550pm")
    assert output.timestamp == datetime(2028, 6, 25, 17, 50).timestamp()


def test_get_no_args_produces_no_error_text(get: GetRunner) -> None:
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
def test_get_invalid_datetime_prints_error(
    get: GetRunner, args: list[str], expected_error_text: str
) -> None:
    output = get(*args)
    assert expected_error_text in output.error_text


def test_get_copy_enabled_by_default(
    get: GetRunner, copy_mock: unittest.mock.Mock
) -> None:
    output = get()
    timestamp = f"<t:{output.timestamp}:{output.format_code}>"
    copy_mock.assert_called_with(timestamp)
    assert output.copied_to_clipboard


def test_get_copy_option(get: GetRunner, copy_mock: unittest.mock.Mock) -> None:
    output = get("--copy")
    timestamp = f"<t:{output.timestamp}:{output.format_code}>"
    copy_mock.assert_called_with(timestamp)
    assert output.copied_to_clipboard


def test_get_copy_short_option(get: GetRunner, copy_mock: unittest.mock.Mock) -> None:
    output = get("-c")
    timestamp = f"<t:{output.timestamp}:{output.format_code}>"
    copy_mock.assert_called_with(timestamp)
    assert output.copied_to_clipboard


def test_get_no_copy_option(get: GetRunner, copy_mock: unittest.mock.Mock) -> None:
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
    get: GetRunner,
    option_name: str,
    option_value: str,
    expected_format_code: str,
) -> None:
    output = get(option_name, option_value)
    assert output.format_code == expected_format_code


def test_get_output_format_option_defaults_to_long_datetime(get: GetRunner) -> None:
    output = get()
    assert output.format_code == "F"


@pytest.mark.parametrize("option_name", ["-o", "--offset"])
@pytest.mark.parametrize(
    ("option_value", "expected_datetime"),
    [
        ("1d", datetime(2026, 5, 25, 14, 35, 49, tzinfo=UTC)),
        ("b3s", datetime(2026, 5, 24, 14, 35, 46, tzinfo=UTC)),
    ],
)
@freezegun.freeze_time("24th May 2026, 14:35:49 UTC")
def test_get_offset_option(
    get: GetRunner, option_name: str, option_value: str, expected_datetime: datetime
) -> None:
    output = get(option_name, option_value)
    assert output.timestamp == expected_datetime.timestamp()


@pytest.mark.parametrize("option_name", ["-p", "--precision"])
@pytest.mark.parametrize(
    ("option_value", "expected_datetime"),
    [
        ("1s", datetime(2030, 1, 1, 23, 43, 12)),
        ("2h", datetime(2030, 1, 2)),
        ("3m", datetime(2030, 1, 1, 23, 42)),
    ],
)
@freezegun.freeze_time(datetime(2030, 1, 1, 23, 43, 12, 121))
def test_get_precision_option(
    get: GetRunner, option_name: str, option_value: str, expected_datetime: datetime
) -> None:
    output = get(option_name, option_value)
    assert output.timestamp == expected_datetime.timestamp()


@pytest.mark.parametrize("option_name", ["-p", "--precision"])
def test_get_invalid_precision_quantity_prints_error(
    get: GetRunner, option_name: str
) -> None:
    output = get(option_name, "61s")
    assert "quantity for second must be between 1 and 60" in output.error_text
    assert "must be a factor of 60" in output.error_text
    assert "actual quantity was 61" in output.error_text


@pytest.mark.parametrize("option_name", ["-p", "--precision"])
def test_get_invalid_precision_format_prints_error(
    get: GetRunner, option_name: str
) -> None:
    output = get(option_name, "24f")
    assert "invalid precision format" in output.error_text


@freezegun.freeze_time("28 May 2021 16:52:04 UTC")
def test_get_config_file_options(get: GetRunner, config_path: pathlib.Path) -> None:
    config_path.write_text("copy=false\nformat='long-time'\nprecision='1h'")
    output = get()
    assert not output.copied_to_clipboard
    assert output.format_code == "T"
    assert output.timestamp == datetime(2021, 5, 28, 17, tzinfo=UTC).timestamp()


@freezegun.freeze_time("28 May 2021 16:52:04 UTC")
def test_get_cli_args_override_config_file_options(
    get: GetRunner, config_path: pathlib.Path
) -> None:
    config_path.write_text("copy=false\nformat='long-time'\nprecision='1h'")
    output = get("--copy", "--format", "short-time", "--precision", "1s")
    assert output.copied_to_clipboard
    assert output.format_code == "t"
    assert output.timestamp == datetime(2021, 5, 28, 16, 52, 4, tzinfo=UTC).timestamp()


def test_show_config(app: AppRunner[str], config_path: pathlib.Path) -> None:
    output = app("show-config")
    assert str(config_path) in output


@freezegun.freeze_time("28 May 2021 16:52:04 UTC")
def test_config_option(app: AppRunner[str], config_path: pathlib.Path) -> None:
    new_config_path = config_path.parent / "new_config.toml"
    new_config_path.write_text("copy=false\nformat='long-time'\nprecision='1h'")
    output = GetOutput(app("--config", str(new_config_path), "get"))
    assert not output.copied_to_clipboard
    assert output.format_code == "T"
    assert output.timestamp == datetime(2021, 5, 28, 17, tzinfo=UTC).timestamp()


@freezegun.freeze_time("28 May 2021 16:52:04 UTC")
def test_config_option_overrides_default_config_file(
    app: AppRunner[str], config_path: pathlib.Path
) -> None:
    config_path.write_text("copy=false\nformat='long-time'\nprecision='1h'")
    new_config_path = config_path.parent / "new_config.toml"
    output = GetOutput(app("--config", str(new_config_path), "get"))
    assert output.copied_to_clipboard
    assert output.format_code == "F"
    assert output.timestamp == datetime(2021, 5, 28, 16, 52, 4, tzinfo=UTC).timestamp()
