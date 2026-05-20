from datetime import time

import freezegun
import pytest

from dstamp import exceptions, parse


@pytest.mark.parametrize("input", range(24))
def test_time_24_hour_hour_only(input: int) -> None:
    assert parse.time(str(input)) == time(input)


@pytest.mark.parametrize(
    ("input", "hour"),
    [
        ("12pm", 12),
        ("12am", 0),
        ("3am", 3),
        ("6pm", 18),
    ],
)
def test_time_12_hour_hour_only(input: str, hour: int) -> None:
    assert parse.time(input) == time(hour)


@pytest.mark.parametrize(
    ("input", "hour", "minute"),
    [
        ("1104", 11, 4),
        ("304", 3, 4),
        ("1754", 17, 54),
        ("006", 0, 6),
        ("0006", 0, 6),
        ("2359", 23, 59),
        ("1104am", 11, 4),
        ("304pm", 15, 4),
        ("1254am", 0, 54),
        ("1259pm", 12, 59),
    ],
)
def test_time_hour_and_minute_only(input: str, hour: int, minute: int) -> None:
    assert parse.time(input) == time(hour, minute)


@pytest.mark.parametrize(
    ("input", "hour", "minute", "second"),
    [
        ("00000", 0, 0, 0),
        ("000000", 0, 0, 0),
        ("23421", 2, 34, 21),
        ("172822", 17, 28, 22),
        ("111111pm", 23, 11, 11),
        ("14932am", 1, 49, 32),
    ],
)
def test_time_full(input: str, hour: int, minute: int, second: int) -> None:
    assert parse.time(input) == time(hour, minute, second)


def test_time_ignores_case() -> None:
    assert parse.time("10aM") == parse.time("10am")


@pytest.mark.parametrize("input", ["2500", "360", "31560"])
def test_time_invalid_time_raises(input: str) -> None:
    with pytest.raises(exceptions.ParserValueError) as e:
        parse.time(input)
    assert e.value.input == input
    assert e.value.output_type == time


def test_time_invalid_format_raises() -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.time("not a time")
    assert e.value.input == "not a time"


def test_time_checks_full_match() -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.time("12pm plus some extra")
    assert e.value.input == "12pm plus some extra"


@pytest.mark.parametrize("input", ["0pm", "13am", "16pm"])
def test_time_24_hour_with_ampm_is_a_format_error(input: str) -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.time(input)
    assert e.value.input == input


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("now", time(15, 54, 4)),
        ("midnight", time()),
        ("noon", time(12)),
    ],
)
@freezegun.freeze_time("20 May 2026 3:54:04pm")
def test_time_keywords(input: str, expected_output: time) -> None:
    assert parse.time(input) == expected_output
