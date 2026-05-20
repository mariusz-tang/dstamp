from datetime import date

import freezegun
import pytest

from dstamp import exceptions, parse


@pytest.mark.parametrize(
    ("input", "expected_output"),
    [
        ("20jan2025", date(2025, 1, 20)),
        ("1may2026", date(2026, 5, 1)),
        ("31dec1", date(1, 12, 31)),
    ],
)
def test_date_full(input: str, expected_output: date) -> None:
    assert parse.date(input) == expected_output


@pytest.mark.parametrize(
    ("month_name", "month_id"),
    [
        ("jan", 1),
        ("feb", 2),
        ("mar", 3),
        ("apr", 4),
        ("may", 5),
        ("jun", 6),
        ("jul", 7),
        ("aug", 8),
        ("sep", 9),
        ("oct", 10),
        ("nov", 11),
        ("dec", 12),
    ],
)
def test_date_months(month_name: str, month_id: int) -> None:
    assert parse.date(f"1{month_name}2000") == date(2000, month_id, 1)


@freezegun.freeze_time("April 15th 2022")
def test_date_no_year_implies_current_year() -> None:
    assert parse.date("10aug") == date(2022, 8, 10)


@pytest.mark.parametrize("input", ["10jan0", "32aug", "29feb2023"])
def test_date_invalid_date_raises(input: str) -> None:
    with pytest.raises(exceptions.ParserValueError) as e:
        parse.date(input)
    assert e.value.input == input
    assert e.value.output_type == date


def test_date_invalid_format_raises() -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.date("not a date")
    assert e.value.input == "not a date"


def test_date_checks_full_match() -> None:
    with pytest.raises(exceptions.ParserFormatError) as e:
        parse.date("12jan plus some extra")
    assert e.value.input == "12jan plus some extra"


def test_date_ignores_case() -> None:
    assert parse.date("10AuG") == parse.date("10aug")
