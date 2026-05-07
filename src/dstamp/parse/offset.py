"""Provides an input parser for time offsets."""

import datetime as dt
import re

_units = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
}


def offset(raw_offset: str | None) -> dt.timedelta:
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
        return dt.timedelta()

    offset = dt.timedelta()
    subtracting = False
    matches = re.findall(r"([+-]?)(\d+)([dhms])", raw_offset)
    for sign, count_str, unit_key in matches:
        subtracting = _update_operation(sign, subtracting)
        offset += _get_suboffset(unit_key, count_str, subtracting)

    return offset


def _update_operation(sign: str, subtracting: bool) -> bool:
    if sign == "+":
        return False
    if sign == "-":
        return True
    # If no sign is provided, persist the current operation.
    return subtracting


def _get_suboffset(unit_key: str, count_str: str, subtracting: bool) -> dt.timedelta:
    unit = _units[unit_key]
    count = int(count_str)
    if subtracting:
        count *= -1
    kwargs = {unit: count}
    return dt.timedelta(**kwargs)
