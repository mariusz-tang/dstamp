"""Contains utilities for rounding datetime objects."""

import datetime as dt
from enum import Enum

from dstamp import exceptions


class Unit(Enum):
    """Represents a rounding unit."""

    HOUR = "hour", "h", 24
    MINUTE = "minute", "m", 60
    SECOND = "second", "s", 60

    def __init__(self, attribute_nanme: str, code: str, max_quantity: int) -> None:
        """Initialize a Unit instance."""
        self.attribute_name = attribute_nanme
        self.code = code
        self.max_quantity = max_quantity


class Precision:
    """Represents a rounding precision."""

    def __init__(self, quantity: int, unit: Unit) -> None:
        """Intialize a Precision instance.

        `quantity` should be a factor of `unit.max_quantity` between 1 and
        unit.max_quantity (inclusive).
        """
        if (
            quantity <= 0
            or quantity > unit.max_quantity
            or unit.max_quantity % quantity != 0
        ):
            raise exceptions.PrecisionQuantityError(quantity, unit)

        self.quantity = quantity
        self.unit = unit

    def __eq__(self, other: object) -> bool:
        """Compare equality of this Precision object with `other`."""
        if type(other) is Precision:
            return self.quantity == other.quantity and self.unit == other.unit

        return NotImplemented


def datetime(datetime: dt.datetime, precision: Precision) -> dt.datetime:
    """Round `datetime` to `precision`."""
    datetime_rounded_down = _round_down(datetime, precision)

    # Find the difference between the original and the rounded-down time,
    # and between the rounded-up time and rounded-down time.
    difference_original_down = datetime - datetime_rounded_down
    attr_name = precision.unit.attribute_name + "s"
    difference_up_down = dt.timedelta(**{attr_name: precision.quantity})

    # Round down if the original was less than halfway to the rounded-up time.
    if difference_original_down < difference_up_down / 2:
        return datetime_rounded_down

    # Otherwise, round up.
    return datetime_rounded_down + difference_up_down


def _round_down(datetime: dt.datetime, precision: Precision) -> dt.datetime:
    # Truncate smaller units.
    datetime_trunacted = _truncate(datetime, precision.unit)

    # Round the `precision.unit` unit down.
    attr_name = precision.unit.attribute_name
    value_original = getattr(datetime, attr_name)
    value_rounded_down = value_original - value_original % precision.quantity

    return datetime_trunacted.replace(**{attr_name: value_rounded_down})


def _truncate(datetime: dt.datetime, unit: Unit) -> dt.datetime:
    """Truncate `datetime` so that `unit` is the smallest non-zero unit."""
    datetime_trunacted = datetime.replace(microsecond=0)
    if unit != Unit.SECOND:
        datetime_trunacted = datetime_trunacted.replace(second=0)
        if unit != Unit.MINUTE:
            datetime_trunacted = datetime_trunacted.replace(minute=0)

    return datetime_trunacted
