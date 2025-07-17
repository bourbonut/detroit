from collections.abc import Callable
from math import cos, sin

from ...selection import Selection
from .common import Curve
from .linear import curve_linear


class RadialCurve(Curve):
    def __init__(self, curve):
        self._curve = curve

    def area_start(self):
        self._curve.area_start()

    def area_end(self):
        self._curve.area_end()

    def line_start(self):
        self._curve.line_start()

    def line_end(self):
        self._curve.line_end()

    def point(self, a, r):
        self._curve.point(r * sin(a), -r * cos(a))


def curve_radial(curve: Curve) -> Callable[[Selection], Curve]:
    def radial(context):
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
        Curve object
    """
    return curve_radial(curve_linear)
