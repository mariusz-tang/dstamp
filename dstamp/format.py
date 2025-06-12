from datetime import datetime
from enum import Enum


class Format(str, Enum):
    SHORT_TIME = "shorttime", "t"
    LONG_TIME = "longtime", "T"
    SHORT_DATE = "shortdate", "d"
    LONG_DATE = "longdate", "D"
    SHORT_DATETIME = "shortdatetime", "f"
    LONG_DATETIME = "longdatetime", "F"
    RELATIVE = "relative", "R"

    def __new__(cls, value, code):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.code = code
        return obj


def convert_to_discord_format(time: datetime, format: Format) -> str:
    timestamp = int(time.timestamp())
    return f"<t:{timestamp}:{format.code}>"
