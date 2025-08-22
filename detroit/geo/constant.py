from ..types import T
from collections.abc import Callable

def constant(x: T) -> Callable[..., T]:
    def f(*args):
        return x
    return f
