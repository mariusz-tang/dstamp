"""Datetime formatting utilities."""

from datetime import datetime
from enum import StrEnum


class Format(StrEnum):
    SHORT_TIME = "t"
    LONG_TIME = "T"
    SHORT_DATE = "d"
    LONG_DATE = "D"
    SHORT_DATETIME = "f"
    LONG_DATETIME = "F"
    RELATIVE = "R"


def human_readable(time: datetime) -> str:
    return time.strftime("%I:%M:%S on %B %d, %Y")


def discord(time: datetime, format: Format) -> str:
    """Convert a datetime object into a Discord-friendly timestamp."""
    timestamp = int(time.timestamp())
    return f"<t:{timestamp}:{format.value}>"
