import pytest

from dstamp import exceptions, parse, round


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("1s", round.Precision(1, round.Unit.SECOND)),
        ("5m", round.Precision(5, round.Unit.MINUTE)),
        ("2m", round.Precision(2, round.Unit.MINUTE)),
        ("2s", round.Precision(2, round.Unit.SECOND)),
        ("24h", round.Precision(24, round.Unit.HOUR)),
        ("60m", round.Precision(60, round.Unit.MINUTE)),
        ("60s", round.Precision(60, round.Unit.SECOND)),
    ],
)
def test_precision(input: str, expected_output: round.Precision) -> None:
    assert parse.precision(input) == expected_output


@pytest.mark.parametrize(
    ("input", "quantity", "unit"),
    [
        ("61s", 61, round.Unit.SECOND),
        ("13h", 13, round.Unit.HOUR),
        ("0m", 0, round.Unit.MINUTE),
    ],
)
def test_invalid_value_raises(input: str, quantity: int, unit: round.Unit) -> None:
    with pytest.raises(exceptions.PrecisionQuantityError) as e:
        parse.precision(input)

    assert e.value.quantity == quantity
    assert e.value.unit == unit


@pytest.mark.parametrize("input", ["-1s", "not a precision", "23s and extra"])
def test_invalid_format_raises(input: str) -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.precision(input)

    assert e.value.input == input
    assert e.value.output_type == round.Precision


def test_ignores_case() -> None:
    assert parse.precision("24h") == parse.precision("24H")
