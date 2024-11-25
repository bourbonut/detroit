from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def interpolate_discrete(range_: list[T]) -> Callable[[float], T]:
    """
    Returns a discrete interpolator for the given array of values.

    Parameters
    ----------
    range_ : list[T]
        List of elements

    Returns
    -------
    Callable[[float], T]
        Interpolator
    """
    n = len(range_)
    return lambda t: range_[max(0, min(n - 1, int(t * n)))]
