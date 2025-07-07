"""utils.patched_time.py

This module defines the current time to be used for freezegun-assisted tests.
"""

from datetime import date, datetime, time

today = date(2025, 1, 2)
current_time = time(12, 53, 42)
now = datetime.combine(today, current_time)
