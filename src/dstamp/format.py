"""format.py

This module provides tools for formatting datetimes for dstamp output.
"""

from datetime import datetime
from enum import Enum


class Format(str, Enum):
    SHORT_TIME = "t"
    LONG_TIME = "T"
    SHORT_DATE = "d"
    LONG_DATE = "D"
    SHORT_DATETIME = "f"
    LONG_DATETIME = "F"
    RELATIVE = "R"


def convert_to_discord_format(time: datetime, format: Format) -> str:
    """Convert a datetime object into a Discord-friendly timestamp."""
    timestamp = int(time.timestamp())
    return f"<t:{timestamp}:{format.value}>"
