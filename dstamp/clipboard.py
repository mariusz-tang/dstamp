"""clipboard.py

This module provides functions for interacting with the clipboard.
"""

import clipman

from . import console

COPY_SUCCESS_TEXT = "Copied to clipboard!"


def copy(text: str):
    """
    Copy text to clipboard.

    If the clipboard manager raises an error, inform the user that this is
    the problem area and reraise the error.
    """
    try:
        clipman.init()
        clipman.set(text)
        console.info(COPY_SUCCESS_TEXT)
    except clipman.exceptions.ClipmanBaseException:  # pragma: no cover
        console.error("There was a problem with the clipboard manager:")
        raise
