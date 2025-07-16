"""round.py

This module contains logic for rounding timestamps to nicer ones.
"""

from enum import Enum

class RoundingUnit(str, Enum):
    HOUR = "h", 24
    MINUTE = "m", 60

    def __new__(cls, code, max_quantity):
        obj = str.__new__(cls, [code])
        obj._value_ = code
        obj.code = code
        obj.max_quantity = max_quantity
        return obj
