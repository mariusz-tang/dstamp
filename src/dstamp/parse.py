"""Input-parsing utilities."""

import datetime as dt
import re
from collections import Counter

from dstamp import exceptions, round

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
    if input == "today":
        return dt.date.today()
    if input in ["tomorrow", "tmrw"]:
        return dt.date.today() + dt.timedelta(1)
    if input == "yesterday":
        return dt.date.today() - dt.timedelta(1)

    m = re.fullmatch(rf"(\d+)({'|'.join(MONTHS)})(\d+)?", input.lower())
    if not m:
        raise exceptions.ParserFormatError(input, dt.date)

    day = int(m[1])
    month = MONTHS.index(m[2]) + 1
    year = int(m[3]) if m[3] else dt.date.today().year

    try:
        return dt.date(year, month, day)
    except ValueError as e:
        raise exceptions.ParserValueError(input, dt.date) from e


def time(input: str) -> dt.time:
    """Parse `input` as a time."""
    if input == "now":
        return dt.datetime.now().time()
    if input == "midnight":
        return dt.time()
    if input == "noon":
        return dt.time(12)

    m = re.fullmatch(r"(\d{1,2})(\d{2})?(\d{2})?(am|pm)?", input.lower())
    if not m:
        raise exceptions.ParserFormatError(input, dt.time)

    hour = int(m[1])
    if ampm := m[4]:
        if not 1 <= hour <= 12:
            # Cannot use 24 hour time and ampm simultaneously.
            raise exceptions.ParserFormatError(input, dt.time)
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
        raise exceptions.ParserValueError(input, dt.time) from e


_OFFSET_UNITS = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
}


def offset(input: str) -> dt.timedelta:
    """Parse `input` as a time offset, represented by a `timedelta` object."""
    unit_pattern = rf"(\d+)([{''.join(_OFFSET_UNITS.keys())}])"

    if not re.fullmatch(rf"b?({unit_pattern})+", input.lower()):
        raise exceptions.ParserFormatError(input, dt.timedelta)

    kwargs = Counter()
    for quantity, unit_code in re.findall(unit_pattern, input.lower()):
        unit = _OFFSET_UNITS[unit_code]
        kwargs[unit] += int(quantity)

    result = dt.timedelta(**kwargs)

    if input.lower().startswith("b"):
        # Return the backwards offset.
        result *= -1

    return result


_ROUNDING_UNITS = {
    "h": round.Unit.HOUR,
    "m": round.Unit.MINUTE,
    "s": round.Unit.SECOND,
}


def precision(input: str) -> round.Precision:
    """Parse `input` as a rounding precision.

    Raises `PrecisionQuantityError` instead of `ParserValueError` if the
    precision quantity is invalid.
    """
    m = re.fullmatch(rf"(\d+)([{''.join(_ROUNDING_UNITS.keys())}])", input.lower())
    if not m:
        raise exceptions.ParserFormatError(input, round.Precision)

    quantity = int(m[1])
    unit = _ROUNDING_UNITS[m[2]]
    return round.Precision(quantity, unit)
