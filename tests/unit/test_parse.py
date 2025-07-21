"""unit/test_parse.py

This module contains unit tests for the dstamp.parse module.
"""

from datetime import date, datetime, time, timedelta

import pytest
from freezegun import freeze_time

from dstamp import parse
from dstamp.round import RoundingUnit
from tests.utils.patched_time import now, today


@pytest.mark.parametrize(
    "raw_input,desired_output",
    (
        (None, timedelta()),
        ("4d+3h10m", timedelta(days=4, hours=3, minutes=10)),
        ("4d-3h10m+3s", timedelta(days=4, hours=-3, minutes=-10, seconds=3)),
        ("4d-3h+10m", timedelta(days=4, hours=-3, minutes=10)),
        ("-300d", timedelta(days=-300)),
    ),
)
def test_offset(raw_input, desired_output):
    assert parse.offset(raw_input) == desired_output


@pytest.mark.parametrize(
    "raw_input,desired_output",
    (
        ("12june2024", datetime(2024, 6, 12)),
        ("24aug2000,midnight", datetime(2000, 8, 24)),
        ("", now),
        ("today,now", now),
        ("now", now),
        ("tmrw,7pm", datetime.combine(today + timedelta(days=1), time(19))),
        ("yesterday,noon", datetime.combine(today - timedelta(days=1), time(12))),
        ("830pm", datetime.combine(today, time(20, 30))),
        ("200943", datetime.combine(today, time(20, 9, 43))),
        ("4jan,1am", datetime.combine(date(today.year, 1, 4), time(1))),
    ),
)
@freeze_time(now)
def test_datetime(raw_input, desired_output, monkeypatch):
    assert parse.datetime_string(raw_input) == desired_output


@pytest.mark.parametrize(
    "input", ("today,now,now", "in two days", "2203pm", "24notamonth2032")
)
def test_datetime_invalid_format(input):
    with pytest.raises(parse.InvalidFormatError):
        parse.datetime_string(input)


@pytest.mark.parametrize("input", ("2500", "32jan2024", "166", "1jan2001,13066pm"))
def test_datetime_invalid_datetime(input):
    with pytest.raises(parse.InvalidValueError):
        parse.datetime_string(input)


@pytest.mark.parametrize(
    "raw_input,desired_output",
    (
        ("20m", (20, RoundingUnit.MINUTE)),
        ("1H", (1, RoundingUnit.HOUR)),
        ("M", (1, RoundingUnit.MINUTE)),
        ("15m", (15, RoundingUnit.MINUTE)),
        ("12s", (12, RoundingUnit.SECOND)),
        ("3S", (3, RoundingUnit.SECOND)),
    ),
)
@freeze_time(now)
def test_rounding_precision(raw_input, desired_output, monkeypatch):
    assert parse.rounding_precision(raw_input) == desired_output


@pytest.mark.parametrize(
    "input", ("60m", "120H", "0m", "24h", "0H", "0s", "13S", "78s")
)
def test_rounding_precision_invalid_quantity(input):
    with pytest.raises(parse.InvalidValueError):
        parse.rounding_precision(input)


@pytest.mark.parametrize("input", ("60", "30g", "1D", "b", "-4m", "21901123103gea"))
def test_rounding_precision_wrong_format(input):
    with pytest.raises(parse.InvalidFormatError):
        parse.rounding_precision(input)
