"""Tests for dstamp.parse."""

from datetime import date, datetime, time, timedelta

import pytest
from freezegun import freeze_time

from dstamp import parse, round

NOW = datetime(2025, 1, 2, 12, 53, 42)
TODAY = NOW.date()


@pytest.mark.parametrize(
    "raw_input,desired_output",
    [
        (None, timedelta()),
        ("4d+3h10m", timedelta(days=4, hours=3, minutes=10)),
        ("4d-3h10m+3s", timedelta(days=4, hours=-3, minutes=-10, seconds=3)),
        ("4d-3h+10m", timedelta(days=4, hours=-3, minutes=10)),
        ("-300d", timedelta(days=-300)),
    ],
)
def test_offset(raw_input, desired_output):
    assert parse.offset(raw_input) == desired_output


@pytest.mark.parametrize(
    "raw_input,desired_output",
    [
        ("12june2024", datetime(2024, 6, 12)),
        ("24aug2000,midnight", datetime(2000, 8, 24)),
        ("", NOW),
        ("today,now", NOW),
        ("now", NOW),
        ("tmrw,7pm", datetime.combine(TODAY + timedelta(days=1), time(19))),
        ("yesterday,noon", datetime.combine(TODAY - timedelta(days=1), time(12))),
        ("830pm", datetime.combine(TODAY, time(20, 30))),
        ("200943", datetime.combine(TODAY, time(20, 9, 43))),
        ("4jan,1am", datetime.combine(date(TODAY.year, 1, 4), time(1))),
        ("12pm", datetime.combine(TODAY, time(12))),
        ("12am", datetime.combine(TODAY, time(0))),
    ],
)
@freeze_time(NOW)
def test_datetime(raw_input, desired_output):
    assert parse.datetime(raw_input) == desired_output


@pytest.mark.parametrize(
    "input", ["today,now,now", "in two days", "2203pm", "24notamonth2032", "0am", "0pm"]
)
def test_datetime_invalid_format(input):
    with pytest.raises(parse.InvalidFormatError):
        parse.datetime(input)


@pytest.mark.parametrize("input", ["2500", "32jan2024", "166", "1jan2001,13066pm"])
def test_datetime_invalid_datetime(input):
    with pytest.raises(parse.InvalidValueError):
        parse.datetime(input)


@pytest.mark.parametrize(
    "raw_input,quantity,unit",
    [
        ("20m", 20, round.Unit.MINUTE),
        ("1H", 1, round.Unit.HOUR),
        ("M", 1, round.Unit.MINUTE),
        ("15m", 15, round.Unit.MINUTE),
        ("12s", 12, round.Unit.SECOND),
        ("3S", 3, round.Unit.SECOND),
    ],
)
@freeze_time(NOW)
def test_rounding_precision(raw_input, quantity, unit):
    precision = parse.rounding_precision(raw_input)
    assert precision.quantity == quantity
    assert precision.unit == unit


@pytest.mark.parametrize(
    "input", ["60m", "120H", "0m", "24h", "0H", "0s", "13S", "78s"]
)
def test_rounding_precision_invalid_quantity(input):
    with pytest.raises(parse.InvalidValueError):
        parse.rounding_precision(input)


@pytest.mark.parametrize("input", ["60", "30g", "1D", "b", "-4m", "21901123103gea"])
def test_rounding_precision_wrong_format(input):
    with pytest.raises(parse.InvalidFormatError):
        parse.rounding_precision(input)
