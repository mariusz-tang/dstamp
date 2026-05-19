"""Input-parsing utilities."""

import datetime as dt
import re


class ParserInputError(ValueError):
    """Raised when a parser receives invalid input."""

    def __init__(self, input: str) -> None:
        """Initialize an error instance with a formatted error message.

        :param input: The input string which caused the parser to fail.
        """
        self.input = input
        super().__init__(f"Invalid parser input: {input}")


class FormatError(ParserInputError):
    """Raised when the input to a parser was not in the right format."""


class InvalidDateError(ParserInputError):
    """Raised when an invalid date object would be created."""


MONTHS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]


def date(input: str) -> dt.date:
    """Parse `input` as a date."""
    m = re.fullmatch(rf"(\d+)({'|'.join(MONTHS)})(\d+)?", input.lower())
    if not m:
        raise FormatError(input)

    day = int(m[1])
    month = MONTHS.index(m[2]) + 1
    year = int(m[3]) if m[3] else dt.date.today().year

    try:
        return dt.date(year, month, day)
    except ValueError as e:
        raise InvalidDateError(input) from e
