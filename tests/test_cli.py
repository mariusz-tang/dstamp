import re
import typing
from datetime import datetime

import freezegun
import pytest
import pytest_mock

import dstamp.cli


class AppRunner[T](typing.Protocol):
    def __call__(self, *args: str) -> T: ...


@pytest.fixture
def app(capsys: pytest.CaptureFixture) -> AppRunner[str]:
    def run(*args: str) -> str:
        dstamp.cli.run(args)
        return capsys.readouterr().out

    return run


class GetOutput:
    def __init__(self, raw_output: str) -> None:
        m = re.match(r"<t:(-?\d+):([dDfFRsStT])>", raw_output)
        assert m, "No timestamp in output"
        self.timestamp = int(m[1])
        self.format_code = m[2]


@pytest.fixture
def get(app: AppRunner[str]) -> AppRunner[GetOutput]:
    def run(*args: str) -> GetOutput:
        return GetOutput(app("get", *args))

    return run


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
