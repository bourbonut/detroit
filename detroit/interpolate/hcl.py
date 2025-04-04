from collections.abc import Callable

from ..color import hcl as color_hcl
from .color import color, hue


class HLCInterpolator:
    def __init__(self, func):
        self.func = func

    def __call__(self, start, end):
        start = color_hcl(start)
        end = color_hcl(end)
        h = self.func(start.h, end.h)
        c = color(start.c, end.c)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.c = c(t)
            start.l = l(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate


def interpolate_hcl(a: str, b: str) -> Callable[[float], str]:
    """
    Returns a CIELChab color space interpolator between the two colors a and b.
    The colors a and b need not be in CIELChab; they will be converted to CIELChab
    using d3.hcl. If either color's hue or chroma is NaN, the opposing color's channel
    value is used. The shortest path between hues is used. The return value of the
    interpolator is an RGB string.

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

    >>> interpolator = d3.interpolate_hcl("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(245, 0, 134)'
    """
    return HLCInterpolator(hue)(a, b)


def interpolate_hcl_long(a: str, b: str) -> Callable[[float], str]:
    """
    Like :code:`interpolate_hcl`, but does not use the shortest path between hues.

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

    >>> interpolator = d3.interpolate_hcl_long("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(0, 130, 64)'
    """
    return HLCInterpolator(color)(a, b)
