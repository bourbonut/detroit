from collections.abc import Callable

from ..types import T


def constant(x: T) -> Callable[..., T]:
    def f(*args):
        return x

    return f
