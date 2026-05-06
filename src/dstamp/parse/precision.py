"""Provides an input parser for rounding precisions."""

import re

from dstamp import round

from .exceptions import InvalidFormatError, InvalidValueError


def rounding_precision(raw_precision: str) -> round.Precision:
    """Accepts precisions in the form of <value><unit>."""
    m = re.fullmatch(r"(\d*)([hms])", raw_precision.lower())

    if m is None:
        raise InvalidFormatError(f"Invalid rounding precision: {raw_precision}.")

    quantity = int(m[1]) if m[1] else 1
    if m[2] == "h":
        unit = round.Unit.HOUR
    elif m[2] == "m":
        unit = round.Unit.MINUTE
    else:
        unit = round.Unit.SECOND

    try:
        return round.Precision(quantity, unit)
    except ValueError as e:
        raise InvalidValueError(
            f"Invalid rounding precision: {raw_precision}.\n{e}"
        ) from e
