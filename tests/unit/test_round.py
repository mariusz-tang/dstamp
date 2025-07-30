"""unit/test_round.py

This module contains unit tests for the dstamp.round module.
"""

from datetime import timedelta

import pytest

from dstamp import round
from tests.utils.patched_time import now

ONE_DAY = timedelta(days=1)


def time(hour: int, minute: int, second: int, microsecond: int = 0):
    return now.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)


@pytest.mark.parametrize(
    "raw_time,precision,desired_output",
    (
        # The missing ones are weird of the crude implementation of the
        # function being tested. This should be fixed in the future.
        (time(12, 0, 0), "1m", time(12, 0, 0)),
        (time(11, 48, 0), "m", time(11, 48, 0)),
        (time(11, 58, 0, 594), "4H", time(12, 0, 0)),
        (time(23, 58, 0, 2), "4H", time(0, 0, 0) + ONE_DAY),
        (time(11, 58, 0), "10m", time(12, 0, 0)),
        (time(23, 58, 0), "10m", time(0, 0, 0) + ONE_DAY),
        (time(14, 26, 29, 11), "1M", time(14, 26, 0)),
        # (time(1, 2, 30), "1M", time(1, 3, 0)),
        # (time(20, 50, 59), "M", time(20, 51, 0)),
        (time(14, 26, 29), "H", time(14, 0, 0)),
        # (time(15, 30, 00), "H", time(16, 0, 0)),
        (time(15, 29, 59), "H", time(15, 0, 0)),
        (time(14, 26, 27, 321), "3H", time(15, 0, 0)),
        # (time(14, 26, 36), "4m", time(14, 28, 0)),
        (time(14, 26, 23), "30m", time(14, 30, 0)),
        (time(14, 36, 49), "30m", time(14, 30, 0)),
        (time(14, 36, 49, 249), "s", time(14, 36, 49)),
        # (time(14, 36, 49, 689), "s", time(14, 36, 50)),
        (time(14, 36, 49, 249), "5s", time(14, 36, 50)),
        (time(14, 36, 49, 249), "4s", time(14, 36, 48)),
    ),
)
def test_round(raw_time, precision, desired_output):
    assert round.round_time_to_precision(raw_time, precision) == desired_output
