"""Provides input parsers for dates and times."""

import datetime as dt
import re

from .exceptions import InvalidFormatError, InvalidValueError


def datetime(raw_datetime: str | None) -> dt.datetime:
    """
    Parse raw_datetime into a datetime.

    raw_datetime should be of the form "ddmmmyyyy,hhmmss", albeit with some
    flexibility and special values allowed.

    If the date is omitted, use the current date.
    If the only time is omitted, use midnight.
    If both are omitted, use the current date and time.

    Valid examples:
    07jun2025,1230
    9august,330pm
    today,now
    tomorrow
    12pm
    73002pm
    noon
    midnight
    """
    if raw_datetime is None or raw_datetime == "":
        return dt.datetime.now().replace(microsecond=0)
    # Ensure there is both a date and time supplied.
    if (x := raw_datetime.count(",")) == 0:
        try:
            return datetime("today," + raw_datetime)
        except InvalidFormatError:
            return datetime(raw_datetime + ",midnight")
    elif x >= 2:
        raise InvalidFormatError

    datestr, timestr = raw_datetime.split(",")
    parsed_date = _date(datestr)
    parsed_time = _time(timestr).replace(microsecond=0)
    timezone = dt.datetime.now().tzinfo
    return dt.datetime.combine(parsed_date, parsed_time, timezone)


def _date(datestr: str) -> dt.date:
    if datestr == "today":
        return dt.date.today()

    if datestr in ("tmrw", "tomorrow"):
        return dt.date.today() + dt.timedelta(days=1)

    if datestr == "yesterday":
        return dt.date.today() - dt.timedelta(days=1)

    m = re.fullmatch(r"(\d{1,2})([a-zA-Z]{3,})(\d*)", datestr)
    if m is None:
        raise InvalidFormatError

    day = int(m[1])
    month = _get_month_from_shortening(m[2].lower())
    year = int(m[3]) if m[3] else dt.date.today().year

    try:
        return dt.date(year, month, day)
    except ValueError as e:
        raise InvalidValueError from e


def _time(timestr: str) -> dt.time:
    if timestr == "now":
        return dt.datetime.now().time()

    if timestr == "midnight":
        return dt.time()

    if timestr == "noon":
        return dt.time(12)

    m = re.fullmatch(r"(\d{1,2}?)(\d{2})?(\d{2})?([ap]m)?", timestr)
    if m is None:
        raise InvalidFormatError

    hour = int(m[1])
    minute = int(m[2]) if m[2] else 0
    second = int(m[3]) if m[3] else 0
    noonstr = m[4]

    if noonstr is not None and (hour == 0 or hour > 12):
        # Disallow noonstrings with 24h format.
        raise InvalidFormatError

    if noonstr == "pm" and hour != 12:
        hour += 12
    elif noonstr == "am" and hour == 12:
        hour = 0

    try:
        return dt.time(hour, minute, second)
    except ValueError as e:
        raise InvalidValueError from e


_months = [
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


def _get_month_from_shortening(shortening: str) -> int:
    """Returns the index of the first month which starts with the given string."""
    for ix, name in enumerate(_months):
        if name.startswith(shortening):
            return ix + 1
    raise InvalidFormatError
