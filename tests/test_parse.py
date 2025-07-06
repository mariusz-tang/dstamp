from datetime import date, datetime, time, timedelta

import pytest
from freezegun import freeze_time

from dstamp import parse
from tests.patched_time import now, today


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
