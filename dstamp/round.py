"""round.py

This module contains logic for rounding timestamps to nicer ones.
"""

from datetime import datetime, timedelta
from enum import Enum

from . import parse


class BaseRoundingError(ValueError):
    """Base class for errors raised due to invalid rounding attempts."""


class RoundingUnit(Enum):
    HOUR = "hour", "h", 24
    MINUTE = "minute", "m", 60

    def __init__(self, attribute_name, code, max_quantity):
        self.attribute_name = attribute_name
        self.code = code
        self.max_quantity = max_quantity


def round_time_to_precision(time: datetime, precision: str):
    quantity, unit = parse.rounding_precision(precision)

    truncated_time = time.replace(second=0, microsecond=0)
    if unit is RoundingUnit.HOUR:
        truncated_time = truncated_time.replace(minute=0)

    # This is currently very crude as it only checks the top-most unit.
    # This means it may not handle values close to half-way as expected.
    initial_value = getattr(time, unit.attribute_name)
    rounded_value = round_int_to_precision(initial_value, quantity)

    # Use timedelta to handle the case where the rounded value is equal to the
    # maximum quantity, eg. if we need to round up to the next day.
    return truncated_time.replace(**{unit.attribute_name: 0}) + timedelta(
        **{f"{unit.attribute_name}s": rounded_value}
    )


def round_int_to_precision(value: int, precision: int) -> int:
    scaled_value = float(value) / precision
    rounded_scaled_value = int(round(scaled_value))
    rounded_value = rounded_scaled_value * precision
    return rounded_value
