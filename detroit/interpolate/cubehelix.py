from collections.abc import Callable

from ..coloration import cubehelix as color_cubehelix
from .color import color, hue


class CubeHelixInterpolator:
    def __init__(self, func):
        self.func = func
        self.gamma = 1

    def __call__(self, start: str, end: str) -> Callable[[float], str]:
        start = color_cubehelix(start)
        end = color_cubehelix(end)
        h = self.func(start.h, end.h)
        s = color(start.s, end.s)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.s = s(t)
            start.l = l(t**self.gamma)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    def set_gamma(self, gamma):
        self.gamma = gamma
        return self


interpolate_cubehelix = CubeHelixInterpolator(hue)
interpolate_cubehelix.__doc__ = """
    Returns a Cubehelix color space interpolator between the two colors a
    and b using a configurable gamma. If the gamma is not specified, it
    defaults to 1.0. The colors a and b need not be in Cubehelix; they will
    be converted to Cubehelix using d3.cubehelix. If either color’s hue or
    saturation is NaN, the opposing color’s channel value is used. The shortest
    path between hues is used. The return value of the interpolator is an
    RGB string.

    Parameters
    ----------
    a : str
        String a
    b : str
        String b

    Returns
    -------
    Callable[[float], str]
        Interpolator
    """

interpolate_cubehelix_long = CubeHelixInterpolator(color)
interpolate_cubehelix_long.__doc__ = """
    Like :code:`interpolate_cubehelix`, but does not use the shortest path between hues.


    Parameters
    ----------
    a : str
        String a
    b : str
        String b

    Returns
    -------
    Callable[[float], str]
        Interpolator
    """
