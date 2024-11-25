from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def interpolate_round(a: T, b: T) -> Callable[[T], T]:
    """
    Returns an interpolator between the two numbers a and b.

    Parameters
    ----------
    a : T
        a value
    b : T
        b value

    Returns
    -------
    Callable[[T], T]
        Interpolator
    """
    a, b = float(a), float(b)
    return lambda t: round(a * (1 - t) + b * t)
