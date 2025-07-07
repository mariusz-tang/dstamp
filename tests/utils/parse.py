import re


class Timestamp:
    """Test utility class for parsing discord timestamps."""

    PATTERN = r"<t:(\d+):([tTdDfFR])>"

    def __init__(self, text: str):
        match = re.search(self.PATTERN, text)
        if match is None:
            raise ValueError(f"No timestamp found in the input: {repr(text)}.")
        self.timestamp = int(match[1])
        self.format_code = match[2]
