"""utils/parse.py

This module provides utility classes for parsing dstamp output.
"""

import re

from dstamp.main import COPY_SUCCESS_TEXT


class Timestamp:
    """Test utility class for parsing discord timestamps."""

    PATTERN = r"<t:(\d+):([tTdDfFR])>"

    def __init__(self, text: str):
        match = re.search(self.PATTERN, text)
        if match is None:
            raise ValueError(f"No timestamp found in the input: {repr(text)}.")
        self.timestamp = int(match[1])
        self.format_code = match[2]


class DstampGetOutput:
    """Test utility class for parsing dstamp get command output."""

    def __init__(self, raw_output: str):
        lines = raw_output.splitlines()
        self.has_rounding_error = "There was an error in rounding:" in raw_output

        if self.has_rounding_error:
            # Rounding error means the program aborted so no other information
            # will be displayed.
            return

        self.timestamp = Timestamp(lines[1])
        self.copied_to_clipboard = COPY_SUCCESS_TEXT in raw_output
