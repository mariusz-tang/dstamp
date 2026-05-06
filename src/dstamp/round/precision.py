"""Provides the rounding precision class."""

from enum import Enum


class Unit(Enum):
    HOUR = "hour", "h", 24
    MINUTE = "minute", "m", 60
    SECOND = "second", "s", 60

    def __init__(self, attribute_name: str, code: str, max_quantity: int) -> None:
        self.attribute_name = attribute_name
        self.code = code
        self.max_quantity = max_quantity


class Precision:
    """Represents a rounding precision.

    For example, (to the nearest) 10 minutes.
    """

    def __init__(self, quantity: int, unit: Unit) -> None:
        if quantity <= 0:
            raise ValueError("Precision quantity must be positive.")
        if quantity >= unit.max_quantity:
            raise ValueError(
                f"Precision quantity for {unit.name} "
                f"must be less than {unit.max_quantity}."
            )
        if unit.max_quantity % quantity != 0:
            raise ValueError(
                f"Precision quantity for {unit.name} "
                f"must be a factor of {unit.max_quantity}."
            )

        self.quantity = quantity
        self.unit = unit
