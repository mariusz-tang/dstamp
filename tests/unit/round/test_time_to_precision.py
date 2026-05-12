"""Tests for the time_to_precision rounding function"""

from datetime import datetime, timedelta

import pytest

from dstamp.round import Precision, Unit, time_to_precision

NOW = datetime(2025, 1, 2, 12, 53, 42, 231)
ONE_DAY = timedelta(days=1)


def time(hour: int, minute: int, second: int, microsecond: int = 0) -> datetime:
    return NOW.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)


@pytest.mark.parametrize(
    "raw_time,precision,desired_output",
    [
        # The missing ones are weird of the crude implementation of the
        # function being tested. This should be fixed in the future.
        (time(12, 0, 0), Precision(1, Unit.SECOND), time(12, 0, 0)),
        (time(11, 48, 0), Precision(1, Unit.MINUTE), time(11, 48, 0)),
        (time(11, 58, 0, 594), Precision(4, Unit.HOUR), time(12, 0, 0)),
        (time(23, 58, 0, 2), Precision(4, Unit.HOUR), time(0, 0, 0) + ONE_DAY),
        (time(11, 58, 0), Precision(10, Unit.MINUTE), time(12, 0, 0)),
        (time(23, 58, 0), Precision(10, Unit.MINUTE), time(0, 0, 0) + ONE_DAY),
        (time(14, 26, 29, 11), Precision(1, Unit.MINUTE), time(14, 26, 0)),
        # (time(1, 2, 30), Precision(1, Unit.MINUTE), time(1, 3, 0)),
        # (time(20, 50, 59), Precision(1, Unit.MINUTE), time(20, 51, 0)),
        (time(14, 26, 29), Precision(1, Unit.HOUR), time(14, 0, 0)),
        # (time(15, 30, 00), Precision(1, Unit.HOUR), time(16, 0, 0)),
        (time(15, 29, 59), Precision(1, Unit.HOUR), time(15, 0, 0)),
        (time(14, 26, 27, 321), Precision(3, Unit.HOUR), time(15, 0, 0)),
        # (time(14, 26, 36), Precision(4, Unit.MINUTE), time(14, 28, 0)),
        (time(14, 26, 23), Precision(30, Unit.MINUTE), time(14, 30, 0)),
        (time(14, 36, 49), Precision(30, Unit.MINUTE), time(14, 30, 0)),
        (time(14, 36, 49, 249), Precision(1, Unit.SECOND), time(14, 36, 49)),
        # (time(14, 36, 49, 689), Precision(1, Unit.SECOND), time(14, 36, 50)),
        (time(14, 36, 49, 249), Precision(5, Unit.SECOND), time(14, 36, 50)),
        (time(14, 36, 49, 249), Precision(4, Unit.SECOND), time(14, 36, 48)),
    ],
)
def test_round(
    raw_time: datetime, precision: Precision, desired_output: datetime
) -> None:
    assert time_to_precision(raw_time, precision) == desired_output
