"""Module for handling clipboard interaction."""

import clipman
from rich.console import Console

console = Console()


def copy(text: str):
    """
    Copy text to clipboard.

    If the clipboard manager raises an error, inform the user that this is
    the problem area and reraise the error.
    """
    try:
        clipman.init()
        clipman.set(text)
        console.print("Copied to clipboard!", style="white")
    except clipman.exceptions.ClipmanBaseException:
        console.print(
            "There was a problem with the clipboard manager:", style="bold red"
        )
        raise
