"""Provides the time rounding function."""

from datetime import datetime, timedelta

from .precision import Precision, Unit


def time_to_precision(time: datetime, precision: Precision) -> datetime:
    truncated_time = time.replace(microsecond=0)
    if precision.unit is not Unit.SECOND:
        truncated_time = truncated_time.replace(second=0)
        if precision.unit is not Unit.MINUTE:
            truncated_time = truncated_time.replace(minute=0)

    # This is currently very crude as it only checks the top-most unit.
    # This means it may not handle values close to half-way as expected.
    initial_value = getattr(time, precision.unit.attribute_name)
    rounded_value = _int_to_precision(initial_value, precision.quantity)

    # Use timedelta to handle the case where the rounded value is equal to the
    # maximum quantity, eg. if we need to round up to the next day.
    return truncated_time.replace(
        **{precision.unit.attribute_name: 0}, tzinfo=None
    ) + timedelta(**{f"{precision.unit.attribute_name}s": rounded_value})


def _int_to_precision(value: int, precision: int) -> int:
    scaled_value = float(value) / precision
    rounded_scaled_value = int(round(scaled_value))
    return rounded_scaled_value * precision
