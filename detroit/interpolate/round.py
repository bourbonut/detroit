from collections.abc import Callable


def interpolate_round(
    a: int | float | str, b: int | float | str
) -> Callable[[float], int]:
    """
    Returns an interpolator between the two numbers a and b.

    Parameters
    ----------
    a : int | float | str
        a value
    b : int | float | str
        b value

    Returns
    -------
    Callable[[float], int]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_round("1.2", "10.4")
    >>> interpolator(0)
    1
    >>> interpolator(1)
    10
    >>> interpolator(0.5)
    6
    """
    a, b = float(a), float(b)
    return lambda t: round(a * (1 - t) + b * t)
