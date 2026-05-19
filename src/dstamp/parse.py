"""Input-parsing utilities."""

import datetime as dt
import re

from dstamp import exceptions

MONTHS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]


def date(input: str) -> dt.date:
    """Parse `input` as a date."""
    m = re.fullmatch(rf"(\d+)({'|'.join(MONTHS)})(\d+)?", input.lower())
    if not m:
        raise exceptions.FormatError(input)

    day = int(m[1])
    month = MONTHS.index(m[2]) + 1
    year = int(m[3]) if m[3] else dt.date.today().year

    try:
        return dt.date(year, month, day)
    except ValueError as e:
        raise exceptions.InvalidDateError(input) from e


def time(input: str) -> dt.time:
    """Parse `input` as a time."""
    m = re.fullmatch(r"(\d{1,2})(\d{2})?(\d{2})?(am|pm)?", input.lower())
    if not m:
        raise exceptions.FormatError(input)

    hour = int(m[1])
    if ampm := m[4]:
        if not 1 <= hour <= 12:
            # Cannot use 24 hour time and ampm simultaneously.
            raise exceptions.FormatError(input)
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            # 12am is the 0th hour.
            hour = 0

    minute = int(m[2]) if m[2] else 0
    second = int(m[3]) if m[3] else 0

    try:
        return dt.time(hour, minute, second)
    except ValueError as e:
        raise exceptions.InvalidTimeError(input) from e
