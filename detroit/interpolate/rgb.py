from collections.abc import Callable

from ..coloration import rgb as color_rgb
from .basis import interpolate_basis
from .basis_closed import interpolate_basis_closed
from .color import color as nogamma
from .color import gamma


class RGBGammaInterpolator:
    def __init__(self, y):
        self.color = gamma(y)

    def __call__(self, start: str, end: str) -> Callable[[float], str]:
        """
        Returns an RGB color space interpolator between the two colors a and b
        with a configurable gamma. If the gamma is not specified, it defaults to
        1.0. The colors a and b need not be in RGB; they will be converted to RGB
        using :code:`d3.rgb`. The return value of the interpolator is an RGB string.

        Parameters
        ----------
        start : str
            Color string a
        end : str
            Color string b

        Returns
        -------
        Callable[[float], str]
            Interpolator
        """
        start = color_rgb(start)
        end = color_rgb(end)
        r = self.color(start.r, end.r)
        g = self.color(start.g, end.g)
        b = self.color(start.b, end.b)
        opacity = nogamma(start.opacity, end.opacity)

        def interpolate(t):
            start.r = r(t)
            start.g = g(t)
            start.b = b(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    def set_gamma(self, y):
        self.color = gamma(y)
        return self


interpolate_rgb = RGBGammaInterpolator(1)


class RGBSplineInterpolator:
    def __init__(self, spline):
        self.spline = spline

    def __call__(self, colors):
        n = len(colors)
        r = [0] * n
        g = [0] * n
        b = [0] * n

        for i, color in enumerate(colors):
            color = color_rgb(color)
            r[i] = color.r or 0
            g[i] = color.g or 0
            b[i] = color.b or 0

        r_spline = self.spline(r)
        g_spline = self.spline(g)
        b_spline = self.spline(b)

        color = color_rgb(0, 0, 0, 1)

        def interpolate(t):
            color.r = r_spline(t)
            color.g = g_spline(t)
            color.b = b_spline(t)
            return str(color)

        return interpolate


def interpolate_rgb_basis(colors: list[str]) -> Callable[[float], str]:
    """
    Returns a uniform nonrational B-spline interpolator through the specified
    array of colors, which are converted to RGB color space. Implicit control
    points are generated such that the interpolator returns colors[0] at t = 0
    and colors[-1] at t = 1. Opacity interpolation is not currently supported.
    See also d3.interpolate_basis, and see scale_chromatic for examples.

    Parameters
    ----------
    colors : list[str]
         List of colors to interpolate

    Returns
    -------
    Callable[[float], str]
        Interpolator
    """
    return RGBSplineInterpolator(interpolate_basis)(colors)


def interpolate_rgb_basis_closed(colors: list[str]) -> Callable[[float], str]:
    """
    Returns a uniform nonrational B-spline interpolator through the specified
    array of colors, which are converted to RGB color space. The control points
    are implicitly repeated such that the resulting spline has cyclical :math:`C^2`
    continuity when repeated around t in [0,1]; this is useful, for example, to
    create cyclical color scales. Opacity interpolation is not currently supported.
    See also d3.interpolate_basis_closed, and see scale_chromatic for examples.

    Parameters
    ----------
    colors : list[str]
         List of colors to interpolate

    Returns
    -------
    Callable[[float], str]
        Interpolator
    """
    return RGBSplineInterpolator(interpolate_basis_closed)(colors)
