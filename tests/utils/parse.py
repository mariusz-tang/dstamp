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

    PATH_PATTERN = r"Using config at (.+)"
    PROPERTY_PATTERN = r"([^:]+): (.+)"

    def __init__(self, raw_output: str):
        lines = raw_output.splitlines()
        m_path = re.fullmatch(self.PATH_PATTERN, lines[0])
        self.config_path = Path(m_path[1])

        joined_output = "".join(lines)
        self.has_using_default_warning = (
            "Using default config settings." in joined_output
        )
        self.not_a_file = False
        self.invalid_toml = False
        if self.has_using_default_warning:
            self.not_a_file = "not a file" in joined_output
            self.invalid_toml = "not a valid TOML file" in joined_output

        properties = dict()
        for line in lines[1:]:
            m = re.fullmatch(self.PROPERTY_PATTERN, line)
            if m is not None:
                properties[m[1]] = m[2]

        self.copy_to_clipboard = properties["copy_to_clipboard"] == "True"
        self.output_format = properties["output_format"]
