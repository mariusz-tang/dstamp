"""Tests for dstamp.format."""

from datetime import datetime

import pytest

from dstamp.format import Format, convert_to_discord_format


@pytest.mark.parametrize(
    "time,format,expected_result",
    [
        (datetime(2026, 5, 6, 23, 54, 7), Format.LONG_DATE, "<t:1778108047:D>"),
        (datetime(2025, 5, 6, 23, 54, 7), Format.LONG_DATETIME, "<t:1746572047:F>"),
        (datetime(2026, 4, 6, 23, 54, 7), Format.LONG_TIME, "<t:1775516047:T>"),
        (datetime(2026, 5, 3, 23, 54, 7), Format.RELATIVE, "<t:1777848847:R>"),
        (datetime(2026, 5, 6, 13, 54, 7), Format.SHORT_DATE, "<t:1778072047:d>"),
        (datetime(2026, 5, 6, 23, 24, 7), Format.SHORT_DATETIME, "<t:1778106247:f>"),
        (datetime(2032, 5, 6, 23, 54, 7), Format.SHORT_TIME, "<t:1967496847:t>"),
    ],
)
def test_convert_to_discord_format(time, format, expected_result):
    formatted_time = convert_to_discord_format(time, format)
    assert formatted_time == expected_result
