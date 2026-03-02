from __future__ import annotations

from collections.abc import Callable

from ..color import cubehelix as color_cubehelix
from .color import color, hue


class CubeHelixInterpolator:
    def __init__(self, func: Callable[[float, float], Callable[[float], float]]):
        self.func = func
        self.gamma = 1

    def __call__(self, start: str, end: str) -> Callable[[float], str]:
        start_color = color_cubehelix(start)
        end_color = color_cubehelix(end)
        h = self.func(start_color.h, end_color.h)
        s = color(start_color.s, end_color.s)
        l = color(start_color.l, end_color.l)
        opacity = color(start_color.opacity, end_color.opacity)

        def interpolate(t: float) -> str:
            start_color.h = h(t)
            start_color.s = s(t)
            start_color.l = l(t**self.gamma)
            start_color.opacity = opacity(t)
            return str(start_color)

        return interpolate

    def set_gamma(self, gamma: float) -> CubeHelixInterpolator:
        """
        Sets gamma and returns itself. See `gamma error in picture scaling
        <http://www.ericbrasseur.org/gamma.html?i=1>`_ for more information.

        Parameters
        ----------
        gamma : float
            Gamma value

        Returns
        -------
        CubeHelixInterpolator
            Itself
        """
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
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_cubehelix("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(238, 0, 209)'
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
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_cubehelix_long("red", "blue")
    >>> interpolator(0)
    'rgb(255, 0, 0)'
    >>> interpolator(1)
    'rgb(0, 0, 255)'
    >>> interpolator(0.5)
    'rgb(238, 0, 209)'
    """
