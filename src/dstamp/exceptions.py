"""Exception classes for errors raised by dstamp."""


class DstampError(Exception):
    """Base class for all exceptions raised by dstamp."""


class ParserInputError(DstampError):
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


class InvalidTimeError(ParserInputError):
    """Raised when an invalid time object would be created."""
