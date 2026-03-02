from collections.abc import Callable

from ..color import hcl as color_hcl
from .color import color, hue


class HLCInterpolator:
    def __init__(self, func: Callable[[float, float], Callable[[float], float]]):
        self.func = func

    def __call__(self, start: str, end: str) -> Callable[[float], str]:
        start_color = color_hcl(start)
        end_color = color_hcl(end)
        h = self.func(start_color.h, end_color.h)
        c = color(start_color.c, end_color.c)
        l = color(start_color.l, end_color.l)
        opacity = color(start_color.opacity, end_color.opacity)

        def interpolate(t: float) -> str:
            start_color.h = h(t)
            start_color.c = c(t)
            start_color.l = l(t)
            start_color.opacity = opacity(t)
            return str(start_color)

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
