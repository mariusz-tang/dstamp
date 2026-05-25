import datetime as dt

import pytest

from dstamp import exceptions, round


@pytest.mark.parametrize(
    ("quantity", "unit"),
    [
        (1, round.Unit.HOUR),
        (1, round.Unit.MINUTE),
        (1, round.Unit.SECOND),
        (12, round.Unit.HOUR),
        (30, round.Unit.MINUTE),
        (30, round.Unit.SECOND),
        (24, round.Unit.HOUR),
        (60, round.Unit.MINUTE),
        (60, round.Unit.SECOND),
    ],
)
def test_precision_constructor(quantity: int, unit: round.Unit) -> None:
    precision = round.Precision(quantity, unit)
    assert precision.quantity == quantity
    assert precision.unit == unit


@pytest.mark.parametrize(
    ("quantity", "unit"),
    [
        (-1, round.Unit.HOUR),
        (0, round.Unit.MINUTE),
        (-2, round.Unit.SECOND),
    ],
)
def test_precision_constructor_non_positive_quantity_raises(
    quantity: int, unit: round.Unit
) -> None:
    with pytest.raises(exceptions.PrecisionQuantityError) as e:
        round.Precision(quantity, unit)

    assert e.value.quantity == quantity
    assert e.value.unit == unit


@pytest.mark.parametrize(
    ("quantity", "unit"),
    [
        (25, round.Unit.HOUR),
        (61, round.Unit.MINUTE),
        (61, round.Unit.SECOND),
    ],
)
def test_precision_constructor_quantity_more_than_max_raises(
    quantity: int, unit: round.Unit
) -> None:
    with pytest.raises(exceptions.PrecisionQuantityError) as e:
        round.Precision(quantity, unit)

    assert e.value.quantity == quantity
    assert e.value.unit == unit


@pytest.mark.parametrize(
    ("quantity", "unit"),
    [
        (13, round.Unit.HOUR),
        (31, round.Unit.MINUTE),
        (7, round.Unit.SECOND),
    ],
)
def test_precision_constructor_quantity_not_a_factor_of_max_raises(
    quantity: int, unit: round.Unit
) -> None:
    with pytest.raises(exceptions.PrecisionQuantityError) as e:
        round.Precision(quantity, unit)

    assert e.value.quantity == quantity
    assert e.value.unit == unit


@pytest.mark.parametrize(
    ("datetime", "precision", "expected_result"),
    [
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(1, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 52),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 741000),
            round.Precision(1, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 53),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(1, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 12, 49),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 22, 241),
            round.Precision(1, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 12, 48),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(1, round.Unit.HOUR),
            dt.datetime(2026, 5, 26, 13),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 28, 52, 241),
            round.Precision(1, round.Unit.HOUR),
            dt.datetime(2026, 5, 26, 12),
        ),
    ],
)
def test_datetime_to_nearest_unit(
    datetime: dt.datetime, precision: round.Precision, expected_result: dt.datetime
) -> None:
    assert round.datetime(datetime, precision) == expected_result


@pytest.mark.parametrize(
    ("datetime", "precision", "expected_result"),
    [
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(4, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 52),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 741000),
            round.Precision(6, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 54),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(2, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 12, 48),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 22, 241),
            round.Precision(15, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 12, 45),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(12, round.Unit.HOUR),
            dt.datetime(2026, 5, 26, 12),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 28, 52, 241),
            round.Precision(2, round.Unit.HOUR),
            dt.datetime(2026, 5, 26, 12),
        ),
    ],
)
def test_datetime_to_nearest_multiples_of_unit(
    datetime: dt.datetime, precision: round.Precision, expected_result: dt.datetime
) -> None:
    assert round.datetime(datetime, precision) == expected_result


@pytest.mark.parametrize(
    ("datetime", "precision", "expected_result"),
    [
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(60, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 49),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(60, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 13),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 241),
            round.Precision(24, round.Unit.HOUR),
            dt.datetime(2026, 5, 27),
        ),
    ],
)
def test_datetime_to_nearest_max_unit(
    datetime: dt.datetime, precision: round.Precision, expected_result: dt.datetime
) -> None:
    assert round.datetime(datetime, precision) == expected_result


@pytest.mark.parametrize(
    ("datetime", "precision", "expected_result"),
    [
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 499999),
            round.Precision(1, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 52),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 52, 500000),
            round.Precision(1, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 53),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 50, 999999),
            round.Precision(6, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 48),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 48, 51),
            round.Precision(6, round.Unit.SECOND),
            dt.datetime(2026, 5, 26, 12, 48, 54),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 52, 29, 999999),
            round.Precision(15, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 12, 45),
        ),
        (
            dt.datetime(2026, 5, 26, 12, 52, 30),
            round.Precision(15, round.Unit.MINUTE),
            dt.datetime(2026, 5, 26, 13),
        ),
        (
            dt.datetime(2026, 5, 26, 11, 59, 59, 999999),
            round.Precision(24, round.Unit.HOUR),
            dt.datetime(2026, 5, 26),
        ),
        (
            dt.datetime(2026, 5, 26, 12),
            round.Precision(24, round.Unit.HOUR),
            dt.datetime(2026, 5, 27),
        ),
    ],
)
def test_datetime_boundary(
    datetime: dt.datetime, precision: round.Precision, expected_result: dt.datetime
) -> None:
    assert round.datetime(datetime, precision) == expected_result
