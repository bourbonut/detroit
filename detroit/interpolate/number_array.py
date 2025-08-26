from collections.abc import Callable

from ..types import T


def interpolate_number_array(
    a: list[T], b: list[T] | None
) -> Callable[[float], list[T]]:
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
    Callable[[float], list[T]]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_number_array([0, 10, 20], [30, 40, 50])
    >>> interpolator(0)
    [0, 10, 20]
    >>> interpolator(1)
    [30, 40, 50]
    >>> interpolator(0.5)
    [15.0, 25.0, 35.0]
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
