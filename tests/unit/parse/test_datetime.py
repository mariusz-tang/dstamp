"""Tests for the datetime parser."""

from datetime import date, datetime, time, timedelta

import pytest
from freezegun import freeze_time

from dstamp import parse

NOW = datetime(2025, 1, 2, 12, 53, 42)
TODAY = NOW.date()


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
