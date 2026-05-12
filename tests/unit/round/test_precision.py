"""Tests for the rounding Precision class."""

import pytest

from dstamp.round import Precision, Unit


@pytest.mark.parametrize(
    "quantity,unit",
    [
        (15, Unit.MINUTE),
        (2, Unit.HOUR),
        (1, Unit.SECOND),
        (30, Unit.MINUTE),
        (12, Unit.HOUR),
        (30, Unit.SECOND),
    ],
)
def test_valid_input(quantity: int, unit: Unit) -> None:
    Precision(quantity, unit)


def test_negative_quantity_raises() -> None:
    with pytest.raises(ValueError, match="Precision quantity must be positive."):
        Precision(-1, Unit.HOUR)


@pytest.mark.parametrize(
    "quantity,unit",
    [
        (60, Unit.MINUTE),
        (24, Unit.HOUR),
        (60, Unit.SECOND),
    ],
)
def test_quantity_too_large_raises(quantity: int, unit: Unit) -> None:
    with pytest.raises(
        ValueError,
        match=f"Precision quantity for {unit.name} "
        f"must be less than {unit.max_quantity}.",
    ):
        Precision(quantity, unit)


@pytest.mark.parametrize(
    "quantity,unit",
    [
        (29, Unit.MINUTE),
        (11, Unit.HOUR),
        (29, Unit.SECOND),
    ],
)
def test_quantity_not_a_factor_of_max_raises(quantity: int, unit: Unit) -> None:
    with pytest.raises(
        ValueError,
        match=f"Precision quantity for {unit.name} "
        f"must be a factor of {unit.max_quantity}.",
    ):
        Precision(quantity, unit)
