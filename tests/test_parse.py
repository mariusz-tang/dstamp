from datetime import date, time

import freezegun
import pytest

from dstamp import parse


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("20jan2025", date(2025, 1, 20)),
        ("1may2026", date(2026, 5, 1)),
        ("31dec1", date(1, 12, 31)),
    ],
)
def test_date_full(input: str, expected_output: date) -> None:
    assert parse.date(input) == expected_output


@pytest.mark.parametrize(
    ("month_name", "month_id"),
    [
        ("jan", 1),
        ("feb", 2),
        ("mar", 3),
        ("apr", 4),
        ("may", 5),
        ("jun", 6),
        ("jul", 7),
        ("aug", 8),
        ("sep", 9),
        ("oct", 10),
        ("nov", 11),
        ("dec", 12),
    ],
)
def test_date_months(month_name: str, month_id: int) -> None:
    assert parse.date(f"1{month_name}2000") == date(2000, month_id, 1)


@freezegun.freeze_time("April 15th 2022")
def test_date_no_year_implies_current_year() -> None:
    assert parse.date("10aug") == date(2022, 8, 10)


@pytest.mark.parametrize("input", ["10jan0", "32aug", "29feb2023"])
def test_date_invalid_date_raises(input: str) -> None:
    with pytest.raises(parse.InvalidDateError) as e:
        parse.date(input)
    assert e.value.input == input


def test_date_invalid_format_raises() -> None:
    with pytest.raises(parse.FormatError) as e:
        parse.date("not a date")
    assert e.value.input == "not a date"


def test_date_checks_full_match() -> None:
    with pytest.raises(parse.FormatError) as e:
        parse.date("12jan plus some extra")
    assert e.value.input == "12jan plus some extra"


def test_date_ignores_case() -> None:
    assert parse.date("10AuG") == parse.date("10aug")


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
    with pytest.raises(parse.InvalidTimeError) as e:
        parse.time(input)
    assert e.value.input == input


def test_time_invalid_format_raises() -> None:
    with pytest.raises(parse.FormatError) as e:
        parse.time("not a time")
    assert e.value.input == "not a time"


def test_time_checks_full_match() -> None:
    with pytest.raises(parse.FormatError) as e:
        parse.time("12pm plus some extra")
    assert e.value.input == "12pm plus some extra"


@pytest.mark.parametrize("input", ["0pm", "13am", "16pm"])
def test_time_24_hour_with_ampm_is_a_format_error(input: str) -> None:
    with pytest.raises(parse.FormatError) as e:
        parse.time(input)
    assert e.value.input == input
