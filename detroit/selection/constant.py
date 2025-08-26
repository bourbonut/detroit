from collections.abc import Callable

from ..types import T


def constant(x: T) -> Callable[..., T]:
    """
    Returns a function which returns the same value :code:`x` constantly.

    Parameters
    ----------
    x : T
        Value to return constantly

    Returns
    -------
    Callable[..., T]
        Function which returns :code:`x` whatever are arguments
    """

    def f(*args: ...) -> T:
        return x

    return f
