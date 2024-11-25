from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def interpolate_number_array(a: list[T], b: list[T] | None) -> Callable[[T], list[T]]:
    """
    Returns an interpolator between the two arbitrary values a and b.

    Parameters
    ----------
    a : list[T]
        a value
    b : list[T] | None
        b value

    Returns
    -------
    Callable[[T], list[T]]
        Interpolator
    """
    if b is None:
        b = []
    n = min(len(b), len(a)) if a else 0
    c = list(b)

    def interpolate(t):
        for i in range(n):
            c[i] = a[i] * (1 - t) + b[i] * t
        return c

    return interpolate


def is_number_array(x):
    return isinstance(x, list) and all(isinstance(i, (int, float)) for i in x)
