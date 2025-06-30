"""parse.py

This module contains parsers for datetimes and offsets.
"""

import re
from datetime import timedelta

units = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
}


def parse_offset(raw_offset: str | None) -> timedelta:
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
