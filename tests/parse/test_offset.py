from datetime import timedelta

import pytest

from dstamp import exceptions, parse


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("1d", timedelta(days=1)),
        ("4h", timedelta(hours=4)),
        ("20m", timedelta(minutes=20)),
        ("2s", timedelta(seconds=2)),
    ],
)
def test_single_offset_unit(input: str, expected_output: timedelta) -> None:
    output = parse.offset(input)
    assert output == expected_output


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("1d5m", timedelta(days=1, minutes=5)),
        ("4h2s", timedelta(hours=4, seconds=2)),
        ("20m3d", timedelta(days=3, minutes=20)),
        ("2s5m", timedelta(minutes=5, seconds=2)),
    ],
)
def test_multiple_offset_units(input: str, expected_output: timedelta) -> None:
    output = parse.offset(input)
    assert output == expected_output


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("1d5m3m", timedelta(days=1, minutes=8)),
        ("4h2s2h", timedelta(hours=6, seconds=2)),
    ],
)
def test_repeated_offset_units(input: str, expected_output: timedelta) -> None:
    output = parse.offset(input)
    assert output == expected_output


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("b1d5m", -timedelta(days=1, minutes=5)),
        ("b4h2s", -timedelta(hours=4, seconds=2)),
        ("b20m3d", -timedelta(days=3, minutes=20)),
        ("b2s5m", -timedelta(minutes=5, seconds=2)),
    ],
)
def test_backwards_offset(input: str, expected_output: timedelta) -> None:
    output = parse.offset(input)
    assert output == expected_output


def test_ignores_case() -> None:
    assert parse.offset("B1d5M") == parse.offset("b1d5m")


def test_checks_full_match() -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.offset("b1d5m and Extra")

    assert e.value.input == "b1d5m and Extra"
    assert e.value.output_type == timedelta


def test_invalid_format_raises() -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.offset("invalid format")

    assert e.value.input == "invalid format"
    assert e.value.output_type == timedelta
