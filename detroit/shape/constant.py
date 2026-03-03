from collections.abc import Callable
from typing import Any

from ..types import T


def constant(x: T) -> Callable[[Any], T]:
    def f(*args: Any) -> T:
        return x

    return f
