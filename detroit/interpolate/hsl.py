from collections.abc import Callable

from ..color import hsl as color_hsl
from .color import color, hue


class HSLInterpolator:
    def __init__(self, func: Callable[[float, float], Callable[[float], float]]):
        self.func = func

    def __call__(self, start: str, end: str):
        start_color = color_hsl(start)
        end_color = color_hsl(end)
        h = self.func(start_color.h, end_color.h)
        s = color(start_color.s, end_color.s)
        l = color(start_color.l, end_color.l)
        opacity = color(start_color.opacity, end_color.opacity)

        def interpolate(t):
            start_color.h = h(t)
            start_color.s = s(t)
            start_color.l = l(t)
            start_color.opacity = opacity(t)
            return str(start_color)

        return interpolate


def interpolate_hsl(a: str, b: str) -> Callable[[float], str]:
    """
    Returns an HSL color space interpolator between the two colors a and b.
    The colors a and b need not be in HSL; they will be converted to HSL
    using d3.hsl. If either color's hue or saturation is NaN, the opposing
    color's channel value is used. The shortest path between hues is used.
    The return value of the interpolator is an RGB string.

    Parameters
    ----------
    a : str
        String a
    b : str
        String b

    Returns
    -------
    Callable[[float], str]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_hsl("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(255, 0, 255)'
    """
    return HSLInterpolator(hue)(a, b)


def interpolate_hsl_long(a: str, b: str) -> Callable[[float], str]:
    """
    Like :code:`interpolate_hsl`, but does not use the shortest path between hues.

    Parameters
    ----------
    a : str
        String a
    b : str
        String b

    Returns
    -------
    Callable[[float], str]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_hsl_long("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(0, 255, 0)'
    """
    return HSLInterpolator(color)(a, b)
