from collections.abc import Callable

from ..types import T


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
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_discrete(["a", "b", "c"])
    >>> interpolator(0)
    'a'
    >>> interpolator(1)
    'c'
    >>> interpolator(0.5)
    'b'
    """
    n = len(range_)
    return lambda t: range_[max(0, min(n - 1, int(t * n)))]
