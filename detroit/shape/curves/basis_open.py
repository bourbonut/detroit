import math

from ...selection import Selection
from .basis import BezierTrait
from .common import Curve, isvaluable


class BasisOpenCurve(Curve, BezierTrait):
    def __init__(self, context):
        self._context = context
        self._line = math.nan

    def area_start(self):
        self._line = 0

    def area_end(self):
        self._line = math.nan

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._point = 0

    def line_end(self):
        if isvaluable(self._line) or (self._line != 0 and self._point == 3):
            self._context.close_path()
        self._line = 1 - self._line

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
        elif self._point == 1:
            self._point = 2
        elif self._point == 2:
            self._point = 3
            x0 = (self._x0 + 4 * self._x1 + x) / 6
            y0 = (self._y0 + 4 * self._y1 + y) / 6
            if isvaluable(self._line):
                self._context.line_to(x0, y0)
            else:
                self._context.move_to(x0, y0)
        elif self._point == 3:
            self._point = 4
            self._bezier_curve_to(x, y)
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = x
        self._y0 = self._y1
        self._y1 = y


def curve_basis_open(context: Selection) -> Curve:
    """
    Produces a cubic basis spline using the specified control points. Unlike
    basis, the first and last points are not repeated, and thus the curve
    typically does not intersect these points.

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object
    """
    return BasisOpenCurve(context)
