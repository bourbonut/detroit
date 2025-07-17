import math

from ...selection import Selection
from .basis import BezierTrait
from .common import Curve


class BasisClosedCurve(Curve, BezierTrait):
    def __init__(self, context):
        self._context = context
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan
        self._x3 = math.nan
        self._y3 = math.nan
        self._x4 = math.nan
        self._y4 = math.nan

    def area_start(self):
        return None

    def area_end(self):
        return None

    def line_start(self):
        self._x0 = math.nan
        self._y0 = math.nan
        self._x1 = math.nan
        self._y1 = math.nan
        self._x2 = math.nan
        self._y2 = math.nan
        self._x3 = math.nan
        self._y3 = math.nan
        self._x4 = math.nan
        self._y4 = math.nan
        self._point = 0

    def line_end(self):
        if self._point == 1:
            self._context.move_to(self._x2, self._y2)
            self._context.close_path()
        elif self._point == 2:
            self._context.move_to(
                (self._x2 + 2 * self._x3) / 3,
                (self._y2 + 2 * self._y3) / 3,
            )
            self._context.line_to(
                (self._x3 + 2 * self._x2) / 3,
                (self._y3 + 2 * self._y2) / 3,
            )
            self._context.close_path()
        elif self._point == 3:
            self.point(self._x2, self._y2)
            self.point(self._x3, self._y3)
            self.point(self._x4, self._y4)

    def point(self, x, y):
        if self._point == 0:
            self._point = 1
            self._x2 = x
            self._y2 = y
        elif self._point == 1:
            self._point = 2
            self._x3 = x
            self._y3 = y
        elif self._point == 2:
            self._point = 3
            self._x4 = x
            self._y4 = y
            self._context.move_to(
                (self._x0 + 4 * self._x1 + x) / 6,
                (self._y0 + 4 * self._y1 + y) / 6,
            )
        else:
            self._bezier_curve_to(x, y)
        self._x0 = self._x1
        self._x1 = x
        self._y0 = self._y1
        self._y1 = y


def curve_basis_closed(context: Selection) -> Curve:
    """
    Produces a closed cubic basis spline using the specified control points.
    When a line segment ends, the first three control points are repeated,
    producing a closed loop with :math:`C^2` continuity.

    Parameters
    ----------
    context : Selection
        Context

    Returns
    -------
    Curve
        Curve object
    """
    return BasisClosedCurve(context)
