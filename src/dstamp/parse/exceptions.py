"""Parsing-related exceptions."""


class ParserInputError(ValueError):
    """Raised when there is a problem with the input received by a parser."""


class InvalidFormatError(ParserInputError):
    """Raised when a parser is provided an improperly-formatted value."""


class InvalidValueError(ParserInputError):
    """Raised when a parser is provided a correctly-formatted but invalid value."""
