"""utils/parse.py

This module provides utility classes for parsing dstamp output.
"""

import re
from pathlib import Path

from dstamp.clipboard import COPY_SUCCESS_TEXT


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
        self.timestamp = Timestamp(lines[0])
        self.copied_to_clipboard = COPY_SUCCESS_TEXT in raw_output


class DstampShowConfigOutput:
    """Test utility class for parsing dstamp show-config command output."""

    FILE_PATTERN = r"Using config at (.+)"

    def __init__(self, raw_output: str):
        lines = raw_output.splitlines()
        m = re.fullmatch(self.FILE_PATTERN, lines[0])
        self.config_path = Path(m[1])
