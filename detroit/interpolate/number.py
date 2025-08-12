from collections.abc import Callable

from ..types import Number


def interpolate_number(a: Number, b: Number) -> Callable[[float], float]:
    """
    Returns an interpolator between the two numbers a and b.

    Parameters
    ----------
    a : Number
        a value
    b : Number
        b value

    Returns
    -------
    Callable[[float], float]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_number(10, 20)
    >>> interpolator(0)
    10.0
    >>> interpolator(1)
    20.0
    >>> interpolator(0.5)
    15.0
    """
    a, b = float(a), float(b)
    return lambda t: a * (1 - t) + b * t
