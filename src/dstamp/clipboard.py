"""clipboard.py

This module provides functions for interacting with the clipboard.
"""

import pyperclip

from dstamp import console

COPY_SUCCESS_TEXT = "Copied to clipboard!"


def copy(text: str) -> None:
    """
    Copy text to clipboard.

    If the clipboard manager raises an error, inform the user that this is
    the problem area and reraise the error.
    """
    try:
        pyperclip.copy(text)
        console.info(COPY_SUCCESS_TEXT)
    except pyperclip.PyperclipException:  # pragma: no cover
        console.error("There was a problem with the clipboard manager:")
        raise
