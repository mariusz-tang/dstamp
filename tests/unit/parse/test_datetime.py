"""Tests for the datetime parser."""

from datetime import date, datetime, time, timedelta

import pytest
from freezegun import freeze_time

from dstamp import parse

NOW = datetime(2025, 1, 2, 12, 53, 42, 213)
NOW_ROUNDED = NOW.replace(microsecond=0)
TODAY = NOW.date()


@pytest.mark.parametrize(
    "raw_input,desired_date",
    [
        # Day and month only assumes the current year.
        ("2jun", datetime(NOW.year, 6, 2)),
        ("31augus", datetime(NOW.year, 8, 31)),
        ("28february", datetime(NOW.year, 2, 28)),
        # Day, month, and year.
        ("12june2024", datetime(2024, 6, 12)),
        ("1dec2026", datetime(2026, 12, 1)),
        ("14novem2025", datetime(2025, 11, 14)),
    ],
)
@freeze_time(NOW)
def test_date_only(raw_input, desired_date):
    assert parse.datetime(raw_input) == desired_date


@pytest.mark.parametrize(
    "raw_input,desired_time",
    [
        # Keywords.
        ("now", NOW_ROUNDED.time()),
        ("noon", time(12)),
        ("midnight", time()),
        # Hour only.
        ("2", time(2)),
        ("06", time(6)),
        ("23", time(23)),
        ("4am", time(4)),
        ("05pm", time(17)),
        # Hour and minute only.
        ("330", time(3, 30)),
        ("1623", time(16, 23)),
        ("830pm", time(20, 30)),
        # Hour, minute, and second.
        ("200943", time(20, 9, 43)),
        ("100942", time(10, 9, 42)),
        ("115943pm", time(23, 59, 43)),
    ],
)
@freeze_time(NOW)
def test_time_only_assumes_today(raw_input, desired_time):
    assert parse.datetime(raw_input) == datetime.combine(TODAY, desired_time)


@freeze_time(NOW)
def test_empty_string_returns_now():
    assert parse.datetime("") == NOW_ROUNDED


@freeze_time(NOW)
def test_none_returns_now():
    assert parse.datetime(None) == NOW_ROUNDED


@pytest.mark.parametrize(
    "raw_input,desired_output",
    [
        ("24aug2000,midnight", datetime(2000, 8, 24)),
        ("today,now", NOW_ROUNDED),
        ("tmrw,7pm", datetime.combine(TODAY + timedelta(days=1), time(19))),
        ("yesterday,noon", datetime.combine(TODAY - timedelta(days=1), time(12))),
        ("4jan,1am", datetime.combine(date(TODAY.year, 1, 4), time(1))),
        ("yesterday,1234am", datetime.combine(TODAY - timedelta(1), time(0, 34))),
    ],
)
@freeze_time(NOW)
def test_full_datetime(raw_input, desired_output):
    assert parse.datetime(raw_input) == desired_output


@freeze_time(NOW)
def test_12am_is_midnight():
    assert parse.datetime("12am") == datetime.combine(TODAY, time())


@freeze_time(NOW)
def test_12pm_is_noon():
    assert parse.datetime("12pm") == datetime.combine(TODAY, time(12))


@pytest.mark.parametrize(
    "input", ["today,now,now", "in two days", "2203pm", "24notamonth2032"]
)
def test_invalid_format_raises_invalid_format_error(input):
    with pytest.raises(parse.InvalidFormatError):
        parse.datetime(input)


@pytest.mark.parametrize("input", ["2500", "32jan2024", "166", "1jan2001,13066pm"])
def test_invalid_datetime_raises_invalid_value_error(input):
    with pytest.raises(parse.InvalidValueError):
        parse.datetime(input)


def test_0am_raises_invalid_format_error():
    with pytest.raises(parse.InvalidFormatError):
        parse.datetime("0am")


def test_0pm_raises_invalid_format_error():
    with pytest.raises(parse.InvalidFormatError):
        parse.datetime("0pm")
