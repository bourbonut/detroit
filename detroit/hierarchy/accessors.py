from collections.abc import Callable
from typing import Any


def optional(f: Callable[..., Any] | None) -> Callable[..., Any] | None:
    if f is None:
        return None
    return required(f)


def required(f: Callable[..., Any]) -> Callable[..., Any]:
    if not callable(f):
        raise TypeError(f"{f!r} is not callable.")
    return f
