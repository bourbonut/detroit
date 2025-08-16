from collections.abc import Callable
from math import cos, sin

from ...selection import Selection
from .common import Curve
from .linear import curve_linear


class RadialCurve(Curve):
    def __init__(self, curve: Curve):
        self._curve = curve

    def area_start(self):
        self._curve.area_start()

    def area_end(self):
        self._curve.area_end()

    def line_start(self):
        self._curve.line_start()

    def line_end(self):
        self._curve.line_end()

    def point(self, a: float, r: float):
        self._curve.point(r * sin(a), -r * cos(a))


def curve_radial(
    curve: Callable[[Selection], Curve],
) -> Callable[[Selection], Curve]:
    """
    Converts a curve function into a radial curve function.

    Parameters
    ----------
    curve : Callable[[Selection], Curve]
        Curve function

    Returns
    -------
    Callable[[Selection], Curve]
        Radial curve function
    """

    def radial(context: Selection) -> Curve:
        if isinstance(curve(None), RadialCurve):
            return curve(context)
        return RadialCurve(curve(context))

    return radial


def curve_radial_linear(context: Selection) -> Curve:
    """
    Produces a polyline through the specified polar points.

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Radial curve
    """
    return curve_radial(curve_linear)(context)
