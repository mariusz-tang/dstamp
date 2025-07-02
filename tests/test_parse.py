from datetime import timedelta

import pytest

from dstamp import parse


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
