from typing import Protocol

type AppResult[T] = tuple[int, T]


class AppRunner[T](Protocol):
    def __call__(self, *args: str) -> AppResult[T]: ...
