"""Tests for the rounding precision parser."""

from datetime import datetime

import pytest
from freezegun import freeze_time

from dstamp import parse, round

NOW = datetime(2025, 1, 2, 12, 53, 42, 123)


@pytest.mark.parametrize(
    "raw_input,quantity,unit",
    [
        ("20m", 20, round.Unit.MINUTE),
        ("1H", 1, round.Unit.HOUR),
        ("M", 1, round.Unit.MINUTE),
        ("15m", 15, round.Unit.MINUTE),
        ("12s", 12, round.Unit.SECOND),
        ("3S", 3, round.Unit.SECOND),
    ],
)
@freeze_time(NOW)
def test_rounding_precision(raw_input: str, quantity: int, unit: round.Unit) -> None:
    precision = parse.rounding_precision(raw_input)
    assert precision.quantity == quantity
    assert precision.unit == unit


@pytest.mark.parametrize(
    "input", ["60m", "120H", "0m", "24h", "0H", "0s", "13S", "78s"]
)
def test_rounding_precision_invalid_quantity(input: str) -> None:
    with pytest.raises(parse.InvalidValueError):
        parse.rounding_precision(input)


@pytest.mark.parametrize("input", ["60", "30g", "1D", "b", "-4m", "21901123103gea"])
def test_rounding_precision_wrong_format(input: str) -> None:
    with pytest.raises(parse.InvalidFormatError):
        parse.rounding_precision(input)
