from datetime import datetime

import pytest

from dstamp import discord


@pytest.mark.parametrize(
    ("timestamp", "format_code"), [(1778885670, "f"), (0, "R"), (-1, "t")]
)
def test_timestamp(timestamp: int, format_code: str) -> None:
    date = datetime.fromtimestamp(timestamp)

    discord_timestamp = discord.timestamp(date, format_code)

    assert discord_timestamp == f"<t:{timestamp}:{format_code}>"


def test_timestamp_truncates_fractional_timestamp() -> None:
    date = datetime.fromtimestamp(0.9)

    discord_timestamp = discord.timestamp(date, "")

    assert discord_timestamp == "<t:0:>"
