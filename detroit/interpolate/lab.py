from collections.abc import Callable

from ..color import lab as color_lab
from .color import color


def interpolate_lab(a: str, b: str) -> Callable[[float], str]:
    """
    Returns a CIELAB color space interpolator between the two colors a and b.
    The colors a and b need not be in CIELAB; they will be converted to CIELAB
    using d3.lab. The return value of the interpolator is an RGB string.

    Parameters
    ----------
    a : str
        Color string a
    b : str
        Color string b

    Returns
    -------
    Callable[[float], str]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_lab("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(193, 0, 136)'
    """
    start = color_lab(a)
    end = color_lab(b)
    l = color(start.l, end.l)
    a = color(start.a, end.a)
    b = color(start.b, end.b)
    opacity = color(start.opacity, end.opacity)

    def interpolate(t):
        start.l = l(t)
        start.a = a(t)
        start.b = b(t)
        start.opacity = opacity(t)
        return str(start)

    return interpolate
