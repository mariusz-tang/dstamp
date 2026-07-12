import contextlib
import pathlib
import re
import tomllib
import typing
import unittest.mock
from datetime import UTC, datetime

import freezegun
import pyperclip
import pytest
import pytest_mock
from logassert import logassert

from dstamp import cli, logging


class RawOutput(typing.NamedTuple):
    out: str
    err: str


class AppRunner[T = RawOutput](typing.Protocol):
    def __call__(self, *args: str) -> T: ...


@pytest.fixture
def app(capsys: pytest.CaptureFixture[str]) -> AppRunner:
    """Return an app runner."""

    def run(*args: str) -> RawOutput:
        with contextlib.suppress(SystemExit):
            # We collect error information in other ways, so we can safely
            # ignore SystemExit. Otherwise, this would cause tests which
            # intentionally cause errors to fail.
            cli.run(args)
        return RawOutput(*capsys.readouterr())

    return run


class GetOutput:
    def __init__(self, raw_output: RawOutput) -> None:
        m = re.search(r"error: (.+)", raw_output.err)
        self.error_text = m[1] if m else ""

        m = re.match(r"<t:(-?\d+):([dDfFRsStT])>", raw_output.out)
        if m:
            self.timestamp = int(m[1])
            self.format_code = m[2]

        self.copied_to_clipboard = "Copied to clipboard!" in raw_output.out


type GetRunner = AppRunner[GetOutput]


@pytest.fixture
def get(app: AppRunner) -> GetRunner:
    def run(*args: str) -> GetOutput:
        return GetOutput(app("get", *args))

    return run


@pytest.fixture(autouse=True)
def copy_mock(mocker: pytest_mock.MockerFixture) -> unittest.mock.Mock:
    return mocker.patch("dstamp.subcommands.get.pyperclip.copy")


def test_no_args_prints_help(app: AppRunner) -> None:
    output = app()
    assert "Show this help message and exit" in output.out


def test_version_option_matches_pyproject(app: AppRunner) -> None:
    pyproject_path = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        project_config = tomllib.load(f)

    output = app("--version")
    assert project_config["project"]["version"] in output.out


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


def test_clipboard_error_is_printed(
    get: GetRunner, copy_mock: unittest.mock.Mock
) -> None:
    copy_mock.side_effect = pyperclip.PyperclipException
    output = get("--copy")
    assert "problem with the clipboard manager" in output.error_text


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


def test_get_datetime_is_logged(
    get: GetRunner, logs: logassert.FixtureLogChecker
) -> None:
    get("16jun2026", "5pm")
    assert "using datetime: " + re.escape(str(datetime(2026, 6, 16, 17))) in logs.info


def test_get_datetime_after_offset_is_logged(
    get: GetRunner, logs: logassert.FixtureLogChecker
) -> None:
    get("16jun2026", "5pm", "--offset", "2h")
    assert (
        "datetime after offset: " + re.escape(str(datetime(2026, 6, 16, 19)))
        in logs.info
    )


def test_get_datetime_after_rounding_is_logged(
    get: GetRunner, logs: logassert.FixtureLogChecker
) -> None:
    get("16jun2026", "5pm", "--precision", "6h")
    assert (
        "datetime after rounding: " + re.escape(str(datetime(2026, 6, 16, 18)))
        in logs.info
    )


def test_show_config(app: AppRunner, config_path: pathlib.Path) -> None:
    output = app("show-config")
    assert str(config_path) in output.out


def test_show_log(app: AppRunner) -> None:
    output = app("show-log")
    assert str(logging.LOG_DIR) in output.out


@freezegun.freeze_time("28 May 2021 16:52:04 UTC")
def test_config_option(app: AppRunner, config_path: pathlib.Path) -> None:
    new_config_path = config_path.parent / "new_config.toml"
    new_config_path.write_text("copy=false\nformat='long-time'\nprecision='1h'")
    output = GetOutput(app("--config", str(new_config_path), "get"))
    assert not output.copied_to_clipboard
    assert output.format_code == "T"
    assert output.timestamp == datetime(2021, 5, 28, 17, tzinfo=UTC).timestamp()


@freezegun.freeze_time("28 May 2021 16:52:04 UTC")
def test_config_option_overrides_default_config_file(
    app: AppRunner, config_path: pathlib.Path
) -> None:
    config_path.write_text("copy=false\nformat='long-time'\nprecision='1h'")
    new_config_path = config_path.parent / "new_config.toml"
    output = GetOutput(app("--config", str(new_config_path), "get"))
    assert output.copied_to_clipboard
    assert output.format_code == "F"
    assert output.timestamp == datetime(2021, 5, 28, 16, 52, 4, tzinfo=UTC).timestamp()


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["invalid", "args"],
        ["-h"],
        ["-h", "get"],
    ],
)
def test_logging_not_configured_if_command_not_resolved(
    app: AppRunner, logging_config_mock: unittest.mock.Mock, args: list[str]
) -> None:
    app(*args)
    logging_config_mock.assert_not_called()


def test_logging_is_configured_if_command_resolved(
    app: AppRunner, logging_config_mock: unittest.mock.Mock
) -> None:
    app("show-config")
    logging_config_mock.assert_called()


def test_unexpected_error_is_printed(
    get: GetRunner, mocker: pytest_mock.MockerFixture
) -> None:
    get_mock = mocker.patch("dstamp.subcommands.get._get")
    get_mock.side_effect = Exception
    output = get()
    assert "unexpected error" in output.error_text


def test_args_are_logged(app: AppRunner, logs: logassert.FixtureLogChecker) -> None:
    args = ["get", "20jan", "5pm", "-p", "2h"]
    app(*args)
    assert ".+".join(args) in logs.info


def test_sys_argv_is_logged(
    mocker: pytest_mock.MockerFixture, logs: logassert.FixtureLogChecker
) -> None:
    args = ["get", "20jan", "5pm", "-p", "2h"]
    mocker.patch("dstamp.cli.sys.argv", ["dstamp", *args])
    # Have to call run directly because the app fixture uses an empty list if
    # called with no args.
    cli.run()

    assert ".+".join(args) in logs.info


def test_config_file_location_is_logged(
    app: AppRunner,
    logs: logassert.FixtureLogChecker,
    config_path: pathlib.Path,
) -> None:
    app("show-config")
    assert f"using config in {config_path}" in logs.info


def test_config_file_location_is_logged_config_option_specified(
    app: AppRunner,
    logs: logassert.FixtureLogChecker,
    tmp_path: pathlib.Path,
) -> None:
    new_config_path = tmp_path / "new_config.toml"
    app("--config", str(new_config_path), "show-config")
    assert f"using config in {new_config_path}" in logs.info


def test_parsed_config_is_logged(
    app: AppRunner, logs: logassert.FixtureLogChecker, config_path: pathlib.Path
) -> None:
    config_path.write_text("copy=false")
    app("show-config")
    assert "computed config options: " + re.escape(str({"copy": False})) in logs.info


def test_unexpected_error_is_logged(
    get: GetRunner, mocker: pytest_mock.MockerFixture, logs: logassert.FixtureLogChecker
) -> None:
    get_mock = mocker.patch("dstamp.subcommands.get._get")
    get_mock.side_effect = Exception
    get()
    assert "unexpected error" in logs.error


def test_invalid_config_options_are_logged(
    get: GetRunner, config_path: pathlib.Path, logs: logassert.FixtureLogChecker
) -> None:
    config_path.write_text("copy=false\nformatt='short'\nprecisionn='1m'")
    get()
    assert "unknown keys in config file:" in logs.warning
    assert "formatt" in logs.warning
    assert "precisionn" in logs.warning


def test_default_log_verbosity_normal(
    get: GetRunner, mocker: pytest_mock.MockerFixture
) -> None:
    get_log_config = mocker.patch("dstamp.logging.get_config")
    get()
    get_log_config.assert_called_once_with("normal")


def test_quiet_option(app: AppRunner, mocker: pytest_mock.MockerFixture) -> None:
    get_log_config = mocker.patch("dstamp.logging.get_config")
    app("--quiet", "get")
    get_log_config.assert_called_once_with("quiet")


def test_quiet_config_option(
    get: GetRunner, mocker: pytest_mock.MockerFixture, config_path: pathlib.Path
) -> None:
    config_path.write_text("quiet=true")
    get_log_config = mocker.patch("dstamp.logging.get_config")
    get()
    get_log_config.assert_called_once_with("quiet")


def test_verbose_option(app: AppRunner, mocker: pytest_mock.MockerFixture) -> None:
    get_log_config = mocker.patch("dstamp.logging.get_config")
    app("--verbose", "get")
    get_log_config.assert_called_once_with("verbose")


def test_verbose_config_option(
    get: GetRunner, mocker: pytest_mock.MockerFixture, config_path: pathlib.Path
) -> None:
    config_path.write_text("verbose=true")
    get_log_config = mocker.patch("dstamp.logging.get_config")
    get()
    get_log_config.assert_called_once_with("verbose")


def test_verbose_overrides_quiet(
    app: AppRunner, mocker: pytest_mock.MockerFixture
) -> None:
    # --verbose should override --quiet because the latter is likely to be set
    # in a config file while the former is likely to only be set on the CLI.
    get_log_config = mocker.patch("dstamp.logging.get_config")
    app("--verbose", "--quiet", "get")
    get_log_config.assert_called_once_with("verbose")


def test_config_path_specified_but_does_not_exists_logs_warning(
    app: AppRunner, config_path: pathlib.Path, logs: logassert.FixtureLogChecker
) -> None:
    app("--config", str(config_path), "get")
    assert "specified config file does not exist" in logs.warning


def test_config_path_specified_but_is_not_a_file_logs_warning(
    app: AppRunner, config_path: pathlib.Path, logs: logassert.FixtureLogChecker
) -> None:
    app("--config", str(config_path.parent), "get")
    assert "specified config path is not a file" in logs.warning
