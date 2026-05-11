"""Tests for dstamp.format."""

from datetime import UTC, datetime

import pytest

from dstamp.format import Format, discord


@pytest.mark.parametrize(
    "timestamp,format,expected_result",
    [
        (0, Format.LONG_DATE, "<t:0:D>"),
        (1725062400, Format.LONG_DATETIME, "<t:1725062400:F>"),
        (93032, Format.LONG_TIME, "<t:93032:T>"),
        (2923, Format.RELATIVE, "<t:2923:R>"),
        (392, Format.SHORT_DATE, "<t:392:d>"),
        (-500, Format.SHORT_DATETIME, "<t:-500:f>"),
        (39042343, Format.SHORT_TIME, "<t:39042343:t>"),
    ],
)
def test_convert_to_discord_format(timestamp, format, expected_result):
    time = datetime.fromtimestamp(timestamp, tz=UTC)
    formatted_time = discord(time, format)
    assert formatted_time == expected_result
