from collections.abc import Callable
from math import cos, sin

from ...path import Path
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
    curve: Callable[[Path], Curve],
) -> Callable[[Path], Curve]:
    """
    Converts a curve function into a radial curve function.

    Parameters
    ----------
    curve : Callable[[Path], Curve]
        Curve function

    Returns
    -------
    Callable[[Path], Curve]
        Radial curve function
    """

    def radial(context: Path) -> Curve:
        if isinstance(curve(Path()), RadialCurve):
            return curve(context)
        return RadialCurve(curve(context))

    return radial


def curve_radial_linear(context: Path) -> Curve:
    """
    Produces a polyline through the specified polar points.

    Parameters
    ----------
    context : Path
        Context

    Returns
    -------
    Curve
        Radial curve
    """
    return curve_radial(curve_linear)(context)
