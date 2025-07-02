"""parse.py

This module contains parsers for datetimes and offsets.
"""

import re
from datetime import date, datetime, time, timedelta

units = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
}


def offset(raw_offset: str | None) -> timedelta:
    """
    Parse raw_offset into a timedelta.

    Accepts sequences of suboffsets consisting of an optional +/- sign,
    a count, and a unit. Units are dhms.

    Examples:
    3d4m
    3d-2m
    +43h
    -2m4s+4s-19m
    """
    if raw_offset is None:
        return timedelta()

    offset = timedelta()
    subtracting = False
    matches = re.findall(r"([+-]?)(\d+)([dhms])", raw_offset)
    for sign, count_str, unit_key in matches:
        subtracting = update_operation(sign, subtracting)
        offset += get_suboffset(unit_key, count_str, subtracting)

    return offset


def update_operation(sign: str, subtracting: bool) -> bool:
    if sign == "+":
        return False
    elif sign == "-":
        return True
    # If no sign is provided, persist the current operation.
    return subtracting


def get_suboffset(unit_key: str, count_str: str, subtracting: bool) -> timedelta:
    unit = units[unit_key]
    count = int(count_str)
    if subtracting:
        count *= -1
    kwargs = {unit: count}
    return timedelta(**kwargs)


class InvalidFormatError(ValueError):
    """Raised when a parser is provided an improperly-formatted value."""


def datetime_string(raw_datetime: str) -> datetime:
    """
    Parse raw_datetime into a datetime.

    raw_datetime should be of the form "ddmmmyyyy,hhmmss", albeit with some
    flexibility and special values allowed.

    If either the date or time is omitted, attempt to use the current day
    or time.

    Valid examples:
    07jun2025,1230
    9august,330pm
    today,now
    tomorrow
    12pm
    73002pm
    """
    if raw_datetime == "":
        return datetime.now()
    # Ensure there is both a date and time supplied.
    if (x := raw_datetime.count(",")) == 0:
        try:
            return datetime_string("today," + raw_datetime)
        except InvalidFormatError:
            return datetime_string(raw_datetime + ",now")
    elif x > 2:
        raise InvalidFormatError

    datestr, timestr = raw_datetime.split(",")
    parsed_date = parse_date(datestr)
    parsed_time = parse_time(timestr)
    timezone = datetime.now().tzinfo
    return datetime.combine(parsed_date, parsed_time, timezone)


def parse_date(datestr: str) -> date:
    if datestr == "today":
        return date.today()

    if datestr in ("tmrw", "tomorrow"):
        return date.today() + timedelta(days=1)

    if datestr == "yesterday":
        return date.today() - timedelta(days=1)

    m = re.fullmatch(r"(\d{1,2})([a-zA-Z]{3,})(\d*)", datestr)
    if m is None:
        raise InvalidFormatError

    day = int(m[1])
    month = get_month_from_shortening(m[2].lower())
    year = int(m[3]) if m[3] else date.today().year

    try:
        return date(year, month, day)
    except ValueError as e:
        raise InvalidFormatError from e


def parse_time(timestr: str) -> time:
    if timestr == "now":
        return datetime.now().time()

    m = re.fullmatch(r"(\d{1,2}?)(\d{2})?(\d{2})?([ap]m)?", timestr)
    if m is None:
        raise InvalidFormatError

    hour = int(m[1])
    minute = int(m[2]) if m[2] else 0
    second = int(m[3]) if m[3] else 0
    noonstr = m[4]

    if noonstr is not None and hour > 12:
        # Disallow noonstrings with 24h format.
        raise InvalidFormatError

    if noonstr == "pm":
        hour += 12

    try:
        return time(hour, minute, second)
    except ValueError as e:
        raise InvalidFormatError from e


months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]


def get_month_from_shortening(shortening: str) -> int:
    """Returns the index of the first month which starts with the given string."""
    for ix, name in enumerate(months):
        if name.startswith(shortening):
            return ix + 1
    raise InvalidFormatError
