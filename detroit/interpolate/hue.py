import math
from collections.abc import Callable

from .color import hue


def interpolate_hue(a: float, b: float) -> Callable[[float], float]:
    """
    Returns an interpolator between the two hue angles a and b.
    If either hue is NaN, the opposing value is used. The shortest
    path between hues is used. The return value of the interpolator
    is a number in :math:`[0, 360)`.

    Parameters
    ----------
    a : float
        Hue angle a
    b : float
        Hue angle b

    Returns
    -------
    Callable[[float], float]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_hue(45, 180)
    >>> interpolator(0)
    45.0
    >>> interpolator(1)
    180.0
    >>> interpolator(0.5)
    112.5
    """
    i = hue(float(a), float(b))

    def interpolate(t):
        x = i(t)
        return x - 360 * math.floor(x / 360)

    return interpolate
