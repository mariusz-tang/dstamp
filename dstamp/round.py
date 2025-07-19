"""round.py

This module contains logic for rounding timestamps to nicer ones.
"""

from enum import Enum

class RoundingUnit(Enum):
    HOUR = "h", 24
    MINUTE = "m", 60

    def __init__(self, code, max_quantity):
        self.code = code
        self.max_quantity = max_quantity
