"""Exception classes for errors raised by dstamp."""

from dstamp import round


class DstampError(Exception):
    """Base class for all exceptions raised by dstamp."""


class ParserInputError(DstampError):
    """Base class for parser input errors."""

    def __init__(self, input: str, output_type: type) -> None:
        """Initialize an error instance with a formatted error message.

        :param input: The input string which caused the parser to fail.
        :param output_type: The expected output type.
        """
        self.input = input
        self.output_type = output_type
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        raise NotImplementedError  # pragma: no cover


class ParserFormatError(ParserInputError):
    """Raised when the input to a parser was not in the right format."""

    def _format_message(self) -> str:
        return f"invalid {self.output_type.__name__.lower()} format: {repr(self.input)}"


class ParserValueError(ParserInputError):
    """Raised when an invalid time object would be created."""

    def _format_message(self) -> str:
        return (
            f"input represents an invalid {self.output_type.__name__.lower()}: "
            f"{repr(self.input)}"
        )


class PrecisionQuantityError(DstampError):
    """Raised when the `Precision` constructor receives an invalid quantity."""

    def __init__(self, quantity: int, unit: round.Unit) -> None:
        """Initialize an error instance with a formatted error message.

        :param quantity: The quantity passed to the `Precision` constructor.
        :param unit: The unit object passed to the `Precision` constructor.
        """
        self.quantity = quantity
        self.unit = unit
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        return (
            f"quantity for {self.unit.name.lower()} must be between 1 and "
            f"{self.unit.max_quantity} (inclusive), and must be a factor of "
            f"{self.unit.max_quantity} (actual quantity was {self.quantity})."
        )
