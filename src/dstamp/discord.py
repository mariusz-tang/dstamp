"""Discord-related formatting utilities."""

from datetime import datetime


def timestamp(time: datetime, format_code: str) -> str:
    """Return a Discord timestamp representing `time`.

    :param time: The time to respresent. If it has a fractional timestamp, it
    is truncated towards zero.
    :param format_code: The format code to use. Tells Discord how to format the
    timestamp.
    """
    return f"<t:{int(time.timestamp())}:{format_code}>"
