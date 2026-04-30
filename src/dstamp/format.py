"""format.py

This module provides tools for formatting datetimes for dstamp output.
"""

from datetime import datetime
from enum import Enum


class Format(str, Enum):
    SHORT_TIME = "short-time", "t"
    LONG_TIME = "long-time", "T"
    SHORT_DATE = "short-date", "d"
    LONG_DATE = "long-date", "D"
    SHORT_DATETIME = "short-datetime", "f"
    LONG_DATETIME = "long-datetime", "F"
    RELATIVE = "relative", "R"

    def __new__(cls, value, code):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.code = code
        return obj


def convert_to_discord_format(time: datetime, format: Format) -> str:
    """Convert a datetime object into a Discord-friendly timestamp."""
    timestamp = int(time.timestamp())
    return f"<t:{timestamp}:{format.code}>"
