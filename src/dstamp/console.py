"""Console printing utilities."""

from rich.console import Console

_console = Console(highlight=False)

print = print


def info(text: str) -> None:
    _console.print(text, style="white")


def warn(text: str) -> None:
    _console.print(text, style="yellow")


def error(text: str) -> None:
    _console.print(text, style="bold red")
