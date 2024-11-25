import math
from collections.abc import Callable

from .color import hue


def interpolate_hue(a: int | float, b: int | float) -> Callable[[float], float]:
    """
    Returns an interpolator between the two hue angles a and b.
    If either hue is NaN, the opposing value is used. The shortest
    path between hues is used. The return value of the interpolator
    is a number in [0, 360).

    Parameters
    ----------
    a : int | float
        Hue angle a
    b : int | float
        Hue angle b

    Returns
    -------
    Callable[[float], float]
        Interpolator
    """
    i = hue(float(a), float(b))

    def interpolate(t):
        x = i(t)
        return x - 360 * math.floor(x / 360)

    return interpolate
